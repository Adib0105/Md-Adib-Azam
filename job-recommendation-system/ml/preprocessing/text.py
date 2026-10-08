"""Use reviewed professional fields, never raw resume identity, in ranking."""

import re
import unicodedata
from models.skill_extractor import normalize_skills
from models.recommendation_model import education_level

PROFILE_FIELDS = {
    "skills",
    "education",
    "experience_years",
    "experience_summary",
    "projects",
    "certifications",
    "preferred_role",
    "career_interests",
    "preferred_location",
    "expected_salary",
    "salary_currency",
    "employment_type",
    "remote_preference",
    "state",
    "willing_to_relocate",
}
SENSITIVE_LINE = re.compile(
    r"\b(?:date of birth|dob|gender|marital status|religion|caste|nationality|"
    r"father(?:'s)? name|mother(?:'s)? name|passport|aadhaar|aadhar)\b",
    re.I,
)


def clean_text(value, limit=12000):
    text = unicodedata.normalize("NFKC", str(value or ""))[:limit]
    text = " ".join(
        line for line in text.splitlines() if not SENSITIVE_LINE.search(line)
    )
    text = re.sub(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b", " ", text)
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"(?<!\w)\+?\d[\d ()-]{7,}\d(?!\w)", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def professional_profile(profile):
    result = {key: profile[key] for key in PROFILE_FIELDS if key in profile}
    result["skills"] = normalize_skills(result.get("skills"))
    return result


def candidate_text(profile):
    # Exclude names, contacts, organization names, raw resume text and degree brands.
    fields = [
        "experience_summary",
        "projects",
        "certifications",
        "preferred_role",
        "career_interests",
    ]
    return clean_text(
        " ".join(
            [" ".join(normalize_skills(profile.get("skills")))]
            + [clean_text(profile.get(key), 5000) for key in fields]
        ),
        30000,
    )


def job_text(job):
    return clean_text(
        " ".join(
            [
                str(job.job_title or ""),
                str(job.job_description or ""),
                " ".join(normalize_skills(job.required_skills)),
                " ".join(normalize_skills(job.preferred_skills)),
            ]
        ),
        20000,
    )


def education_feature(text):
    """Only qualification level is used; college prestige is not a signal."""
    return education_level(text)
