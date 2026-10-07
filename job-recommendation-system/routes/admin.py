from datetime import date
from uuid import uuid4
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.database import db, User, Job
from routes.auth import admin_required
from routes.control import page_query
from services.security_service import audit
from services.notification_service import saved_job_updated
from services.analytics_service import admin_analytics
from services.data_service import clean_job_rows
from utils.constants import EMPLOYMENT_TYPES
from utils.validators import (
    text_field,
    number_field,
    ValidationError,
    choice_field,
    CURRENCIES,
)

admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.get("/")
@admin_required
def dashboard():
    return render_template("admin/dashboard.html", data=admin_analytics())


@admin.get("/jobs")
@admin_required
def listing():
    query = request.args.get("q", "").strip()[:160]
    statement = db.select(Job)
    if query:
        statement = statement.where(
            db.or_(
                Job.job_title.icontains(query, autoescape=True),
                Job.company_name.icontains(query, autoescape=True),
            )
        )
    source = request.args.get("source")
    if source == "external":
        statement = statement.where(Job.is_external.is_(True))
    elif source == "demo":
        statement = statement.where(Job.is_synthetic.is_(True))
    state = request.args.get("state")
    if state in {"archived", "deleted"}:
        statement = statement.where(getattr(Job, state).is_(True))
    result = page_query(statement.order_by(Job.id.desc()), 20)
    return render_template("admin/jobs.html", records=result.items, page=result)


def job_form(job=None):
    if request.method == "POST":
        try:
            for key, maximum in [
                ("job_title", 160),
                ("company_name", 160),
                ("job_description", 12000),
                ("location", 100),
                ("industry", 80),
                ("education", 160),
            ]:
                text_field(
                    request.form,
                    key,
                    maximum,
                    key in {"job_title", "company_name", "job_description"},
                )
            number_field(request.form, "salary_min", 100000000, True)
            number_field(request.form, "salary_max", 100000000, True)
            # Validate explicit admin ranges instead of silently repairing data entry.
            lower = number_field(request.form, "salary_min", 100000000, True)
            upper = number_field(request.form, "salary_max", 100000000, True)
            if lower is not None and upper is not None and upper < lower:
                raise ValidationError(
                    "Maximum salary must not be below minimum salary."
                )
            if (
                len(request.form.get("required_skills", "")) > 6000
                or len(request.form.get("preferred_skills", "")) > 6000
            ):
                raise ValidationError(
                    "Each skills list must be at most 6000 characters."
                )
            raw = request.form.to_dict()
            raw["is_synthetic"] = (
                "true" if request.form.get("is_synthetic") == "on" else "false"
            )
            cleaned, errors = clean_job_rows([raw])
            if errors or not cleaned:
                raise ValidationError(
                    errors[0]["error"] if errors else "Check the job fields."
                )
            fields = cleaned[0]
            fields.pop("source_id")
            fields["salary_currency"] = choice_field(
                request.form,
                "salary_currency",
                CURRENCIES,
                job.salary_currency if job else "INR",
            )
            fields["salary_period"] = choice_field(
                request.form,
                "salary_period",
                {"year", "month", "week", "day", "hour", "unknown"},
                job.salary_period if job else "year",
            )
            fields["remote_type"] = choice_field(
                request.form,
                "remote_type",
                {"unknown", "remote", "onsite", "hybrid"},
                "remote" if fields["location"].casefold() == "remote" else "unknown",
            )
            fields["remote_allowed"] = fields["remote_type"] == "remote"
            fields["freshness_override"] = choice_field(
                request.form,
                "freshness_override",
                {"auto", "Older listing", "Possibly expired"},
                "auto",
            )
            if not job or not job.is_external:
                fields["source"] = "demo" if fields["is_synthetic"] else "manual"
                fields["source_name"] = (
                    "Demo" if fields["is_synthetic"] else "Local employer entry"
                )
            else:
                fields["is_synthetic"] = False

        except (ValidationError, ValueError) as exc:
            flash(str(exc), "error")
            return render_template(
                "admin/job_form.html",
                job=job,
                types=EMPLOYMENT_TYPES,
                today=date.today(),
            ), 400
        if job is None:
            job = Job(source_id="ADMIN-" + str(uuid4()))
            db.session.add(job)
        for key, value in fields.items():
            setattr(job, key, value)
        job.active = request.form.get("active") == "on"
        db.session.flush()
        audit("job_saved", subject_type="job", subject_id=job.id)
        saved_job_updated(job)
        db.session.commit()
        flash(
            "Job saved. Model features refresh automatically when listing text changes.",
            "success",
        )
        return redirect(url_for("admin.listing"))
    return render_template(
        "admin/job_form.html", job=job, types=EMPLOYMENT_TYPES, today=date.today()
    )


@admin.route("/jobs/new", methods=["GET", "POST"])
@admin_required
def create_job():
    return job_form()


@admin.route("/jobs/<int:job_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_job(job_id):
    return job_form(db.get_or_404(Job, job_id))


@admin.post("/jobs/<int:job_id>/delete")
@admin_required
def delete_job(job_id):
    # Soft deletion preserves application and historical recommendation integrity.
    job = db.get_or_404(Job, job_id)
    job.active = False
    job.deleted = True
    audit("job_deleted", subject_type="job", subject_id=job.id)
    db.session.commit()
    flash(
        "Job removed from active listings. Existing tracker and history records are retained.",
        "success",
    )
    return redirect(url_for("admin.listing"))


@admin.get("/users")
@admin_required
def users():
    page = page_query(
        db.select(User).where(User.is_admin.is_(False)).order_by(User.created_at.desc())
    )
    return render_template("admin/users.html", records=page.items, page=page)
