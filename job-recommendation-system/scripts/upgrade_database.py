"""Run this once before starting production workers. SQLite is backed up automatically."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import create_app
from services.schema_service import SCHEMA_VERSION

if __name__ == "__main__":
    create_app({"AUTO_UPGRADE_SCHEMA": True, "SEED_ON_START": False})
    print(
        f"Database schema is ready at version {SCHEMA_VERSION}. Existing records were retained."
    )
