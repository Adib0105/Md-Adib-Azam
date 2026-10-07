from flask import current_app
from models.database import db, Job, JobProvider, ExternalJobIdentity
from services.job_providers.adzuna_provider import AdzunaProvider
from services.job_providers.usajobs_provider import USAJobsProvider

PROVIDERS = {"adzuna": AdzunaProvider, "usajobs": USAJobsProvider}


def cached_lookup(provider, external_id):
    identity = db.session.scalar(
        db.select(ExternalJobIdentity).where(
            ExternalJobIdentity.provider == provider,
            ExternalJobIdentity.external_id == external_id,
        )
    )
    job = db.session.get(Job, identity.job_id) if identity else None
    return job.as_dict() if job else None


def get_provider(slug):
    if slug not in PROVIDERS:
        raise ValueError("Unknown job provider.")
    overrides = current_app.extensions.get("provider_overrides", {})
    return overrides.get(slug) or PROVIDERS[slug](
        current_app.config, lookup=cached_lookup
    )


def initialize_providers():
    for slug in PROVIDERS:
        if not db.session.get(JobProvider, slug):
            db.session.add(
                JobProvider(
                    slug=slug, enabled=current_app.config["ENABLE_" + slug.upper()]
                )
            )
    db.session.commit()


def provider_summaries(private=False):
    rows = []
    for slug in PROVIDERS:
        provider = get_provider(slug)
        state = db.session.get(JobProvider, slug)
        row = {
            "slug": slug,
            "name": provider.name,
            "configured": provider.configured,
            "enabled": bool(state and state.enabled),
            "status": state.status
            if provider.configured and state
            else "not_configured",
        }
        if private and state:
            row.update(
                last_success=state.last_success.isoformat() + "Z"
                if state.last_success
                else None,
                last_attempt=state.last_attempt.isoformat() + "Z"
                if state.last_attempt
                else None,
                last_error=state.last_error,
                response_ms=state.response_ms,
                requests=state.requests,
                failures=state.failures,
                jobs_fetched=state.jobs_fetched,
                jobs_inserted=state.jobs_inserted,
                jobs_updated=state.jobs_updated,
                jobs_skipped=state.jobs_skipped,
                quota="Not reported by these providers",
            )
        rows.append(row)
    return rows
