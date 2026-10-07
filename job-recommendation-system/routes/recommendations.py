from flask import (
    Blueprint,
    g,
    request,
    render_template,
    jsonify,
    flash,
    redirect,
    url_for,
)
from models.database import db, RecommendationRun
from models.skill_extractor import SKILLS
from routes.auth import login_required
from routes.jobs import flags, pagination
from services.recommendation_service import recommendations, snapshot, active_jobs
from services.analytics_service import market_analytics, skill_analytics, career_paths
from utils.validators import validate_skills, ValidationError
from services.settings_service import weights as configured_weights

recs = Blueprint("recs", __name__)


@recs.get("/recommendations")
@login_required
def listing():
    all_rows = recommendations(g.user)
    rows, pager = pagination(all_rows)
    return render_template(
        "jobs.html",
        rows=rows,
        pager=pager,
        title="Made for your next chapter",
        subtitle="Every match has a reason. Explore yours.",
        filterable=False,
        **flags(),
    )


@recs.get("/insights")
@login_required
def insights():
    return render_template("career_insights.html", data=market_analytics(active_jobs()))


@recs.get("/skills")
@login_required
def skills():
    rows = recommendations(g.user)
    return render_template(
        "skill_analysis.html",
        data=skill_analytics(g.user, rows),
        paths=career_paths(rows)[:8],
    )


@recs.route("/simulator", methods=["GET", "POST"])
@login_required
def simulator():
    rows = recommendations(g.user)
    analytics = skill_analytics(g.user, rows)
    simulations, selected = [], []
    status = 200
    if request.method == "POST":
        try:
            selected = validate_skills(request.form.get("skills", ""))
            selected = [
                s
                for s in selected
                if s.casefold() not in {x.casefold() for x in g.user.skill_names}
            ]
            if not selected:
                raise ValidationError(
                    "Choose at least one skill you have not added to your profile."
                )
            if len(selected) > 8:
                raise ValidationError("Simulate up to eight skills at a time.")
            if any(s not in SKILLS for s in selected):
                raise ValidationError("Choose skills from the suggested dictionary.")
            after = {
                r["job"].id: r for r in recommendations(g.user, extra_skills=selected)
            }
            for row in rows:
                simulated = after[row["job"].id]
                simulations.append(
                    {
                        "job": row["job"],
                        "before": row["score"],
                        "after": simulated["score"],
                        "gain": round(simulated["score"] - row["score"], 1),
                    }
                )
            simulations.sort(key=lambda r: (-r["gain"], -r["after"], r["job"].id))
            simulations = simulations[:12]
        except ValidationError as exc:
            flash(str(exc), "error")
            status = 400
    return render_template(
        "career_simulator.html",
        simulations=simulations,
        selected=selected,
        gaps=analytics["gaps"],
        skill_dictionary=SKILLS,
    ), status


@recs.get("/history")
@login_required
def history():
    runs = db.session.scalars(
        db.select(RecommendationRun)
        .where(RecommendationRun.user_id == g.user.id)
        .order_by(RecommendationRun.id.desc())
        .limit(30)
    ).all()
    # Compare the same job IDs across snapshots rather than unrelated top averages.
    comparisons = []
    if len(runs) >= 2:
        previous = {r.job_id: r for r in runs[1].results}
        for row in runs[0].results:
            if row.job_id in previous:
                comparisons.append(
                    {
                        "title": row.job_title,
                        "company": row.company_name,
                        "before": previous[row.job_id].overall_score,
                        "after": row.overall_score,
                        "change": round(
                            row.overall_score - previous[row.job_id].overall_score, 1
                        ),
                    }
                )
        comparisons.sort(key=lambda item: -item["change"])
    charts = {
        "Best match per snapshot": {
            "type": "line",
            "labels": [r.created_at.strftime("%d %b %H:%M") for r in reversed(runs)],
            "values": [
                max((x.overall_score for x in r.results), default=0)
                for r in reversed(runs)
            ],
        }
    }
    return render_template(
        "history.html", runs=runs, comparisons=comparisons[:12], charts=charts
    )


@recs.post("/history/snapshot")
@login_required
def save_snapshot():
    snapshot(g.user, "Manual refresh")
    flash(
        "Current results saved. Identical consecutive snapshots are reused.", "success"
    )
    return redirect(url_for("recs.history"))


@recs.get("/methodology")
def methodology():
    return render_template("methodology.html", weights=configured_weights())


def serialized_recommendations(rows):
    return [
        {
            "job_id": r["job"].id,
            "title": r["job"].job_title,
            "overall_score": r["score"],
            "scores": r["scores"],
            "contributions": r["contributions"],
            "matched_skills": r["matched"],
            "missing_skills": r["missing"],
            "reasons": r["reasons"],
            "confidence": r["confidence"],
        }
        for r in rows
    ]


@recs.get("/api/recommendations")
@login_required
def api_recommendations():
    rows, pager = pagination(recommendations(g.user), per_page=20)
    return jsonify(
        items=serialized_recommendations(rows),
        total=pager["total"],
        page=pager["page"],
        pages=pager["pages"],
    )


@recs.post("/api/recommend")
@login_required
def api_recommend():
    run = snapshot(g.user, "API refresh")
    return jsonify(
        run_id=run.id, items=serialized_recommendations(recommendations(g.user)[:20])
    )
