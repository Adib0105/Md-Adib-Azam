import pytest
from models.database import db, User


def test_create_admin_command_hashes_password_and_prevents_promotion(app, monkeypatch):
    from scripts import create_admin
    import secrets

    password = secrets.token_urlsafe(24) + "9a"
    monkeypatch.setattr(create_admin, "create_app", lambda: app)
    monkeypatch.setattr("sys.argv", ["create_admin.py"])
    answers = iter(["Created Admin", "newadmin@example.com"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(create_admin.getpass, "getpass", lambda _: password)
    create_admin.main()
    with app.app_context():
        user = db.session.scalar(
            db.select(User).where(User.email == "newadmin@example.com")
        )
        assert (
            user.is_admin
            and user.check_password(password)
            and user.password_hash != password
        )
    answers = iter(["Candidate", "candidate@example.com"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr("sys.argv", ["create_admin.py", "--reset-existing"])
    with pytest.raises(SystemExit, match="candidates are never silently promoted"):
        create_admin.main()


@pytest.mark.parametrize(
    "path", ["/api/admin/analytics", "/api/admin/providers/health"]
)
def test_admin_api_guards(app, admin_client, path):
    assert app.test_client().get(path).status_code == 401
    result = admin_client.get(path)
    assert result.status_code == 200
    assert "password" not in result.get_data(as_text=True)


def test_file_backup_authenticated_roundtrip(tmp_path):
    from app import create_app
    import secrets

    password = secrets.token_urlsafe(24) + "9a"
    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "backup-test",
            "TEST_PASSWORD_HASH_METHOD": "pbkdf2:sha256:1000",
            "SQLALCHEMY_DATABASE_URI": "sqlite:///" + str(tmp_path / "source.sqlite"),
            "INSTANCE_PATH": str(tmp_path / "instance"),
            "SEED_ON_START": False,
            "MODEL_CACHE": False,
            "WTF_CSRF_ENABLED": False,
        }
    )
    with app.app_context():
        admin = User(
            full_name="Backup Admin", email="backup@example.com", is_admin=True
        )
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
    client = app.test_client()
    client.post(
        "/admin/login", data={"email": "backup@example.com", "password": password}
    )
    assert (
        client.post("/admin/backups", data={"current_password": password}).status_code
        == 302
    )
    files = list((tmp_path / "instance" / "backups").glob("*.sqlite"))
    assert len(files) == 1
    response = client.post(
        "/admin/backups/download",
        data={"current_password": password, "filename": files[0].name},
    )
    assert response.status_code == 200 and response.data.startswith(b"SQLite format 3")
    response.close()
    with app.app_context():
        db.session.remove()
        db.engine.dispose()
