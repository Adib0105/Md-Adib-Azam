"""Deterministic, explainable hybrid ranking; scores are not hiring probabilities."""

import re
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from models.skill_extractor import normalize_skills
from utils.constants import CITY_STATES


def bounded(number):
    return float(np.clip(number, 0, 100))


def get_matching_skills(candidate, required):
    names = {s.casefold() for s in normalize_skills(candidate)}
    return [s for s in normalize_skills(required) if s.casefold() in names]


def get_missing_skills(candidate, required):
    names = {s.casefold() for s in normalize_skills(candidate)}
    return [s for s in normalize_skills(required) if s.casefold() not in names]


def calculate_skill_score(candidate, required, preferred=None):
    required, preferred = normalize_skills(required), normalize_skills(preferred)
    preferred = get_missing_skills(required, preferred)
    if not required and not preferred:
        return 50.0  # Employer requirements are unknown, not a perfect match.
    required_ratio = (
        len(get_matching_skills(candidate, required)) / len(required) if required else 0
    )
    preferred_ratio = (
        len(get_matching_skills(candidate, preferred)) / len(preferred)
        if preferred
        else 0
    )
    if not preferred:
        return 100 * required_ratio
    if not required:
        return 100 * preferred_ratio
    return 100 * (0.85 * required_ratio + 0.15 * preferred_ratio)


def calculate_semantic_similarity(candidate_vector, job_vectors):
    """TF-IDF cosine measures lexical overlap, not deep language understanding."""
    return np.clip(
        cosine_similarity(candidate_vector, job_vectors).ravel() * 100, 0, 100
    )


def calculate_experience_score(candidate, minimum=0, maximum=None):
    if candidate is None:
        return 50.0
    minimum = max(float(minimum or 0), 0)
    candidate = max(float(candidate), 0)
    if candidate < minimum:
        return bounded(100 * candidate / minimum)
    # Exceeding experience is not treated as disqualification.
    return 100.0


EDUCATION_PATTERNS = [
    (5, r"\b(ph\.?d|doctorate)\b"),
    (4, r"\b(m\.?\s?tech|mca|mba|m\.?\s?sc|m\.?\s?a|master(?:s|['’]s)?)\b"),
    (
        3,
        r"\b(b\.?\s?tech|b\.?\s?e|bca|b\.?\s?sc|b\.?\s?a|bcom|b\.?\s?com|bachelor(?:s|['’]s)?|graduate|graduation)\b",
    ),
    (2, r"\b(diploma|polytechnic|associate)\b"),
    (1, r"\b(12th|class\s*xii|higher secondary|hsc)\b"),
    (0, r"\b(10th|class\s*x|secondary|ssc)\b"),
]


def education_level(text):
    for level, pattern in EDUCATION_PATTERNS:
        if re.search(pattern, str(text or ""), re.I):
            return level
    return None


def calculate_education_score(candidate, required):
    if not required or str(required).casefold() in {
        "any",
        "not required",
        "any education",
    }:
        return 100.0
    candidate_level, required_level = (
        education_level(candidate),
        education_level(required),
    )
    if candidate_level is None or required_level is None:
        return 50.0
    return bounded(100 - max(required_level - candidate_level, 0) * 25)


def city_key(text):
    text = str(text or "").strip().casefold()
    return {"bengaluru": "bangalore", "gurgaon": "gurugram"}.get(text, text)


def calculate_location_score(preferred, job_location, state="", relocate=False):
    location = city_key(job_location)
    if location == "remote":
        return 100.0
    if not location or location == "unspecified":
        return 50.0
    choices = [city_key(x) for x in re.split(r"[,/;|]", preferred or "") if x.strip()]
    if not choices and not state:
        return 50.0
    if location in choices:
        return 100.0
    job_state = CITY_STATES.get(location, "").casefold()
    # A declared preference takes precedence over the candidate's current state.
    preferred_states = {
        CITY_STATES.get(choice, choice).casefold() for choice in choices
    }
    if not choices and state:
        preferred_states.add(state.casefold())
    if job_state and job_state in preferred_states:
        return 80.0
    return 85.0 if relocate else 30.0


def calculate_salary_score(expected, minimum, maximum):
    if expected is None or expected <= 0 or maximum is None:
        return 50.0
    if expected <= maximum:
        return 100.0
    return bounded(100 * maximum / expected)


ROLE_FAMILIES = {
    "data analyst": "analytics reporting insights dashboards",
    "business intelligence": "analytics reporting insights dashboards",
    "power bi": "analytics reporting insights dashboards",
    "mis": "analytics reporting insights dashboards",
    "business analyst": "analytics requirements process stakeholder",
    "data scientist": "analytics statistics machine learning modeling",
    "machine learning": "statistics machine learning modeling",
    "python developer": "software programming backend python",
    "web developer": "software programming frontend web",
    "software developer": "software programming development",
}


def role_text(text):
    value = str(text or "").casefold()
    return (
        value
        + " "
        + " ".join(
            expansion for term, expansion in ROLE_FAMILIES.items() if term in value
        )
    )


def calculate_role_score(vector, matrix):
    return calculate_semantic_similarity(vector, matrix)


def calculate_final_score(scores, weights):
    return round(
        bounded(sum(scores[key] * weight for key, weight in weights.items())), 1
    )


def generate_recommendation_explanation(profile, job, scores, matched, missing):
    reasons = [f"{len(matched)} of {len(job.required_skills)} required skills matched."]
    if matched:
        reasons.append("Shared skills: " + ", ".join(matched[:5]) + ".")
    experience = profile.get("experience_years")
    if experience is None or job.experience_known is False:
        reasons.append("Experience is unknown; a neutral 50/100 is used.")
    elif experience >= job.experience_min:
        reasons.append(
            f"Your {experience:g} years meet the minimum of {job.experience_min:g} years."
        )
    else:
        reasons.append(
            f"Experience gap: {job.experience_min - experience:g} years below the minimum; no automatic rejection."
        )
    if scores["salary"] == 100:
        reasons.append("The listed salary can meet your annual expectation.")
    elif (
        profile.get("expected_salary") is None
        or job.max_salary is None
        or (job.salary_currency or "INR") != profile.get("salary_currency", "INR")
        or (job.salary_period or "year") != "year"
    ):
        reasons.append(
            "Salary information is incomplete or uses a different currency/pay period; a neutral 50/100 is used."
        )
    else:
        reasons.append("The maximum listed salary is below your expectation.")
    if scores["location"] == 100:
        reasons.append("This is remote or matches a preferred city.")
    elif scores["location"] == 80:
        reasons.append("This location shares a state with your preference.")
    if (
        profile.get("employment_type")
        and profile["employment_type"] != job.employment_type
    ):
        reasons.append(
            "Employment type differs from your preference; use the type filter if this is a requirement."
        )
    if missing:
        reasons.append(f"{len(missing)} required skills still need review or learning.")
    return reasons


def match_label(score):
    return (
        "Excellent match"
        if score >= 90
        else "Strong match"
        if score >= 80
        else "Good match"
        if score >= 70
        else "Moderate match"
        if score >= 60
        else "Low match"
    )
