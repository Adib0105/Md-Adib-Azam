"""Allowlisted, plain-text public content and non-secret operating settings."""

from flask import current_app, g, has_app_context
from models.database import db, SiteSetting
from config import validate_weights
from utils.validators import ValidationError

CONTENT_DEFAULTS = {
    "hero_title": "Find the right job. Build the right skills.",
    "hero_subtitle": "Discover jobs from supported providers, understand your match and find the skills that move your career forward. Demo jobs remain available offline.",
    "cta_text": "Find my matches",
    "marquee_heading": "Latest job opportunities",
    "featured_categories": "Data Analyst, Python Developer, Business Analyst, Power BI Developer, SQL Developer, Cybersecurity Analyst",
    "about": "JobMatch is an AI-assisted job recommendation and career intelligence college project. It brings resume review, explainable ranking, external job discovery and practical learning insights into one workspace.",
    "contact_details": "GitHub: github.com/Adib0105 · Portfolio: github.com/Adib0105/Md-Adib-Azam",
    "footer_text": "JobMatch — College Project · Developed by Md Adib Azam · Bengal College of Polytechnic, Durgapur",
    "privacy": "JobMatch stores account, profile, reviewed resume and tracker data in the operator’s database. External job searches send your search terms and selected filters to the chosen provider. Your resume is not sent to job providers. Password recovery and opted-in alerts use the configured mail service. The operator is responsible for retention, backups and deployment-specific privacy notices.",
    "terms": "Demo listings are synthetic. External listings belong to their credited providers and may change or expire. Matching scores are estimates, not hiring probabilities or guarantees. Applying on a source opens that provider; JobMatch does not submit applications for you. Verify eligibility, working arrangements and salary with the source.",
    "faq": "Are demo jobs real? No, they are fictional.\nDoes JobMatch apply for me? No, you apply on the source and track your progress here.\nDoes Google supply data to JobMatch? No, the Google button is an outbound search link.\nCan I use it offline? Yes, demo jobs and local career tools work without provider keys.",
}
SETTING_DEFAULTS = {
    "real_job_cache_ttl_minutes": 30,
    "external_job_stale_days": 14,
    "external_job_max_age_days": 60,
}


def settings():
    if has_app_context() and hasattr(g, "site_values"):
        return g.site_values
    values = {row.key: row.value for row in db.session.scalars(db.select(SiteSetting))}
    if has_app_context():
        g.site_values = values
    return values


def content():
    values = settings()
    return {
        key: values.get("content." + key, default)
        for key, default in CONTENT_DEFAULTS.items()
    }


def setting(key):
    return settings().get(
        key, current_app.config.get(key.upper(), SETTING_DEFAULTS.get(key))
    )


def weights():
    result = settings().get(
        "recommendation_weights", current_app.config["RECOMMENDATION_WEIGHTS"]
    )
    validate_weights(result)
    return result


def put_setting(key, value):
    row = db.session.get(SiteSetting, key)
    if row:
        row.value = value
    else:
        db.session.add(SiteSetting(key=key, value=value))
    if has_app_context():
        g.pop("site_values", None)


def update_content(form):
    for key in CONTENT_DEFAULTS:
        value = str(form.get(key, "")).strip()
        maximum = 200 if key in {"hero_title", "cta_text", "marquee_heading"} else 12000
        if not value or len(value) > maximum:
            raise ValidationError(
                f"{key.replace('_', ' ').title()} must contain 1–{maximum} characters."
            )
    for key in CONTENT_DEFAULTS:
        put_setting("content." + key, str(form[key]).strip())
