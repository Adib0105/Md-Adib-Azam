"""Candidate-owned alerts, notifications, tracker details and resume comparison."""

import re
from flask import (
    Blueprint,
    g,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    abort,
    jsonify,
)
from models.database import (
    db,
    JobAlert,
    JobAlertDelivery,
    Notification,
    Application,
    utcnow,
)
from routes.auth import login_required
from routes.jobs import visible_job
from services.job_catalog import parse_filters
from services.recommendation_service import engine
from models.skill_extractor import extract_skills
from services.security_service import rate_limit, audit
from utils.validators import (
    text_field,
    choice_field,
    date_field,
    safe_external_url,
    ValidationError,
)
from utils.constants import APPLICATION_STATUSES

workspace = Blueprint("workspace", __name__)


def owned(model, identity):
    result = db.session.scalar(
        db.select(model).where(model.id == identity, model.user_id == g.user.id)
    )
    if not result:
        abort(404)
    return result


@workspace.get("/notifications")
@login_required
def notifications():
    records = db.session.scalars(
        db.select(Notification)
        .where(Notification.user_id == g.user.id)
        .order_by(Notification.id.desc())
        .limit(100)
    ).all()
    return render_template("notifications.html", records=records)


@workspace.get("/api/notifications")
@login_required
def api_notifications():
    records = db.session.scalars(
        db.select(Notification)
        .where(Notification.user_id == g.user.id)
        .order_by(Notification.id.desc())
        .limit(100)
    ).all()
    return jsonify(
        items=[
            {
                "id": n.id,
                "title": n.title,
                "message": n.message,
                "link": n.link,
                "read": bool(n.read_at),
            }
            for n in records
        ]
    )


@workspace.post("/notifications/<int:notification_id>/read")
@login_required
def read_notification(notification_id):
    owned(Notification, notification_id).read_at = utcnow()
    db.session.commit()
    return redirect(url_for("workspace.notifications"))


@workspace.route("/alerts", methods=["GET", "POST"])
@login_required
def alerts():
    if request.method == "POST":
        rate_limit("alerts_create", 20, 3600, str(g.user.id))
        try:
            if (
                db.session.scalar(
                    db.select(db.func.count(JobAlert.id)).where(
                        JobAlert.user_id == g.user.id
                    )
                )
                >= 10
            ):
                raise ValidationError("You can have up to 10 job alerts.")
            name = text_field(request.form, "name", 100, True)
            filters = parse_filters(request.form)
            frequency = choice_field(
                request.form, "frequency", {"daily", "weekly"}, "daily"
            )
            email_enabled = request.form.get("email_enabled") == "on"
            if email_enabled and not g.user.email_verified_at:
                raise ValidationError(
                    "Verify your email in Account settings before enabling email alerts."
                )
            db.session.add(
                JobAlert(
                    user_id=g.user.id,
                    name=name,
                    filters=filters,
                    frequency=frequency,
                    email_enabled=email_enabled,
                )
            )
            audit("alert_created")
            db.session.commit()
            flash(
                "Alert created. The scheduled worker will check newly added jobs.",
                "success",
            )
        except ValidationError as exc:
            flash(str(exc), "error")
            return render_template(
                "alerts.html",
                records=db.session.scalars(
                    db.select(JobAlert).where(JobAlert.user_id == g.user.id)
                ).all(),
            ), 400
        return redirect(url_for("workspace.alerts"))
    records = db.session.scalars(
        db.select(JobAlert)
        .where(JobAlert.user_id == g.user.id)
        .order_by(JobAlert.id.desc())
    ).all()
    return render_template("alerts.html", records=records)


@workspace.post("/alerts/<int:alert_id>/<action>")
@login_required
def change_alert(alert_id, action):
    alert = owned(JobAlert, alert_id)
    if action == "delete":
        db.session.execute(
            db.delete(JobAlertDelivery).where(JobAlertDelivery.alert_id == alert.id)
        )
        db.session.delete(alert)
    elif action == "toggle":
        alert.enabled = not alert.enabled
    else:
        abort(404)
    audit("alert_" + action, subject_type="alert", subject_id=alert_id)
    db.session.commit()
    return redirect(url_for("workspace.alerts"))


@workspace.post("/applications/<int:application_id>/details")
@login_required
def application_details(application_id):
    record = owned(Application, application_id)
    try:
        values = {
            "notes": text_field(request.form, "notes", 5000),
            "company_contact": text_field(request.form, "company_contact", 254),
            "application_date": date_field(request.form, "application_date"),
            "follow_up_date": date_field(request.form, "follow_up_date"),
            "application_url": safe_external_url(
                request.form.get("application_url", "")
            ),
            "status": choice_field(
                request.form, "status", set(APPLICATION_STATUSES), record.status
            ),
        }
    except ValidationError as exc:
        abort(400, description=str(exc))
    for key, value in values.items():
        setattr(record, key, value)
    db.session.commit()
    flash("Application details saved.", "success")
    return redirect(url_for("candidate.applications"))


@workspace.get("/resume/compare/<int:job_id>")
@login_required
def compare_resume(job_id):
    job = visible_job(job_id)
    if not g.user.resume_text:
        flash(
            "Upload and review a resume first, then compare it with this job.", "info"
        )
        return redirect(url_for("candidate.profile"))
    skills = extract_skills(g.user.resume_text)
    required = job.required_skills
    matched = [s for s in required if s.casefold() in {v.casefold() for v in skills}]
    missing = [s for s in required if s not in matched]
    from models.recommendation_model import calculate_semantic_similarity

    vectorizer, matrix, _, _ = engine().features_for([job])
    similarity = round(
        float(
            calculate_semantic_similarity(
                vectorizer.transform([g.user.resume_text]), matrix
            )[0]
        ),
        1,
    )
    coverage = round(100 * len(matched) / len(required), 1) if required else None
    score = (
        round(0.7 * coverage + 0.3 * similarity, 1)
        if coverage is not None
        else similarity
    )
    suggestions = [
        "Add measurable outcomes to projects: scale, time saved, accuracy or users served.",
        "Connect relevant experience to the duties in the original listing.",
    ]
    if missing:
        suggestions.append(
            "If you have used these skills, describe specific examples: "
            + ", ".join(missing[:6])
            + ". Do not add skills you cannot demonstrate."
        )
    if not re.search(r"\d+\s*(%|users|hours|records)", g.user.resume_text, re.I):
        suggestions.append(
            "Your reviewed resume contains few measurable results; include a truthful metric where useful."
        )
    return render_template(
        "resume_compare.html",
        job=job,
        matched=matched,
        missing=missing,
        score=score,
        coverage=coverage,
        similarity=similarity,
        suggestions=suggestions,
    )
