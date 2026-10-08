import io
import json
from pathlib import Path
import pytest
from models.database import db, User, ResumeDraft
from models.ml_data import (
    InteractionEvent,
    Experiment,
    ExperimentAssignment,
    RecommendationExposure,
)
from ml.pipelines.demo_dataset import create_demo_dataset
from ml.pipelines.dataset import (
    load_dataset,
    split_dataset,
    validate_complete_judgments,
)
from ml.evaluation.evaluate_models import evaluate
from services.recommendation_service import (
    recommendations,
    snapshot,
    engine,
    active_jobs,
)


def test_candidate_group_split_and_honest_evaluation(tmp_path):
    path = tmp_path / "demo.jsonl"
    create_demo_dataset(path)
    records, version = load_dataset(path)
    train, test, _ = split_dataset(records)
    assert not {r["candidate_id"] for r in train} & {r["candidate_id"] for r in test}
    assert len(train) == 180 and len(test) == 60 and len(version) == 64
    report = evaluate(path)
    assert report["dataset"]["kind"] == "synthetic"
    assert report["best_model"] is None and report["best_model_on_fixture"]
    assert report["models"]["embedding"]["metrics"] is None
    assert report["models"]["ltr_logistic"]["metrics"]["ndcg@10"] >= 0
    assert report["dataset"]["evaluation_candidates"] == 3


def test_empty_or_insufficient_dataset_never_fabricates_metrics(tmp_path):
    path = tmp_path / "empty.jsonl"
    path.write_text("")
    report = evaluate(path)
    assert report["status"] == "insufficient_data"
    assert all(result["metrics"] is None for result in report["models"].values())


@pytest.mark.parametrize(
    "change",
    ["label", "sensitive", "future", "duplicate", "bad_skill", "bad_experience"],
)
def test_dataset_rejects_leakage_invalid_data_and_future_snapshots(tmp_path, change):
    path = tmp_path / "input.jsonl"
    create_demo_dataset(path)
    record = json.loads(path.read_text().splitlines()[0])
    if change == "label":
        record["relevance_label"] = 4
    elif change == "sensitive":
        record["candidate_features"]["gender"] = "male"
    elif change == "future":
        record["job_features"]["posted_date"] = "2027-01-01"
    elif change == "bad_skill":
        record["candidate_features"]["skills"] = 7
    elif change == "bad_experience":
        record["candidate_features"]["experience_years"] = float("nan")
    contents = json.dumps(record) + "\n"
    if change == "duplicate":
        contents += contents
    path.write_text(contents)
    with pytest.raises((ValueError, TypeError)):
        load_dataset(path)


def test_unjudged_pairs_are_not_treated_as_negative(tmp_path):
    path = tmp_path / "input.jsonl"
    create_demo_dataset(path)
    records, _ = load_dataset(path)
    with pytest.raises(ValueError, match="unjudged"):
        validate_complete_judgments(records[1:])


def test_temporal_split_uses_utc_and_label_availability(tmp_path):
    path = tmp_path / "temporal.jsonl"
    create_demo_dataset(path)
    template = json.loads(path.read_text().splitlines()[0])
    timestamps = [
        "2026-10-02T10:00:00+02:00",
        "2026-10-02T09:00:00+00:00",
        "2026-10-02T10:30:00+00:00",
        "2026-10-02T07:00:00-04:00",
    ]
    rows = []
    for index, timestamp in enumerate(timestamps):
        row = json.loads(json.dumps(template))
        row.update(
            dataset_kind="behavioral",
            candidate_id=f"snapshot-{index}",
            snapshot_at=timestamp,
            behavior_cutoff=timestamp,
            judged_at=timestamp,
        )
        row["job_features"]["is_synthetic"] = False
        row["job_features"]["posted_date"] = "2026-10-01"
        rows.append(row)
    # A late observation cannot fit a model pretending to predict before that observation.
    rows[0]["judged_at"] = "2026-10-03T00:00:00+00:00"
    path.write_text("\n".join(json.dumps(row) for row in rows))
    records, _ = load_dataset(path)
    train, test, _ = split_dataset(records)
    assert {r["candidate_id"] for r in test} == {"snapshot-3"}
    assert {r["candidate_id"] for r in train} == {"snapshot-1", "snapshot-2"}
    rows[1].pop("judged_at")
    path.write_text("\n".join(json.dumps(row) for row in rows))
    with pytest.raises(ValueError, match="observation time"):
        load_dataset(path)


def test_real_snapshot_preserves_unknown_and_noncomparable_fields(tmp_path):
    path = tmp_path / "manual.jsonl"
    create_demo_dataset(path)
    row = json.loads(path.read_text().splitlines()[0])
    row["dataset_kind"] = "manual"
    with pytest.raises(ValueError, match="synthetic"):
        path.write_text(json.dumps(row))
        load_dataset(path)
    row["job_features"].update(
        is_synthetic=False,
        is_external=True,
        experience_known=False,
        salary_currency="USD",
        salary_period="hour",
        remote_type="hybrid",
        remote_allowed=True,
    )
    path.write_text(json.dumps(row))
    records, _ = load_dataset(path)
    fields = records[0]["cleaned_job"]
    assert fields["salary_currency"] == "USD" and fields["salary_period"] == "hour"
    assert fields["experience_known"] is False and fields["is_external"] is True
    assert fields["remote_type"] == "hybrid" and fields["remote_allowed"] is True


def test_blind_review_export_is_private_unlabeled_and_preserves_provenance(app):
    from scripts.export_relevance_template import export_review_template

    path, count, kind = export_review_template(app, max_candidates=1, max_jobs=2)
    rows = [json.loads(line) for line in path.read_text().splitlines()]
    assert count == 2 and kind == "synthetic" and path.stat().st_mode & 0o777 == 0o600
    assert all(
        row["relevance_label"] is None and row["dataset_kind"] == kind for row in rows
    )
    assert all(
        "email" not in row["candidate_features"]
        and "full_name" not in row["candidate_features"]
        for row in rows
    )
    assert all("salary_currency" in row["job_features"] for row in rows)
    with pytest.raises(ValueError, match="label"):
        load_dataset(path)
    with pytest.raises(FileExistsError):
        export_review_template(app)


def test_v2_to_v3_migration_preserves_profile_tracker_and_recommendation_history(
    tmp_path,
):
    import sqlite3
    from app import create_app
    from models.database import Job, Application, SavedJob, RecommendationRun, utcnow

    settings = {
        "TESTING": True,
        "TEST_PASSWORD_HASH_METHOD": "pbkdf2:sha256:1000",
        "SECRET_KEY": "migration-fixture-only",
        "INSTANCE_PATH": str(tmp_path),
        "SEED_ON_START": False,
        "MODEL_CACHE": False,
        "ML_STRATEGY": "weighted",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///v2.sqlite",
    }
    previous = create_app(settings)
    with previous.app_context():
        user = User(
            full_name="Retained Profile",
            email="migration-fixture@example.com",
            resume_text="Reviewed resume retained",
            preferred_role="Data Analyst",
        )
        user.set_password("migration-fixture-only")
        job = Job(
            job_title="Data Analyst",
            company_name="Migration Fixture",
            posted_date=utcnow().date(),
            required_skills=["SQL"],
            preferred_skills=[],
        )
        db.session.add_all([user, job])
        db.session.flush()
        db.session.add_all(
            [
                SavedJob(user_id=user.id, job_id=job.id),
                Application(user_id=user.id, job_id=job.id, status="Interview"),
            ]
        )
        db.session.commit()
        run = snapshot(user)
        user_id, run_id, score, fingerprint = (
            user.id,
            run.id,
            run.results[0].overall_score,
            run.fingerprint,
        )
        db.session.remove()
        # Version 3 changes only these four additive tables; removing them yields the v2 layout.
        with db.engine.begin() as connection:
            for name in [
                "recommendation_exposures",
                "ml_experiment_assignments",
                "ml_experiments",
                "interaction_events",
            ]:
                db.metadata.tables[name].drop(connection)
            connection.exec_driver_sql("DELETE FROM schema_revisions WHERE version=3")
            connection.exec_driver_sql(
                "INSERT INTO schema_revisions(version,applied_at) VALUES(2,'2026-10-01')"
            )
        db.engine.dispose()
    upgraded = create_app(settings)
    with upgraded.app_context():
        assert db.session.get(User, user_id).resume_text == "Reviewed resume retained"
        assert db.session.scalar(db.select(Application.status)) == "Interview"
        assert db.session.scalar(db.select(db.func.count(SavedJob.id))) == 1
        run = db.session.get(RecommendationRun, run_id)
        assert run.fingerprint == fingerprint and run.results[0].overall_score == score
        for model in [
            InteractionEvent,
            Experiment,
            ExperimentAssignment,
            RecommendationExposure,
        ]:
            assert db.session.scalar(db.select(db.func.count()).select_from(model)) == 0
        backups = list((tmp_path / "backups").glob("upgrade-v3-*.sqlite"))
        assert len(backups) == 1
        with sqlite3.connect(backups[0]) as backup:
            assert backup.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
            assert (
                backup.execute(
                    "SELECT fingerprint FROM recommendation_runs WHERE id=?", (run_id,)
                ).fetchone()[0]
                == fingerprint
            )
        db.session.remove()
        db.engine.dispose()


@pytest.mark.parametrize(
    "path",
    [
        "/resume/intelligence",
        "/career/path",
        "/api/personalization",
        "/api/career/gap/1",
    ],
)
def test_new_candidate_pages_auth_and_render(client, logged_in, path):
    assert client.application.test_client().get(path).status_code in {302, 401}
    assert logged_in.get(path).status_code == 200


def test_ml_lab_admin_guard_and_real_counts(app, admin_client):
    assert app.test_client().get("/admin/ml-lab").status_code in {302, 401}
    response = admin_client.get("/admin/ml-lab")
    assert b'id="charts-data"' in response.data
    assert response.status_code == 200
    text = response.get_data(as_text=True)
    assert "Recorded evaluation dataset" in text and "Synthetic evaluation" in text
    assert "Experiments are disabled by default" in text
    candidate = app.test_client()
    candidate.post(
        "/login", data={"email": "candidate@example.com", "password": "Testpass123"}
    )
    assert candidate.get("/admin/ml-lab").status_code == 403


def test_resume_to_review_profile_recommendation_integration(
    app, logged_in, resume_docx
):
    response = logged_in.post(
        "/resume/upload", data={"resume": (io.BytesIO(resume_docx), "resume.docx")}
    )
    assert "/resume/review/" in response.location
    with app.app_context():
        draft = db.session.scalar(db.select(ResumeDraft))
        assert "skill_inventory" in draft.extracted["intelligence"]
        draft_id = draft.id
        data = {
            key: draft.extracted.get(key, "")
            for key in [
                "education",
                "preferred_role",
                "certifications",
                "projects",
                "experience_summary",
            ]
        }
        data.update(
            action="confirm",
            skills=", ".join(draft.extracted["skills"]),
            experience_years="1",
            resume_text=draft.extracted["text"],
        )
    assert logged_in.post("/resume/review/" + draft_id, data=data).status_code == 302
    assert logged_in.get("/resume/intelligence").status_code == 200
    items = logged_in.get("/api/recommendations").get_json()["items"]
    assert items and items[0]["model"]["strategy"] == "hybrid"


def test_profile_save_apply_feedback_personalization_and_snapshot(app, logged_in):
    with app.app_context():
        user = db.session.scalar(db.select(User).where(User.is_admin.is_(False)))
        initial = recommendations(user)
        baseline = recommendations(user, strategy="weighted")
        job_ids = [row["job"].id for row in initial[:5]]
        first = snapshot(user)
        assert snapshot(user).id == first.id
    for identity in job_ids:
        assert logged_in.post(f"/jobs/{identity}/save").status_code == 302
    assert logged_in.post(f"/jobs/{job_ids[0]}/apply").status_code == 302
    assert (
        logged_in.post(
            f"/jobs/{job_ids[-1]}/feedback", data={"action": "ignored"}
        ).status_code
        == 302
    )
    state = logged_in.get("/api/personalization").get_json()
    assert state["enabled"] and state["distinct_jobs"] >= 5
    with app.app_context():
        user = db.session.scalar(db.select(User).where(User.is_admin.is_(False)))
        updated = recommendations(user)
        assert updated[0]["weights"]["behavior"] <= 0.10
        assert [r["score"] for r in recommendations(user, strategy="weighted")] == [
            r["score"] for r in baseline
        ]
        assert snapshot(user).id != first.id
        assert db.session.scalar(db.select(db.func.count(InteractionEvent.id))) >= 7


def test_experiment_assignment_precedes_exposure_and_is_reused(app, logged_in):
    with app.app_context():
        app.config["ML_EXPERIMENT"] = "fixture-ab"
        db.session.add(Experiment(slug="fixture-ab", enabled=True))
        db.session.commit()
    response = logged_in.get("/api/recommendations")
    assert response.status_code == 200
    with app.app_context():
        assignment = db.session.scalar(db.select(ExperimentAssignment))
        assignment_id = assignment.id
        assert all(
            exposure.assignment_id == assignment_id
            and exposure.created_at >= assignment.assigned_at
            for exposure in db.session.scalars(db.select(RecommendationExposure))
        )
        job_id = response.get_json()["items"][0]["job_id"]
    assert logged_in.get("/recommendations").status_code == 200
    assert logged_in.post(f"/jobs/{job_id}/save").status_code == 302
    with app.app_context():
        assert db.session.scalar(db.select(db.func.count(ExperimentAssignment.id))) == 1
        from routes.ml import experiment_summary

        summary = experiment_summary()
        assert sum(row["saves"] for row in summary) == 1
    admin_client = app.test_client()
    admin_client.post(
        "/admin/login",
        data={
            "email": "admin@example.com",
            "password": app.config["TEST_ADMIN_PASSWORD"],
        },
    )
    assert admin_client.get("/admin/ml-lab").status_code == 200


def test_feedback_requires_csrf_and_valid_action(app, logged_in):
    app.config["WTF_CSRF_ENABLED"] = True
    assert (
        logged_in.post("/jobs/1/feedback", data={"action": "rejected"}).status_code
        == 400
    )
    app.config["WTF_CSRF_ENABLED"] = False
    assert (
        logged_in.post("/jobs/1/feedback", data={"action": "offer"}).status_code == 400
    )
    assert (
        logged_in.post("/jobs/99999/feedback", data={"action": "ignored"}).status_code
        == 404
    )


def test_parser_timeout_is_graceful(app, monkeypatch):
    import subprocess
    from services.resume_service import parse_resume_isolated
    from models.resume_parser import ResumeError

    def timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired("worker", 15)

    monkeypatch.setattr(subprocess, "run", timeout)
    with app.app_context(), pytest.raises(ResumeError, match="timed out"):
        parse_resume_isolated("resume.docx", b"document")


def test_corrupt_or_legacy_executable_tfidf_cache_is_not_loaded(app):
    with app.app_context():
        app.config["MODEL_CACHE"] = True
        Path(app.instance_path, "model.joblib").write_bytes(b"not a trusted pickle")
        Path(app.instance_path, "tfidf-cache.npz").write_bytes(b"broken cache")
        assert engine().features_for(active_jobs()) is not None
        assert engine().fit_count == 1
        assert (
            Path(app.instance_path, "model.joblib").read_bytes()
            == b"not a trusted pickle"
        )
