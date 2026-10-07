"""Caches job-only TF-IDF features and stores immutable recommendation snapshots."""

import hashlib
import json
import threading
from collections import OrderedDict
from uuid import uuid4
from pathlib import Path
import joblib
import sklearn
from flask import current_app
from services.job_catalog import eligible_conditions
from services.settings_service import weights as configured_weights
from sklearn.feature_extraction.text import TfidfVectorizer
from models.database import db, Job, RecommendationRun, Recommendation
from models.skill_extractor import normalize_skills, extract_skills
from models.recommendation_model import (
    calculate_skill_score,
    calculate_semantic_similarity,
    calculate_experience_score,
    calculate_education_score,
    calculate_location_score,
    calculate_salary_score,
    calculate_role_score,
    calculate_final_score,
    role_text,
    get_matching_skills,
    get_missing_skills,
    generate_recommendation_explanation,
    match_label,
)


def profile_data(user):
    fields = [
        "education",
        "experience_years",
        "experience_summary",
        "preferred_role",
        "preferred_location",
        "expected_salary",
        "employment_type",
        "remote_preference",
        "salary_currency",
        "state",
        "willing_to_relocate",
        "certifications",
        "projects",
        "career_interests",
        "resume_text",
    ]
    return {
        **{field: getattr(user, field) for field in fields},
        "skills": user.skill_names,
    }


def profile_completion(user):
    sections = {
        "Basic details": bool(user.full_name and user.city),
        "Education": bool(user.education),
        "Skills": bool(user.skills),
        "Resume": bool(user.resume_text),
        "Experience": user.experience_years is not None,
        "Career preferences": bool(user.preferred_role and user.preferred_location),
        "Salary preference": user.expected_salary is not None,
        "Certifications": bool(user.certifications),
        "Projects": bool(user.projects),
        "Career interests": bool(user.career_interests),
    }
    percent = round(100 * sum(sections.values()) / len(sections))
    return {
        "percent": percent,
        "sections": sections,
        "suggestions": [
            f"Add {label.lower()}."
            for label, present in sections.items()
            if not present
        ],
    }


def confidence(profile):
    fields = [
        "skills",
        "education",
        "preferred_role",
        "preferred_location",
        "resume_text",
        "projects",
        "certifications",
    ]
    available = sum(bool(profile.get(field)) for field in fields)
    available += profile.get("experience_years") is not None
    available += profile.get("expected_salary") is not None
    return "High" if available >= 8 else "Medium" if available >= 4 else "Low"


def candidate_text(profile):
    fields = [
        "education",
        "experience_summary",
        "projects",
        "certifications",
        "preferred_role",
        "career_interests",
        "resume_text",
    ]
    return " ".join(
        [" ".join(profile.get("skills", []))]
        + [str(profile.get(key) or "") for key in fields]
    )[:65000]


def job_text(job):
    return " ".join(
        [
            job.job_title,
            job.job_description,
            job.industry,
            job.location,
            " ".join(job.required_skills),
            " ".join(job.preferred_skills),
        ]
    )


class RecommendationEngine:
    def __init__(self):
        self.lock = threading.RLock()
        self.signature = None
        self.features = None
        self.fit_count = 0
        self.memory_cache = OrderedDict()

    def features_for(self, jobs):
        payload = [[job.id, job_text(job)] for job in jobs]
        signature = hashlib.sha256(
            json.dumps([sklearn.__version__, "v1", payload], sort_keys=True).encode()
        ).hexdigest()
        with self.lock:
            if signature == self.signature:
                return self.features
            if signature in self.memory_cache:
                self.signature = signature
                self.features = self.memory_cache[signature]
                self.memory_cache.move_to_end(signature)
                return self.features
            path = Path(current_app.instance_path) / "model.joblib"
            features = None
            if current_app.config["MODEL_CACHE"] and path.exists():
                try:
                    # Only this app's private local artifact is loaded. Never accept model uploads.
                    stored = joblib.load(path)
                    if stored.get("signature") == signature:
                        features = stored["features"]
                except Exception:
                    current_app.logger.warning(
                        "Rebuilding an unreadable local TF-IDF cache."
                    )
            if features is None:
                vectorizer = TfidfVectorizer(
                    ngram_range=(1, 2),
                    sublinear_tf=True,
                    stop_words="english",
                    max_features=20000,
                )
                matrix = vectorizer.fit_transform(
                    [text.strip() or "unspecified" for _, text in payload]
                )
                role_vectorizer = TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)
                role_matrix = role_vectorizer.fit_transform(
                    [role_text(job.job_title).strip() or "unspecified" for job in jobs]
                )
                features = (vectorizer, matrix, role_vectorizer, role_matrix)
                self.fit_count += 1
                if current_app.config["MODEL_CACHE"]:
                    temporary = path.with_name(f"model-{uuid4().hex}.tmp")
                    joblib.dump(
                        {"signature": signature, "features": features}, temporary
                    )
                    temporary.replace(path)
            self.signature, self.features = signature, features
            self.memory_cache[signature] = features
            if len(self.memory_cache) > 8:
                self.memory_cache.popitem(last=False)
            return features

    def rank(self, profile, jobs):
        if not jobs:
            return []
        jobs = sorted(jobs, key=lambda job: job.id)
        vectorizer, matrix, role_vectorizer, role_matrix = self.features_for(jobs)
        semantics = calculate_semantic_similarity(
            vectorizer.transform([candidate_text(profile)]), matrix
        )
        roles = calculate_role_score(
            role_vectorizer.transform([role_text(profile.get("preferred_role"))]),
            role_matrix,
        )
        weights = configured_weights()
        result = []
        for index, job in enumerate(jobs):
            matched = get_matching_skills(profile.get("skills"), job.required_skills)
            missing = get_missing_skills(profile.get("skills"), job.required_skills)
            scores = {
                "skills": calculate_skill_score(
                    profile.get("skills"), job.required_skills, job.preferred_skills
                ),
                "semantic": float(semantics[index]),
                "experience": 50.0
                if job.experience_known is False
                else calculate_experience_score(
                    profile.get("experience_years"),
                    job.experience_min,
                    job.experience_max,
                ),
                "education": 50.0
                if job.is_external and not job.education_required
                else calculate_education_score(
                    profile.get("education"), job.education_required
                ),
                "location": calculate_location_score(
                    profile.get("preferred_location"),
                    job.location,
                    profile.get("state", ""),
                    profile.get("willing_to_relocate", False),
                ),
                "salary": 50.0
                if (job.salary_currency or "INR")
                != profile.get("salary_currency", "INR")
                or (job.salary_period or "year") != "year"
                else calculate_salary_score(
                    profile.get("expected_salary"), job.min_salary, job.max_salary
                ),
                "role": float(roles[index]),
            }
            total = calculate_final_score(scores, weights)
            result.append(
                {
                    "job": job,
                    "score": total,
                    "scores": {k: round(v, 2) for k, v in scores.items()},
                    "contributions": {
                        k: round(v * weights[k], 2) for k, v in scores.items()
                    },
                    "matched": matched,
                    "missing": missing,
                    "confidence": confidence(profile),
                    "context": context_signals(profile, job),
                    "label": match_label(total),
                    "reasons": generate_recommendation_explanation(
                        profile, job, scores, matched, missing
                    ),
                }
            )
        return sorted(
            result,
            key=lambda row: (
                -row["score"],
                -sum(row["context"].values()),
                row["job"].id,
            ),
        )

    def search(self, query, rows):
        if not rows or not query.strip():
            return rows
        rows = sorted(rows, key=lambda row: row["job"].id)
        jobs = [row["job"] for row in rows]
        vectorizer, matrix, _, _ = self.features_for(jobs)
        text_scores = calculate_semantic_similarity(
            vectorizer.transform([query]), matrix
        )
        query_skills = extract_skills(query)
        tokens = set(query.casefold().split())
        results = []
        for index, row in enumerate(rows):
            job = row["job"]
            text = job_text(job).casefold() + " " + job.company_name.casefold()
            coverage = sum(token in text for token in tokens) / max(len(tokens), 1)
            overlap = len(get_matching_skills(query_skills, job.required_skills)) / max(
                len(query_skills), 1
            )
            if coverage == 0 and text_scores[index] == 0:
                continue
            score = (
                0.45 * float(text_scores[index])
                + 25 * coverage
                + 15 * overlap
                + 0.15 * row["score"]
            )
            results.append({**row, "search_score": score})
        return sorted(
            results,
            key=lambda row: (-row["search_score"], -row["score"], row["job"].id),
        )

    def similar(self, target, jobs, limit=3):
        if len(jobs) < 2:
            return []
        ids = [job.id for job in jobs]
        if target.id not in ids:
            jobs = jobs + [target]
            ids.append(target.id)
        _, matrix, _, _ = self.features_for(jobs)
        scores = calculate_semantic_similarity(matrix[ids.index(target.id)], matrix)
        ordered = sorted(zip(jobs, scores), key=lambda item: (-item[1], item[0].id))
        return [job for job, _ in ordered if job.id != target.id][:limit]


def context_signals(profile, job):
    """Transparent tie-breakers preserve the seven-factor 0–100 match score."""
    remote = profile.get("remote_preference", "any")
    return {
        "employment": int(
            bool(profile.get("employment_type"))
            and profile["employment_type"] == job.employment_type
        ),
        "remote": int(remote == job.remote_type and remote != "any"),
        "freshness": 2
        if job.freshness == "Fresh"
        else 1
        if job.freshness == "Recently posted"
        else 0,
        "information": int(
            confidence(profile) == "High"
            and job.experience_known is not False
            and bool(job.required_skills)
        ),
    }


def active_jobs():
    return db.session.scalars(
        db.select(Job)
        .where(*eligible_conditions())
        .order_by(Job.featured.desc(), Job.posted_date.desc(), Job.id)
        .limit(current_app.config["MAX_RANKING_JOBS"])
    ).all()


def engine():
    return current_app.extensions["recommendation_engine"]


def recommendations(user, extra_skills=None, jobs=None):
    profile = profile_data(user)
    if extra_skills:
        profile["skills"] = normalize_skills(profile["skills"] + extra_skills)
    return engine().rank(profile, active_jobs() if jobs is None else jobs)


def snapshot(user, reason="profile", force=False):
    jobs = active_jobs()
    profile = profile_data(user)
    weights = configured_weights()
    payload = [profile, weights, [j.as_dict() for j in jobs]]
    fingerprint = hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode()
    ).hexdigest()
    latest = db.session.scalar(
        db.select(RecommendationRun)
        .where(RecommendationRun.user_id == user.id)
        .order_by(RecommendationRun.id.desc())
    )
    if latest and latest.fingerprint == fingerprint and not force:
        return latest
    rows = engine().rank(profile, jobs)
    run = RecommendationRun(
        user_id=user.id,
        fingerprint=fingerprint,
        reason=reason,
        weights=dict(weights),
        profile_summary={
            "skills": user.skill_names,
            "role": user.preferred_role,
            "confidence": confidence(profile),
        },
    )
    db.session.add(run)
    db.session.flush()
    for row in rows[:50]:
        job = row["job"]
        db.session.add(
            Recommendation(
                run_id=run.id,
                job_id=job.id,
                job_title=job.job_title,
                company_name=job.company_name,
                overall_score=row["score"],
                scores=row["scores"],
            )
        )
    db.session.commit()
    return run
