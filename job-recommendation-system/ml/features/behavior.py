"""Bounded behavior summaries with explicit timestamps and cold-start fallback."""

from collections import Counter
from datetime import timedelta
from flask import current_app
from sqlalchemy.orm import joinedload
from models.database import db, SavedJob, Application, JobView, utcnow
from models.ml_data import InteractionEvent
from models.skill_extractor import normalize_skills

ACTION_WEIGHTS = {
    "viewed": 0.15,
    "saved": 0.7,
    "applied": 1.0,
    "interview": 1.2,
    "offer": 1.5,
    "rejected": -1.0,
    "ignored": -0.5,
    "unsaved": 0.0,
    "outcome_rejected": 0.0,
}
MEANINGFUL = {"saved", "applied", "interview", "offer", "rejected", "ignored"}


def build_behavior(events, *, cutoff=None, min_jobs=5, min_actions=3):
    cutoff = cutoff or utcnow()
    cutoff = cutoff.replace(tzinfo=None)
    past = [
        event
        for event in events
        if event["at"].replace(tzinfo=None) <= cutoff
        and event["action"] in ACTION_WEIGHTS
    ]
    # Only the newest signal of each kind contributes; repeated clicks cannot flood weights.
    latest = {}
    for event in sorted(past, key=lambda e: (e["at"], e.get("id", 0))):
        if event["action"] == "outcome_rejected":
            continue
        group = (
            "preference"
            if event["action"] in {"rejected", "ignored"}
            else (
                "save"
                if event["action"] in {"saved", "unsaved"}
                else (
                    "application"
                    if event["action"]
                    in {"applied", "interview", "offer", "outcome_rejected"}
                    else "view"
                )
            )
        )
        latest[event["job_id"], group] = event
    selected = list(latest.values())
    meaningful = {
        event["job_id"] for event in selected if event["action"] in MEANINGFUL
    }
    enough = (
        len({e["job_id"] for e in selected}) >= min_jobs
        and len(meaningful) >= min_actions
    )
    preferences = {
        key: Counter()
        for key in ["roles", "locations", "skills", "employment_types", "remote_modes"]
    }
    for event in selected:
        age = max(0, (cutoff.date() - event["at"].replace(tzinfo=None).date()).days)
        strength = ACTION_WEIGHTS[event["action"]] * (0.5 ** (age / 90))
        job = event["job"]
        for key, values in [
            ("roles", [job.job_title]),
            ("locations", [job.location]),
            ("skills", normalize_skills(job.required_skills)),
            ("employment_types", [job.employment_type]),
            ("remote_modes", [job.remote_type or "unknown"]),
        ]:
            for value in values:
                preferences[key][str(value).casefold()] += strength
    return {
        "enabled": enough,
        "distinct_jobs": len({e["job_id"] for e in selected}),
        "meaningful_jobs": len(meaningful),
        "preferences": preferences,
        "cutoff": cutoff.isoformat(),
        "reason": (
            "Enough distinct, meaningful prior interactions."
            if enough
            else "Cold start: fewer than five jobs or three meaningful job actions."
        ),
    }


def behavior_for(user, cutoff=None):
    cutoff = cutoff or utcnow()
    events = db.session.scalars(
        db.select(InteractionEvent)
        .options(joinedload(InteractionEvent.job))
        .where(
            InteractionEvent.user_id == user.id,
            InteractionEvent.created_at <= cutoff,
            InteractionEvent.created_at >= cutoff - timedelta(days=365),
        )
        .order_by(InteractionEvent.created_at.desc(), InteractionEvent.id.desc())
        .limit(500)
    ).all()
    values = [
        {
            "id": e.id,
            "job_id": e.job_id,
            "job": e.job,
            "action": e.action,
            "at": e.created_at,
        }
        for e in events
    ]
    covered = {(e.job_id, e.action) for e in events}
    # Backward-compatible history: timestamped saved/viewed/applied records can be reused.
    for model, timestamp, action in [
        (SavedJob, "created_at", "saved"),
        (JobView, "viewed_at", "viewed"),
        (Application, "applied_date", "applied"),
    ]:
        records = db.session.scalars(
            db.select(model)
            .options(joinedload(model.job))
            .where(
                model.user_id == user.id,
                getattr(model, timestamp) <= cutoff,
                getattr(model, timestamp) >= cutoff - timedelta(days=365),
            )
            .order_by(getattr(model, timestamp).desc())
            .limit(200)
        ).all()
        for record in records:
            # New event history supersedes mutable legacy records, including unsaves.
            if model is SavedJob and any(
                e.job_id == record.job_id and e.action in {"saved", "unsaved"}
                for e in events
            ):
                continue
            if (record.job_id, action) not in covered:
                values.append(
                    {
                        "id": 0,
                        "job_id": record.job_id,
                        "job": record.job,
                        "action": action,
                        "at": getattr(record, timestamp),
                    }
                )
    return build_behavior(
        values,
        cutoff=cutoff,
        min_jobs=current_app.config["BEHAVIOR_MIN_JOBS"],
        min_actions=current_app.config["BEHAVIOR_MIN_ACTIONS"],
    )


def behavior_score(profile, job):
    if not profile or not profile["enabled"]:
        return 50.0
    preferences = profile["preferences"]
    values = []
    for key, terms in [
        ("roles", [job.job_title]),
        ("locations", [job.location]),
        ("skills", normalize_skills(job.required_skills)),
        ("employment_types", [job.employment_type]),
        ("remote_modes", [job.remote_type or "unknown"]),
    ]:
        counter = preferences[key]
        scale = max([abs(v) for v in counter.values()] + [1.0])
        signals = [counter.get(str(term).casefold(), 0) / scale for term in terms]
        values.append(sum(signals) / len(signals) if signals else 0.0)
    return max(0.0, min(100.0, 50 + 50 * sum(values) / len(values)))
