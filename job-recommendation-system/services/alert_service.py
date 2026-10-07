"""Explicit worker entry point; reads cached/local jobs, never polls APIs implicitly."""

from datetime import timedelta
from uuid import uuid4
from flask import current_app
from models.database import db, User, Job, JobAlert, JobAlertDelivery, utcnow
from services.job_catalog import job_query
from services.recommendation_service import recommendations
from services.notification_service import notify_user
from services.mail_service import send_mail
from services.security_service import audit


def process_due_alerts(limit=100):
    now = utcnow()
    ids = db.session.scalars(
        db.select(JobAlert.id)
        .where(JobAlert.enabled.is_(True), JobAlert.next_run_at <= now)
        .order_by(JobAlert.next_run_at)
        .limit(limit)
    ).all()
    processed = 0
    for alert_id in ids:
        lease = uuid4().hex
        won = db.session.execute(
            db.update(JobAlert)
            .where(
                JobAlert.id == alert_id,
                JobAlert.enabled.is_(True),
                JobAlert.next_run_at <= now,
                db.or_(JobAlert.lock_until.is_(None), JobAlert.lock_until < now),
            )
            .values(lock_token=lease, lock_until=now + timedelta(minutes=10))
        ).rowcount
        db.session.commit()
        if not won:
            continue
        alert = db.session.get(JobAlert, alert_id)
        user = db.session.get(User, alert.user_id)
        if not user or not user.is_active:
            alert.next_run_at = now + timedelta(days=1)
            alert.lock_until = alert.lock_token = None
            db.session.commit()
            continue
        statement = (
            job_query(alert.filters)
            .where(Job.first_seen_at >= alert.created_at)
            .order_by(Job.first_seen_at.desc(), Job.id)
            .limit(current_app.config["MAX_RANKING_JOBS"])
        )
        rows = recommendations(user, jobs=db.session.scalars(statement).all())
        matches = [
            r["job"]
            for r in rows
            if r["score"] >= (alert.filters.get("min_match") or 0)
        ][:50]
        for job in matches:
            delivery = db.session.scalar(
                db.select(JobAlertDelivery).where(
                    JobAlertDelivery.alert_id == alert.id,
                    JobAlertDelivery.job_id == job.id,
                )
            )
            if not delivery:
                db.session.add(JobAlertDelivery(alert_id=alert.id, job_id=job.id))
                notify_user(
                    user.id,
                    "new_job",
                    "New match: " + job.job_title[:120],
                    f"{job.company_name} · {job.source_name}. Matched your {alert.name} alert.",
                    f"/jobs/{job.id}",
                    f"alert:{alert.id}:{job.id}",
                )
        db.session.commit()
        pending = db.session.execute(
            db.select(JobAlertDelivery, Job)
            .join(Job, Job.id == JobAlertDelivery.job_id)
            .where(
                JobAlertDelivery.alert_id == alert.id,
                JobAlertDelivery.email_sent.is_(False),
            )
            .order_by(JobAlertDelivery.id)
            .limit(50)
        ).all()
        # Single worker lease prevents concurrent duplicate sends. SMTP cannot promise
        # exactly-once delivery if a worker crashes after send but before DB commit.
        failed = False
        if pending and alert.email_enabled and user.email_verified_at:
            base = current_app.config["APP_BASE_URL"].rstrip("/")
            body = (
                "New jobs for your JobMatch alert:\n\n"
                + "\n".join(
                    f"{job.job_title} — {job.company_name} ({job.source_name})\n{base}/jobs/{job.id}"
                    for _, job in pending
                )
                + f"\n\nManage alerts: {base}/alerts"
            )
            if send_mail(user.email, "New jobs for your JobMatch alert", body):
                for delivery, _ in pending:
                    delivery.email_sent = True
            else:
                failed = True
        alert.last_run_at = now
        alert.next_run_at = now + (
            timedelta(minutes=30)
            if failed
            else timedelta(days=7 if alert.frequency == "weekly" else 1)
        )
        alert.last_error = (
            "Email delivery unavailable; retry scheduled." if failed else ""
        )
        alert.lock_until = alert.lock_token = None
        audit(
            "alert_processed",
            actor_id=user.id,
            subject_type="alert",
            subject_id=alert.id,
            details={"matches": len(matches), "email_failed": failed},
        )
        db.session.commit()
        processed += 1
    return processed
