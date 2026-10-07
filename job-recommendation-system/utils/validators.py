import math
import re
import ipaddress
from datetime import date
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
from models.skill_extractor import normalize_skills
from utils.constants import EMPLOYMENT_TYPES


class ValidationError(ValueError):
    pass


def text_field(form, key, maximum, required=False):
    value = str(form.get(key, "")).strip()
    if required and not value:
        raise ValidationError(f"{key.replace('_', ' ').title()} is required.")
    if len(value) > maximum:
        raise ValidationError(
            f"{key.replace('_', ' ').title()} must be at most {maximum} characters."
        )
    return value


def number_field(form, key, maximum, integer=False):
    value = str(form.get(key, "")).replace(",", "").strip()
    if not value:
        return None
    try:
        parsed = float(value)
    except ValueError as exc:
        raise ValidationError(f"Enter a valid {key.replace('_', ' ')}.") from exc
    if not math.isfinite(parsed) or not 0 <= parsed <= maximum:
        raise ValidationError(
            f"{key.replace('_', ' ').title()} must be between 0 and {maximum:g}."
        )
    if integer and not parsed.is_integer():
        raise ValidationError(
            f"{key.replace('_', ' ').title()} must be a whole number."
        )
    return int(parsed) if integer else parsed


def validate_email(value):
    value = value.strip().casefold()
    if len(value) > 254 or not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", value):
        raise ValidationError("Enter a valid email address.")
    return value


def validate_password(value):
    if len(value) < 8 or len(value) > 128:
        raise ValidationError("Use a password containing 8–128 characters.")
    if not re.search(r"[A-Za-z]", value) or not re.search(r"\d", value):
        raise ValidationError(
            "Include at least one letter and one number in your password."
        )
    return value


def validate_skills(value):
    if len(str(value)) > 6000:
        raise ValidationError("The skills list is too long.")
    skills = normalize_skills(value)
    if len(skills) > 80:
        raise ValidationError("Add at most 80 skills.")
    return skills


def validate_profile(form):
    limits = {
        "full_name": 100,
        "phone": 30,
        "city": 80,
        "state": 80,
        "country": 80,
        "education": 180,
        "experience_summary": 5000,
        "preferred_role": 160,
        "preferred_location": 160,
        "employment_type": 50,
        "certifications": 5000,
        "projects": 5000,
        "career_interests": 3000,
    }
    result = {
        k: text_field(form, k, n, required=k == "full_name") for k, n in limits.items()
    }
    if result["employment_type"] and result["employment_type"] not in EMPLOYMENT_TYPES:
        raise ValidationError("Choose a supported employment type.")
    result["experience_years"] = number_field(form, "experience_years", 60)
    result["expected_salary"] = number_field(form, "expected_salary", 100000000, True)
    result["willing_to_relocate"] = form.get("willing_to_relocate") == "on"
    result["remote_preference"] = choice_field(
        form, "remote_preference", {"any", "remote", "hybrid", "onsite"}, "any"
    )
    result["salary_currency"] = choice_field(form, "salary_currency", CURRENCIES, "INR")
    return result, validate_skills(form.get("skills", ""))


CURRENCIES = {
    "INR",
    "USD",
    "GBP",
    "EUR",
    "AUD",
    "CAD",
    "NZD",
    "SGD",
    "ZAR",
    "BRL",
    "MXN",
    "PLN",
    "CHF",
}


def choice_field(form, key, choices, default=""):
    value = str(form.get(key, default)).strip()
    if value not in choices:
        raise ValidationError(f"Choose a valid {key.replace('_', ' ')}.")
    return value


def date_field(form, key):
    value = str(form.get(key, "")).strip()
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValidationError(f"Enter a valid {key.replace('_', ' ')}.") from exc


def safe_external_url(value, required=False):
    value = str(value or "").strip()
    if not value and not required:
        return ""
    if len(value) > 2048 or any(ord(c) < 33 for c in value) or "\\" in value:
        raise ValidationError("Use a valid public HTTP or HTTPS address.")
    try:
        parsed = urlsplit(value)
        host = (parsed.hostname or "").rstrip(".").lower()
        if (
            parsed.scheme not in {"http", "https"}
            or not host
            or parsed.username
            or parsed.password
        ):
            raise ValueError()
        if (
            parsed.port not in {None, 80, 443}
            or host == "localhost"
            or host.endswith((".localhost", ".local", ".internal"))
            or "." not in host
        ):
            raise ValueError()
        try:
            address = ipaddress.ip_address(host)
        except ValueError:
            address = None
        if address is not None and not address.is_global:
            raise ValueError()
        # Provider attribution links never carry credential query parameters.
        blocked = {
            "app_key",
            "app_id",
            "api_key",
            "apikey",
            "authorization",
            "password",
            "secret",
        }
        query = urlencode(
            [
                (k, v)
                for k, v in parse_qsl(parsed.query, keep_blank_values=True)
                if k.casefold() not in blocked
            ]
        )
        return urlunsplit(
            (parsed.scheme, parsed.netloc, parsed.path, query, parsed.fragment)
        )
    except (ValueError, UnicodeError) as exc:
        raise ValidationError("Use a valid public HTTP or HTTPS address.") from exc
