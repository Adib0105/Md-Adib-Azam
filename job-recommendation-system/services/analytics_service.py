from collections import Counter, defaultdict
from statistics import mean
from models.database import (
    db,
    User,
    Job,
    Application,
    Recommendation,
    RecommendationRun,
    SearchEvent,
)


def chart(kind, pairs):
    return {
        "type": kind,
        "labels": [p[0] for p in pairs],
        "values": [round(p[1], 2) for p in pairs],
    }


def market_analytics(jobs):
    skills, roles, locations, industries = Counter(), Counter(), Counter(), Counter()
    salaries_by_role = defaultdict(list)
    salary_bands = Counter(
        {"< 3 LPA": 0, "3–6 LPA": 0, "6–10 LPA": 0, "10–15 LPA": 0, "15+ LPA": 0}
    )
    experiences = Counter(
        {
            "Fresher (0)": 0,
            "Early career (1–2)": 0,
            "Mid career (3–5)": 0,
            "Senior (6+)": 0,
        }
    )
    remote = Counter({"Remote": 0, "Onsite": 0, "Hybrid": 0, "Unknown": 0})
    for job in jobs:
        skills.update(set(job.required_skills))
        roles[job.job_title] += 1
        locations[job.location] += 1
        industries[job.industry] += 1
        remote[
            (
                "Remote"
                if job.remote_allowed or job.location.casefold() == "remote"
                else job.remote_type.title()
            )
        ] += 1
        experience = job.experience_min
        experiences[
            (
                "Unknown"
                if not job.experience_known
                else (
                    "Fresher (0)"
                    if experience == 0
                    else (
                        "Early career (1–2)"
                        if experience <= 2
                        else "Mid career (3–5)" if experience <= 5 else "Senior (6+)"
                    )
                )
            )
        ] += 1
        if (
            job.salary_currency == "INR"
            and job.salary_period == "year"
            and job.min_salary is not None
            and job.max_salary is not None
        ):
            midpoint = (job.min_salary + job.max_salary) / 2 / 100000
            salaries_by_role[job.job_title].append(midpoint)
            salary_bands[
                (
                    "< 3 LPA"
                    if midpoint < 3
                    else (
                        "3–6 LPA"
                        if midpoint < 6
                        else (
                            "6–10 LPA"
                            if midpoint < 10
                            else "10–15 LPA" if midpoint < 15 else "15+ LPA"
                        )
                    )
                )
            ] += 1
    charts = {
        "Most demanded skills": chart("bar", skills.most_common(10)),
        "Top job roles": chart("bar", roles.most_common(8)),
        "Average salary midpoint by role (LPA)": chart(
            "bar",
            sorted(
                [(role, mean(values)) for role, values in salaries_by_role.items()],
                key=lambda p: -p[1],
            )[:10],
        ),
        "Hiring locations": chart("bar", locations.most_common()),
        "Jobs by industry": chart("doughnut", industries.most_common()),
        "Remote and onsite": chart("doughnut", list(remote.items())),
        "Minimum experience required": chart("bar", list(experiences.items())),
        "Annual salary midpoint distribution": chart("bar", list(salary_bands.items())),
    }
    return {
        "charts": charts,
        "total": len(jobs),
        "skills": len(skills),
        "locations": len(locations),
        "remote": remote["Remote"],
        "synthetic": sum(j.is_synthetic for j in jobs),
    }


def skill_analytics(user, rows):
    jobs = [row["job"] for row in rows]
    demand = Counter(skill for job in jobs for skill in set(job.required_skills))
    gaps = Counter(skill for row in rows[:20] for skill in row["missing"])
    owned = {skill.skill_name.casefold(): skill for skill in user.skills}
    compared = [
        {
            "name": name,
            "jobs": number,
            "percent": round(100 * number / max(len(jobs), 1), 1),
            "owned": name.casefold() in owned,
            "level": (
                owned[name.casefold()].proficiency_level
                if name.casefold() in owned
                else "Missing"
            ),
        }
        for name, number in demand.most_common(18)
    ]
    personal = [
        {
            "name": s.skill_name,
            "level": s.proficiency_level,
            "percent": round(100 * demand[s.skill_name] / max(len(jobs), 1), 1),
        }
        for s in user.skills
    ]
    return {
        "demand": compared,
        "personal": personal,
        "gaps": gaps.most_common(10),
        "top_count": min(len(rows), 20),
        "strong": [s for s in personal if s["level"] == "Advanced"],
        "developing": [s for s in personal if s["level"] == "Beginner"],
        "missing": [s for s in compared if not s["owned"]],
    }


def career_paths(rows):
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["job"].job_title].append(row)
    paths = []
    for title, values in grouped.items():
        top = sorted(values, key=lambda r: -r["score"])[:3]
        paths.append(
            {
                "title": title,
                "score": round(mean(row["score"] for row in top), 1),
                "count": len(values),
                "matched": top[0]["matched"][:4],
                "missing": top[0]["missing"][:3],
                "best_id": top[0]["job"].id,
            }
        )
    return sorted(paths, key=lambda row: (-row["score"], row["title"]))


def admin_analytics():
    all_jobs = db.session.scalars(db.select(Job).where(Job.active.is_(True))).all()
    data = market_analytics(all_jobs)
    applications = db.session.scalars(db.select(Application)).all()
    statuses = Counter(row.status for row in applications)
    searches = db.session.execute(
        db.select(SearchEvent.query, db.func.count(SearchEvent.id))
        .group_by(SearchEvent.query)
        .order_by(db.func.count(SearchEvent.id).desc())
        .limit(8)
    ).all()
    data["charts"].update(
        {
            "Application status": chart("doughnut", list(statuses.items())),
            "Most searched terms": chart("bar", searches),
        }
    )
    data["candidates"] = (
        db.session.scalar(
            db.select(db.func.count(User.id)).where(User.is_admin.is_(False))
        )
        or 0
    )
    data["applications"] = len(applications)
    # The metric explicitly includes historical snapshots, not just the newest scores.
    data["average"] = round(
        db.session.scalar(db.select(db.func.avg(Recommendation.overall_score))) or 0, 1
    )
    data["runs"] = (
        db.session.scalar(db.select(db.func.count(RecommendationRun.id))) or 0
    )
    from models.database import SavedJob, AuditLog, utcnow

    data["real"] = db.session.scalar(
        db.select(db.func.count(Job.id)).where(Job.is_external.is_(True))
    )
    data["fetched_today"] = db.session.scalar(
        db.select(db.func.count(Job.id)).where(
            Job.is_external.is_(True),
            Job.last_synced_at
            >= utcnow().replace(hour=0, minute=0, second=0, microsecond=0),
        )
    )
    data["active_users"] = db.session.scalar(
        db.select(db.func.count(User.id)).where(
            User.is_active.is_(True), User.is_admin.is_(False)
        )
    )
    data["saved"] = db.session.scalar(db.select(db.func.count(SavedJob.id)))
    data["resets"] = db.session.scalar(
        db.select(db.func.count(AuditLog.id)).where(
            AuditLog.action == "password_reset_requested"
        )
    )
    data["popular"] = sorted(all_jobs, key=lambda job: (-job.views, job.id))[:6]
    return data
