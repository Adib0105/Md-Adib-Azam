from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from urllib.parse import urlparse

TRUSTED_ATS = {
    "greenhouse.io", "boards.greenhouse.io", "job-boards.greenhouse.io",
    "lever.co", "jobs.lever.co", "workable.com", "apply.workable.com",
    "breezy.hr", "ashbyhq.com", "jobs.ashbyhq.com", "smartrecruiters.com",
}

SCAM_RULES = {
    "payment_requested": (r"registration fee|security deposit|pay(?:ment)? for (?:training|interview|application)|refundable deposit", 55),
    "messaging_only": (r"whatsapp only|telegram only|contact.*telegram|dm on whatsapp", 25),
    "unrealistic_income": (r"earn\s*(?:rs\.?|₹)?\s*\d{4,}\s*(?:per day|daily)", 20),
    "instant_hire": (r"no interview.*instant joining|100% guaranteed job|guaranteed selection", 25),
    "sensitive_request": (r"otp|upi pin|bank password|card cvv", 100),
}

SENIOR_MARKERS = ["senior", "lead", "manager", "principal", "director", "head of", "architect"]
ENTRY_MARKERS = ["junior", "associate", "executive", "intern", "trainee", "l1", "level 1", "fresher"]

@dataclass
class Intelligence:
    remote: bool
    remote_evidence: list[str]
    scam_score: int
    scam_flags: list[str]
    trusted_host: bool
    seniority: str
    hard_requirements: list[str]
    review_reasons: list[str]


def host_is_trusted(url: str) -> bool:
    host = (urlparse(url).hostname or "").lower()
    return any(host == d or host.endswith("." + d) for d in TRUSTED_ATS)


def analyze_text(title: str, description: str, url: str) -> Intelligence:
    text = f"{title}\n{description}".lower()
    remote_evidence = []
    for phrase in ["fully remote", "100% remote", "work from home", "wfh", "remote india", "india - remote", "india remote"]:
        if phrase in text:
            remote_evidence.append(phrase)
    remote = bool(remote_evidence)

    scam_score, scam_flags = 0, []
    for name, (pattern, weight) in SCAM_RULES.items():
        if re.search(pattern, text, re.I):
            scam_score += weight
            scam_flags.append(name)
    scam_score = min(scam_score, 100)

    t = title.lower()
    if any(x in t for x in SENIOR_MARKERS): seniority = "senior"
    elif any(x in t for x in ENTRY_MARKERS): seniority = "entry"
    else: seniority = "unspecified"

    reqs = []
    patterns = [
        r"(?:minimum|at least)\s+\d+\+?\s+years?[^.;\n]*",
        r"\d+\+?\s+years? (?:of )?experience[^.;\n]*",
        r"bachelor'?s degree[^.;\n]*", r"graduate[^.;\n]*",
        r"night shift[^.;\n]*", r"rotational shift[^.;\n]*",
        r"typing speed[^.;\n]*", r"\d+\s*wpm[^.;\n]*",
    ]
    for p in patterns:
        reqs.extend(m.group(0).strip() for m in re.finditer(p, text, re.I))

    review = []
    if not remote: review.append("Remote status is not explicit")
    if seniority == "senior": review.append("Title appears senior for current target profile")
    if scam_score >= 40: review.append("High scam-risk signals")
    if not host_is_trusted(url): review.append("Application host is not in trusted ATS allow-list; verify employer domain")

    return Intelligence(remote, remote_evidence, scam_score, scam_flags, host_is_trusted(url), seniority,
                        list(dict.fromkeys(reqs))[:12], review)


def as_record(x: Intelligence) -> dict:
    d = asdict(x)
    d["analyzed_at"] = datetime.now(timezone.utc).isoformat()
    return d
