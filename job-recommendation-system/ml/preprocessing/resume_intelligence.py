"""Dictionary/section heuristics with evidence, provenance and review confidence."""

import re
from models.skill_extractor import SKILL_GROUPS, normalize_skills, extract_skills
from models.resume_parser import extract_resume_fields

QUALITY_WEIGHTS = {
    "completeness": 0.20,
    "skill_evidence": 0.20,
    "project_evidence": 0.20,
    "experience_evidence": 0.15,
    "role_alignment": 0.10,
    "education_evidence": 0.10,
    "certification_evidence": 0.05,
}
SOFT = set(SKILL_GROUPS["Business"].split("|")) | {
    "Conflict Resolution",
    "Customer Retention",
}
LANGUAGES = {
    "Python",
    "Java",
    "JavaScript",
    "TypeScript",
    "C++",
    "C#",
    "R",
    "Go",
    "Rust",
    "PHP",
    "Kotlin",
    "Swift",
    "Bash",
    "SQL",
}
TOOLS = {
    "Excel",
    "Power BI",
    "Tableau",
    "Pandas",
    "NumPy",
    "Photoshop",
    "Illustrator",
    "Canva",
    "Figma",
    "Git",
    "Docker",
    "PostgreSQL",
    "MySQL",
    "TensorFlow",
    "PyTorch",
    "Scikit-learn",
    "Zendesk",
    "Salesforce",
    "Jira",
}


def analyze_resume(text, fields=None):
    fields = fields or extract_resume_fields(text)
    skills = normalize_skills(fields["skills"])
    evidence_text = "\n".join(
        [
            fields.get("projects", ""),
            fields.get("experience_summary", ""),
            fields.get("certifications", ""),
        ]
    )
    evidence = set(extract_skills(evidence_text))
    inventory = [
        {
            "skill": skill,
            "category": "soft" if skill in SOFT else "technical",
            "evidence": "professional section" if skill in evidence else "mention only",
            "confidence": 0.85 if skill in evidence else 0.60,
            "method": "dictionary occurrence; confidence is a heuristic, not calibrated probability",
        }
        for skill in skills
    ]
    organizations = sorted(
        {
            value.strip()
            for value in re.findall(
                r"\b(?:at|company\s*:)\s+([A-Z][\w& .-]{1,70})(?=\n|\(|,|$)",
                fields.get("experience_summary", ""),
                re.M,
            )
        }
    )[:20]
    return {
        "technical_skills": [s for s in skills if s not in SOFT],
        "soft_skills": [s for s in skills if s in SOFT],
        "tools": [s for s in skills if s in TOOLS],
        "programming_languages": [s for s in skills if s in LANGUAGES],
        "domains": [
            group
            for group, values in SKILL_GROUPS.items()
            if set(values.split("|")) & set(skills)
        ],
        "education": fields.get("education", ""),
        "experience_summary": fields.get("experience_summary", ""),
        "years_of_experience": fields.get("experience_years"),
        "projects": fields.get("projects", ""),
        "certifications": fields.get("certifications", ""),
        "detected_roles": fields.get("job_titles", []),
        "organizations": organizations,
        "skill_inventory": inventory,
        "field_confidence": {
            key: 0.75 if fields.get(key) else 0.0
            for key in ["education", "projects", "certifications", "experience_summary"]
        },
        "experience_confidence": (
            0.8 if fields.get("experience_years") is not None else 0.0
        ),
        "method": "section headings, explicit year statements and skill dictionary; review all fields",
    }


def resume_quality(profile, intelligence, weights=None):
    import math

    weights = dict(weights or QUALITY_WEIGHTS)
    if (
        set(weights) != set(QUALITY_WEIGHTS)
        or any(
            not isinstance(w, (int, float)) or not math.isfinite(w) or not 0 <= w <= 1
            for w in weights.values()
        )
        or abs(sum(weights.values()) - 1) > 1e-9
    ):
        raise ValueError(
            "Resume quality weights must match the component contract and sum to one."
        )
    text = profile.get("resume_text", "")
    fields = ["education", "skills", "projects", "preferred_role", "resume_text"]
    inventory = intelligence["skill_inventory"]
    evidence = sum(row["evidence"] == "professional section" for row in inventory)
    project = profile.get("projects", "")
    experience = profile.get("experience_summary", "")
    role_skills = extract_skills(
        profile.get("preferred_role", "") + " " + profile.get("career_interests", "")
    )
    values = {
        "completeness": (
            100 * sum(bool(profile.get(field)) for field in fields) / len(fields),
            "Reviewed resume, target role, skills, projects and education are checked.",
        ),
        "skill_evidence": (
            100 * evidence / len(inventory) if inventory else 0,
            f"{evidence}/{len(inventory)} detected skills have mentions in a project, experience or certification section.",
        ),
        "project_evidence": (
            (
                100
                if project
                and re.search(r"\d+\s*(?:%|users|hours|records|rows)", project, re.I)
                else 65 if project else 0
            ),
            "Project text earns evidence points; a stated measurable result adds points. Its truth is not verified.",
        ),
        "experience_evidence": (
            (
                100
                if experience and profile.get("experience_years") is not None
                else 65 if experience else 0
            ),
            "An experience section and explicit years are checked. A fresher may reasonably have no work experience.",
        ),
        "role_alignment": (
            (
                100
                * len(set(role_skills) & set(profile.get("skills", [])))
                / len(role_skills)
                if role_skills
                else 50 if profile.get("preferred_role") else 0
            ),
            "Dictionary skills in the stated target role/interests are compared; unspecified role skills use a neutral 50.",
        ),
        "education_evidence": (
            100 if profile.get("education") else 0,
            "Presence of a reviewed education statement; no college prestige scoring.",
        ),
        "certification_evidence": (
            100 if profile.get("certifications") else 0,
            "Presence of reviewed certification text; issuing organizations are not verified.",
        ),
    }
    if not text:
        values = {
            key: (0.0, "Upload and review a readable resume to analyze its evidence.")
            for key in values
        }
    components = [
        {
            "name": key,
            "score": round(value, 1),
            "weight": weights[key],
            "points": round(value * weights[key], 2),
            "explanation": explanation,
        }
        for key, (value, explanation) in values.items()
    ]
    return {
        "score": round(sum(component["points"] for component in components), 1),
        "components": components,
        "label": "Resume Strength",
        "method": "Configurable evidence checklist; not an official ATS score, hiring prediction or verified credential assessment.",
    }
