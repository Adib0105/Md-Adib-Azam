"""Feedback records contain IDs and actions, never resume text or credentials."""

from models.database import db
from models.ml_data import InteractionEvent
from ml.features.behavior import ACTION_WEIGHTS


def record_interaction(user, job_id, action, origin="explicit"):
    if action not in ACTION_WEIGHTS:
        raise ValueError("Unsupported feedback action.")
    db.session.add(
        InteractionEvent(user_id=user.id, job_id=job_id, action=action, origin=origin)
    )


def record_application_status(user, record):
    action = {
        "Interview": "interview",
        "Offer": "offer",
        "Rejected": "outcome_rejected",
    }.get(record.status)
    if action:
        # Employer rejection is an outcome, not evidence that the user dislikes a role.
        record_interaction(user, record.job_id, action, "application_status")
