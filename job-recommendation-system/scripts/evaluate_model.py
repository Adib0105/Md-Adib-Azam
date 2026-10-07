"""Synthetic smoke evaluation, NOT evidence of real-world recommendation quality."""

import argparse
import json
import math
import sys
import tempfile
from datetime import date
from pathlib import Path
from statistics import mean

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import create_app
from models.database import Job
from services.data_service import generate_dataset, clean_job_rows
from services.recommendation_service import engine

SCENARIOS = [
    {
        "name": "Early-career analyst",
        "preferred_role": "Data Analyst",
        "skills": ["SQL", "Python", "Excel", "Power BI", "Statistics", "Data Cleaning"],
        "education": "BTech",
        "experience_years": 1,
        "preferred_location": "Kolkata / Remote",
        "expected_salary": 450000,
        "projects": "Retail reporting dashboards, sales analysis and data cleaning.",
        "related": [
            "Business Intelligence Analyst",
            "MIS Executive",
            "Business Analyst",
        ],
    },
    {
        "name": "Junior web developer",
        "preferred_role": "Web Developer",
        "skills": ["HTML", "CSS", "JavaScript", "React", "Git", "Bootstrap"],
        "education": "Diploma",
        "experience_years": 0,
        "preferred_location": "Remote",
        "expected_salary": 350000,
        "projects": "Responsive accessible web interfaces and reusable React components.",
        "related": ["Software Developer", "UX Researcher"],
    },
    {
        "name": "Experienced support candidate",
        "preferred_role": "Customer Support Executive",
        "skills": [
            "Customer Support",
            "Communication",
            "CRM",
            "Ticketing",
            "Email Support",
            "Zendesk",
        ],
        "education": "12th",
        "experience_years": 2,
        "preferred_location": "Kolkata / Remote",
        "expected_salary": 300000,
        "projects": "Customer ticket resolution, response time reporting and quality assurance.",
        "related": ["Operations Analyst", "Quality Assurance Analyst"],
    },
    {
        "name": "Cloud operations candidate",
        "preferred_role": "Cloud Engineer",
        "skills": ["AWS", "Linux", "Docker", "Networking", "Terraform", "Kubernetes"],
        "education": "BTech",
        "experience_years": 3,
        "preferred_location": "Bangalore / Remote",
        "expected_salary": 900000,
        "projects": "Reliable infrastructure automation, cloud deployments and system monitoring.",
        "related": ["Cybersecurity Analyst", "Data Engineer"],
    },
]


def relevance(scenario, job):
    """Human-authored role-family proxy, independent of numerical model scores."""
    if job.job_title == scenario["preferred_role"]:
        return 3 if job.experience_min <= scenario["experience_years"] else 2
    if job.job_title in scenario["related"]:
        return 1
    return 0


def metrics(ranked, relevant, k):
    labels = [relevant[row["job"].id] for row in ranked[:k]]
    returned = len(labels)
    hits = sum(label > 0 for label in labels)
    total_relevant = sum(value > 0 for value in relevant.values())

    def dcg(values):
        return sum(
            (2**value - 1) / math.log2(index + 2) for index, value in enumerate(values)
        )

    ideal = dcg(sorted(relevant.values(), reverse=True)[:k])
    return {
        f"precision@{k}": round(hits / returned, 4) if returned else 0,
        f"recall@{k}": round(hits / total_relevant, 4) if total_relevant else 0,
        f"ndcg@{k}": round(dcg(labels) / ideal, 4) if ideal else 0,
    }


def evaluate(k=10):
    with tempfile.TemporaryDirectory() as directory:
        raw = generate_dataset(
            Path(directory) / "jobs.csv", reference_date=date(2026, 10, 7)
        )
        clean, _ = clean_job_rows(raw)
        jobs = [Job(id=i + 1, **row) for i, row in enumerate(clean)]
        app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "evaluation-temporary-key",
                "SEED_ON_START": False,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
                "INSTANCE_PATH": str(Path(directory) / "instance"),
                "MODEL_CACHE": False,
            }
        )
        result = []
        with app.app_context():
            for scenario in SCENARIOS:
                ranked = engine().rank(scenario, jobs)
                labels = {job.id: relevance(scenario, job) for job in jobs}
                result.append(
                    {
                        "scenario": scenario["name"],
                        **metrics(ranked, labels, k),
                        "top_roles": [row["job"].job_title for row in ranked[:5]],
                    }
                )
        return {
            "evaluation": "synthetic role-family smoke test",
            "dataset_jobs": len(jobs),
            "k": k,
            "limitations": "Hand-authored relevance proxies and generated job templates. No real candidate judgments, hiring outcomes, held-out test population or fairness validation. These metrics do not prove real-world recommendation quality.",
            "scenarios": result,
            "macro_average": {
                key: round(mean(row[key] for row in result), 4)
                for key in [f"precision@{k}", f"recall@{k}", f"ndcg@{k}"]
            },
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--k", type=int, default=10)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not 1 <= args.k <= 640:
        parser.error("k must be from 1 to 640.")
    output = json.dumps(evaluate(args.k), indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output + "\n", encoding="utf-8")
    print(output)
