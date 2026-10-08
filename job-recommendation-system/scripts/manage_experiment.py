"""Operator-only experiment creation; no automatic enrollment without metadata."""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import create_app
from models.database import db
from models.ml_data import Experiment


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("slug")
    parser.add_argument("--enable", action="store_true")
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z0-9-]{1,80}", args.slug):
        parser.error("Use a lowercase experiment slug.")
    app = create_app()
    with app.app_context():
        record = db.session.get(Experiment, args.slug)
        if record is None:
            record = Experiment(
                slug=args.slug,
                description="Recorded comparison of the seven-factor baseline and hybrid-v1; observational action rates, not causal claims.",
            )
            db.session.add(record)
        record.enabled = args.enable
        db.session.commit()
    print(
        f"Experiment {args.slug}: {'enabled' if args.enable else 'disabled'}. Set ML_EXPERIMENT to this slug and restart to enroll candidates."
    )


if __name__ == "__main__":
    main()
