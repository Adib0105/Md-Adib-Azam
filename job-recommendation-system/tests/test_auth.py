import re
from models.database import db, User


def test_registration_hashes_password_and_rejects_duplicate(app, client):
    data = {
        "full_name": "New User",
        "email": "NEW@example.com",
        "password": "Secure123",
        "confirm_password": "Secure123",
        "is_admin": "true",
    }
    assert client.post("/register", data=data).status_code == 302
    with app.app_context():
        user = db.session.scalar(db.select(User).where(User.email == "new@example.com"))
        assert user and not user.is_admin
        assert user.password_hash != data["password"] and user.check_password(
            data["password"]
        )
    assert client.post("/register", data=data).status_code == 400


def test_invalid_registration_and_login(client):
    assert (
        client.post(
            "/register", data={"full_name": "X", "email": "invalid", "password": "a"}
        ).status_code
        == 400
    )
    assert (
        client.post(
            "/login", data={"email": "candidate@example.com", "password": "wrong"}
        ).status_code
        == 401
    )
    assert client.get("/dashboard").status_code == 302
    assert client.get("/api/recommendations").status_code == 401


def test_admin_separation_and_logout(logged_in):
    assert logged_in.get("/admin/").status_code == 403
    assert logged_in.post("/logout").status_code == 302
    assert logged_in.get("/api/profile").status_code == 401
    assert (
        logged_in.post(
            "/login",
            data={
                "email": "admin@example.com",
                "password": logged_in.application.config["TEST_ADMIN_PASSWORD"],
            },
        ).status_code
        == 401
    )
    assert (
        logged_in.post(
            "/admin/login",
            data={"email": "candidate@example.com", "password": "Testpass123"},
        ).status_code
        == 401
    )


def test_csrf_required_and_rotation(app):
    app.config["WTF_CSRF_ENABLED"] = True
    client = app.test_client()
    assert (
        client.post(
            "/login", data={"email": "candidate@example.com", "password": "Testpass123"}
        ).status_code
        == 400
    )
    page = client.get("/login").get_data(as_text=True)
    token = re.search(r'name="csrf_token" value="([^"]+)"', page).group(1)
    assert (
        client.post(
            "/login",
            data={
                "csrf_token": token,
                "email": "candidate@example.com",
                "password": "Testpass123",
            },
        ).status_code
        == 302
    )
    assert client.post("/jobs/1/save", data={"csrf_token": token}).status_code == 400
    page = client.get("/profile").get_data(as_text=True)
    new_token = re.search(r'name="csrf_token" value="([^"]+)"', page).group(1)
    assert (
        client.post("/jobs/1/save", data={"csrf_token": new_token}).status_code == 302
    )


def test_api_excludes_sensitive_fields(logged_in):
    response = logged_in.get("/api/profile")
    assert response.status_code == 200
    assert (
        not {"password_hash", "password", "resume_text", "email", "is_admin"}
        & response.json.keys()
    )


def test_login_throttling(client):
    for _ in range(8):
        assert (
            client.post(
                "/login", data={"email": "candidate@example.com", "password": "wrong"}
            ).status_code
            == 401
        )
    assert (
        client.post(
            "/login", data={"email": "candidate@example.com", "password": "wrong"}
        ).status_code
        == 429
    )


def test_headers_and_friendly_errors(client):
    result = client.get("/does-not-exist")
    assert result.status_code == 404
    assert result.headers["X-Content-Type-Options"] == "nosniff"
    assert result.headers["X-Frame-Options"] == "DENY"
    assert "Traceback" not in result.get_data(as_text=True)
