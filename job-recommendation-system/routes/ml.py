"""Authenticated resume/career tools and an operator-only, read-only Model Lab."""

import json
from collections import Counter
from pathlib import Path
from flask import (
    Blueprint,
    current_app,
    g,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    abort,
    jsonify,
)
from config import ROOT
from models.database import db, User, Job, Recommendation
from models.ml_data import (
    InteractionEvent,
    ExperimentAssignment,
    RecommendationExposure,
    Experiment,
)
from routes.auth import login_required, admin_required
from routes.jobs import visible_job
from services.recommendation_service import profile_data, active_jobs
from services.career_intelligence import (
    skill_gap,
    learning_path,
    career_path,
    role_gap,
    CURATED_ROLES,
)
from services.analytics_service import chart
from services.interaction_service import record_interaction
from services.security_service import rate_limit
from ml.preprocessing.resume_intelligence import analyze_resume, resume_quality
from ml.features.behavior import behavior_for

ml_pages = Blueprint("ml_pages", __name__)


@ml_pages.get("/resume/intelligence")
@login_required
def resume_intelligence():
    profile = profile_data(g.user)
    intelligence = analyze_resume(g.user.resume_text or "")
    quality = resume_quality(
        profile, intelligence, current_app.config.get("RESUME_QUALITY_WEIGHTS")
    )
    return render_template(
        "resume_intelligence.html", intelligence=intelligence, quality=quality
    )


@ml_pages.get("/career/path")
@login_required
def career():
    jobs = active_jobs()
    target = request.args.get("role", g.user.preferred_role or "Data Analyst").strip()[
        :160
    ]
    roles = sorted(
        {job.job_title for job in jobs} | {title for title, _ in CURATED_ROLES}
    )
    return render_template(
        "career_path.html",
        paths=career_path(g.user, jobs),
        target=role_gap(g.user, target, jobs),
        roles=roles,
    )


@ml_pages.get("/api/career/role-gap")
@login_required
def api_role_gap():
    role = request.args.get("role", g.user.preferred_role or "Data Analyst").strip()[
        :160
    ]
    return jsonify(role_gap(g.user, role, active_jobs()))


@ml_pages.get("/api/career/gap/<int:job_id>")
@login_required
def api_gap(job_id):
    job = visible_job(job_id)
    gap = skill_gap(
        g.user.skill_names,
        job.required_skills,
        {s.skill_name: s.proficiency_level for s in g.user.skills},
    )
    return jsonify(
        job_id=job_id,
        role=job.job_title,
        gap=gap,
        learning_path=learning_path(g.user.skill_names, gap),
    )


@ml_pages.post("/jobs/<int:job_id>/feedback")
@login_required
def feedback(job_id):
    visible_job(job_id)
    rate_limit("job_feedback", 30, 3600, str(g.user.id))
    action = request.form.get("action")
    if action not in {"rejected", "ignored"}:
        abort(400, description="Choose not interested or explicitly ignore this job.")
    record_interaction(g.user, job_id, action, "candidate_feedback")
    db.session.commit()
    flash(
        "Your feedback was recorded. Personalization uses enough distinct prior interactions and at most 10% of the weight.",
        "success",
    )
    return redirect(url_for("jobs.detail", job_id=job_id))


@ml_pages.get("/api/personalization")
@login_required
def personalization():
    profile = behavior_for(g.user)
    return jsonify(
        enabled=profile["enabled"],
        distinct_jobs=profile["distinct_jobs"],
        meaningful_jobs=profile["meaningful_jobs"],
        reason=profile["reason"],
        preferences={
            name: dict(values) for name, values in profile["preferences"].items()
        },
        maximum_weight=current_app.config["BEHAVIOR_MAX_WEIGHT"],
    )


def evaluation_report():
    path = Path(current_app.instance_path) / "ml" / "model_evaluation.json"
    if not path.exists():
        path = ROOT / "docs/model_evaluation.json"
    try:
        if path.stat().st_size > 2 * 1024 * 1024:
            raise ValueError("Report too large.")
        report = json.loads(path.read_text(encoding="utf-8"))
        if (
            not isinstance(report, dict)
            or report.get("report_version") != "evaluation-v1"
        ):
            raise ValueError("Invalid report version.")
        return report
    except (OSError, ValueError, TypeError):
        return {
            "status": "not_evaluated",
            "dataset": {},
            "models": {},
            "limitations": [
                "Run the offline evaluation with an independently reviewed dataset."
            ],
        }


def experiment_summary():
    assignments = db.session.scalars(db.select(ExperimentAssignment)).all()
    # Correlate to the single most recent user/job exposure; aggregate in SQL,
    # never join every repeated display and multiply an action's attribution.
    last_exposure = (
        db.select(RecommendationExposure.id)
        .where(
            RecommendationExposure.user_id == InteractionEvent.user_id,
            RecommendationExposure.job_id == InteractionEvent.job_id,
            RecommendationExposure.created_at <= InteractionEvent.created_at,
        )
        .order_by(
            RecommendationExposure.created_at.desc(), RecommendationExposure.id.desc()
        )
        .limit(1)
        .correlate(InteractionEvent)
        .scalar_subquery()
    )
    attributed = db.session.execute(
        db.select(
            RecommendationExposure.assignment_id,
            InteractionEvent.action,
            db.func.count(InteractionEvent.id),
        )
        .select_from(InteractionEvent)
        .join(RecommendationExposure, RecommendationExposure.id == last_exposure)
        .where(
            InteractionEvent.action.in_(["viewed", "saved", "applied"]),
            db.func.julianday(InteractionEvent.created_at)
            - db.func.julianday(RecommendationExposure.created_at)
            <= 7,
            RecommendationExposure.assignment_id.is_not(None),
        )
        .group_by(RecommendationExposure.assignment_id, InteractionEvent.action)
    ).all()
    exposure_counts = dict(
        db.session.execute(
            db.select(
                RecommendationExposure.assignment_id,
                db.func.count(RecommendationExposure.id),
            ).group_by(RecommendationExposure.assignment_id)
        ).all()
    )
    result = []
    for experiment in db.session.scalars(db.select(Experiment)):
        for variant in ["A", "B"]:
            cohort = [
                a.id
                for a in assignments
                if a.experiment_slug == experiment.slug and a.variant == variant
            ]
            counts = Counter()
            for assignment_id, action, count in attributed:
                if assignment_id in cohort:
                    counts[action] += count
            result.append(
                {
                    "experiment": experiment.slug,
                    "variant": variant,
                    "assigned": len(cohort),
                    "exposures": sum(
                        exposure_counts.get(identity, 0) for identity in cohort
                    ),
                    "clicks": counts["viewed"],
                    "saves": counts["saved"],
                    "applies": counts["applied"],
                }
            )
    return result


@ml_pages.get("/admin/ml-lab")
@admin_required
def ml_lab():
    report = evaluation_report()
    dataset = report.get("dataset", {})
    models = report.get("models", {})
    charts = {}
    valid = {
        name: result["metrics"]
        for name, result in models.items()
        if result.get("metrics")
    }
    charts["Model comparison · NDCG@10"] = chart(
        "bar", [(name, value["ndcg@10"]) for name, value in valid.items()]
    )
    for label, metric in [
        ("Precision@K", "precision"),
        ("Recall@K", "recall"),
        ("NDCG@K", "ndcg"),
    ]:
        charts[label] = chart(
            "bar",
            [
                (f"{name} K={k}", values[f"{metric}@{k}"])
                for name, values in valid.items()
                for k in [5, 10, 20]
            ],
        )
    registry = current_app.extensions["ranker_registry"]
    ranker = registry.load()
    importance = (
        ranker.metadata.get("feature_importance", {})
        if ranker
        else next(
            (
                result.get("metadata", {}).get("feature_importance", {})
                for result in models.values()
                if result.get("metadata")
            ),
            {},
        )
    )
    charts["Model explainability · feature importance"] = chart(
        "bar", sorted(importance.items(), key=lambda pair: -pair[1])
    )
    scores = db.session.scalars(
        db.select(Recommendation.overall_score)
        .order_by(Recommendation.id.desc())
        .limit(10000)
    ).all()
    histogram = Counter({"0–19": 0, "20–39": 0, "40–59": 0, "60–79": 0, "80–100": 0})
    for score in scores:
        histogram[
            ["0–19", "20–39", "40–59", "60–79", "80–100"][min(int(score // 20), 4)]
        ] += 1
    charts["Recommendation distribution · latest 10,000 snapshot rows"] = chart(
        "bar", list(histogram.items())
    )
    counts = {
        "candidates": db.session.scalar(
            db.select(db.func.count(User.id)).where(User.is_admin.is_(False))
        ),
        "jobs": db.session.scalar(db.select(db.func.count(Job.id))),
        "interactions": db.session.scalar(
            db.select(db.func.count(InteractionEvent.id))
        ),
        "exposures": db.session.scalar(
            db.select(db.func.count(RecommendationExposure.id))
        ),
    }
    return render_template(
        "admin/ml_lab.html",
        report=report,
        dataset=dataset,
        models=models,
        charts=charts,
        counts=counts,
        embedding=current_app.extensions["embedding_service"].status(),
        ranker=ranker.metadata if ranker else None,
        ranker_status=registry.reason,
        experiments=experiment_summary(),
    )
