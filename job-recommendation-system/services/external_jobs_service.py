"""TTL cache + database leases coalesce provider requests across processes."""

import hashlib
import json
import time
from datetime import timedelta
from uuid import uuid4
from sqlalchemy.exc import IntegrityError
from models.database import (
    db,
    Job,
    JobProvider,
    ExternalJobIdentity,
    ExternalJobCache,
    utcnow,
)
from services.job_providers.base import ProviderError
from services.job_providers.provider_registry import get_provider
from services.settings_service import setting
from services.security_service import consume_limit, audit
from services.notification_service import saved_job_updated
from flask import current_app


def upsert_jobs(provider, records):
    ids = []
    counts = {"inserted": 0, "updated": 0, "skipped": 0}
    for fields in records[:50]:
        try:
            with db.session.begin_nested():
                identity = db.session.scalar(
                    db.select(ExternalJobIdentity).where(
                        ExternalJobIdentity.provider == provider,
                        ExternalJobIdentity.external_id == fields["external_id"],
                    )
                )
                job = (
                    db.session.get(Job, identity.job_id)
                    if identity
                    else db.session.scalar(
                        db.select(Job).where(
                            Job.fingerprint == fields["fingerprint"],
                            Job.is_external.is_(True),
                        )
                    )
                )
                created = job is None
                if created:
                    job = Job(
                        source_id="EXT-"
                        + provider
                        + "-"
                        + hashlib.sha256(fields["external_id"].encode()).hexdigest()[
                            :32
                        ]
                    )
                    db.session.add(job)
                own_source = created or job.source == provider
                changed = False
                if own_source:
                    changed = not created and any(
                        getattr(job, k) != fields[k]
                        for k in (
                            "job_title",
                            "company_name",
                            "job_description",
                            "min_salary",
                            "max_salary",
                            "location",
                        )
                    )
                    for key, value in fields.items():
                        setattr(job, key, value)
                    job.last_synced_at = utcnow()
                    if not job.first_seen_at:
                        job.first_seen_at = utcnow()
                    db.session.flush()
                    if changed:
                        saved_job_updated(job)
                if not identity:
                    identity = ExternalJobIdentity(
                        provider=provider,
                        external_id=fields["external_id"],
                        job_id=job.id,
                        source_url=fields["source_url"],
                    )
                    db.session.add(identity)
                identity.last_seen_at = utcnow()
                identity.source_url = fields["source_url"]
                db.session.flush()
                ids.append(job.id)
                counts[
                    "inserted" if created else "updated" if own_source else "skipped"
                ] += 1
        except (IntegrityError, KeyError, TypeError):
            counts["skipped"] += 1
    return list(dict.fromkeys(ids)), counts


def cache_parameters(slug, filters):
    keys = (
        "q",
        "location",
        "country",
        "category",
        "page",
        "per_page",
        "min_salary",
        "max_salary",
        "type",
        "posted",
        "sort",
    )
    params = {k: filters.get(k) for k in keys if filters.get(k) not in {None, ""}}
    params["sort"] = (
        params.get("sort")
        if params.get("sort") in {"salary", "newest"}
        else "relevance"
    )
    if slug == "usajobs":
        params["country"] = "us"
        params["remote"] = bool(filters.get("remote"))
    return params


def cache_result(cache, *, status, message="", fallback=False):
    return {
        "ids": list(cache.job_ids or []) if cache else [],
        "provider": cache.provider if cache else None,
        "provider_total": cache.total if cache else 0,
        "status": status,
        "message": message,
        "fallback": fallback,
        "fetched_at": cache.fetched_at if cache else None,
    }


def live_search(slug, filters, force=False):
    provider = get_provider(slug)
    state = db.session.get(JobProvider, slug)
    params = cache_parameters(slug, filters)
    key = hashlib.sha256(
        json.dumps(["v2", slug, params], sort_keys=True).encode()
    ).hexdigest()
    cache = db.session.get(ExternalJobCache, key)
    now = utcnow()
    if not state or not state.enabled or not provider.configured:
        message = (
            "Connect a supported job provider to enable live job discovery."
            if not provider.configured
            else "This provider is disabled."
        )
        return cache_result(
            cache,
            status="unavailable",
            message=message
            + (
                " Showing cached results."
                if cache and cache.job_ids
                else " Showing JobMatch demo jobs."
            ),
            fallback=not bool(cache and cache.job_ids),
        )
    if cache and cache.expires_at and cache.expires_at > now and not force:
        return cache_result(
            cache, status="cached", message="Showing recently cached provider results."
        )
    if cache and cache.retry_after and cache.retry_after > now and not force:
        return cache_result(
            cache,
            status="stale",
            message="Live refresh unavailable. "
            + (
                "Showing cached results."
                if cache.job_ids
                else "Showing JobMatch demo jobs."
            ),
            fallback=not bool(cache.job_ids),
        )
    if not cache:
        try:
            db.session.add(ExternalJobCache(key=key, provider=slug, parameters=params))
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        cache = db.session.get(ExternalJobCache, key)
    lease = str(uuid4())
    won = db.session.execute(
        db.update(ExternalJobCache)
        .where(
            ExternalJobCache.key == key,
            db.or_(
                ExternalJobCache.lock_until.is_(None), ExternalJobCache.lock_until < now
            ),
        )
        .values(lock_until=now + timedelta(seconds=45), lock_token=lease)
    ).rowcount
    db.session.commit()
    if not won:
        return cache_result(
            cache,
            status="refreshing",
            message="A provider refresh is already running. "
            + (
                "Showing cached results."
                if cache.job_ids
                else "Please retry in a moment; showing demo jobs."
            ),
            fallback=not bool(cache.job_ids),
        )
    started = time.monotonic()
    try:
        if not consume_limit(
            "provider_hour",
            slug,
            current_app.config["PROVIDER_REQUESTS_PER_HOUR"],
            3600,
        ):
            raise ProviderError("Provider request budget reached. Try again later.")
        state.last_attempt = now
        state.requests += 1
        db.session.commit()
        result = provider.search_jobs(**params)
        ids, counts = upsert_jobs(slug, result.jobs)
        state = db.session.get(JobProvider, slug)
        state.status = "ok"
        state.last_success = utcnow()
        state.last_error = ""
        state.response_ms = round((time.monotonic() - started) * 1000)
        state.jobs_fetched += len(result.jobs)
        state.jobs_inserted += counts["inserted"]
        state.jobs_updated += counts["updated"]
        state.jobs_skipped += counts["skipped"] + result.skipped
        db.session.execute(
            db.update(ExternalJobCache)
            .where(ExternalJobCache.key == key, ExternalJobCache.lock_token == lease)
            .values(
                job_ids=ids,
                total=result.total,
                fetched_at=utcnow(),
                expires_at=utcnow()
                + timedelta(minutes=setting("real_job_cache_ttl_minutes")),
                retry_after=None,
                lock_until=None,
                lock_token=None,
                last_error="",
            )
        )
        audit(
            "provider_sync",
            subject_type="provider",
            subject_id=slug,
            details={"fetched": len(result.jobs), **counts},
        )
        db.session.commit()
        db.session.expire(cache)
        return cache_result(
            cache, status="live", message="Results refreshed from the provider."
        )
    except ProviderError as exc:
        db.session.rollback()
        state = db.session.get(JobProvider, slug)
        state.status = "unavailable"
        state.last_error = str(exc)[:160]
        state.failures += 1
        state.response_ms = round((time.monotonic() - started) * 1000)
        db.session.execute(
            db.update(ExternalJobCache)
            .where(ExternalJobCache.key == key, ExternalJobCache.lock_token == lease)
            .values(
                retry_after=utcnow() + timedelta(minutes=2),
                lock_until=None,
                lock_token=None,
                last_error=str(exc)[:160],
            )
        )
        audit(
            "provider_failure",
            subject_type="provider",
            subject_id=slug,
            details={"error": "provider_unavailable"},
        )
        db.session.commit()
        cache = db.session.get(ExternalJobCache, key)
        return cache_result(
            cache,
            status="stale",
            message="Live refresh unavailable. "
            + (
                "Showing cached results."
                if cache.job_ids
                else "Showing JobMatch demo jobs."
            ),
            fallback=not bool(cache.job_ids),
        )
