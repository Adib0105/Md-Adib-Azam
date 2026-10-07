from datetime import date, timedelta
import pytest
from models.database import (
    db,
    User,
    Job,
    JobAlert,
    JobAlertDelivery,
    Notification,
    Application,
    AuditLog,
    utcnow,
)
from services.alert_service import process_due_alerts
from services.settings_service import CONTENT_DEFAULTS
from services.mail_service import send_mail


@pytest.mark.parametrize(
    "path",
    [
        "/admin/providers",
        "/admin/settings",
        "/admin/content",
        "/admin/applications",
        "/admin/analytics",
        "/admin/health",
        "/admin/email",
        "/admin/security",
        "/admin/backups",
    ],
)
def test_control_pages(admin_client, path):
    assert admin_client.get(path).status_code == 200


@pytest.mark.parametrize(
    "path",
    [
        "/",
        "/about",
        "/info/privacy",
        "/info/terms",
        "/info/faq",
        "/info/contact_details",
        "/real-jobs",
        "/api/providers",
        "/forgot-password",
    ],
)
def test_public_pages(client, path):
    assert client.get(path).status_code == 200


def test_suspend_revoke_prevent_admin_self_changes(app, admin_client):
    candidate = app.test_client()
    candidate.post(
        "/login", data={"email": "candidate@example.com", "password": "Testpass123"}
    )
    assert (
        admin_client.post(
            "/admin/users/1/status", data={"action": "suspend"}
        ).status_code
        == 302
    )
    assert candidate.get("/dashboard").status_code == 302
    assert (
        candidate.post(
            "/login", data={"email": "candidate@example.com", "password": "Testpass123"}
        ).status_code
        == 401
    )
    assert (
        admin_client.post(
            "/admin/users/2/status", data={"action": "suspend"}
        ).status_code
        == 400
    )
    admin_client.post("/admin/users/1/status", data={"action": "activate"})
    assert (
        candidate.post(
            "/login", data={"email": "candidate@example.com", "password": "Testpass123"}
        ).status_code
        == 302
    )


def test_job_flags_bulk_csv_and_public_visibility(app, admin_client):
    visitor = app.test_client()
    assert (
        admin_client.post(
            "/admin/jobs/1/action", data={"action": "unpublish"}
        ).status_code
        == 302
    )
    assert (
        visitor.get("/jobs/1").status_code == 404
        and visitor.get("/api/jobs/1").status_code == 404
    )
    assert admin_client.get("/jobs/1").status_code == 200
    admin_client.post("/admin/jobs/1/action", data={"action": "restore"})
    assert visitor.get("/jobs/1").status_code == 200
    admin_client.post(
        "/admin/jobs/bulk", data={"job_ids": ["1", "2"], "action": "archive"}
    )
    assert visitor.get("/api/jobs").json["total"] == 46
    admin_client.post(
        "/admin/jobs/bulk", data={"job_ids": ["1", "2"], "action": "activate"}
    )
    with app.app_context():
        db.session.get(Job, 1).company_name = "=DANGEROUS()"
        db.session.commit()
    csv = admin_client.post(
        "/admin/jobs/bulk", data={"job_ids": ["1"], "action": "export"}
    )
    assert csv.status_code == 200 and "'=DANGEROUS()" in csv.get_data(as_text=True)
    assert (
        admin_client.post(
            "/admin/jobs/bulk", data={"job_ids": ["bad"], "action": "delete"}
        ).status_code
        == 400
    )
    with app.app_context():
        assert (
            db.session.scalar(
                db.select(db.func.count(AuditLog.id)).where(
                    AuditLog.action == "jobs_bulk_export"
                )
            )
            == 1
        )


def test_settings_validation_content_escape_and_provider_state(app, admin_client):
    with app.app_context():
        values = {
            "weight_" + k: v for k, v in app.config["RECOMMENDATION_WEIGHTS"].items()
        }
    form = {
        **values,
        "real_job_cache_ttl_minutes": "20",
        "external_job_stale_days": "12",
        "external_job_max_age_days": "55",
    }
    assert (
        admin_client.post(
            "/admin/settings", data={**form, "weight_skills": "nan"}
        ).status_code
        == 400
    )
    assert (
        admin_client.post(
            "/admin/settings", data={**form, "weight_skills": "0.99"}
        ).status_code
        == 400
    )
    assert admin_client.post("/admin/settings", data=form).status_code == 302
    assert (
        admin_client.post(
            "/admin/content",
            data={**CONTENT_DEFAULTS, "hero_title": "<script>alert(1)</script>"},
        ).status_code
        == 302
    )
    page = app.test_client().get("/").get_data(as_text=True)
    assert (
        "&lt;script&gt;alert(1)&lt;/script&gt;" in page
        and "<script>alert(1)</script>" not in page
    )
    assert admin_client.post("/admin/providers/adzuna/disable").status_code == 302
    assert (
        app.test_client().get("/api/providers").json["providers"][0]["enabled"] is False
    )
    assert admin_client.post("/admin/providers/adzuna/test").status_code == 302
    assert admin_client.post("/admin/providers/adzuna/clear-cache").status_code == 302


def test_tracker_details_notifications_and_owner_boundary(app, logged_in):
    logged_in.post("/jobs/1/apply")
    payload = {
        "notes": "Follow up on portfolio",
        "application_date": date.today().isoformat(),
        "follow_up_date": date.today().isoformat(),
        "company_contact": "Recruiting team",
        "application_url": "https://example.com/careers/1",
        "status": "Assessment",
    }
    assert logged_in.post("/applications/1/details", data=payload).status_code == 302
    assert (
        logged_in.post(
            "/applications/1/details",
            data={**payload, "application_url": "javascript:alert(1)"},
        ).status_code
        == 400
    )
    logged_in.get("/dashboard")
    notifications = logged_in.get("/api/notifications").json["items"]
    assert any(n["title"] == "Application follow-up due" for n in notifications)
    other = app.test_client()
    other.post(
        "/register",
        data={
            "full_name": "Other Candidate",
            "email": "other@example.com",
            "password": "Otherpass987",
            "confirm_password": "Otherpass987",
        },
    )
    assert other.post("/applications/1/details", data=payload).status_code == 404
    assert (
        other.post(f"/notifications/{notifications[0]['id']}/read").status_code == 404
    )
    assert (
        logged_in.post(f"/notifications/{notifications[0]['id']}/read").status_code
        == 302
    )
    with app.app_context():
        assert db.session.get(Application, 1).status == "Assessment"


def test_alert_new_only_dedup_owner_email_and_failure_retry(app, logged_in):
    assert (
        logged_in.post(
            "/alerts",
            data={"name": "Python opportunities", "q": "Python", "email_enabled": "on"},
        ).status_code
        == 400
    )
    with app.app_context():
        user = db.session.get(User, 1)
        user.email_verified_at = utcnow()
        db.session.commit()
    assert (
        logged_in.post(
            "/alerts",
            data={
                "name": "Python opportunities",
                "q": "Python",
                "frequency": "daily",
                "email_enabled": "on",
            },
        ).status_code
        == 302
    )
    with app.app_context():
        # Existing catalog entries must not trigger a new-job alert.
        assert process_due_alerts() == 1
        assert db.session.scalar(db.select(db.func.count(JobAlertDelivery.id))) == 0
        alert = db.session.scalar(db.select(JobAlert))
        job = db.session.get(Job, 1)
        job.job_title = "Python Analyst"
        job.first_seen_at = utcnow()
        alert.next_run_at = utcnow() - timedelta(seconds=1)
        db.session.commit()
        app.config["MAIL_BACKEND"] = "disabled"
        assert process_due_alerts() == 1
        assert db.session.scalar(db.select(db.func.count(JobAlertDelivery.id))) == 1
        assert (
            db.session.scalar(
                db.select(db.func.count(Notification.id)).where(
                    Notification.kind == "new_job"
                )
            )
            == 1
        )
        assert alert.last_error and alert.next_run_at < utcnow() + timedelta(hours=1)
        app.config["MAIL_BACKEND"] = "memory"
        alert.next_run_at = utcnow() - timedelta(seconds=1)
        db.session.commit()
        assert process_due_alerts() == 1
        assert db.session.scalar(db.select(JobAlertDelivery)).email_sent
        mail_count = len(app.extensions["mail_outbox"])
        alert.next_run_at = utcnow() - timedelta(seconds=1)
        db.session.commit()
        process_due_alerts()
        assert len(app.extensions["mail_outbox"]) == mail_count
        aid = alert.id
    other = app.test_client()
    other.post(
        "/register",
        data={
            "full_name": "Other",
            "email": "other@example.com",
            "password": "Otherpass987",
            "confirm_password": "Otherpass987",
        },
    )
    assert other.post(f"/alerts/{aid}/delete").status_code == 404
    assert logged_in.post(f"/alerts/{aid}/toggle").status_code == 302
    assert logged_in.post(f"/alerts/{aid}/delete").status_code == 302


def test_resume_comparison_uses_reviewed_resume_not_profile_skills(app, logged_in):
    assert logged_in.get("/resume/compare/1").status_code == 302
    with app.app_context():
        user = db.session.get(User, 1)
        user.resume_text = "Python analysis improved accuracy by 15%."
        job = db.session.get(Job, 1)
        job.required_skills = ["Python", "SQL"]
        db.session.commit()
    result = logged_in.get("/resume/compare/1")
    assert result.status_code == 200
    text = result.get_data(as_text=True)
    assert (
        "Missing keywords" in text
        and "50.0%" in text
        and "ATS score or hiring guarantee" in text
    )


def test_backup_requires_reauthentication_and_rejects_paths(app, admin_client):
    assert (
        admin_client.post(
            "/admin/backups", data={"current_password": "wrong"}
        ).status_code
        == 400
    )
    assert (
        admin_client.post(
            "/admin/backups/download",
            data={
                "current_password": app.config["TEST_ADMIN_PASSWORD"],
                "filename": "../../secret",
            },
        ).status_code
        == 400
    )
    assert (
        admin_client.post(
            "/admin/backups",
            data={"current_password": app.config["TEST_ADMIN_PASSWORD"]},
        ).status_code
        == 400
    )  # memory DB, explicitly unsupported


def test_smtp_tls_and_private_development_mail(app, tmp_path, monkeypatch):
    calls = []

    class SMTP:
        def __init__(self, *args, **kwargs):
            calls.append("connect")

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def starttls(self, **kwargs):
            calls.append("tls")

        def login(self, *args):
            calls.append("login")

        def send_message(self, message):
            calls.append("send")

    monkeypatch.setattr("services.mail_service.smtplib.SMTP", SMTP)
    with app.app_context():
        app.config.update(
            MAIL_BACKEND="smtp",
            MAIL_SERVER="smtp.example.com",
            MAIL_USERNAME="fixture",
            MAIL_PASSWORD="not-a-real-secret",
            MAIL_USE_TLS=True,
        )
        assert send_mail("recipient@example.com", "Test", "Fixture body")
        assert calls == ["connect", "tls", "login", "send"]
        app.config["MAIL_BACKEND"] = "file"
        assert send_mail("recipient@example.com", "Test", "Private body")
        from pathlib import Path

        path = next((Path(app.instance_path) / "mail").glob("*.eml"))
        assert "Private body" in path.read_text()
        import os

        if os.name != "nt":
            assert path.stat().st_mode & 0o777 == 0o600


@pytest.mark.parametrize(
    "path",
    [
        "/alerts",
        "/notifications/1/read",
        "/applications/1/details",
        "/account/password",
        "/account/email",
        "/account/sessions/1/revoke",
        "/admin/jobs/1/action",
        "/admin/jobs/bulk",
        "/admin/providers/adzuna/disable",
        "/admin/users/1/status",
        "/admin/content",
        "/admin/settings",
        "/admin/backups",
        "/admin/backups/download",
    ],
)
def test_new_writes_require_csrf(app, admin_client, path):
    app.config["WTF_CSRF_ENABLED"] = True
    assert admin_client.post(path).status_code == 400
