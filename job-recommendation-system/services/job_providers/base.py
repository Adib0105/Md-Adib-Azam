import hashlib
import json
import math
import re
import unicodedata
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.parse import urlencode
from urllib.request import Request, build_opener, HTTPRedirectHandler
from urllib.error import HTTPError, URLError
from models.database import utcnow
from models.skill_extractor import extract_skills
from utils.validators import safe_external_url, ValidationError


class ProviderError(Exception):
    """Only a safe error code/message, never a credential-bearing request URL."""


@dataclass
class ProviderResult:
    jobs: list
    total: int
    skipped: int = 0


class TextOnly(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, value):
        self.parts.append(value)


def plain(value, maximum=12000):
    parser = TextOnly()
    parser.feed(str(value or "")[: maximum * 4])
    return re.sub(r"\s+", " ", " ".join(parser.parts)).strip()[:maximum]


def source_datetime(value):
    try:
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if dt.tzinfo:
            dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
        return dt
    except (ValueError, TypeError):
        return None


def salary_number(value):
    try:
        number = float(value)
        return (
            round(number)
            if math.isfinite(number) and 0 <= number <= 100000000
            else None
        )
    except (TypeError, ValueError):
        return None


def fingerprint(title, company, location):
    def normalized(value):
        value = unicodedata.normalize("NFKC", value).casefold()
        return " ".join(re.findall(r"\w+", value))

    return hashlib.sha256(
        "|".join(normalized(v) for v in (title, company, location)).encode()
    ).hexdigest()


def normalize_common(
    *,
    provider,
    source_name,
    external_id,
    title,
    company,
    description,
    location,
    url,
    created=None,
    updated=None,
    deadline=None,
    minimum=None,
    maximum=None,
    currency="INR",
    period="year",
    employment="Other",
    industry="Other",
    remote="unknown",
    education="",
    metadata=None,
):
    title, company, location = (
        plain(title, 160),
        plain(company, 160),
        plain(location, 100) or "Unspecified",
    )
    identifier = str(external_id or "").strip()
    if not title or not company or not identifier or len(identifier) > 180:
        raise ValidationError("Provider record is missing required identity fields.")
    url = safe_external_url(url, required=True)
    description = plain(description)
    posted, changed, closing = (
        source_datetime(created),
        source_datetime(updated),
        source_datetime(deadline),
    )
    if posted and posted > utcnow():
        posted = None
    low, high = salary_number(minimum), salary_number(maximum)
    if low is not None and high is not None and low > high:
        low, high = high, low
    return {
        "job_title": title,
        "company_name": company,
        "job_description": description,
        "location": location,
        "state": "",
        "required_skills": extract_skills(description + " " + title),
        "preferred_skills": [],
        "min_salary": low,
        "max_salary": high,
        "salary_currency": currency,
        "salary_period": period,
        "employment_type": employment,
        "industry": plain(industry, 80) or "Other",
        "education_required": plain(education, 160),
        "experience_min": 0,
        "experience_max": None,
        "experience_known": False,
        "posted_date": (posted or utcnow()).date(),
        "application_deadline": closing.date() if closing else None,
        "company_rating": None,
        "source": provider,
        "source_name": source_name,
        "external_id": identifier,
        "source_url": url,
        "external_created_at": posted,
        "external_updated_at": changed,
        "is_external": True,
        "is_synthetic": False,
        "remote_type": remote,
        "remote_allowed": remote == "remote",
        "fingerprint": fingerprint(title, company, location),
        "raw_source_data": metadata or {},
    }


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ProviderError("Provider redirect refused.")


def fetch_json(url, parameters, headers, config):
    request = Request(
        url + "?" + urlencode(parameters),
        headers={"Accept": "application/json", **headers},
    )
    try:
        with build_opener(NoRedirect()).open(
            request, timeout=config.get("PROVIDER_TIMEOUT_SECONDS", 8)
        ) as response:
            limit = config.get("PROVIDER_MAX_RESPONSE_BYTES", 2 * 1024 * 1024)
            data = response.read(limit + 1)
            if len(data) > limit:
                raise ProviderError("Provider response exceeded the size limit.")
            value = json.loads(data.decode("utf-8"))
            if not isinstance(value, dict):
                raise ProviderError("Provider response format was invalid.")
            return value
    except HTTPError as exc:
        raise ProviderError(f"Provider returned HTTP {exc.code}.") from None
    except (URLError, OSError, ValueError, UnicodeError):
        raise ProviderError(
            "Provider request failed or returned invalid JSON."
        ) from None


class JobProviderBase(ABC):
    slug = ""
    name = ""

    def __init__(self, config, transport=None, lookup=None):
        self.config = config
        self.transport = transport or fetch_json
        self.lookup = lookup

    @property
    @abstractmethod
    def configured(self): ...
    @abstractmethod
    def search_jobs(self, **filters): ...
    @abstractmethod
    def normalize_job(self, raw, **context): ...
    def get_job(self, external_id):
        """Cache-backed lookup; neither provider is given an invented detail endpoint."""
        return self.lookup(self.slug, str(external_id)) if self.lookup else None

    def health_check(self):
        if not self.configured:
            return {"available": False, "status": "not_configured"}
        self.search_jobs(
            q="data",
            country="us" if self.slug == "usajobs" else "in",
            per_page=1,
            page=1,
        )
        return {"available": True, "status": "ok"}

    def normalize_results(self, records, total, **context):
        if not isinstance(records, list):
            raise ProviderError("Provider results format was invalid.")
        jobs, skipped = [], 0
        for raw in records[:50]:
            try:
                jobs.append(self.normalize_job(raw, **context))
            except (ValidationError, TypeError, ValueError, KeyError, AttributeError):
                skipped += 1
        try:
            total = max(0, min(int(total), 10000000))
        except (ValueError, TypeError):
            total = len(jobs)
        return ProviderResult(jobs, total, skipped)
