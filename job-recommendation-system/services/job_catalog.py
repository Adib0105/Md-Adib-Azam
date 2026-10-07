"""One source of truth for eligibility, freshness, currencies and SQL filters."""

from datetime import date, timedelta
from urllib.parse import urlencode
from models.database import db, Job, ExternalJobIdentity, utcnow
from models.skill_extractor import normalize_skills
from services.settings_service import setting
from utils.validators import (
    number_field,
    text_field,
    choice_field,
    ValidationError,
    CURRENCIES,
)

SOURCES = {"all", "demo", "manual", "external", "adzuna", "usajobs"}
COUNTRIES = {
    "in",
    "gb",
    "us",
    "au",
    "at",
    "be",
    "br",
    "ca",
    "ch",
    "de",
    "es",
    "fr",
    "it",
    "mx",
    "nl",
    "nz",
    "pl",
    "sg",
    "za",
}


def freshness_label(job):
    if not job.is_external:
        return "Demo listing" if job.is_synthetic else "Local listing"
    now = utcnow()
    age = (now.date() - job.posted_date).days
    if (
        job.application_deadline
        and job.application_deadline < now.date()
        or not job.last_synced_at
        or job.last_synced_at < now - timedelta(days=setting("external_job_stale_days"))
        or age > setting("external_job_max_age_days")
    ):
        return "Possibly expired"
    if job.freshness_override in {"Older listing", "Possibly expired"}:
        return job.freshness_override
    if not job.external_created_at:
        return "Date not supplied"
    return "Fresh" if age <= 2 else "Recently posted" if age <= 14 else "Older listing"


def salary_display(job):
    def amount(value):
        if value is None:
            return None
        if job.salary_currency == "INR" and job.salary_period == "year":
            return f"₹{value / 100000:g} LPA"
        return f"{job.salary_currency} {value:,.0f}"

    lower, upper = amount(job.min_salary), amount(job.max_salary)
    label = (
        f"{lower} – {upper}"
        if lower and upper and lower != upper
        else lower or upper or "Salary not listed"
    )
    return label + (
        f" / {job.salary_period}"
        if (lower or upper)
        and not (job.salary_currency == "INR" and job.salary_period == "year")
        else ""
    )


def eligible_conditions():
    now = utcnow()
    return [
        Job.active.is_(True),
        Job.published.is_(True),
        Job.archived.is_(False),
        Job.deleted.is_(False),
        db.or_(
            Job.application_deadline.is_(None), Job.application_deadline >= now.date()
        ),
        db.or_(
            Job.is_external.is_(False),
            db.and_(
                Job.last_synced_at
                >= now - timedelta(days=setting("external_job_stale_days")),
                Job.posted_date
                >= now.date() - timedelta(days=setting("external_job_max_age_days")),
                Job.freshness_override != "Possibly expired",
            ),
        ),
    ]


def parse_filters(values):
    f = {
        key: text_field(values, key, maximum)
        for key, maximum in {
            "q": 160,
            "location": 160,
            "title": 160,
            "company": 160,
            "industry": 80,
            "education": 160,
            "skills": 1000,
            "category": 80,
        }.items()
    }
    f["source"] = choice_field(values, "source", SOURCES, "all")
    f["country"] = choice_field(values, "country", COUNTRIES, "in")
    f["currency"] = choice_field(values, "currency", CURRENCIES | {""}, "")
    f["type"] = str(values.get("type", values.get("employment_type", ""))).strip()
    if f["type"] not in {
        "",
        "Full-time",
        "Part-time",
        "Contract",
        "Internship",
        "Permanent",
        "Other",
    }:
        raise ValidationError("Choose a valid employment type.")
    f["sort"] = choice_field(
        values,
        "sort",
        {"relevance", "match", "salary", "newest", "rating"},
        "relevance" if f["q"] else "match",
    )
    remote = str(values.get("remote", "")).lower()
    if remote not in {"", "false", "true", "on", "1", "0"}:
        raise ValidationError("Choose a valid remote filter.")
    f["remote"] = remote in {"true", "on", "1"}
    for key, maximum, integer in [
        ("min_salary", 100000000, True),
        ("max_salary", 100000000, True),
        ("experience", 60, False),
        ("min_match", 100, False),
        ("posted", 365, True),
    ]:
        f[key] = number_field(values, key, maximum, integer)
    if (
        f["min_salary"] is not None
        and f["max_salary"] is not None
        and f["min_salary"] > f["max_salary"]
    ):
        raise ValidationError("Minimum salary cannot exceed maximum salary.")
    for key, default, maximum in [("page", 1, 10000), ("per_page", 20, 50)]:
        f[key] = number_field(values, key, maximum, True)
        f[key] = default if f[key] is None else f[key]
        if f[key] < 1:
            raise ValidationError(f"{key} must be positive.")
    return f


def job_query(filters=None, *, include_closed=False):
    f = filters or {}
    query = db.select(Job)
    if not include_closed:
        query = query.where(*eligible_conditions())
    for key, column in [
        ("title", Job.job_title),
        ("company", Job.company_name),
        ("location", Job.location),
        ("industry", Job.industry),
        ("education", Job.education_required),
    ]:
        if f.get(key):
            query = query.where(column.icontains(f[key], autoescape=True))
    source = f.get("source", "all")
    if source == "demo":
        query = query.where(Job.is_synthetic.is_(True))
    elif source == "external":
        query = query.where(Job.is_external.is_(True))
    elif source in {"adzuna", "usajobs"}:
        query = query.where(
            db.or_(
                Job.source == source,
                Job.id.in_(
                    db.select(ExternalJobIdentity.job_id).where(
                        ExternalJobIdentity.provider == source
                    )
                ),
            )
        )
    elif source == "manual":
        query = query.where(Job.source == "manual")
    if f.get("remote"):
        query = query.where(
            db.or_(
                Job.remote_allowed.is_(True), db.func.lower(Job.location) == "remote"
            )
        )
    if f.get("type"):
        query = query.where(Job.employment_type == f["type"])
    if f.get("posted") is not None:
        query = query.where(
            Job.posted_date >= date.today() - timedelta(days=f["posted"]),
            db.or_(Job.is_external.is_(False), Job.external_created_at.is_not(None)),
        )
    for key, column, direction in [
        ("min_salary", Job.max_salary, "min"),
        ("max_salary", Job.min_salary, "max"),
        ("experience", Job.experience_min, "max"),
    ]:
        if f.get(key) is not None:
            query = query.where(
                column >= f[key] if direction == "min" else column <= f[key]
            )
    if f.get("min_salary") is not None or f.get("max_salary") is not None:
        currency = f.get("currency") or (
            "USD"
            if f.get("source") == "usajobs"
            else country_currency(f.get("country", "in"))
        )
        query = query.where(
            Job.salary_currency == currency, Job.salary_period == "year"
        )
    elif f.get("currency"):
        query = query.where(Job.salary_currency == f["currency"])
    if f.get("experience") is not None:
        query = query.where(Job.experience_known.is_(True))
    for skill in normalize_skills(f.get("skills", "")):
        query = query.where(
            db.or_(
                db.cast(Job.required_skills, db.Text).icontains(skill, autoescape=True),
                db.cast(Job.preferred_skills, db.Text).icontains(
                    skill, autoescape=True
                ),
            )
        )
    # A bounded lexical prefilter prevents loading the entire external catalogue.
    for token in str(f.get("q", "")).split()[:12]:
        query = query.where(
            db.or_(
                Job.job_title.icontains(token, autoescape=True),
                Job.company_name.icontains(token, autoescape=True),
                Job.job_description.icontains(token, autoescape=True),
                Job.location.icontains(token, autoescape=True),
            )
        )
    return query


def country_currency(country):
    return {
        "in": "INR",
        "gb": "GBP",
        "us": "USD",
        "au": "AUD",
        "ca": "CAD",
        "nz": "NZD",
        "sg": "SGD",
        "za": "ZAR",
        "br": "BRL",
        "mx": "MXN",
        "pl": "PLN",
        "ch": "CHF",
    }.get(country, "EUR")


def google_jobs_url(query="", location=""):
    terms = " ".join(
        x
        for x in [
            str(query)[:160].strip() or "jobs",
            "jobs" if query else "",
            "in " + str(location)[:160].strip() if location else "",
        ]
        if x
    )
    return "https://www.google.com/search?" + urlencode({"q": terms})
