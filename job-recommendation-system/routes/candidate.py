from collections import Counter
from datetime import timedelta
from uuid import uuid4
from flask import (
    Blueprint,
    g,
    request,
    render_template,
    redirect,
    url_for,
    flash,
    abort,
)
from models.database import (
    db,
    CandidateSkill,
    SavedJob,
    Application,
    ResumeDraft,
    utcnow,
)
from models.resume_parser import parse_resume, ResumeError
from models.skill_extractor import SKILLS
from routes.auth import login_required
from services.recommendation_service import recommendations, snapshot, active_jobs
from services.analytics_service import career_paths, skill_analytics
from utils.constants import EMPLOYMENT_TYPES, APPLICATION_STATUSES, PROFICIENCIES
from utils.validators import (
    validate_profile,
    validate_skills,
    number_field,
    text_field,
    ValidationError,
)

candidate = Blueprint("candidate", __name__)


def replace_skills(user, skills, form=None):
    existing = {skill.skill_name: skill.proficiency_level for skill in user.skills}
    # Flush removals before reinserting to satisfy (user_id, skill_name) uniqueness.
    user.skills.clear()
    db.session.flush()
    for name in skills:
        level = (form or {}).get(f"level_{name}", existing.get(name, "Intermediate"))
        if level not in PROFICIENCIES:
            level = "Intermediate"
        user.skills.append(CandidateSkill(skill_name=name, proficiency_level=level))


@candidate.get("/")
def index():
    jobs = active_jobs()
    categories = Counter(job.job_title for job in jobs)
    return render_template(
        "index.html", total_jobs=len(jobs), categories=categories.most_common(8)
    )


@candidate.get("/dashboard")
@login_required
def dashboard():
    rows = recommendations(g.user)
    saved = db.session.scalars(
        db.select(SavedJob).where(SavedJob.user_id == g.user.id)
    ).all()
    applications = db.session.scalars(
        db.select(Application).where(Application.user_id == g.user.id)
    ).all()
    skills = skill_analytics(g.user, rows)
    counts = Counter(a.status for a in applications)
    return render_template(
        "dashboard.html",
        rows=rows[:4],
        total=len(rows),
        best=rows[0]["score"] if rows else 0,
        saved_ids={s.job_id for s in saved},
        application_ids={a.job_id for a in applications},
        saved_count=len(saved),
        application_count=len(applications),
        paths=career_paths(rows)[:4],
        gaps=skills["gaps"][:4],
        demand=skills["demand"][:5],
        recent=sorted(
            [r["job"] for r in rows], key=lambda j: j.posted_date, reverse=True
        )[:3],
        charts={
            "Applications": {
                "type": "doughnut",
                "labels": list(counts),
                "values": list(counts.values()),
            }
        },
    )


@candidate.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        try:
            fields, skills = validate_profile(request.form)
        except ValidationError as exc:
            flash(str(exc), "error")
            return render_template(
                "profile.html",
                skill_dictionary=SKILLS,
                employment_types=EMPLOYMENT_TYPES,
                levels=PROFICIENCIES,
            ), 400
        for field, value in fields.items():
            setattr(g.user, field, value)
        replace_skills(g.user, skills, request.form)
        db.session.commit()
        snapshot(g.user, "Profile updated")
        flash("Profile saved and recommendations recalculated.", "success")
        return redirect(url_for("candidate.profile"))
    return render_template(
        "profile.html",
        skill_dictionary=SKILLS,
        employment_types=EMPLOYMENT_TYPES,
        levels=PROFICIENCIES,
    )


@candidate.post("/resume/upload")
@login_required
def upload_resume():
    upload = request.files.get("resume")
    try:
        if not upload:
            raise ResumeError("Choose a PDF or DOCX file first.")
        extracted = parse_resume(upload.filename, upload.read(5 * 1024 * 1024 + 1))
    except ResumeError as exc:
        flash(str(exc), "error")
        return redirect(url_for("candidate.profile"))
    db.session.execute(
        db.delete(ResumeDraft).where(
            db.or_(
                ResumeDraft.user_id == g.user.id,
                ResumeDraft.created_at < utcnow() - timedelta(hours=1),
            )
        )
    )
    draft = ResumeDraft(
        id=str(uuid4()),
        user_id=g.user.id,
        filename=extracted.pop("filename"),
        extracted=extracted,
    )
    db.session.add(draft)
    db.session.commit()
    return redirect(url_for("candidate.review_resume", draft_id=draft.id))


@candidate.route("/resume/review/<draft_id>", methods=["GET", "POST"])
@login_required
def review_resume(draft_id):
    draft = db.session.scalar(
        db.select(ResumeDraft).where(
            ResumeDraft.id == draft_id,
            ResumeDraft.user_id == g.user.id,
            ResumeDraft.created_at >= utcnow() - timedelta(hours=1),
        )
    )
    if not draft:
        abort(404)
    if request.method == "POST":
        if request.form.get("action") == "discard":
            db.session.delete(draft)
            db.session.commit()
            flash("Resume draft discarded.", "success")
            return redirect(url_for("candidate.profile"))
        try:
            skills = validate_skills(request.form.get("skills", ""))
            fields = {
                field: text_field(request.form, field, maximum)
                for field, maximum in {
                    "education": 180,
                    "preferred_role": 160,
                    "certifications": 5000,
                    "projects": 5000,
                    "experience_summary": 5000,
                }.items()
            }
            experience = number_field(request.form, "experience_years", 60)
            resume_text = text_field(request.form, "resume_text", 50000)
        except ValidationError as exc:
            flash(str(exc), "error")
            return render_template("resume_review.html", draft=draft), 400
        replace_skills(g.user, skills)
        for field, value in fields.items():
            setattr(g.user, field, value)
        g.user.experience_years = experience
        g.user.resume_text = resume_text
        g.user.resume_filename = draft.filename
        db.session.delete(draft)
        db.session.commit()
        snapshot(g.user, "Resume confirmed")
        flash(
            "Reviewed resume details saved. You can edit them in your profile.",
            "success",
        )
        return redirect(url_for("candidate.profile"))
    return render_template("resume_review.html", draft=draft)


@candidate.post("/resume/remove")
@login_required
def remove_resume():
    g.user.resume_text, g.user.resume_filename = "", ""
    db.session.execute(db.delete(ResumeDraft).where(ResumeDraft.user_id == g.user.id))
    db.session.commit()
    snapshot(g.user, "Resume removed")
    flash(
        "Stored resume text removed. Reviewed profile fields remain editable.",
        "success",
    )
    return redirect(url_for("candidate.profile"))


@candidate.get("/applications")
@login_required
def applications():
    records = db.session.scalars(
        db.select(Application)
        .where(Application.user_id == g.user.id)
        .order_by(Application.applied_date.desc())
    ).all()
    scores = {row["job"].id: row["score"] for row in recommendations(g.user)}
    return render_template(
        "applications.html",
        records=records,
        scores=scores,
        statuses=APPLICATION_STATUSES,
    )


@candidate.post("/applications/<int:application_id>/status")
@login_required
def update_status(application_id):
    record = db.session.scalar(
        db.select(Application).where(
            Application.id == application_id, Application.user_id == g.user.id
        )
    )
    if not record:
        abort(404)
    status = request.form.get("status")
    if status not in APPLICATION_STATUSES:
        abort(400, description="Choose a valid application status.")
    record.status = status
    db.session.commit()
    flash("Application status updated.", "success")
    return redirect(url_for("candidate.applications"))
