"""Idempotent local setup. Demo credentials are opt-in and never used in production."""

import argparse
import os
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
        help="Explicitly create known local demonstration accounts",
    )
    args = parser.parse_args()
    if args.demo and os.getenv("APP_ENV") == "production":
        parser.error("Demo accounts are forbidden when APP_ENV=production.")
    app = create_app({"SEED_ON_START": False})
    with app.app_context():
        print(seed_jobs(ROOT / "data"))
        if args.demo:
            accounts = [
                ("demo@jobmatch.com", "Demo@123", False),
                ("admin@jobmatch.com", "Admin@123", True),
            ]
            for email, password, is_admin in accounts:
                if db.session.scalar(db.select(User).where(User.email == email)):
                    continue
                user = User(
                    full_name="Demo Administrator" if is_admin else "Rahul Kumar",
                    email=email,
                    is_admin=is_admin,
                )
                user.set_password(password)
                if not is_admin:
                    user.city, user.state, user.education = (
                        "Kolkata",
                        "West Bengal",
                        "B.Tech Computer Science",
                    )
                    user.experience_years, user.expected_salary = 1, 500000
                    (
                        user.preferred_role,
                        user.preferred_location,
                        user.employment_type,
                    ) = "Data Analyst", "Kolkata / Remote", "Full-time"
                    user.projects = "Retail sales dashboard using SQL, Python, Excel and Power BI. Cleaned transaction data and explained sales trends."
                    user.certifications = (
                        "Foundations of Data Analytics (demonstration)"
                    )
                    user.experience_summary = (
                        "One year analyzing sales and customer support reporting."
                    )
                    user.career_interests = "Business intelligence, customer analytics and data visualization."
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
                if not is_admin:
                    snapshot(user, "Demo starting profile")
            print(
                "Local demo accounts are ready. See README for sign-in details. Never deploy these accounts publicly."
            )


if __name__ == "__main__":
    main()
