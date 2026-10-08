import hashlib
import json
import math
from datetime import timedelta
from types import SimpleNamespace
import numpy as np
import pytest
from config import HYBRID_WEIGHTS, validate_ml_config
from models.database import db, User, utcnow
from ml.models.embeddings import EmbeddingService
from ml.models.rankers import train_ranker, PortableRanker, RankerRegistry, canonical
from ml.features.schema import feature_vector, feature_matrix, FEATURE_NAMES
from ml.features.representation import serialize_representation
from ml.features.behavior import build_behavior, behavior_score
from ml.pipelines.hybrid import hybrid_weights
from ml.evaluation.metrics import ranking_metrics
from services.recommendation_service import recommendations, engine, active_jobs
from services.career_intelligence import skill_gap, learning_path
from ml.preprocessing.resume_intelligence import analyze_resume, resume_quality
from ml.preprocessing.text import candidate_text


class FixtureEncoder:
    """Deterministic test double, never used for evaluation quality claims."""

    def __init__(self):
        self.calls = []

    def encode(self, texts, **kwargs):
        self.calls.append((texts, kwargs))
        return np.asarray(
            [
                [byte + 1 for byte in hashlib.sha256(text.encode()).digest()[:4]]
                for text in texts
            ],
            dtype=float,
        )


def embedding(tmp_path, revision="fixture-v1", encoder=None):
    return EmbeddingService(
        {
            "EMBEDDINGS_ENABLED": True,
            "EMBEDDING_DIMENSION": 4,
            "EMBEDDING_MODEL_REVISION": revision,
            "EMBEDDING_BATCH_SIZE": 2,
        },
        tmp_path,
        encoder=encoder or FixtureEncoder(),
    )


def test_embedding_batch_cache_content_changes_and_candidate_privacy(tmp_path):
    service = embedding(tmp_path)
    original = service.vectors(
        ["SQL dashboards", "Python services", "SQL dashboards"], persist=True
    )
    assert len(service.encoder.calls) == 1 and len(service.encoder.calls[0][0]) == 2
    assert service.encoder.calls[0][1]["batch_size"] == 2
    assert np.allclose(np.linalg.norm(original, axis=1), 1)
    assert np.array_equal(
        service.vectors(["SQL dashboards"], persist=True)[0], original[0]
    )
    assert service.encoded == 2
    restarted = embedding(tmp_path)
    assert np.allclose(
        restarted.vectors(["SQL dashboards"], persist=True)[0], original[0]
    )
    assert restarted.encoded == 0
    restarted.vectors(["SQL dashboards updated"], persist=True)
    assert restarted.encoded == 1
    changed_model = embedding(tmp_path, "fixture-v2")
    changed_model.vectors(["SQL dashboards"], persist=True)
    assert changed_model.encoded == 1
    assert service.vectors([]).shape == (0, 4)


def test_embedding_corrupt_cached_vector_is_rebuilt(tmp_path):
    import sqlite3

    first = embedding(tmp_path)
    first.vectors(["SQL"], persist=True)
    with sqlite3.connect(first.cache_path) as connection:
        connection.execute("UPDATE embeddings SET vector='[NaN]'")
    restarted = embedding(tmp_path)
    assert restarted.vectors(["SQL"], persist=True).shape == (1, 4)
    assert restarted.encoded == 1


def test_embedding_missing_backend_attempted_once_and_fallback(tmp_path):
    service = EmbeddingService({"EMBEDDINGS_ENABLED": True}, tmp_path)
    assert service.similarities("candidate", ["job"]) is None
    assert service.reason == "local_model_missing" and service.attempted
    assert service.similarities("other candidate", ["other job"]) is None
    assert service.encoded == 0


def test_embedding_load_is_local_only_and_version_checked(tmp_path, monkeypatch):
    import sys

    path = tmp_path / "model"
    path.mkdir()
    (path / "jobmatch-model.json").write_text(
        json.dumps({"model_name": "fixture", "revision": "commit"})
    )
    captured = []

    class Backend(FixtureEncoder):
        def __init__(self, *args, **kwargs):
            super().__init__()
            captured.append(kwargs)

        def get_sentence_embedding_dimension(self):
            return 4

    monkeypatch.setitem(
        sys.modules,
        "sentence_transformers",
        SimpleNamespace(SentenceTransformer=Backend),
    )
    config = {
        "EMBEDDINGS_ENABLED": True,
        "EMBEDDING_MODEL_NAME": "fixture",
        "EMBEDDING_MODEL_REVISION": "commit",
        "EMBEDDING_MODEL_PATH": str(path),
        "EMBEDDING_DIMENSION": 4,
    }
    service = EmbeddingService(config, tmp_path)
    assert service.vectors(["SQL"]) is not None
    assert (
        captured[0]["local_files_only"] is True
        and captured[0]["trust_remote_code"] is False
    )
    assert captured[0]["model_kwargs"] == {"use_safetensors": True}
    wrong = EmbeddingService(
        {**config, "EMBEDDING_MODEL_REVISION": "different"}, tmp_path
    )
    assert wrong.load() is None and wrong.reason == "model_version_mismatch"


def test_hybrid_weights_are_normalized_and_behavior_bounded():
    values = hybrid_weights(HYBRID_WEIGHTS, False)
    assert sum(values.values()) == pytest.approx(1)
    assert values["semantic"] == values["behavior"] == 0
    adapted = hybrid_weights(HYBRID_WEIGHTS, True, {"enabled": True})
    assert adapted["behavior"] == 0.10 and sum(adapted.values()) == pytest.approx(1)


def test_hybrid_semantic_and_lexical_are_distinct(app, tmp_path):
    with app.app_context():
        service = embedding(tmp_path)
        app.extensions["hybrid_recommender"].embeddings = service
        user = db.session.scalar(db.select(User).where(User.is_admin.is_(False)))
        rows = recommendations(user)
        assert rows[0]["scores"]["semantic"] is not None
        assert rows[0]["score"] == pytest.approx(
            sum(rows[0]["contributions"].values()), abs=0.1
        )
        assert rows[0]["scores"]["tfidf"] != rows[0]["scores"]["semantic"]
        count = service.encoded
        assert recommendations(user)[0]["reasons"] == rows[0]["reasons"]
        assert service.encoded == count


@pytest.mark.parametrize(
    "invalid", [float("nan"), float("inf"), -1, 101, "not-a-number"]
)
def test_invalid_features_are_rejected(invalid):
    with pytest.raises((ValueError, TypeError)):
        feature_vector({"skills": invalid})


def test_feature_contract_excludes_labels_and_identities():
    a = feature_vector(
        {"skills": 50, "relevance_label": 3, "candidate_id": "person", "gender": "male"}
    )
    b = feature_vector({"skills": 50})
    assert a == b and len(a) == len(FEATURE_NAMES)
    assert feature_matrix([]).shape == (0, len(FEATURE_NAMES))


def test_stopword_only_and_punctuation_job_text_does_not_break_ranking(app):
    from models.database import Job

    with app.app_context():
        job = Job(
            id=9999,
            job_title="!!!",
            company_name="Unknown",
            job_description="the and of",
            required_skills=[],
            preferred_skills=[],
            posted_date=utcnow().date(),
            experience_min=0,
            is_external=True,
            experience_known=False,
            location="Unspecified",
            employment_type="Full-time",
        )
        rows = engine().rank_baseline({"skills": []}, [job])
        assert len(rows) == 1 and math.isfinite(rows[0]["score"])
        assert rows[0]["scores"]["semantic"] == 0 and rows[0]["scores"]["role"] == 0


@pytest.mark.parametrize("kind", ["logistic", "random_forest"])
def test_ranker_training_persistence_inference_and_explanation(tmp_path, kind):
    matrix = np.random.default_rng(2026).random((40, len(FEATURE_NAMES)))
    labels = np.asarray([0, 1, 2, 3] * 10)
    ranker = train_ranker(
        matrix, labels, kind, dataset_version="unit-fixture", dataset_kind="synthetic"
    )
    prediction = ranker.predict(matrix)
    path = tmp_path / "ranker.json"
    ranker.save(path)
    restored = PortableRanker.load(path)
    assert np.allclose(prediction, restored.predict(matrix))
    assert set(restored.explain(matrix[:1])) == set(FEATURE_NAMES)
    assert (
        np.isfinite(prediction).all()
        and (prediction >= 0).all()
        and (prediction <= 100).all()
    )
    assert restored.predict(np.empty((0, len(FEATURE_NAMES)))).size == 0
    assert restored.metadata["training_samples"] == 40


def test_logistic_binary_ordinal_export_parity():
    matrix = np.random.default_rng(5).random((20, len(FEATURE_NAMES)))
    ranker = train_ranker(
        matrix, [0, 3] * 10, dataset_version="binary-fixture", dataset_kind="synthetic"
    )
    assert ranker.predict(matrix).shape == (20,)


def rehash(artifact):
    artifact["sha256"] = hashlib.sha256(
        canonical({key: artifact[key] for key in ["metadata", "model"]})
    ).hexdigest()


@pytest.mark.parametrize(
    "field,value",
    [
        ("feature_version", "old"),
        ("feature_names", ["label"]),
        ("dependency_versions", {}),
        ("dataset_kind", "fabricated"),
    ],
)
def test_incompatible_artifact_metadata_is_rejected(field, value):
    matrix = np.random.default_rng(3).random((12, len(FEATURE_NAMES)))
    artifact = train_ranker(
        matrix, [0, 1, 2] * 4, dataset_version="fixture", dataset_kind="synthetic"
    ).artifact
    artifact["metadata"][field] = value
    rehash(artifact)
    with pytest.raises(ValueError):
        PortableRanker(artifact)


def test_artifact_digest_corruption_and_cyclic_tree_are_rejected():
    matrix = np.random.default_rng(3).random((20, len(FEATURE_NAMES)))
    artifact = train_ranker(
        matrix,
        [0, 1, 2, 3] * 5,
        "random_forest",
        dataset_version="fixture",
        dataset_kind="synthetic",
    ).artifact
    artifact["model"]["trees"][0]["left"][0] = 0
    with pytest.raises(ValueError, match="integrity"):
        PortableRanker(artifact)
    rehash(artifact)
    with pytest.raises(ValueError, match="cyclic"):
        PortableRanker(artifact)


def test_corrupt_ranker_keeps_recommendations_available(app):
    from pathlib import Path

    with app.app_context():
        app.config["ML_STRATEGY"] = "ltr"
        path = Path(app.instance_path) / "ml/ranker.json"
        path.parent.mkdir()
        path.write_text("corrupted artifact")
        user = db.session.scalar(db.select(User).where(User.is_admin.is_(False)))
        rows = recommendations(user)
        assert rows and rows[0]["model"]["strategy"] == "hybrid"
        assert rows[0]["model"]["ranker_status"] == "invalid_or_incompatible_artifact"


def test_frozen_training_vocabulary_persists_and_synthetic_is_opt_in(app):
    from pathlib import Path

    with app.app_context():
        jobs = active_jobs()
        features = engine().features_for(jobs)
        matrix = np.random.default_rng(8).random((20, len(FEATURE_NAMES)))
        ranker = train_ranker(
            matrix,
            [0, 1, 2, 3] * 5,
            dataset_version="fixture",
            dataset_kind="synthetic",
            representation=serialize_representation(features),
        )
        path = Path(app.instance_path) / "ml/ranker.json"
        ranker.save(path)
        assert RankerRegistry(app.instance_path).load() is None
        registry = RankerRegistry(app.instance_path, allow_synthetic=True)
        restored = registry.load()
        assert restored is not None
        assert np.allclose(
            restored.frozen_features()[0].transform(["SQL dashboards"]).toarray(),
            features[0].transform(["SQL dashboards"]).toarray(),
        )
        app.extensions["ranker_registry"] = registry
        app.extensions["hybrid_recommender"].registry = registry
        user = db.session.scalar(db.select(User).where(User.is_admin.is_(False)))
        rows = recommendations(user, strategy="ltr")
        assert rows[0]["model"]["strategy"] == "ltr"
        assert rows[0]["score"] == pytest.approx(
            sum(rows[0]["contributions"].values()), abs=0.1
        )
        assert rows[0]["ml_explanation"]


def test_metrics_against_hand_calculated_values():
    values = ranking_metrics(["b", "a", "d", "c"], {"a": 3, "b": 0, "c": 2, "d": 1})
    assert values["precision@5"] == 2 / 5 and values["recall@5"] == 1
    assert values["mrr"] == values["map"] == 0.5
    ideal = 7 + 3 / math.log2(3) + 1 / math.log2(4)
    actual = 7 / math.log2(3) + 1 / math.log2(4) + 3 / math.log2(5)
    assert values["ndcg@5"] == pytest.approx(actual / ideal)
    assert all(value == 0 for value in ranking_metrics([], {}).values())


@pytest.mark.parametrize(
    "ids,judgments", [([1, 1], {1: 3}), ([2], {1: 3}), ([1], {1: 4})]
)
def test_metrics_reject_invalid_judgments(ids, judgments):
    with pytest.raises(ValueError):
        ranking_metrics(ids, judgments)


def test_cold_start_deduplicates_repeated_views_and_ignores_future_events():
    now = utcnow()
    job = SimpleNamespace(
        job_title="Data Analyst",
        location="Remote",
        required_skills=["SQL"],
        employment_type="Full-time",
        remote_type="remote",
    )
    events = [{"job_id": 1, "action": "viewed", "at": now, "job": job}] * 100
    events += [
        {"job_id": 2, "action": "applied", "at": now + timedelta(days=1), "job": job}
    ]
    profile = build_behavior(events, cutoff=now)
    assert profile["distinct_jobs"] == 1 and not profile["enabled"]
    assert behavior_score(profile, job) == 50


def test_behavior_uses_only_prior_distinct_meaningful_jobs_and_outcome_rejection_is_neutral():
    now = utcnow()
    job = SimpleNamespace(
        job_title="Data Analyst",
        location="Remote",
        required_skills=["SQL"],
        employment_type="Full-time",
        remote_type="remote",
    )
    events = [
        {
            "id": i,
            "job_id": i,
            "action": "applied" if i <= 3 else "viewed",
            "at": now,
            "job": job,
        }
        for i in range(1, 6)
    ]
    before = build_behavior(events, cutoff=now)
    events.append(
        {"id": 9, "job_id": 1, "action": "outcome_rejected", "at": now, "job": job}
    )
    after = build_behavior(events, cutoff=now)
    assert before["enabled"] and before["preferences"] == after["preferences"]
    assert behavior_score(before, job) > 50


def test_skill_gaps_partial_matches_and_prerequisite_order():
    gap = skill_gap(
        ["SQL", "MS Excel"],
        ["SQL", "Excel", "Pandas", "Machine Learning"],
        {"SQL": "Beginner"},
    )
    assert gap["matched"] == ["Excel"] and gap["partial"] == ["SQL"]
    assert gap["gap_percent"] == 62.5
    path = learning_path(["SQL", "Excel"], gap)
    names = [item["skill"] for item in path]
    assert (
        names.index("Python") < names.index("Pandas") < names.index("Machine Learning")
    )
    assert (
        names.index("Probability")
        < names.index("Statistics")
        < names.index("Machine Learning")
    )
    assert names[-1] == "Portfolio project"
    assert skill_gap([], [])["readiness"] is None
    assert "SQL" in skill_gap(["PostgreSQL"], ["SQL"])["partial"]


def test_resume_evidence_quality_and_sensitive_ranking_exclusion():
    text = "Skills: Python, SQL, PowerBI, Communication\nProjects\nPython and SQL dashboard covering 1000 records\nEducation\nBTech\nExperience\nData Analyst at Example Labs (2024)\n1 year of experience\nCertifications\nSQL certificate"
    intelligence = analyze_resume(text)
    assert "Power BI" in intelligence["technical_skills"]
    assert "Communication" in intelligence["soft_skills"]
    assert intelligence["organizations"] == ["Example Labs "] or intelligence[
        "organizations"
    ] == ["Example Labs"]
    assert any(
        row["skill"] == "Python" and row["confidence"] == 0.85
        for row in intelligence["skill_inventory"]
    )
    quality = resume_quality(
        {
            "resume_text": text,
            "projects": "Python 1000 records",
            "skills": ["Python"],
            "education": "BTech",
            "preferred_role": "Python Developer",
        },
        intelligence,
    )
    assert quality["score"] == pytest.approx(
        sum(component["points"] for component in quality["components"]), abs=0.1
    )
    assert resume_quality({}, analyze_resume(""))["score"] == 0
    a = candidate_text(
        {
            "skills": ["SQL"],
            "resume_text": "Name One religion gender",
            "full_name": "Name One",
            "gender": "male",
        }
    )
    b = candidate_text(
        {
            "skills": ["SQL"],
            "resume_text": "Name Two",
            "full_name": "Name Two",
            "gender": "female",
        }
    )
    assert a == b == "SQL"


@pytest.mark.parametrize(
    "setting,value",
    [
        ("ML_STRATEGY", "invalid"),
        ("BEHAVIOR_MAX_WEIGHT", 0.8),
        ("BEHAVIOR_MIN_JOBS", 1),
        ("EMBEDDING_BATCH_SIZE", 0),
    ],
)
def test_invalid_ml_configuration_is_rejected(app, setting, value):
    with pytest.raises(ValueError):
        validate_ml_config({**app.config, setting: value})
