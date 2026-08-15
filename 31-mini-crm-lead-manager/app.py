from __future__ import annotations

import argparse
import csv
import sqlite3
from datetime import date
from pathlib import Path


SCHEMA = """
CREATE TABLE IF NOT EXISTS leads (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  company TEXT NOT NULL,
  stage TEXT NOT NULL,
  value REAL NOT NULL CHECK(value >= 0),
  follow_up TEXT NOT NULL,
  UNIQUE(name, company)
);
"""
STAGE_POINTS = {"New": 10, "Contacted": 25, "Qualified": 50, "Proposal": 75, "Won": 100}


def connect(path: str | Path) -> sqlite3.Connection:
    database = sqlite3.connect(path)
    database.row_factory = sqlite3.Row
    database.executescript(SCHEMA)
    return database


def lead_score(stage: str, value: float, follow_up: str, today: date | None = None) -> int:
    today = today or date.today()
    score = STAGE_POINTS.get(stage, 0)
    score += min(25, int(value / 2000))
    if date.fromisoformat(follow_up) <= today:
        score += 15
    return min(score, 100)


def import_csv(database: sqlite3.Connection, path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as source:
        rows = list(csv.DictReader(source))
    database.executemany(
        """
        INSERT INTO leads(name, company, stage, value, follow_up)
        VALUES(:name,:company,:stage,:value,:follow_up)
        ON CONFLICT(name,company) DO UPDATE SET
          stage=excluded.stage,value=excluded.value,follow_up=excluded.follow_up
        """,
        rows,
    )
    database.commit()
    return len(rows)


def dashboard(database: sqlite3.Connection) -> list[dict[str, object]]:
    leads = database.execute("SELECT * FROM leads").fetchall()
    output = [
        {
            **dict(row),
            "score": lead_score(row["stage"], row["value"], row["follow_up"]),
        }
        for row in leads
    ]
    return sorted(output, key=lambda lead: (-lead["score"], -lead["value"]))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", default="crm.db")
    parser.add_argument("--import-csv", type=Path)
    parser.add_argument("--dashboard", action="store_true")
    args = parser.parse_args()
    with connect(args.database) as database:
        if args.import_csv:
            print(f"Imported {import_csv(database, args.import_csv)} leads")
        if args.dashboard:
            print("Lead priorities")
            for lead in dashboard(database):
                print(f"{lead['score']:>3}  {lead['name']:<12} {lead['stage']:<10} value={lead['value']:>8.0f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
