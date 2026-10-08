"""CSV cleaning, deterministic synthetic data, and idempotent database seeding."""

import csv
import json
import random
import re
from datetime import date, timedelta
from pathlib import Path
from models.database import db, Job
from models.skill_extractor import normalize_skills, extract_skills
from utils.constants import CITY_STATES, EMPLOYMENT_TYPES

ROLE_SPECS = [
    (
        "Data Analyst",
        "SQL|Excel|Python|Power BI|Statistics|Data Cleaning",
        "Tableau|DAX|Pandas|Presentation|ETL",
        350000,
        "Diploma",
        "analyze sales funnels|validate transaction data|build weekly KPI dashboards|explain customer retention",
    ),
    (
        "Business Analyst",
        "SQL|Excel|Business Analysis|Requirements Gathering|Communication",
        "Agile|Jira|Tableau|Process Improvement",
        400000,
        "BA",
        "map operational workflows|interview stakeholders|document business requirements|evaluate product changes",
    ),
    (
        "Power BI Developer",
        "Power BI|DAX|SQL|Power Query|Data Modeling",
        "Azure|ETL|Excel|Dashboard Design",
        450000,
        "BTech",
        "design dimensional models|optimize DAX measures|publish operational dashboards|reconcile reporting metrics",
    ),
    (
        "MIS Executive",
        "Excel|Reporting|Data Cleaning|Communication",
        "SQL|Power BI|Excel VBA|Advanced Excel",
        240000,
        "12th",
        "maintain daily reports|reconcile inventory records|automate spreadsheet checks|prepare management summaries",
    ),
    (
        "SQL Developer",
        "SQL|PostgreSQL|Database Design|ETL",
        "Python|SQL Server|Advanced SQL|Git",
        400000,
        "BCA",
        "optimize database queries|design warehouse tables|build scheduled data pipelines|audit data consistency",
    ),
    (
        "Python Developer",
        "Python|Flask|SQL|Git|REST API",
        "Django|FastAPI|Docker|Linux",
        420000,
        "Diploma",
        "build backend APIs|write integration tests|improve service reliability|maintain internal automation",
    ),
    (
        "Junior Data Scientist",
        "Python|Statistics|Machine Learning|Pandas|SQL",
        "Scikit-learn|NLP|A/B Testing|Feature Engineering",
        550000,
        "BSc",
        "evaluate classification models|prepare experimentation datasets|explain model errors|prototype demand forecasts",
    ),
    (
        "Machine Learning Engineer",
        "Python|Machine Learning|Scikit-learn|Docker|Model Evaluation",
        "PyTorch|TensorFlow|MLOps|AWS",
        750000,
        "BTech",
        "serve prediction models|monitor model drift|build reproducible ML pipelines|optimize inference workloads",
    ),
    (
        "Software Developer",
        "Java|SQL|Git|OOP|Algorithms",
        "Python|Docker|REST API|Agile",
        450000,
        "BTech",
        "implement service features|review maintainable code|resolve production defects|improve automated testing",
    ),
    (
        "Web Developer",
        "HTML|CSS|JavaScript|React|Git",
        "Node.js|TypeScript|Accessibility|Bootstrap",
        350000,
        "Diploma",
        "build accessible interfaces|integrate REST APIs|optimize page performance|create reusable UI components",
    ),
    (
        "Digital Marketing Analyst",
        "Google Analytics|SEO|Excel|Digital Marketing",
        "Google Ads|SQL|Campaign Analysis|Power BI",
        300000,
        "BA",
        "measure campaign conversion|audit acquisition channels|build attribution reports|recommend landing page experiments",
    ),
    (
        "SEO Analyst",
        "SEO|Google Analytics|Content Marketing|Excel",
        "SEM|Copywriting|HTML|Market Research",
        280000,
        "12th",
        "audit site content|research search demand|track organic conversions|improve technical SEO checks",
    ),
    (
        "Customer Support Executive",
        "Customer Support|Communication|CRM|Ticketing",
        "Zendesk|Email Support|Chat Support|Conflict Resolution",
        220000,
        "12th",
        "resolve customer tickets|maintain accurate case notes|meet response time targets|identify recurring service problems",
    ),
    (
        "Operations Analyst",
        "Excel|SQL|Operations|Process Improvement",
        "Power BI|Supply Chain|Inventory Management|Forecasting",
        330000,
        "BA",
        "analyze fulfillment delays|monitor service metrics|identify process bottlenecks|plan operational capacity",
    ),
    (
        "Financial Analyst",
        "Excel|Financial Analysis|Accounting|Financial Modeling",
        "SQL|Power BI|Budgeting|Valuation",
        400000,
        "BCom",
        "prepare budget variance reports|model unit economics|analyze monthly cash flow|validate financial assumptions",
    ),
    (
        "Cybersecurity Analyst",
        "Cybersecurity|Networking|Linux|SIEM",
        "Splunk|Incident Response|Wireshark|Python",
        500000,
        "BTech",
        "triage security alerts|investigate suspicious logs|document response procedures|assess infrastructure vulnerabilities",
    ),
    (
        "Cloud Engineer",
        "AWS|Linux|Networking|Docker",
        "Terraform|Kubernetes|Azure|Monitoring",
        600000,
        "BTech",
        "operate cloud infrastructure|improve deployment reliability|monitor system capacity|automate infrastructure changes",
    ),
    (
        "Graphic Designer",
        "Photoshop|Illustrator|Canva|Typography",
        "Figma|Branding|Video Editing|InDesign",
        260000,
        "Diploma",
        "design campaign assets|maintain visual guidelines|prepare print layouts|adapt creative for digital channels",
    ),
    (
        "Marketing Analyst",
        "Excel|Market Research|Google Analytics|Campaign Analysis",
        "SQL|Tableau|A/B Testing|Communication",
        340000,
        "BA",
        "segment customer audiences|measure marketing efficiency|research competitor positioning|present customer insights",
    ),
    (
        "HR Analyst",
        "Excel|HR Analytics|Communication|Reporting",
        "SQL|Power BI|HRIS|Payroll",
        320000,
        "BA",
        "analyze workforce trends|audit HR data quality|report recruitment efficiency|monitor employee retention",
    ),
    (
        "Business Intelligence Analyst",
        "SQL|Power BI|Data Modeling|Data Visualization",
        "Tableau|DAX|Excel|Stakeholder Management",
        480000,
        "BSc",
        "define consistent KPI metrics|build self-service analytics|document reporting models|translate business questions into dashboards",
    ),
    (
        "Quality Assurance Analyst",
        "Quality Assurance|SQL|Communication|Problem Solving",
        "Python|Jira|REST API|Agile",
        300000,
        "Diploma",
        "design test scenarios|verify data integrity|reproduce reported defects|track release readiness",
    ),
    (
        "UX Researcher",
        "UX Research|Figma|Communication|Prototyping",
        "UI Design|A/B Testing|Accessibility|Presentation",
        420000,
        "BA",
        "conduct usability sessions|synthesize research findings|validate interface prototypes|present user journey insights",
    ),
    (
        "Data Engineer",
        "Python|SQL|ETL|Data Modeling|PostgreSQL",
        "Spark|Azure|AWS|Databricks",
        600000,
        "BTech",
        "build ingestion pipelines|monitor dataset freshness|design analytical storage|enforce data quality contracts",
    ),
]
COMPANIES = [
    "Northstar",
    "Cedar",
    "Bluepeak",
    "Meridian",
    "Orbit",
    "Aster",
    "Riverstone",
    "Lumina",
    "Juniper",
    "Nexa",
    "Cobalt",
    "Maple",
    "Vantage",
    "Prism",
    "Evergreen",
    "Nimbus",
]
INDUSTRIES = [
    "Technology",
    "Retail",
    "Finance",
    "Healthcare",
    "Education",
    "Logistics",
    "Media",
    "Manufacturing",
]
DOMAINS = [
    "subscription growth",
    "regional expansion",
    "customer experience",
    "inventory accuracy",
    "digital transformation",
    "service efficiency",
    "quality improvement",
    "cost optimization",
]
CITIES = [
    "Kolkata",
    "Bangalore",
    "Hyderabad",
    "Delhi",
    "Noida",
    "Gurugram",
    "Mumbai",
    "Pune",
    "Chennai",
    "Ahmedabad",
    "Patna",
    "Remote",
]


def generate_dataset(path, count=640, seed=2026, reference_date=None):
    rng = random.Random(seed)
    today = reference_date or date.today()
    rows = []
    for index in range(count):
        role, required, preferred, base, education, tasks = ROLE_SPECS[
            index % len(ROLE_SPECS)
        ]
        required = required.split("|")
        preferred = preferred.split("|")
        extra = rng.choice(preferred)
        if index % 3 == 0:
            required.append(extra)
            preferred.remove(extra)
        minimum = rng.choices([0, 1, 2, 3, 4, 5], weights=[30, 25, 20, 12, 8, 5])[0]
        if role.startswith("Junior"):
            minimum = min(minimum, 1)
        job_type = rng.choices(EMPLOYMENT_TYPES, weights=[78, 5, 9, 8])[0]
        if job_type == "Internship":
            minimum = 0
        salary_min = (
            int(base * (1 + 0.28 * minimum) * rng.uniform(0.82, 1.18) / 10000) * 10000
        )
        if job_type == "Internship":
            salary_min = rng.choice([120000, 180000, 240000])
        salary_max = salary_min + rng.choice([120000, 180000, 250000, 350000])
        company = f"{rng.choice(COMPANIES)} {rng.choice(['Labs', 'Solutions', 'Works', 'Systems', 'Partners'])}"
        industry = rng.choice(INDUSTRIES)
        location = CITIES[(index + index // len(ROLE_SPECS)) % len(CITIES)]
        domain = rng.choice(DOMAINS)
        responsibilities = rng.sample(tasks.split("|"), 3)
        focus = rng.choice(
            [
                "weekly business reviews",
                "a new product launch",
                "an expanding customer base",
                "a cross-functional transformation program",
                "regional service teams",
            ]
        )
        description = (
            f"Join the {industry.lower()} team at {company} as a {role}. "
            f"Your work supports {domain} for {focus}. "
            f"You will {responsibilities[0]}, {responsibilities[1]}, and {responsibilities[2]}. "
            f"Use {', '.join(required[:3])} to deliver clear, documented work. "
            f"Collaborate with a team of {rng.randint(4, 18)} across {rng.choice(['product and operations', 'finance and strategy', 'design and engineering', 'customer success and sales'])}. "
            f"Success means {rng.choice(['reliable weekly delivery', 'measurable quality improvements', 'clear stakeholder communication', 'well-tested, reusable outputs'])}. "
            "This is a fictional demonstration listing; no employer receives applications."
        )
        rows.append(
            {
                "job_id": f"SYN-{index + 1:04}",
                "job_title": role,
                "company_name": company,
                "location": location,
                "salary_min": salary_min,
                "salary_max": salary_max,
                "experience_min": minimum,
                "experience_max": minimum + rng.choice([1, 2, 3]),
                "required_skills": "|".join(required),
                "preferred_skills": "|".join(preferred),
                "education": education,
                "industry": industry,
                "employment_type": job_type,
                "job_description": description,
                "company_rating": round(rng.uniform(3.2, 4.9), 1),
                "posted_date": (today - timedelta(days=rng.randint(0, 40))).isoformat(),
                "deadline": (today + timedelta(days=rng.randint(15, 90))).isoformat(),
                "is_synthetic": "true",
            }
        )
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0])
        writer.writeheader()
        writer.writerows(rows)
    return rows


def clean_text(value, limit=50000):
    return re.sub(r"[\x00-\x08\x0b-\x1f\x7f]", "", str(value or "")).strip()[:limit]


def optional_number(value, integer=False):
    if value is None or str(value).strip().casefold() in {"", "nan", "none", "null"}:
        return None
    number = float(str(value).replace(",", "").replace("₹", "").strip())
    if not 0 <= number <= 1e9:
        raise ValueError("Numeric value is negative, non-finite, or too large.")
    return int(number) if integer else number


def clean_job_rows(rows):
    cleaned, seen, errors = [], set(), []
    for index, row in enumerate(rows, start=2):
        try:
            title = re.sub(r"\s+", " ", clean_text(row.get("job_title"), 160))
            company = re.sub(r"\s+", " ", clean_text(row.get("company_name"), 160))
            if not title or not company:
                raise ValueError("Title and company are required.")
            lower = optional_number(row.get("salary_min"), True)
            upper = optional_number(row.get("salary_max"), True)
            if lower is not None and upper is not None and upper < lower:
                lower, upper = upper, lower
            exp_min = optional_number(row.get("experience_min")) or 0
            exp_max = optional_number(row.get("experience_max"))
            if exp_min > 60 or (
                exp_max is not None and (exp_max < exp_min or exp_max > 60)
            ):
                raise ValueError("Invalid experience range.")
            description = clean_text(row.get("job_description"), 12000)
            required = normalize_skills(
                row.get("required_skills", "")
            ) or extract_skills(description)
            preferred = normalize_skills(row.get("preferred_skills", ""))
            location = (
                re.sub(r"\s+", " ", clean_text(row.get("location"), 100))
                or "Unspecified"
            )
            location = next(
                (c for c in CITIES if c.casefold() == location.casefold()), location
            )
            location = {"Bengaluru": "Bangalore", "Gurgaon": "Gurugram"}.get(
                location, location
            )
            identity = (
                title.casefold(),
                company.casefold(),
                location.casefold(),
                lower,
                upper,
                exp_min,
                tuple(required),
                description.casefold(),
            )
            if identity in seen:
                continue
            seen.add(identity)
            rating = optional_number(row.get("company_rating"))
            if rating is not None and rating > 5:
                raise ValueError("Company rating must be between 0 and 5.")
            posted = (
                date.fromisoformat(row["posted_date"])
                if row.get("posted_date")
                else date.today()
            )
            deadline = (
                date.fromisoformat(row["deadline"]) if row.get("deadline") else None
            )
            if deadline and deadline < posted:
                raise ValueError("Deadline precedes posted date.")
            job_type = clean_text(row.get("employment_type"), 50) or "Full-time"
            job_type = next(
                (t for t in EMPLOYMENT_TYPES if t.casefold() == job_type.casefold()),
                job_type,
            )
            if job_type not in EMPLOYMENT_TYPES:
                raise ValueError("Unsupported employment type.")
            cleaned.append(
                {
                    "source_id": clean_text(row.get("job_id"), 80) or None,
                    "remote_type": (
                        "remote"
                        if clean_text(row.get("location"), 100).casefold() == "remote"
                        else "onsite"
                    ),
                    "remote_allowed": clean_text(row.get("location"), 100).casefold()
                    == "remote",
                    "job_title": title,
                    "company_name": company,
                    "location": location,
                    "state": CITY_STATES.get(location.casefold(), ""),
                    "min_salary": lower,
                    "max_salary": upper,
                    "experience_min": exp_min,
                    "experience_max": exp_max,
                    "required_skills": required,
                    "preferred_skills": preferred,
                    "education_required": clean_text(row.get("education"), 160),
                    "industry": clean_text(row.get("industry"), 80) or "Other",
                    "employment_type": job_type,
                    "job_description": description,
                    "company_rating": rating,
                    "posted_date": posted,
                    "application_deadline": deadline,
                    "is_synthetic": str(row.get("is_synthetic", "true")).casefold()
                    == "true",
                }
            )
        except (ValueError, TypeError) as exc:
            errors.append({"row": index, "error": str(exc)})
    return cleaned, errors


def seed_jobs(data_dir):
    data_dir = Path(data_dir)
    path = data_dir / "jobs.csv"
    if not path.exists():
        generate_dataset(path)
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows, errors = clean_job_rows(list(csv.DictReader(handle)))
    source_ids = set(db.session.scalars(db.select(Job.source_id)).all())
    added = 0
    for row in rows:
        if row["source_id"] in source_ids:
            continue
        db.session.add(Job(**row))
        source_ids.add(row["source_id"])
        added += 1
    db.session.commit()
    if rows:
        with (data_dir / "processed_jobs.csv").open(
            "w", encoding="utf-8", newline=""
        ) as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=list(rows[0]) + ["processed_text"],
                lineterminator="\n",
            )
            writer.writeheader()
            for row in rows:
                processed = " ".join(
                    [
                        row["job_title"],
                        row["job_description"],
                        " ".join(row["required_skills"]),
                        " ".join(row["preferred_skills"]),
                    ]
                )
                writer.writerow(
                    {
                        **row,
                        "required_skills": json.dumps(row["required_skills"]),
                        "preferred_skills": json.dumps(row["preferred_skills"]),
                        "processed_text": processed,
                    }
                )
    return {"added": added, "cleaned": len(rows), "errors": errors}
