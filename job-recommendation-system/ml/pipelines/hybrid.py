"""Transparent fusion with missing-modality fallback and bounded personalization."""

from datetime import date
from flask import current_app
from models.recommendation_model import match_label
from ml import PIPELINE_VERSION
from ml.preprocessing.text import candidate_text, job_text
from ml.features.behavior import behavior_score
from ml.features.schema import feature_matrix


def hybrid_weights(configured, semantic_available, behavior=None, max_behavior=0.10):
    weights = dict(configured)
    if not semantic_available:
        weights["semantic"] = 0.0
    weights["behavior"] = 0.0
    total = sum(weights.values())
    if total <= 0:
        raise ValueError("At least one available feature must have a positive weight.")
    weights = {key: value / total for key, value in weights.items()}
    if behavior and behavior["enabled"]:
        weights = {key: value * (1 - max_behavior) for key, value in weights.items()}
        weights["behavior"] = max_behavior
    return weights


def context_features(profile, job, as_of=None):
    employment = profile.get("employment_type")
    remote = profile.get("remote_preference", "any")
    mode = job.remote_type or "unknown"
    if mode == "unknown" and str(job.location).casefold() == "remote":
        mode = "remote"
    posted = job.posted_date
    if job.is_external and not job.external_created_at:
        freshness = 50.0
    elif not posted:
        freshness = 50.0
    else:
        age = max(0, ((as_of or date.today()) - posted).days)
        freshness = max(0.0, 100 * (1 - age / 90))
    return {
        "employment": (
            50.0
            if not employment or job.employment_type in {None, "Other", "Unknown"}
            else 100.0 if employment == job.employment_type else 0.0
        ),
        "remote": (
            50.0
            if remote == "any" or mode == "unknown"
            else 100.0 if remote == mode else 0.0
        ),
        "freshness": freshness,
    }


class HybridRecommender:
    def __init__(self, embeddings, registry):
        self.embeddings = embeddings
        self.registry = registry

    def rank(self, profile, baseline, *, behavior=None, strategy="hybrid", as_of=None):
        if not baseline:
            return []
        semantics = self.embeddings.similarities(
            candidate_text(profile), [job_text(row["job"]) for row in baseline]
        )
        weights = hybrid_weights(
            current_app.config["HYBRID_WEIGHTS"],
            semantics is not None,
            behavior,
            current_app.config["BEHAVIOR_MAX_WEIGHT"],
        )
        results = []
        for index, row in enumerate(baseline):
            scores = {
                **row["scores"],
                "tfidf": row["scores"]["semantic"],
                "semantic": float(semantics[index]) if semantics is not None else None,
                **context_features(profile, row["job"], as_of),
                "behavior": behavior_score(behavior, row["job"]),
            }
            contributions = {
                key: (scores[key] or 0.0) * weight for key, weight in weights.items()
            }
            score = round(sum(contributions.values()), 1)
            factors = sorted(
                [
                    key
                    for key in weights
                    if weights[key] > 0 and scores[key] is not None
                ],
                key=lambda key: (-scores[key], key),
            )
            reasons = row["reasons"] + [
                (
                    "Semantic embeddings contribute to this match."
                    if semantics is not None
                    else "Semantic embeddings are unavailable; their weight is redistributed across available features."
                ),
                "Strongest factors: " + ", ".join(factors[:3]) + ".",
                "Weakest factors: " + ", ".join(reversed(factors[-3:])) + ".",
            ]
            adjustment = {
                "enabled": bool(behavior and behavior["enabled"]),
                "weight": weights["behavior"],
                "reason": (
                    behavior["reason"]
                    if behavior
                    else "Cold start: profile-based matching."
                ),
                "distinct_jobs": behavior["distinct_jobs"] if behavior else 0,
                "meaningful_jobs": behavior["meaningful_jobs"] if behavior else 0,
            }
            if adjustment["enabled"]:
                reasons.append(
                    f"Prior feedback adjusts {100 * weights['behavior']:g}% of the weight; the profile baseline stays available."
                )
            results.append(
                {
                    **row,
                    "baseline_score": row["score"],
                    "score": score,
                    "scores": {
                        key: round(value, 4) if value is not None else None
                        for key, value in scores.items()
                    },
                    "contributions": {
                        key: round(value, 4) for key, value in contributions.items()
                    },
                    "weights": weights,
                    "reasons": reasons,
                    "strongest": factors[:3],
                    "weakest": list(reversed(factors[-3:])),
                    "personalization": adjustment,
                    "label": match_label(score),
                    "model": {
                        "strategy": "hybrid",
                        "version": PIPELINE_VERSION,
                        "embedding_version": (
                            self.embeddings.version if semantics is not None else None
                        ),
                        "embedding_status": self.embeddings.reason,
                    },
                }
            )
        if strategy == "ltr":
            ranker = self.registry.load()
            if (
                ranker
                and ranker.representation
                and ranker.representation.get("embedding_version")
                != (self.embeddings.version if semantics is not None else None)
            ):
                self.registry.reason = "embedding_representation_mismatch"
                ranker = None
            if ranker:
                matrix = feature_matrix(results)
                utilities = ranker.predict(matrix)
                for index, row in enumerate(results):
                    row["hybrid_score"] = row["score"]
                    row["contributions"] = {
                        key: value * 0.8 for key, value in row["contributions"].items()
                    }
                    row["contributions"]["ranker"] = float(utilities[index]) * 0.2
                    row["score"] = round(sum(row["contributions"].values()), 1)
                    row["label"] = match_label(row["score"])
                    row["ml_utility"] = round(float(utilities[index]), 2)
                    row["ml_explanation"] = None
                    row["model"] = {
                        **row["model"],
                        "strategy": "ltr",
                        "version": ranker.metadata["version"],
                        "ranker": ranker.metadata["model_name"],
                        "dataset_kind": ranker.metadata["dataset_kind"],
                    }
                    row["reasons"].append(
                        "Experimental ranker: 80% transparent hybrid match + 20% expected ordinal relevance utility; this is not a hiring probability."
                    )
            else:
                for row in results:
                    row["model"]["ranker_status"] = self.registry.reason
                    row["reasons"].append(
                        "ML ranker unavailable or incompatible; using the hybrid baseline."
                    )
        ordered = sorted(results, key=lambda row: (-row["score"], row["job"].id))
        if strategy == "ltr" and ranker:
            top = ordered[:20]
            effects = ranker.explain(feature_matrix(top))
            for index, row in enumerate(top):
                row["ml_explanation"] = {
                    name: round(values[index], 4) for name, values in effects.items()
                }
        return ordered
