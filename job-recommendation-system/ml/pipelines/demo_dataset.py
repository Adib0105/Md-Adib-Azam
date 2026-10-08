"""Hand-authored fictional scenarios and ordinal judgments, independent of scores.

The explicit label table is a synthetic teaching fixture, not external human review.
"""

import json
from pathlib import Path

JOBS = [
    (
        "Junior Data Analyst",
        "Clean shop sales exports and explain weekly trends with spreadsheets and SQL.",
        "Excel|SQL|Data Cleaning",
        0,
    ),
    (
        "Data Analyst",
        "Build dashboards of orders, margins and regional performance for retail managers.",
        "SQL|Power BI|Statistics|Communication",
        1,
    ),
    (
        "Senior Data Analyst",
        "Design randomized experiments and advise product leaders on metric definitions.",
        "Advanced SQL|Statistics|A/B Testing|Stakeholder Management",
        5,
    ),
    (
        "Data Scientist",
        "Validate churn models with held-out samples and report uncertainty to stakeholders.",
        "Python|Pandas|Machine Learning|Model Evaluation|Statistics",
        3,
    ),
    (
        "Analytics Engineer",
        "Maintain tested transformations and dimensional models in the analytical warehouse.",
        "SQL|ETL|Data Modeling|Git",
        2,
    ),
    (
        "Frontend Developer",
        "Create accessible browser interfaces from designs using reusable UI components.",
        "JavaScript|React|HTML|CSS|Accessibility",
        1,
    ),
    (
        "Python Backend Developer",
        "Implement authenticated REST services, database migrations and server tests.",
        "Python|Flask|SQL|REST API|Git",
        2,
    ),
    (
        "Cloud Engineer",
        "Monitor Linux services, automate cloud infrastructure and diagnose deployment outages.",
        "AWS|Linux|Docker|Networking|Terraform",
        2,
    ),
    (
        "Security Operations Analyst",
        "Triage alerts, investigate logs and document incident response procedures.",
        "SIEM|Linux|Networking|Incident Response",
        1,
    ),
    (
        "Customer Support Executive",
        "Resolve delivery complaints by phone and email with clear CRM ticket notes.",
        "CRM|Customer Support|Communication|Ticketing",
        0,
    ),
    (
        "Technical Support Specialist",
        "Troubleshoot network and desktop software problems, documenting support tickets.",
        "Technical Support|Networking|Customer Support|Ticketing",
        1,
    ),
    (
        "Graphic Designer",
        "Prepare print layouts and brand-consistent social campaign artwork.",
        "Photoshop|Illustrator|Typography|Canva",
        0,
    ),
    (
        "UX Researcher",
        "Run usability interviews, test prototypes and synthesize qualitative findings.",
        "UX Research|Figma|Prototyping|Communication",
        2,
    ),
    (
        "Marketing Analyst",
        "Measure campaign conversion, analyze audiences and evaluate channel experiments.",
        "Excel|Google Analytics|Campaign Analysis|A/B Testing",
        1,
    ),
    (
        "HR Analyst",
        "Clean workforce records and summarize hiring and retention metrics for HR.",
        "Excel|HR Analytics|Reporting|Communication",
        1,
    ),
    (
        "Financial Analyst",
        "Build valuation and budgeting models and summarize annual financial statements.",
        "Accounting|Financial Modeling|Excel|Budgeting",
        2,
    ),
    (
        "Data Engineering Intern",
        "Help ingest CSV files, validate columns and document simple data pipelines.",
        "Python|SQL|Data Cleaning",
        0,
    ),
    (
        "BI Developer",
        "Create semantic reporting models, DAX measures and refreshable management dashboards.",
        "Power BI|DAX|SQL|Data Modeling",
        2,
    ),
    (
        "Machine Learning Engineer",
        "Deploy and monitor prediction services with repeatable model evaluation.",
        "Python|Machine Learning|MLOps|Docker|Model Evaluation",
        4,
    ),
    (
        "Quality Assurance Analyst",
        "Write test plans and reproduce API and database defects with developers.",
        "Quality Assurance|SQL|REST API|Problem Solving",
        1,
    ),
]
# candidate profile, and one explicit judgment per JOBS entry. No model calls here.
SCENARIOS = [
    (
        "analyst-student",
        "Junior Data Analyst",
        "Excel|SQL|Data Cleaning",
        0,
        "Cleaned college sales data and summarized trends.",
        [3, 2, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 3, 1, 0, 1],
    ),
    (
        "analyst-junior",
        "Data Analyst",
        "SQL|Excel|Power BI|Statistics|Communication",
        1,
        "Retail dashboards and weekly reports for shop operations.",
        [3, 3, 1, 1, 2, 0, 1, 0, 0, 1, 0, 0, 0, 2, 2, 1, 2, 2, 0, 1],
    ),
    (
        "analyst-senior",
        "Senior Data Analyst",
        "Advanced SQL|Python|Statistics|A/B Testing|Stakeholder Management|Power BI",
        6,
        "Product experiments, measurement design and decision presentations.",
        [1, 2, 3, 2, 2, 0, 1, 0, 0, 0, 0, 0, 1, 3, 1, 1, 0, 2, 1, 1],
    ),
    (
        "scientist",
        "Data Scientist",
        "Python|Pandas|SQL|Machine Learning|Statistics|Model Evaluation",
        3,
        "Evaluated customer churn models on unseen samples.",
        [1, 2, 2, 3, 2, 0, 2, 1, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 2, 1],
    ),
    (
        "frontend",
        "Frontend Developer",
        "JavaScript|React|HTML|CSS|Accessibility|Git",
        1,
        "Accessible browser UI components and responsive web pages.",
        [0, 0, 0, 0, 0, 3, 1, 0, 0, 0, 1, 1, 2, 0, 0, 0, 0, 0, 0, 2],
    ),
    (
        "backend",
        "Python Backend Developer",
        "Python|Flask|SQL|REST API|Git|Docker",
        2,
        "Authentication, API tests and server-side database migrations.",
        [1, 1, 0, 1, 2, 1, 3, 2, 1, 0, 2, 0, 0, 0, 0, 0, 2, 1, 1, 3],
    ),
    (
        "cloud",
        "Cloud Engineer",
        "AWS|Linux|Docker|Networking|Terraform|Monitoring",
        3,
        "Infrastructure as code and reliable cloud deployments.",
        [0, 0, 0, 0, 1, 0, 2, 3, 2, 0, 2, 0, 0, 0, 0, 0, 1, 0, 1, 1],
    ),
    (
        "security",
        "Security Operations Analyst",
        "SIEM|Linux|Networking|Incident Response|Splunk",
        2,
        "Security log triage and incident investigation.",
        [0, 0, 0, 0, 0, 0, 1, 2, 3, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    ),
    (
        "support",
        "Customer Support Executive",
        "CRM|Customer Support|Communication|Ticketing|Email Support",
        2,
        "Resolved delivery issues and tracked response time in CRM.",
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 1, 1, 1, 0, 0, 0, 0, 1],
    ),
    (
        "designer",
        "Graphic Designer",
        "Photoshop|Illustrator|Typography|Canva|Figma",
        1,
        "Brand artwork, poster layouts and social campaign graphics.",
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 3, 2, 1, 0, 0, 0, 0, 0, 0],
    ),
    (
        "marketing",
        "Marketing Analyst",
        "Excel|Google Analytics|Campaign Analysis|A/B Testing|Communication",
        2,
        "Channel conversion reporting and campaign experiments.",
        [2, 2, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 3, 1, 1, 0, 1, 0, 0],
    ),
    (
        "finance",
        "Financial Analyst",
        "Accounting|Financial Modeling|Excel|Budgeting|Financial Analysis",
        3,
        "Budget forecasts and company valuation models.",
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 3, 0, 0, 0, 0],
    ),
]


def create_demo_dataset(path):
    rows = []
    for name, role, skills, years, project, labels in SCENARIOS:
        for index, (title, description, required, minimum) in enumerate(JOBS):
            rows.append(
                {
                    "schema_version": "relevance-v1",
                    "dataset_kind": "synthetic",
                    "candidate_id": name,
                    "job_id": f"fixture-job-{index + 1:02d}",
                    "snapshot_at": "2026-10-08T00:00:00+00:00",
                    "judged_at": "2026-10-08T00:00:00+00:00",
                    "judgment_method": "Explicit author-created fictional role/duty judgment table; not employer or independent reviewer labels.",
                    "candidate_features": {
                        "preferred_role": role,
                        "skills": skills.split("|"),
                        "experience_years": years,
                        "projects": project,
                        "education": "BTech",
                        "preferred_location": "Remote",
                        "expected_salary": 500000,
                        "salary_currency": "INR",
                        "employment_type": "Full-time",
                        "remote_preference": "any",
                    },
                    "job_features": {
                        "job_title": title,
                        "company_name": f"Fictional Fixture {index + 1}",
                        "job_description": description,
                        "required_skills": required,
                        "experience_min": minimum,
                        "education": "BTech",
                        "location": "Remote" if index % 2 == 0 else "Kolkata",
                        "salary_min": 400000,
                        "salary_max": 800000,
                        "employment_type": (
                            "Internship" if title.endswith("Intern") else "Full-time"
                        ),
                        "posted_date": "2026-10-01",
                        "is_synthetic": "true",
                    },
                    "relevance_label": labels[index],
                }
            )
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n",
        encoding="utf-8",
    )
    return len(rows)
