"""Administrator control center; no credential values enter templates or exports."""

import csv
import io
import re
from pathlib import Path
from flask import (
    Blueprint,
    g,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    abort,
    current_app,
    Response,
    jsonify,
    send_file,
)
from models.database import (
    db,
    User,
    Job,
    Application,
    SavedJob,
    SearchEvent,
    JobProvider,
    ExternalJobCache,
    AuditLog,
    Recommendation,
    RecommendationRun,
    utcnow,
)
from routes.auth import admin_required
from services.security_service import audit, revoke_sessions, rate_limit
from services.job_providers.provider_registry import provider_summaries, PROVIDERS
from services.external_jobs_service import live_search
from services.job_catalog import parse_filters
from services.settings_service import (
    content,
    update_content,
    weights,
    put_setting,
    setting,
)
from services.mail_service import mail_status
from services.schema_service import sqlite_backup
from config import validate_weights
from utils.validators import ValidationError, number_field

control = Blueprint("control", __name__, url_prefix="/admin")


def page_query(statement, per_page=30):
    try:
        page = max(1, min(int(request.args.get("page", 1)), 10000))
    except ValueError:
        abort(400, description="Page must be a whole number.")
    return db.paginate(statement, page=page, per_page=per_page, error_out=False)


@control.get("/providers")
@admin_required
def providers():
    return render_template(
        "admin/providers.html", providers=provider_summaries(private=True)
    )


@control.post("/providers/<slug>/<action>")
@admin_required
def provider_action(slug, action):
    if slug not in PROVIDERS:
        abort(404)
    rate_limit("admin_provider", 30, 3600)
    state = db.get_or_404(JobProvider, slug)
    message = "Provider updated."
    if action in {"enable", "disable"}:
        state.enabled = action == "enable"
    elif action == "clear-cache":
        db.session.execute(
            db.delete(ExternalJobCache).where(
                ExternalJobCache.provider == slug,
                db.or_(
                    ExternalJobCache.lock_until.is_(None),
                    ExternalJobCache.lock_until < utcnow(),
                ),
            )
        )
        message = (
            "Search cache cleared; stored listings and tracker records are retained."
        )
    elif action in {"sync", "test"}:
        try:
            filters = parse_filters(request.form)
        except ValidationError as exc:
            abort(400, description=str(exc))
        if action == "test":
            filters.update(
                q="data", per_page=1, country="us" if slug == "usajobs" else "in"
            )
        result = live_search(slug, filters, force=True)
        message = result["message"]
    else:
        abort(404)
    audit("provider_" + action, subject_type="provider", subject_id=slug)
    db.session.commit()
    flash(message, "info")
    return redirect(url_for("control.providers"))


JOB_ACTIONS = {
    "archive",
    "restore",
    "delete",
    "publish",
    "unpublish",
    "feature",
    "unfeature",
    "verify",
    "unverify",
    "activate",
}


def apply_job_action(job, action):
    if action == "archive":
        job.archived = True
    elif action == "delete":
        job.deleted, job.active = True, False
    elif action in {"restore", "activate"}:
        job.deleted, job.archived, job.active, job.published = False, False, True, True
    elif action in {"publish", "unpublish"}:
        job.published = action == "publish"
    elif action in {"feature", "unfeature"}:
        job.featured = action == "feature"
    elif action in {"verify", "unverify"}:
        job.verified = action == "verify"


@control.post("/jobs/<int:job_id>/action")
@admin_required
def job_action(job_id):
    job = db.get_or_404(Job, job_id)
    action = request.form.get("action")
    if action not in JOB_ACTIONS:
        abort(400)
    apply_job_action(job, action)
    audit("job_" + action, subject_type="job", subject_id=job_id)
    db.session.commit()
    return redirect(url_for("admin.listing"))


@control.post("/jobs/bulk")
@admin_required
def bulk_jobs():
    raw = request.form.getlist("job_ids")
    if not raw or len(raw) > 200 or any(not re.fullmatch(r"\d{1,10}", s) for s in raw):
        abort(400, description="Select 1–200 valid jobs.")
    action = request.form.get("action")
    if action not in {"archive", "delete", "activate", "export"}:
        abort(400)
    records = db.session.scalars(
        db.select(Job).where(Job.id.in_([int(s) for s in raw])).order_by(Job.id)
    ).all()
    audit("jobs_bulk_" + action, details={"count": len(records)})
    if action == "export":
        stream = io.StringIO(newline="")
        writer = csv.writer(stream)
        writer.writerow(
            ["id", "title", "company", "location", "source", "salary", "url"]
        )

        def cell(value):
            value = str(value)
            return (
                "'" + value
                if value.lstrip().startswith(("=", "+", "-", "@", "\t", "\r"))
                else value
            )

        for job in records:
            writer.writerow(
                [
                    cell(v)
                    for v in [
                        job.id,
                        job.job_title,
                        job.company_name,
                        job.location,
                        job.source_name,
                        job.salary_display,
                        job.source_url,
                    ]
                ]
            )
        db.session.commit()
        return Response(
            stream.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=jobmatch-jobs.csv"},
        )
    for job in records:
        apply_job_action(job, action)
    db.session.commit()
    flash(f"Updated {len(records)} jobs.", "success")
    return redirect(url_for("admin.listing"))


@control.post("/users/<int:user_id>/status")
@admin_required
def user_status(user_id):
    user = db.get_or_404(User, user_id)
    if user.is_admin or user.id == g.user.id:
        abort(
            400,
            description="Administrator accounts are managed with the secure setup command.",
        )
    action = request.form.get("action")
    if action not in {"suspend", "activate"}:
        abort(400)
    user.is_active = action == "activate"
    revoke_sessions(user)
    audit("user_" + action, subject_type="user", subject_id=user_id)
    db.session.commit()
    return redirect(url_for("admin.users"))


@control.get("/applications")
@admin_required
def applications():
    records = page_query(db.select(Application).order_by(Application.updated_at.desc()))
    return render_template(
        "admin/records.html",
        title="Application activity",
        kind="applications",
        page=records,
    )


@control.get("/analytics")
@admin_required
def analytics():
    from services.analytics_service import chart

    count = db.func.count(SearchEvent.id)

    def groups(column, clause):
        return db.session.execute(
            db.select(column, count)
            .where(clause)
            .group_by(column)
            .order_by(count.desc())
            .limit(10)
        ).all()

    charts = {
        "Top searches": chart("bar", groups(SearchEvent.query, db.true())),
        "Zero-result searches": chart(
            "bar", groups(SearchEvent.query, SearchEvent.result_count == 0)
        ),
        "Searched locations": chart(
            "bar", groups(SearchEvent.location, SearchEvent.location != "")
        ),
    }
    for name, column in [
        ("Top companies", Job.company_name),
        ("Popular roles", Job.job_title),
    ]:
        charts[name] = chart(
            "bar",
            db.session.execute(
                db.select(column, db.func.count(Job.id))
                .where(Job.deleted.is_(False))
                .group_by(column)
                .order_by(db.func.count(Job.id).desc())
                .limit(8)
            ).all(),
        )
    return render_template(
        "admin/analytics.html",
        charts=charts,
        average=round(
            db.session.scalar(db.select(db.func.avg(Recommendation.overall_score)))
            or 0,
            1,
        ),
        runs=db.session.scalar(db.select(db.func.count(RecommendationRun.id))),
    )


@control.route("/content", methods=["GET", "POST"])
@admin_required
def cms():
    if request.method == "POST":
        try:
            update_content(request.form)
        except ValidationError as exc:
            abort(400, description=str(exc))
        audit("content_updated")
        db.session.commit()
        flash("Public content updated.", "success")
        return redirect(url_for("control.cms"))
    return render_template("admin/content.html", content=content())


@control.route("/settings", methods=["GET", "POST"])
@admin_required
def settings():
    if request.method == "POST":
        try:
            values = {k: float(request.form.get("weight_" + k, "")) for k in weights()}
            validate_weights(values)
            limits = {
                "real_job_cache_ttl_minutes": (1, 1440),
                "external_job_stale_days": (1, 90),
                "external_job_max_age_days": (1, 365),
            }
            parsed = {}
            for key, (minimum, maximum) in limits.items():
                parsed[key] = number_field(request.form, key, maximum, True)
                if parsed[key] is None or parsed[key] < minimum:
                    raise ValidationError(f"{key} must be {minimum}–{maximum}.")
            put_setting("recommendation_weights", values)
            for key, value in parsed.items():
                put_setting(key, value)
        except (ValueError, TypeError) as exc:
            db.session.rollback()
            abort(400, description=str(exc))
        audit("settings_updated")
        db.session.commit()
        flash("Matching weights and cache settings updated.", "success")
        return redirect(url_for("control.settings"))
    return render_template(
        "admin/settings.html",
        weights=weights(),
        settings={
            key: setting(key)
            for key in [
                "real_job_cache_ttl_minutes",
                "external_job_stale_days",
                "external_job_max_age_days",
            ]
        },
    )


@control.get("/security")
@control.get("/audit")
@admin_required
def security():
    statement = db.select(AuditLog).order_by(AuditLog.id.desc())
    if request.args.get("action"):
        statement = statement.where(AuditLog.action == request.args["action"][:80])
    return render_template(
        "admin/records.html",
        title="Security & audit log",
        kind="audit",
        page=page_query(statement),
    )


@control.get("/health")
@control.get("/email")
@admin_required
def health():
    db.session.execute(db.text("SELECT 1"))
    counts = {
        "Database": "Connected",
        "Environment": current_app.config["APP_ENV"],
        "Search cache entries": db.session.scalar(
            db.select(db.func.count(ExternalJobCache.key))
        ),
        "Provider failures": db.session.scalar(
            db.select(db.func.sum(JobProvider.failures))
        )
        or 0,
        "Password reset requests": db.session.scalar(
            db.select(db.func.count(AuditLog.id)).where(
                AuditLog.action == "password_reset_requested"
            )
        ),
        "Active candidates": db.session.scalar(
            db.select(db.func.count(User.id)).where(
                User.is_active.is_(True), User.is_admin.is_(False)
            )
        ),
        "Saved jobs": db.session.scalar(db.select(db.func.count(SavedJob.id))),
    }
    return render_template(
        "admin/health.html",
        metrics=counts,
        mail=mail_status(),
        providers=provider_summaries(private=True),
    )


@control.route("/backups", methods=["GET", "POST"])
@admin_required
def backups():
    if request.method == "POST":
        rate_limit("backup", 5, 3600, str(g.user.id))
        if not g.user.check_password(request.form.get("current_password", "")):
            abort(400, description="Current administrator password is required.")
        try:
            target = sqlite_backup()
        except ValueError as exc:
            abort(400, description=str(exc))
        audit("backup_created", details={"name": target.name})
        db.session.commit()
        flash("Private database backup created.", "success")
        return redirect(url_for("control.backups"))
    folder = Path(current_app.instance_path) / "backups"
    files = sorted(
        [p.name for p in folder.glob("*.sqlite") if p.is_file()], reverse=True
    )[:30]
    return render_template("admin/backups.html", files=files)


@control.post("/backups/download")
@admin_required
def download_backup():
    rate_limit("backup_download", 10, 3600, str(g.user.id))
    if not g.user.check_password(request.form.get("current_password", "")):
        abort(400, description="Current administrator password is required.")
    name = request.form.get("filename", "")
    if not re.fullmatch(r"(?:backup|upgrade-v2)-\d{8}T\d{6}-[a-f0-9]{8}\.sqlite", name):
        abort(400)
    path = Path(current_app.instance_path) / "backups" / name
    if not path.is_file() or path.is_symlink():
        abort(404)
    audit("backup_downloaded", details={"name": name})
    db.session.commit()
    return send_file(
        path,
        as_attachment=True,
        download_name=name,
        mimetype="application/octet-stream",
    )


admin_api = Blueprint("admin_api", __name__, url_prefix="/api/admin")


@admin_api.get("/providers/health")
@admin_required
def api_provider_health():
    return jsonify(providers=provider_summaries(private=True))


@admin_api.get("/analytics")
@admin_required
def api_analytics():
    def count(model):
        return db.session.scalar(db.select(db.func.count()).select_from(model)) or 0

    return jsonify(
        users=count(User),
        jobs=count(Job),
        real_jobs=db.session.scalar(
            db.select(db.func.count(Job.id)).where(Job.is_external.is_(True))
        ),
        saved=count(SavedJob),
        applications=count(Application),
        recommendation_runs=count(RecommendationRun),
        average_match=round(
            db.session.scalar(db.select(db.func.avg(Recommendation.overall_score)))
            or 0,
            1,
        ),
        searches=count(SearchEvent),
    )
