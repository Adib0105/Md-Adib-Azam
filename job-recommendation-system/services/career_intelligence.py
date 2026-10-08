"""Skill readiness and prerequisite paths; no placement or salary predictions."""

from collections import Counter
from models.skill_extractor import normalize_skill, normalize_skills

RELATED = {
    "SQL": {"Advanced SQL", "MySQL", "PostgreSQL", "SQL Server", "SQLite"},
    "Excel": {"Advanced Excel", "Excel VBA"},
    "Python": {"Pandas", "NumPy"},
}
DEPENDENCIES = {
    "Pandas": ["Python"],
    "NumPy": ["Python"],
    "Machine Learning": ["Python", "Pandas", "Statistics"],
    "Deep Learning": ["Machine Learning"],
    "Statistics": ["Probability"],
    "Power BI": ["Excel", "Data Cleaning"],
    "DAX": ["Power BI"],
    "Advanced SQL": ["SQL"],
    "ETL": ["SQL", "Python"],
    "Data Modeling": ["SQL"],
    "MLOps": ["Machine Learning", "Git", "Docker"],
    "Tableau": ["Data Visualization"],
}
CURATED_ROLES = [
    ("Student", ["Excel", "Communication"]),
    ("Junior Data Analyst", ["Excel", "SQL", "Data Cleaning", "Statistics"]),
    (
        "Data Analyst",
        ["Excel", "SQL", "Python", "Power BI", "Statistics", "Communication"],
    ),
    (
        "Senior Data Analyst",
        [
            "Advanced SQL",
            "Python",
            "Power BI",
            "Statistics",
            "Stakeholder Management",
            "A/B Testing",
        ],
    ),
    ("Analytics Engineer", ["SQL", "Python", "ETL", "Data Modeling", "Git"]),
    (
        "Data Scientist",
        [
            "Python",
            "SQL",
            "Pandas",
            "Statistics",
            "Machine Learning",
            "Model Evaluation",
        ],
    ),
]


def skill_gap(candidate_skills, required_skills, levels=None):
    candidate = set(normalize_skills(candidate_skills))
    required = normalize_skills(required_skills)
    levels = {normalize_skill(key): value for key, value in (levels or {}).items()}
    details = []
    for skill in required:
        if skill in candidate and levels.get(skill, "Intermediate") != "Beginner":
            status, credit = "matched", 1.0
        elif (
            skill in candidate
            or RELATED.get(skill, set()) & candidate
            or any(
                skill in related and parent in candidate
                for parent, related in RELATED.items()
            )
        ):
            status, credit = "partial", 0.5
        else:
            status, credit = "missing", 0.0
        details.append(
            {
                "skill": skill,
                "status": status,
                "credit": credit,
                "priority": (
                    "High" if not credit else "Medium" if credit < 1 else "Maintain"
                ),
                "current_level": levels.get(
                    skill, "Unspecified" if skill in candidate else "Not demonstrated"
                ),
                "target_level": "Intermediate",
                "reason": "Required in the selected role/job; proficiency is self-reported.",
            }
        )
    coverage = sum(item["credit"] for item in details)
    return {
        "matched": [r["skill"] for r in details if r["status"] == "matched"],
        "partial": [r["skill"] for r in details if r["status"] == "partial"],
        "missing": [r["skill"] for r in details if r["status"] == "missing"],
        "details": details,
        "gap_percent": (
            round(100 * (1 - coverage / len(required)), 1) if required else None
        ),
        "readiness": round(100 * coverage / len(required), 1) if required else None,
        "method": "Required-skill coverage: exact/intermediate=1, related/beginner=0.5, missing=0. Unknown requirements are not scored.",
    }


def learning_path(candidate_skills, gap):
    owned = set(normalize_skills(candidate_skills)) - set(gap["partial"])
    ordered, visiting, added = [], set(), set()

    def visit(skill, needed_by=None):
        if skill in added or skill in owned:
            return
        if skill in visiting:
            raise ValueError("Learning prerequisite cycle.")
        visiting.add(skill)
        for dependency in DEPENDENCIES.get(skill, []):
            visit(dependency, skill)
        visiting.remove(skill)
        added.add(skill)
        ordered.append(
            {
                "skill": skill,
                "priority": "High" if needed_by else "Medium",
                "reason": (
                    f"Prerequisite for {needed_by}."
                    if needed_by
                    else "Required skill gap for the target role."
                ),
                "current_level": (
                    "Beginner/related"
                    if skill in gap["partial"]
                    else "Not demonstrated"
                ),
                "target_level": "Intermediate",
                "dependencies": DEPENDENCIES.get(skill, []),
            }
        )

    for skill in gap["missing"] + gap["partial"]:
        visit(skill)
    if ordered:
        ordered.append(
            {
                "skill": "Portfolio project",
                "priority": "High",
                "reason": "Demonstrate the newly learned skills with a reproducible project and documented results.",
                "current_level": "Not assessed",
                "target_level": "Demonstrated evidence",
                "dependencies": [row["skill"] for row in ordered],
            }
        )
    return ordered


def career_path(user, jobs):
    levels = {skill.skill_name: skill.proficiency_level for skill in user.skills}
    output = []
    for title, curated in CURATED_ROLES:
        observations = [
            job for job in jobs if job.job_title.casefold() == title.casefold()
        ]
        demand = Counter(
            skill
            for job in observations
            for skill in normalize_skills(job.required_skills)
        )
        required = (
            [
                skill
                for skill, count in demand.items()
                if count / len(observations) >= 0.5
            ]
            if observations
            else curated
        )
        gap = skill_gap(user.skill_names, required, levels)
        gap["source"] = (
            f"Required skills in {len(observations)} current catalogue listings (majority threshold)."
            if observations
            else "Curated educational role template; validate with actual employers."
        )
        output.append(
            {
                "role": title,
                "gap": gap,
                "learning_path": learning_path(user.skill_names, gap),
                "difficulty": (
                    "Low skill gap"
                    if gap["gap_percent"] is not None and gap["gap_percent"] < 30
                    else (
                        "Moderate skill gap"
                        if gap["gap_percent"] is not None and gap["gap_percent"] < 65
                        else "Large skill gap"
                    )
                ),
                "transition_from": output[-1]["role"] if output else None,
            }
        )
    return output


def role_gap(user, role, jobs):
    observations = [job for job in jobs if job.job_title.casefold() == role.casefold()]
    fallback = next(
        (
            skills
            for title, skills in CURATED_ROLES
            if title.casefold() == role.casefold()
        ),
        [],
    )
    demand = Counter(
        skill for job in observations for skill in normalize_skills(job.required_skills)
    )
    required = (
        [skill for skill, count in demand.items() if count / len(observations) >= 0.5]
        if observations
        else fallback
    )
    gap = skill_gap(
        user.skill_names,
        required,
        {skill.skill_name: skill.proficiency_level for skill in user.skills},
    )
    return {
        "role": role,
        "gap": gap,
        "learning_path": learning_path(user.skill_names, gap),
        "listings": len(observations),
        "source": (
            "Current catalogue majority-required skills"
            if observations
            else (
                "Curated educational template"
                if fallback
                else "Requirements unavailable"
            )
        ),
    }
