import re
from datetime import timedelta
import pytest
from models.database import (
    db,
    User,
    UserSession,
    PasswordResetToken,
    EmailVerificationToken,
    utcnow,
)
from services.security_service import token_hash, consume_limit
from services.account_service import (
    request_password_reset,
    reset_password,
    request_email_verification,
    confirm_email,
)
from utils.validators import ValidationError


def latest_token(app):
    message = app.extensions["mail_outbox"][-1].get_content()
    return re.search(r"token=([A-Za-z0-9_-]+)", message).group(1)


def test_reset_generic_hash_single_use_and_revokes(app, logged_in):
    other = app.test_client()
    assert (
        other.post(
            "/login", data={"email": "candidate@example.com", "password": "Testpass123"}
        ).status_code
        == 302
    )
    unknown = app.test_client().post(
        "/api/password/forgot", json={"email": "unknown@example.com"}
    )
    known = app.test_client().post(
        "/api/password/forgot", json={"email": "candidate@example.com"}
    )
    assert unknown.json == known.json and known.status_code == 200
    token = latest_token(app)
    with app.app_context():
        record = db.session.scalar(db.select(PasswordResetToken))
        assert record.token_hash == token_hash(token) and record.token_hash != token
    payload = {
        "token": token,
        "password": "Newpassword987",
        "confirm_password": "Newpassword987",
    }
    reset = app.test_client()
    assert reset.post("/api/password/reset", json=payload).status_code == 200
    assert reset.post("/api/password/reset", json=payload).status_code == 400
    assert logged_in.get("/dashboard").status_code == 302
    assert other.get("/dashboard").status_code == 302
    assert (
        reset.post(
            "/login", data={"email": "candidate@example.com", "password": "Testpass123"}
        ).status_code
        == 401
    )
    assert (
        reset.post(
            "/login",
            data={"email": "candidate@example.com", "password": "Newpassword987"},
        ).status_code
        == 302
    )


def test_reset_expiry_rotation_admin_and_trusted_origin(app, client):
    app.config["APP_BASE_URL"] = "https://trusted.example.com"
    client.post(
        "/api/password/forgot",
        json={"email": "admin@example.com"},
        headers={"Host": "evil.example.net"},
    )
    token = latest_token(app)
    assert (
        "https://trusted.example.com/reset-password"
        in app.extensions["mail_outbox"][-1].get_content()
    )
    assert "evil.example.net" not in app.extensions["mail_outbox"][-1].get_content()
    with app.app_context():
        db.session.scalar(db.select(PasswordResetToken)).expires_at = (
            utcnow() - timedelta(seconds=1)
        )
        db.session.commit()
        with pytest.raises(ValidationError):
            reset_password(token, "RandomReset987", "RandomReset987")
        request_password_reset("admin@example.com")
        fresh = latest_token(app)
        user = reset_password(fresh, "RandomReset987", "RandomReset987")
        assert user.is_admin
    assert (
        client.post(
            "/login", data={"email": "admin@example.com", "password": "RandomReset987"}
        ).status_code
        == 401
    )
    assert (
        client.post(
            "/admin/login",
            data={"email": "admin@example.com", "password": "RandomReset987"},
        ).status_code
        == 302
    )


def test_remember_cookie_idle_and_session_owner(app, client):
    response = client.post(
        "/login",
        data={
            "email": "candidate@example.com",
            "password": "Testpass123",
            "remember": "on",
        },
    )
    assert (
        "Expires=" in response.headers["Set-Cookie"]
        and "HttpOnly" in response.headers["Set-Cookie"]
    )
    with app.app_context():
        record = db.session.scalar(db.select(UserSession))
        assert record.remember
        record.expires_at = utcnow() - timedelta(seconds=1)
        db.session.commit()
    assert client.get("/account").status_code == 302
    client.post(
        "/login", data={"email": "candidate@example.com", "password": "Testpass123"}
    )
    with app.app_context():
        record = db.session.scalar(
            db.select(UserSession).order_by(UserSession.id.desc())
        )
        record.last_seen_at = utcnow() - timedelta(minutes=61)
        db.session.commit()
    assert client.get("/account").status_code == 302


def test_change_password_invalidates_verification_and_sessions(app, logged_in):
    with app.app_context():
        user = db.session.get(User, 1)
        request_email_verification(user, "next@example.com", "Testpass123")
        token = latest_token(app)
    logged_in.post(
        "/account/password",
        data={
            "current_password": "wrong",
            "password": "Changed987",
            "confirm_password": "Changed987",
        },
    )
    assert logged_in.get("/account").status_code == 200
    logged_in.post(
        "/account/password",
        data={
            "current_password": "Testpass123",
            "password": "Changed987",
            "confirm_password": "Changed987",
        },
    )
    assert logged_in.get("/account").status_code == 302
    with app.app_context():
        with pytest.raises(ValidationError):
            confirm_email(token)


def test_email_confirmation_post_only_and_invalidates_old_reset(app, logged_in):
    with app.app_context():
        request_password_reset("candidate@example.com")
        old_reset = latest_token(app)
    logged_in.post(
        "/account/email",
        data={"email": "changed@example.com", "current_password": "Testpass123"},
    )
    token = latest_token(app)
    assert logged_in.get("/verify-email?token=" + token).status_code == 200
    with app.app_context():
        assert db.session.get(User, 1).email == "candidate@example.com"
        record = db.session.scalar(db.select(EmailVerificationToken))
        assert record.token_hash == token_hash(token) and record.used_at is None
    assert logged_in.post("/verify-email", data={"token": token}).status_code == 302
    assert logged_in.post("/verify-email", data={"token": token}).status_code == 400
    with app.app_context():
        assert db.session.get(User, 1).email == "changed@example.com"
        with pytest.raises(ValidationError):
            reset_password(old_reset, "Password987", "Password987")


def test_shared_rate_limit_and_recovery_csrf(app, client):
    with app.app_context():
        assert consume_limit("test", "same-person", 1, 300)
    with app.app_context():
        assert not consume_limit("test", "same-person", 1, 300)
    app.config["WTF_CSRF_ENABLED"] = True
    assert (
        client.post("/api/password/forgot", json={"email": "a@example.com"}).status_code
        == 400
    )
    csrf = client.get("/api/csrf").json["csrf_token"]
    assert (
        client.post(
            "/api/password/forgot",
            json={"email": "a@example.com"},
            headers={"X-CSRFToken": csrf},
        ).status_code
        == 200
    )
    assert client.post("/api/password/reset", json={}).status_code == 400


def test_default_password_hash_is_scrypt(app):
    with app.app_context():
        app.config["TEST_PASSWORD_HASH_METHOD"] = None
        user = User()
        user.set_password("Apassword987")
        assert user.password_hash.startswith("scrypt:") and user.check_password(
            "Apassword987"
        )


@pytest.mark.parametrize(
    "path",
    [
        "/account",
        "/alerts",
        "/notifications",
        "/api/notifications",
        "/resume/compare/1",
    ],
)
def test_new_candidate_pages_require_auth(client, path):
    assert client.get(path).status_code == (401 if path.startswith("/api/") else 302)


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
def test_admin_boundaries(logged_in, path):
    assert logged_in.get(path).status_code == 403


@pytest.mark.parametrize(
    "path",
    [
        "/admin/providers/adzuna/disable",
        "/admin/jobs/1/action",
        "/admin/jobs/bulk",
        "/admin/users/1/status",
        "/admin/content",
        "/admin/settings",
        "/admin/backups",
        "/admin/backups/download",
    ],
)
def test_admin_write_boundaries(logged_in, path):
    assert logged_in.post(path).status_code == 403


@pytest.mark.parametrize(
    "config",
    [
        {"APP_BASE_URL": "http://insecure.example.com"},
        {"SECRET_KEY": "short"},
        {"MAIL_BACKEND": "file"},
        {"MAIL_BACKEND": "smtp", "MAIL_USE_TLS": False},
    ],
)
def test_production_rejects_unsafe_config(tmp_path, config):
    from app import create_app

    with pytest.raises(RuntimeError):
        create_app(
            {
                "APP_ENV": "production",
                "SECRET_KEY": "x" * 48,
                "APP_BASE_URL": "https://example.com",
                "MAIL_BACKEND": "disabled",
                "SEED_ON_START": False,
                "INSTANCE_PATH": str(tmp_path),
                **config,
            }
        )
