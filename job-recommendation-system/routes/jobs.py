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
    current_app,
)
from sqlalchemy.exc import IntegrityError
from models.database import db, Job, SavedJob, Application, SearchEvent, JobView, utcnow
from routes.auth import login_required
from services.recommendation_service import (
    active_jobs,
    recommendations,
    engine,
    profile_data,
)
from models.skill_extractor import SKILLS
from services.job_catalog import parse_filters, job_query, eligible_conditions
from services.external_jobs_service import live_search
from services.job_providers.provider_registry import provider_summaries
from services.security_service import rate_limit
from utils.constants import EMPLOYMENT_TYPES
from utils.validators import ValidationError

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


def request_filters():
    try:
        return parse_filters(request.args)
    except ValidationError as exc:
        abort(400, description=str(exc))


def query_rows(filters, ids=None):
    statement = job_query(filters)
    if ids is not None:
        statement = statement.where(Job.id.in_(ids))
    sort = filters.get("sort")
    if sort == "salary":
        # Compare annual salaries only within the explicitly selected currency.
        from services.job_catalog import country_currency

        currency = filters.get("currency") or (
            "USD"
            if filters.get("source") == "usajobs"
            else country_currency(filters.get("country", "in"))
        )
        statement = statement.where(
            Job.salary_currency == currency, Job.salary_period == "year"
        ).order_by(Job.max_salary.desc(), Job.id)
    else:
        statement = statement.order_by(
            Job.featured.desc(), Job.posted_date.desc(), Job.id
        )
    pool = db.session.scalars(
        statement.limit(current_app.config["MAX_RANKING_JOBS"])
    ).all()
    rows = engine().rank(profile_data(g.user) if g.user else {"skills": []}, pool)
    if filters.get("q") and sort == "relevance":
        rows = engine().search(filters["q"], rows)
    if g.user and filters.get("min_match"):
        rows = [r for r in rows if r["score"] >= filters["min_match"]]
    if sort == "salary":
        rows.sort(key=lambda r: (-(r["job"].max_salary or 0), r["job"].id))
    elif sort == "newest":
        rows.sort(key=lambda r: (-r["job"].posted_date.toordinal(), r["job"].id))
    elif sort == "rating":
        rows.sort(key=lambda r: (-(r["job"].company_rating or 0), r["job"].id))
    return rows


def record_search(filters, count):
    if filters.get("q") and filters.get("page", 1) == 1:
        db.session.add(
            SearchEvent(
                query=filters["q"].casefold(),
                user_id=g.user.id if g.user else None,
                source=filters["source"],
                location=filters["location"],
                result_count=count,
            )
        )
        db.session.commit()


def visible_job(job_id):
    job = db.get_or_404(Job, job_id)
    if (not job.published or job.deleted) and not (g.user and g.user.is_admin):
        abort(404)
    return job


def public_item(row):
    return {
        **row["job"].as_dict(),
        "match_score": row["score"] if g.user else None,
        "skill_match": row["matched"] if g.user else [],
        "context": row["context"] if g.user else {},
    }


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
    filters = request_filters()
    all_rows = query_rows(filters)
    record_search(filters, len(all_rows))
    rows, pager = pagination(all_rows)
    return render_template(
        "jobs.html",
        rows=rows,
        pager=pager,
        title="Explore opportunities",
        subtitle="Real sources. Clear labels. A match you can understand.",
        filterable=True,
        types=EMPLOYMENT_TYPES,
        live=None,
        **flags(),
    )


def live_results():
    filters = request_filters()
    slug = request.args.get("provider", "adzuna")
    if slug not in {"adzuna", "usajobs"}:
        abort(400, description="Choose Adzuna or USAJOBS.")
    rate_limit("live_search", 60, 60)
    filters["source"] = slug
    if slug == "usajobs":
        filters["country"] = "us"
    live = live_search(slug, filters)
    if live["fallback"]:
        fallback = {**filters, "source": "demo"}
        rows = query_rows(fallback)[: filters["per_page"]]
    else:
        rows = query_rows(filters, live["ids"])
    record_search(filters, len(rows))
    return filters, rows, live


@jobs.get("/real-jobs")
def real_jobs():
    filters, rows, live = live_results()
    page = filters["page"]
    from math import ceil

    pages = (
        max(1, ceil(live["provider_total"] / filters["per_page"]))
        if not live["fallback"]
        else page
    )
    parameters = request.args.to_dict()
    pager = {
        "page": page,
        "pages": pages,
        "total": len(rows),
        "previous": url_for(
            "jobs.real_jobs", **{**parameters, "page": max(1, page - 1)}
        ),
        "next": url_for("jobs.real_jobs", **{**parameters, "page": page + 1}),
    }
    return render_template(
        "jobs.html",
        rows=rows,
        pager=pager,
        title="Discover real opportunities",
        subtitle="Supported providers, thoughtful matches, your next chapter.",
        filterable=True,
        live=live,
        types=EMPLOYMENT_TYPES,
        **flags(),
    )


@jobs.get("/api/jobs/live")
def api_live():
    filters, rows, live = live_results()
    return jsonify(items=[public_item(r) for r in rows], page=filters["page"], **live)


@jobs.get("/api/providers")
def api_providers():
    return jsonify(providers=provider_summaries())


@jobs.get("/jobs/<int:job_id>")
def detail(job_id):
    job = visible_job(job_id)
    db.session.execute(
        db.update(Job).where(Job.id == job_id).values(views=Job.views + 1)
    )
    db.session.commit()
    if g.user:
        viewed = db.session.scalar(
            db.select(JobView).where(
                JobView.user_id == g.user.id, JobView.job_id == job_id
            )
        )
        if viewed:
            viewed.viewed_at = utcnow()
        else:
            db.session.add(JobView(user_id=g.user.id, job_id=job_id))
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
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
    closed = not db.session.scalar(
        db.select(Job.id).where(Job.id == job_id, *eligible_conditions())
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
    visible_job(job_id)
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
    job = visible_job(job_id)
    if not db.session.scalar(
        db.select(Job.id).where(Job.id == job_id, *eligible_conditions())
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
        db.session.add(
            Application(
                user_id=g.user.id,
                job_id=job_id,
                application_date=date.today(),
                application_url=job.source_url if job.is_external else "",
            )
        )
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
@jobs.get("/api/jobs/search")
def api_jobs():
    filters = request_filters()
    rows, pager = pagination(query_rows(filters))
    return jsonify(
        items=[public_item(r) for r in rows],
        page=pager["page"],
        pages=pager["pages"],
        total=pager["total"],
        ranking_pool_limit=current_app.config["MAX_RANKING_JOBS"],
    )


@jobs.get("/api/jobs/<int:job_id>")
def api_job(job_id):
    return jsonify(visible_job(job_id).as_dict())


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
