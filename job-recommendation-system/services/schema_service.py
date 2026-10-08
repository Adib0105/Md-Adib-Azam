"""Versioned additive upgrades; never drop an existing table or user record."""

import sqlite3
from pathlib import Path
from uuid import uuid4
from sqlalchemy import inspect, text
from sqlalchemy.schema import CreateColumn
from flask import current_app
from models.database import db, utcnow

SCHEMA_VERSION = 3


def sqlite_backup(label="backup"):
    if db.engine.dialect.name != "sqlite" or db.engine.url.database in {
        None,
        "",
        ":memory:",
    }:
        raise ValueError(
            "File backups are available for file-based SQLite databases only."
        )
    folder = Path(current_app.instance_path) / "backups"
    folder.mkdir(mode=0o700, parents=True, exist_ok=True)
    target = folder / f"{label}-{utcnow():%Y%m%dT%H%M%S}-{uuid4().hex[:8]}.sqlite"
    with (
        sqlite3.connect(str(db.engine.url.database)) as source,
        sqlite3.connect(target) as dest,
    ):
        source.backup(dest)
        result = dest.execute("PRAGMA integrity_check").fetchone()[0]
    target.chmod(0o600)
    if result != "ok":
        target.unlink(missing_ok=True)
        raise ValueError("Backup integrity check failed.")
    return target


def upgrade_schema():
    inspector = inspect(db.engine)
    existing = set(inspector.get_table_names())
    old = "users" in existing and "schema_revisions" not in existing
    missing = []
    for table in db.metadata.sorted_tables:
        if table.name in existing:
            names = {column["name"] for column in inspector.get_columns(table.name)}
            missing.extend(
                (table, col) for col in table.columns if col.name not in names
            )
    missing_tables = set(db.metadata.tables) - existing
    needs_upgrade = old or bool(missing) or bool(existing and missing_tables)
    if needs_upgrade and not current_app.config["AUTO_UPGRADE_SCHEMA"]:
        raise RuntimeError(
            "Database upgrade required. Back up the database, then run python scripts/upgrade_database.py."
        )
    if (
        needs_upgrade
        and db.engine.dialect.name == "sqlite"
        and db.engine.url.database not in {None, "", ":memory:"}
    ):
        sqlite_backup(f"upgrade-v{SCHEMA_VERSION}")
    with db.engine.begin() as connection:
        quote = db.engine.dialect.identifier_preparer.quote
        for table, column in missing:
            if column.primary_key:
                raise RuntimeError(
                    "Unexpected missing primary key; manual database repair is required."
                )
            definition = str(CreateColumn(column).compile(dialect=db.engine.dialect))
            connection.execute(
                text(f"ALTER TABLE {quote(table.name)} ADD COLUMN {definition}")
            )
        db.metadata.create_all(connection)
        for table in db.metadata.sorted_tables:
            for index in table.indexes:
                index.create(connection, checkfirst=True)
        # Unique indexes also protect upgraded tables (create_all skips old tables).
        connection.execute(
            text(
                "CREATE UNIQUE INDEX IF NOT EXISTS uq_external_fingerprint ON jobs (fingerprint)"
            )
        )
        connection.execute(
            text(
                "CREATE UNIQUE INDEX IF NOT EXISTS uq_external_identity ON jobs (source, external_id)"
            )
        )
        if old:
            connection.execute(
                text(
                    "UPDATE jobs SET source = CASE WHEN is_synthetic THEN 'demo' ELSE 'manual' END, source_name = CASE WHEN is_synthetic THEN 'Demo' ELSE 'Local employer entry' END"
                )
            )
            connection.execute(
                text(
                    "UPDATE jobs SET remote_allowed = :yes, remote_type = 'remote' WHERE lower(location) = 'remote'"
                ),
                {"yes": True},
            )
            connection.execute(
                text(
                    "UPDATE jobs SET first_seen_at = :now WHERE first_seen_at IS NULL"
                ),
                {"now": utcnow().isoformat(" ")},
            )
            # The retired v1 seed administrator used public demo credentials.
            # Disable that identity without deleting its records or storing its old password.
            connection.execute(
                text(
                    "UPDATE users SET is_active = :no, session_version = session_version + 1 WHERE is_admin = :yes AND email = 'admin@jobmatch.com' AND full_name = 'Demo Administrator'"
                ),
                {"yes": True, "no": False},
            )
        exists = connection.execute(
            text("SELECT version FROM schema_revisions WHERE version = :version"),
            {"version": SCHEMA_VERSION},
        ).first()
        if not exists:
            connection.execute(
                text(
                    "INSERT INTO schema_revisions (version, applied_at) VALUES (:version, :now)"
                ),
                {"version": SCHEMA_VERSION, "now": utcnow().isoformat(" ")},
            )
    return {
        "version": SCHEMA_VERSION,
        "columns_added": len(missing),
        "legacy_upgrade": old,
    }
