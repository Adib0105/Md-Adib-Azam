from datetime import date
from math import ceil
from flask import (
    Blueprint,
    g,
    request,
    render_template,
    redirect,
    url_for,
    flash,
    abort,
    jsonify,
)
from sqlalchemy.exc import IntegrityError
from models.database import db, Job, SavedJob, Application, SearchEvent
from routes.auth import login_required
from services.recommendation_service import (
    active_jobs,
    recommendations,
    engine,
    profile_data,
)
from models.skill_extractor import normalize_skills, SKILLS
from utils.constants import EMPLOYMENT_TYPES
from utils.validators import number_field, ValidationError

jobs = Blueprint("jobs", __name__)


def flags():
    if not g.user:
        return {"saved_ids": set(), "application_ids": set()}
    return {
        "saved_ids": set(
            db.session.scalars(
                db.select(SavedJob.job_id).where(SavedJob.user_id == g.user.id)
            ).all()
        ),
        "application_ids": set(
            db.session.scalars(
                db.select(Application.job_id).where(Application.user_id == g.user.id)
            ).all()
        ),
    }


def ranked_jobs():
    return (
        recommendations(g.user)
        if g.user
        else engine().rank({"skills": []}, active_jobs())
    )


def filtered_rows(rows):
    query = request.args.get("q", "").strip()[:160]
    # Search ranks semantically before applying structured constraints.
    if query:
        rows = engine().search(query, rows)
    try:
        low = number_field(request.args, "min_salary", 100000000, True)
        high = number_field(request.args, "max_salary", 100000000, True)
        experience = number_field(request.args, "experience", 60)
        minimum_match = number_field(request.args, "min_match", 100) or 0
        if low is not None and high is not None and low > high:
            raise ValidationError("Minimum salary cannot exceed maximum salary.")
    except ValidationError as exc:
        abort(400, description=str(exc))
    result = []
    for row in rows:
        job = row["job"]
        if any(
            request.args.get(key)
            and request.args[key].casefold() not in getattr(job, column).casefold()
            for key, column in [
                ("title", "job_title"),
                ("company", "company_name"),
                ("location", "location"),
                ("industry", "industry"),
            ]
        ):
            continue
        if request.args.get("type") and request.args["type"] != job.employment_type:
            continue
        required = {s.casefold() for s in job.required_skills + job.preferred_skills}
        if any(
            s.casefold() not in required
            for s in normalize_skills(request.args.get("skills", ""))
        ):
            continue
        # Salary filters keep listings whose ranges overlap the selected interval.
        if low is not None and (job.max_salary is None or job.max_salary < low):
            continue
        if high is not None and (job.min_salary is None or job.min_salary > high):
            continue
        if experience is not None and job.experience_min > experience:
            continue
        if g.user and row["score"] < minimum_match:
            continue
        result.append(row)
    sort = request.args.get("sort", "relevance" if query else "match")
    if sort == "salary":
        result.sort(key=lambda row: (-(row["job"].max_salary or 0), row["job"].id))
    elif sort == "newest":
        result.sort(
            key=lambda row: (-row["job"].posted_date.toordinal(), row["job"].id)
        )
    elif sort == "rating":
        result.sort(key=lambda row: (-(row["job"].company_rating or 0), row["job"].id))
    elif sort == "match":
        result.sort(key=lambda row: (-row["score"], row["job"].id))
    return result


def pagination(rows, per_page=12):
    try:
        page = max(1, int(request.args.get("page", 1)))
    except ValueError:
        abort(400, description="Page must be a whole number.")
    count = len(rows)
    pages = max(1, ceil(count / per_page))
    page = min(page, pages)
    parameters = request.args.to_dict()
    links = {}
    for key, number in [("previous", page - 1), ("next", page + 1)]:
        parameters["page"] = number
        links[key] = url_for(request.endpoint, **parameters)
    return rows[(page - 1) * per_page : page * per_page], {
        "page": page,
        "pages": pages,
        "total": count,
        **links,
    }


@jobs.get("/jobs")
def listing():
    all_rows = ranked_jobs()
    query = request.args.get("q", "").strip()[:160]
    if query and not request.args.get("page"):
        db.session.add(SearchEvent(query=query.casefold()))
        db.session.commit()
    rows, pager = pagination(filtered_rows(all_rows))
    return render_template(
        "jobs.html",
        rows=rows,
        pager=pager,
        title="Explore opportunities",
        subtitle="Find your next move, one thoughtful match at a time.",
        filterable=True,
        locations=sorted({r["job"].location for r in all_rows}),
        industries=sorted({r["job"].industry for r in all_rows}),
        types=EMPLOYMENT_TYPES,
        **flags(),
    )


@jobs.get("/jobs/<int:job_id>")
def detail(job_id):
    job = db.get_or_404(Job, job_id)
    db.session.execute(
        db.update(Job).where(Job.id == job_id).values(views=Job.views + 1)
    )
    db.session.commit()
    available = active_jobs()
    pool = available if any(j.id == job_id for j in available) else available + [job]
    row, estimated = None, None
    if g.user:
        rows = recommendations(g.user, jobs=pool)
        row = next(r for r in rows if r["job"].id == job_id)
        if row["missing"]:
            simulated = recommendations(g.user, extra_skills=row["missing"], jobs=pool)
            estimated = next(r["score"] for r in simulated if r["job"].id == job_id)
    similar = engine().similar(job, pool)
    closed = not job.active or (
        job.application_deadline and job.application_deadline < date.today()
    )
    return render_template(
        "job_details.html",
        job=job,
        row=row,
        estimated=estimated,
        similar=similar,
        closed=closed,
        **flags(),
    )


def back_to_job(job_id):
    # Never redirect to arbitrary caller-supplied URLs.
    if request.form.get("return_to") == "saved":
        return redirect(url_for("jobs.saved"))
    return redirect(url_for("jobs.detail", job_id=job_id))


@jobs.post("/jobs/<int:job_id>/save")
@login_required
def save(job_id):
    db.get_or_404(Job, job_id)
    record = db.session.scalar(
        db.select(SavedJob).where(
            SavedJob.user_id == g.user.id, SavedJob.job_id == job_id
        )
    )
    if record:
        db.session.delete(record)
        message = "Job removed from saved jobs."
    else:
        db.session.add(SavedJob(user_id=g.user.id, job_id=job_id))
        message = "Job saved to your shortlist."
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
    flash(message, "success")
    return back_to_job(job_id)


@jobs.post("/jobs/<int:job_id>/apply")
@login_required
def apply(job_id):
    job = db.get_or_404(Job, job_id)
    if not job.active or (
        job.application_deadline and job.application_deadline < date.today()
    ):
        abort(
            400,
            description="This listing is closed and cannot be added as a new application.",
        )
    record = db.session.scalar(
        db.select(Application).where(
            Application.user_id == g.user.id, Application.job_id == job_id
        )
    )
    if not record:
        db.session.add(Application(user_id=g.user.id, job_id=job_id))
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
    flash(
        "Added to your local tracker. No application was sent to an employer.",
        "success",
    )
    return redirect(url_for("candidate.applications"))


@jobs.get("/saved")
@login_required
def saved():
    state = flags()
    records = db.session.scalars(
        db.select(Job).join(SavedJob).where(SavedJob.user_id == g.user.id)
    ).all()
    available = active_jobs()
    ids = {j.id for j in available}
    pool = available + [j for j in records if j.id not in ids]
    rows = [
        r
        for r in recommendations(g.user, jobs=pool)
        if r["job"].id in state["saved_ids"]
    ]
    rows, pager = pagination(rows)
    return render_template(
        "jobs.html",
        rows=rows,
        pager=pager,
        title="Your saved jobs",
        subtitle="A shortlist of possibilities, ready when you are.",
        filterable=False,
        **state,
    )


@jobs.get("/api/jobs")
def api_jobs():
    rows, pager = pagination(filtered_rows(ranked_jobs()))
    return jsonify(
        items=[
            {**r["job"].as_dict(), "match_score": r["score"] if g.user else None}
            for r in rows
        ],
        page=pager["page"],
        pages=pager["pages"],
        total=pager["total"],
    )


@jobs.get("/api/jobs/<int:job_id>")
def api_job(job_id):
    return jsonify(db.get_or_404(Job, job_id).as_dict())


@jobs.get("/api/skills")
def api_skills():
    query = request.args.get("q", "").casefold()[:100]
    return jsonify(skills=[s for s in SKILLS if query in s.casefold()])


@jobs.get("/api/profile")
@login_required
def api_profile():
    profile = profile_data(g.user)
    profile.pop("resume_text", None)
    return jsonify(full_name=g.user.full_name, **profile)
