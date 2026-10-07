import io
import secrets
import pytest
from docx import Document
from app import create_app
from models.database import db, User, Job, CandidateSkill
from services.data_service import generate_dataset, clean_job_rows


@pytest.fixture
def app(tmp_path):
    application = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-only-secret-not-a-deployment-key",
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "INSTANCE_PATH": str(tmp_path / "instance"),
            "SEED_ON_START": False,
            "WTF_CSRF_ENABLED": False,
            "MODEL_CACHE": False,
            "TEST_PASSWORD_HASH_METHOD": "pbkdf2:sha256:1000",
            "MAIL_BACKEND": "memory",
            "MAIL_ASYNC": False,
        }
    )
    with application.app_context():
        raw = generate_dataset(tmp_path / "jobs.csv", count=48)
        rows, _ = clean_job_rows(raw)
        db.session.add_all([Job(**row) for row in rows])
        candidate = User(
            full_name="Test Candidate",
            email="candidate@example.com",
            city="Kolkata",
            state="West Bengal",
            education="BTech Computer Science",
            experience_years=1,
            expected_salary=500000,
            preferred_role="Data Analyst",
            preferred_location="Kolkata / Remote",
            employment_type="Full-time",
            projects="Retail data analysis, sales reporting and KPI dashboards in SQL and Power BI.",
        )
        candidate.set_password("Testpass123")
        candidate.skills = [
            CandidateSkill(skill_name=s)
            for s in ["SQL", "Excel", "Python", "Power BI", "Statistics"]
        ]
        admin = User(full_name="Test Admin", email="admin@example.com", is_admin=True)
        application.config["TEST_ADMIN_PASSWORD"] = secrets.token_urlsafe(24) + "9a"
        admin.set_password(application.config["TEST_ADMIN_PASSWORD"])
        db.session.add_all([candidate, admin])
        db.session.commit()
    yield application
    with application.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def logged_in(client):
    response = client.post(
        "/login", data={"email": "candidate@example.com", "password": "Testpass123"}
    )
    assert response.status_code == 302
    return client


@pytest.fixture
def admin_client(client):
    response = client.post(
        "/admin/login",
        data={
            "email": "admin@example.com",
            "password": client.application.config["TEST_ADMIN_PASSWORD"],
        },
    )
    assert response.status_code == 302
    return client


@pytest.fixture
def resume_docx():
    doc = Document()
    for text in [
        "Test Candidate",
        "Education",
        "B.Tech Computer Science",
        "Experience",
        "1 year of experience in data analysis",
        "Skills",
        "Python, SQL, Microsoft Excel, PowerBI",
        "Projects",
        "Retail sales dashboard built using Python and SQL.",
        "Certifications",
        "Data analytics certification",
    ]:
        doc.add_paragraph(text)
    output = io.BytesIO()
    doc.save(output)
    return output.getvalue()
