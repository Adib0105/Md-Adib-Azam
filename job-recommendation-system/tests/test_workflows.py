import io
from datetime import date, timedelta
import pytest
from models.database import db, User, Job, SavedJob, Application, RecommendationRun
from services.data_service import generate_dataset, clean_job_rows, seed_jobs


@pytest.mark.parametrize(
    "path",
    [
        "/dashboard",
        "/profile",
        "/recommendations",
        "/jobs",
        "/jobs/1",
        "/saved",
        "/applications",
        "/insights",
        "/skills",
        "/simulator",
        "/history",
        "/methodology",
    ],
)
def test_candidate_pages(logged_in, path):
    result = logged_in.get(path)
    assert result.status_code == 200
    assert b"Traceback" not in result.data


def test_job_filters_search_and_pagination(logged_in):
    result = logged_in.get(
        "/api/jobs?q=python&location=Remote&min_salary=100000&sort=salary"
    )
    assert result.status_code == 200
    assert all(
        row["location"] == "Remote" and row["max_salary"] >= 100000
        for row in result.json["items"]
    )
    first = logged_in.get("/api/jobs").json
    second = logged_in.get("/api/jobs?page=2").json
    assert first["total"] == 48 and first["pages"] == 4
    assert {x["id"] for x in first["items"]}.isdisjoint(
        {x["id"] for x in second["items"]}
    )
    assert logged_in.get("/jobs?min_salary=abc").status_code == 400
    assert logged_in.get("/jobs?min_salary=100&max_salary=1").status_code == 400
    assert logged_in.get("/jobs?page=bad").status_code == 400
    assert logged_in.get("/api/jobs?skills=PowerBI").status_code == 200
    assert logged_in.get("/api/jobs?q=zzzzunfindable").json["total"] == 0


def test_save_apply_status_and_owner_isolation(app, logged_in):
    assert logged_in.post("/jobs/1/save").status_code == 302
    assert logged_in.get("/saved").status_code == 200
    assert logged_in.post("/jobs/1/apply").status_code == 302
    assert logged_in.post("/jobs/1/apply").status_code == 302
    with app.app_context():
        assert db.session.scalar(db.select(db.func.count(Application.id))) == 1
        application_id = db.session.scalar(db.select(Application.id))
    assert (
        logged_in.post(
            f"/applications/{application_id}/status", data={"status": "Interview"}
        ).status_code
        == 302
    )
    assert (
        logged_in.post(
            f"/applications/{application_id}/status", data={"status": "bad"}
        ).status_code
        == 400
    )
    outsider = app.test_client()
    outsider.post(
        "/register",
        data={
            "full_name": "Other",
            "email": "other@example.com",
            "password": "Otherpass123",
            "confirm_password": "Otherpass123",
        },
    )
    assert (
        outsider.post(
            f"/applications/{application_id}/status", data={"status": "Offer"}
        ).status_code
        == 404
    )
    assert (
        b"Interview"
        not in outsider.get("/applications").data.split(
            b'<div class="panel table-wrap">'
        )[-1]
        or b"Your next step starts here" in outsider.get("/applications").data
    )
    assert logged_in.post("/jobs/1/save").status_code == 302
    with app.app_context():
        assert db.session.scalar(db.select(db.func.count(SavedJob.id))) == 0


def test_profile_validation_xss_and_history(app, logged_in):
    profile = {
        "full_name": "<script>alert(1)</script>",
        "education": "Diploma",
        "experience_years": "0",
        "skills": "SQL, MS Excel, Excel",
        "preferred_role": "Data Analyst",
        "expected_salary": "500000",
    }
    assert logged_in.post("/profile", data=profile).status_code == 302
    response = logged_in.get("/profile")
    assert b"<script>alert(1)</script>" not in response.data
    assert b"&lt;script&gt;" in response.data
    with app.app_context():
        user = db.session.scalar(
            db.select(User).where(User.email == "candidate@example.com")
        )
        assert set(user.skill_names) == {"SQL", "Excel"}
        assert user.experience_years == 0
        assert db.session.scalar(db.select(db.func.count(RecommendationRun.id))) == 1
    assert (
        logged_in.post(
            "/profile", data={**profile, "expected_salary": "NaN"}
        ).status_code
        == 400
    )
    assert (
        logged_in.post(
            "/profile", data={**profile, "experience_years": "-1"}
        ).status_code
        == 400
    )
    assert logged_in.post("/api/recommend").status_code == 200
    assert logged_in.get("/history").status_code == 200


def test_simulator_validation(logged_in):
    assert (
        logged_in.post("/simulator", data={"skills": "Tableau,DAX"}).status_code == 200
    )
    assert logged_in.post("/simulator", data={"skills": "SQL"}).status_code == 400
    assert (
        logged_in.post("/simulator", data={"skills": "Unknown super skill"}).status_code
        == 400
    )


def test_admin_crud_invalidates_job_and_preserves_application(app, admin_client):
    data = {
        "job_title": "Test Engineer",
        "company_name": "Example Lab",
        "job_description": "Build a Python testing workflow.",
        "location": "Remote",
        "salary_min": "400000",
        "salary_max": "600000",
        "experience_min": "0",
        "experience_max": "2",
        "required_skills": "Python,SQL",
        "employment_type": "Full-time",
        "active": "on",
        "is_synthetic": "on",
    }
    assert admin_client.post("/admin/jobs/new", data=data).status_code == 302
    with app.app_context():
        job = db.session.scalar(db.select(Job).where(Job.job_title == "Test Engineer"))
        job_id = job.id
        user = db.session.scalar(
            db.select(User).where(User.email == "candidate@example.com")
        )
        db.session.add(Application(user_id=user.id, job_id=job_id))
        db.session.commit()
    assert (
        admin_client.post(
            f"/admin/jobs/{job_id}/edit", data={**data, "job_title": "Updated Engineer"}
        ).status_code
        == 302
    )
    assert (
        admin_client.post(
            f"/admin/jobs/{job_id}/edit", data={**data, "salary_max": "1"}
        ).status_code
        == 400
    )
    assert admin_client.post(f"/admin/jobs/{job_id}/delete").status_code == 302
    with app.app_context():
        assert not db.session.get(Job, job_id).active
        assert db.session.scalar(db.select(db.func.count(Application.id))) == 1
    assert admin_client.post(f"/jobs/{job_id}/apply").status_code == 400
    for path in [
        "/admin/",
        "/admin/jobs",
        "/admin/users",
        "/admin/jobs/new",
        f"/admin/jobs/{job_id}/edit",
    ]:
        assert admin_client.get(path).status_code == 200


def test_expired_jobs_excluded(app, logged_in):
    with app.app_context():
        job = db.session.get(Job, 1)
        job.application_deadline = date.today() - timedelta(days=1)
        db.session.commit()
    assert logged_in.get("/api/jobs").json["total"] == 47
    assert logged_in.post("/jobs/1/apply").status_code == 400
    assert logged_in.get("/jobs/1").status_code == 200


def test_size_limit(logged_in):
    assert (
        logged_in.post(
            "/resume/upload",
            data={"resume": (io.BytesIO(b"a" * 6 * 1024 * 1024), "big.pdf")},
        ).status_code
        == 413
    )


def test_dataset_diversity_and_cleaning(app, tmp_path):
    raw = generate_dataset(tmp_path / "dataset.csv")
    assert len(raw) >= 500
    assert len({r["job_description"] for r in raw}) == len(raw)
    assert len({r["job_title"] for r in raw}) == 24
    assert len({r["location"] for r in raw if r["job_title"] == "Data Analyst"}) == 12
    valid = {
        **raw[0],
        "salary_min": "600,000",
        "salary_max": "400000",
        "required_skills": "MS Excel | Excel | SQL",
    }
    rows, errors = clean_job_rows(
        [
            valid,
            valid,
            {**raw[1], "salary_min": "-1"},
            {**raw[2], "required_skills": "", "salary_min": "", "salary_max": ""},
        ]
    )
    assert len(rows) == 2 and len(errors) == 1
    assert rows[0]["min_salary"] == 400000 and rows[0]["max_salary"] == 600000
    assert rows[0]["required_skills"] == ["Excel", "SQL"]
    assert rows[1]["required_skills"]


def test_restart_persistence_and_idempotent_seed(tmp_path):
    from app import create_app

    config = {
        "TESTING": True,
        "SECRET_KEY": "temporary-test-key",
        "INSTANCE_PATH": str(tmp_path / "persist"),
        "SQLALCHEMY_DATABASE_URI": "sqlite:///persistence.db",
        "SEED_ON_START": False,
        "MODEL_CACHE": True,
    }
    generate_dataset(tmp_path / "data" / "jobs.csv", count=30)
    first = create_app(config)
    with first.app_context():
        assert seed_jobs(tmp_path / "data")["added"] == 30
        assert seed_jobs(tmp_path / "data")["added"] == 0
        user = User(full_name="Persistent", email="persist@example.com")
        user.set_password("Persist123")
        db.session.add(user)
        db.session.commit()
        db.session.remove()
    second = create_app(config)
    with second.app_context():
        assert db.session.scalar(db.select(db.func.count(Job.id))) == 30
        assert db.session.scalar(
            db.select(User).where(User.email == "persist@example.com")
        ).check_password("Persist123")
