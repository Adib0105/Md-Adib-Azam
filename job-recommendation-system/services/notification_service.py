"""Owner-scoped, deduplicated notifications; no external messages on page render."""

from datetime import date
from sqlalchemy.exc import IntegrityError
from models.database import db, Notification, Application, SavedJob, utcnow


def notify_user(user_id, kind, title, message, link, key):
    if not link.startswith("/") or link.startswith("//"):
        link = "/dashboard"
    exists = db.session.scalar(
        db.select(Notification.id).where(
            Notification.user_id == user_id, Notification.dedupe_key == key
        )
    )
    if exists:
        return None
    try:
        with db.session.begin_nested():
            item = Notification(
                user_id=user_id,
                kind=kind,
                title=title[:160],
                message=message[:600],
                link=link[:250],
                dedupe_key=key[:180],
            )
            db.session.add(item)
            db.session.flush()
        return item
    except IntegrityError:
        return None


def account_notices(user, gaps=None):
    from services.recommendation_service import profile_completion

    completion = profile_completion(user)
    if completion["percent"] < 70:
        notify_user(
            user.id,
            "profile",
            "A clearer profile means clearer matches",
            f"Your profile is {completion['percent']}% complete. Add your experience, preferences and skills.",
            "/profile",
            "profile-incomplete",
        )
    if gaps:
        name, count = gaps[0]
        notify_user(
            user.id,
            "skill",
            "One skill to explore",
            f"{name} appears in {count} of your strongest opportunities. Try it in the career simulator.",
            "/simulator",
            f"skill:{name}:{utcnow():%Y-%m}",
        )
    records = db.session.scalars(
        db.select(Application)
        .where(
            Application.user_id == user.id,
            Application.follow_up_date <= date.today(),
            Application.status.not_in(["Rejected", "Withdrawn", "Offer"]),
        )
        .limit(100)
    ).all()
    for row in records:
        notify_user(
            user.id,
            "reminder",
            "Application follow-up due",
            f"Review your next step for {row.job.job_title} at {row.job.company_name}.",
            "/applications",
            f"followup:{row.id}:{row.follow_up_date}",
        )
    db.session.commit()


def saved_job_updated(job):
    ids = db.session.scalars(
        db.select(SavedJob.user_id).where(SavedJob.job_id == job.id)
    ).yield_per(100)
    for user_id in ids:
        notify_user(
            user_id,
            "saved_job",
            "A saved job was updated",
            f"Review the latest details for {job.job_title} at {job.company_name}.",
            f"/jobs/{job.id}",
            f"job-update:{job.id}:{utcnow():%Y-%m-%d}",
        )
