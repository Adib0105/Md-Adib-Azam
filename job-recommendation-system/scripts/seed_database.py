"""Idempotent job setup. --demo creates a candidate only; never an administrator."""

import argparse
import os
import secrets
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import create_app
from config import ROOT
from models.database import db, User, CandidateSkill
from services.data_service import seed_jobs
from services.recommendation_service import snapshot


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Create an opt-in local demo candidate (no administrator)",
    )
    args = parser.parse_args()
    if args.demo and os.getenv("APP_ENV") == "production":
        parser.error("Demo accounts are forbidden when APP_ENV=production.")
    app = create_app({"SEED_ON_START": False})
    with app.app_context():
        print(seed_jobs(ROOT / "data"))
        if args.demo and not db.session.scalar(
            db.select(User).where(User.email == "demo@jobmatch.com")
        ):
            user = User(
                full_name="Rahul Kumar",
                email="demo@jobmatch.com",
                city="Kolkata",
                state="West Bengal",
                education="B.Tech Computer Science",
                experience_years=1,
                expected_salary=500000,
                preferred_role="Data Analyst",
                preferred_location="Kolkata / Remote",
                employment_type="Full-time",
                projects="Retail sales dashboard using SQL, Python, Excel and Power BI. Cleaned transactions and explained sales trends.",
                certifications="Foundations of Data Analytics (demonstration)",
                experience_summary="One year analyzing sales and customer support reporting.",
                career_interests="Business intelligence, customer analytics and data visualization.",
            )
            demo_password = secrets.token_urlsafe(18) + "9a"
            user.set_password(demo_password)
            for name in [
                "Python",
                "SQL",
                "Excel",
                "Power BI",
                "Pandas",
                "Statistics",
                "Communication",
                "Data Cleaning",
            ]:
                user.skills.append(
                    CandidateSkill(
                        skill_name=name,
                        proficiency_level="Advanced"
                        if name in {"SQL", "Excel"}
                        else "Intermediate",
                    )
                )
            db.session.add(user)
            db.session.commit()
            snapshot(user, "Demo starting profile")
            print("Local demo candidate: demo@jobmatch.com")
            print("Generated one-time setup password: " + demo_password)
        print(
            "Jobs are ready. Create an administrator separately with python scripts/create_admin.py."
        )


if __name__ == "__main__":
    main()
