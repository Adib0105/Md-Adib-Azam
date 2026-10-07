import sqlite3
from pathlib import Path
import pytest
from app import create_app
from models.database import db, User, Job, Application
from services.schema_service import upgrade_schema


def legacy_db(tmp_path):
    path = tmp_path / "legacy.sqlite"
    with sqlite3.connect(path) as connection:
        connection.executescript(
            (Path(__file__).parent / "fixtures/v1_schema.sql").read_text()
        )
        connection.execute(
            "INSERT INTO users(id,full_name,email,password_hash,is_admin,resume_text,created_at) VALUES(1,'Preserved Candidate','preserve@example.com','hash-retained',0,'resume retained','2026-01-01')"
        )
        connection.execute(
            "INSERT INTO users(id,full_name,email,password_hash,is_admin,created_at) VALUES(2,'Demo Administrator','admin@jobmatch.com','retired-hash',1,'2026-01-01')"
        )
        connection.execute(
            "INSERT INTO jobs(id,job_title,company_name,job_description,required_skills,preferred_skills,location,experience_min,employment_type,industry,posted_date,active,is_synthetic,views) VALUES(10,'Analyst','Fixture','Retained listing','[\"SQL\"]','[]','Remote',0,'Full-time','IT','2026-01-01',1,1,7)"
        )
        connection.execute(
            "INSERT INTO applications(id,user_id,job_id,status,applied_date) VALUES(1,1,10,'Interview','2026-01-02')"
        )
    return path


def test_v1_upgrade_preserves_data_backup_and_idempotence(tmp_path):
    path = legacy_db(tmp_path)
    app = create_app(
        {
            "TESTING": True,
            "TEST_PASSWORD_HASH_METHOD": "pbkdf2:sha256:1000",
            "SECRET_KEY": "migration-test-only",
            "SQLALCHEMY_DATABASE_URI": "sqlite:///" + str(path),
            "INSTANCE_PATH": str(tmp_path / "instance"),
            "SEED_ON_START": False,
            "MODEL_CACHE": False,
        }
    )
    with app.app_context():
        assert db.session.get(User, 1).resume_text == "resume retained"
        assert db.session.get(User, 1).password_hash == "hash-retained"
        assert not db.session.get(User, 2).is_active
        assert (
            db.session.get(Job, 10).remote_allowed
            and db.session.get(Job, 10).source == "demo"
        )
        assert db.session.get(Application, 1).status == "Interview"
        assert upgrade_schema()["columns_added"] == 0
        backups = list((Path(app.instance_path) / "backups").glob("*.sqlite"))
        assert len(backups) == 1
        with sqlite3.connect(backups[0]) as backup:
            assert (
                backup.execute("SELECT resume_text FROM users WHERE id=1").fetchone()[0]
                == "resume retained"
            )
            assert backup.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        db.session.remove()
        db.engine.dispose()


def test_manual_upgrade_gate_is_non_destructive(tmp_path):
    path = legacy_db(tmp_path)
    with pytest.raises(RuntimeError, match="Database upgrade required"):
        create_app(
            {
                "TESTING": True,
                "TEST_PASSWORD_HASH_METHOD": "pbkdf2:sha256:1000",
                "SECRET_KEY": "migration-test-only",
                "SQLALCHEMY_DATABASE_URI": "sqlite:///" + str(path),
                "INSTANCE_PATH": str(tmp_path / "instance"),
                "SEED_ON_START": False,
                "AUTO_UPGRADE_SCHEMA": False,
            }
        )
    with sqlite3.connect(path) as connection:
        assert connection.execute("SELECT count(*) FROM users").fetchone()[0] == 2
        assert "is_active" not in {
            r[1] for r in connection.execute("PRAGMA table_info(users)")
        }
