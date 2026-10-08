"""Export a private, blind review template; labels must be supplied by reviewers."""

import argparse
import hashlib
import json
import secrets
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import create_app
from models.database import db, User, utcnow
from ml.preprocessing.text import professional_profile, clean_text
from services.recommendation_service import active_jobs, profile_data


def export_review_template(app, max_candidates=20, max_jobs=20):
    if not 1 <= max_candidates <= 100 or not 1 <= max_jobs <= 100:
        raise ValueError("Use 1–100 candidates and jobs per review partition.")
    rows = []
    with app.app_context():
        salt = secrets.token_hex(32)
        snapshot = utcnow().isoformat() + "+00:00"
        jobs = active_jobs()[:max_jobs]
        kind = "synthetic" if any(job.is_synthetic for job in jobs) else "manual"
        candidates = db.session.scalars(
            db.select(User)
            .where(User.is_admin.is_(False), User.is_active.is_(True))
            .order_by(User.id)
            .limit(max_candidates)
        ).all()
        for user in candidates:
            profile = professional_profile(profile_data(user))
            profile = {
                key: clean_text(value, 12000) if isinstance(value, str) else value
                for key, value in profile.items()
            }
            candidate_id = hashlib.sha256(f"{salt}|{user.id}".encode()).hexdigest()[:20]
            for job in jobs:
                rows.append(
                    {
                        "schema_version": "relevance-v1",
                        "dataset_kind": kind,
                        "candidate_id": candidate_id,
                        "job_id": f"job-snapshot-{job.id}",
                        "snapshot_at": snapshot,
                        "candidate_features": profile,
                        "job_features": {
                            "job_title": job.job_title,
                            "company_name": job.company_name,
                            "job_description": job.job_description,
                            "required_skills": job.required_skills,
                            "preferred_skills": job.preferred_skills,
                            "salary_min": job.min_salary,
                            "salary_max": job.max_salary,
                            "salary_currency": job.salary_currency,
                            "salary_period": job.salary_period,
                            "experience_min": job.experience_min,
                            "experience_max": job.experience_max,
                            "experience_known": job.experience_known,
                            "education": job.education_required,
                            "location": job.location,
                            "employment_type": job.employment_type,
                            "remote_type": job.remote_type,
                            "remote_allowed": job.remote_allowed,
                            "is_external": job.is_external,
                            "posted_date": job.posted_date.isoformat(),
                            "is_synthetic": job.is_synthetic,
                        },
                        "relevance_label": None,
                        "judgment_method": "Independent reviewer must set 0–3 without seeing model scores and record judged_at.",
                    }
                )
        folder = Path(app.instance_path) / "ml"
        folder.mkdir(parents=True, exist_ok=True, mode=0o700)
        path = folder / "relevance-review-template.jsonl"
        with path.open("x", encoding="utf-8") as handle:
            path.chmod(0o600)
            handle.write(
                "\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n"
            )
    return path, len(rows), kind


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-candidates", type=int, default=20)
    parser.add_argument("--max-jobs", type=int, default=20)
    args = parser.parse_args()
    try:
        path, count, kind = export_review_template(
            create_app(), args.max_candidates, args.max_jobs
        )
    except (ValueError, FileExistsError) as exc:
        parser.error(str(exc))
    print(
        f"Exported {count} unlabeled {kind} judgments to {path}. Review personal information and provenance before sharing; do not commit this file. Null labels are refused."
    )


if __name__ == "__main__":
    main()
