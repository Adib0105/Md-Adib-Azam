from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import httpx
import yaml
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent
DB = ROOT / "jobs.db"

# Resume-backed vocabulary only. Expand after you can honestly demonstrate a skill.
PROFILE_TERMS = {
    "customer support": 12, "customer service": 12, "chat support": 12,
    "email support": 12, "technical support": 9, "crm": 9,
    "issue resolution": 8, "customer queries": 8, "ms excel": 6,
    "excel": 6, "ms office": 5, "python": 5, "mysql": 5,
    "wordpress": 3, "digital marketing": 5, "graphic design": 5,
    "canva": 3, "photoshop": 3, "illustrator": 3, "git": 2, "github": 2,
    "hindi": 4, "english": 3, "bengali": 3,
}

SCAM_PATTERNS = [
    r"registration fee", r"security deposit", r"pay.*training", r"payment.*apply",
    r"whatsapp only", r"telegram only", r"earn .* per day", r"no interview.*instant joining",
]

@dataclass
class Job:
    title: str
    company: str
    url: str
    description: str
    source: str
    posted_at: str = ""


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def init_db() -> sqlite3.Connection:
    con = sqlite3.connect(DB)
    con.execute("""CREATE TABLE IF NOT EXISTS jobs (
      id TEXT PRIMARY KEY, company TEXT, title TEXT, url TEXT, source TEXT,
      score INTEGER, verdict TEXT, status TEXT, reason TEXT,
      discovered_at TEXT, applied_at TEXT
    )""")
    return con


def job_id(job: Job) -> str:
    return hashlib.sha256(f"{job.company}|{job.title}|{job.url}".lower().encode()).hexdigest()[:20]


def scam_check(job: Job) -> tuple[bool, list[str]]:
    text = f"{job.title} {job.company} {job.description} {job.url}".lower()
    reasons = []
    if urlparse(job.url).scheme != "https": reasons.append("non-HTTPS application URL")
    for pattern in SCAM_PATTERNS:
        if re.search(pattern, text): reasons.append(f"suspicious phrase: {pattern}")
    return (len(reasons) == 0, reasons)


def score_job(job: Job, target_titles: list[str]) -> tuple[int, list[str]]:
    text = f"{job.title} {job.description}".lower()
    score = 0
    hits = []
    for term, weight in PROFILE_TERMS.items():
        if term in text:
            score += weight
            hits.append(term)
    title_lower = job.title.lower()
    if any(t.lower() in title_lower or title_lower in t.lower() for t in target_titles):
        score += 30
        hits.append("target title")
    if "remote" in text or "work from home" in text or "wfh" in text:
        score += 15
        hits.append("remote")
    return min(score, 100), hits


def greenhouse_jobs(board: str) -> list[Job]:
    """Public Greenhouse Job Board API discovery. No employer credentials required for reading jobs."""
    url = f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs?content=true"
    with httpx.Client(timeout=20, follow_redirects=True) as client:
        r = client.get(url)
        r.raise_for_status()
        data = r.json()
    jobs = []
    for item in data.get("jobs", []):
        content = BeautifulSoup(item.get("content", ""), "html.parser").get_text(" ", strip=True)
        jobs.append(Job(item["title"], board, item["absolute_url"], content, "Greenhouse", item.get("updated_at", "")))
    return jobs


def lever_jobs(site: str) -> list[Job]:
    """Public Lever postings API discovery."""
    url = f"https://api.lever.co/v0/postings/{site}?mode=json"
    with httpx.Client(timeout=20, follow_redirects=True) as client:
        r = client.get(url)
        r.raise_for_status()
        data = r.json()
    jobs = []
    for item in data:
        text = BeautifulSoup(item.get("descriptionPlain", "") or item.get("description", ""), "html.parser").get_text(" ", strip=True)
        company = site
        jobs.append(Job(item.get("text", ""), company, item.get("hostedUrl", ""), text, "Lever"))
    return jobs


def process(jobs: list[Job], cfg: dict) -> list[dict]:
    con = init_db()
    out = []
    targets = cfg["search"]["target_titles"]
    minimum = int(cfg["search"]["minimum_match_score"])
    for job in jobs:
        jid = job_id(job)
        if con.execute("SELECT 1 FROM jobs WHERE id=?", (jid,)).fetchone():
            continue
        safe, scam_reasons = scam_check(job)
        score, hits = score_job(job, targets)
        remote = any(x in job.description.lower() for x in ["remote", "work from home", "wfh"])
        if cfg["search"].get("remote_only", True) and not remote:
            verdict, reason = "SKIP", "not explicitly remote"
        elif not safe:
            verdict, reason = "SKIP", "; ".join(scam_reasons)
        elif score >= minimum:
            verdict, reason = "QUALIFIED", ", ".join(hits)
        else:
            verdict, reason = "REVIEW" if score >= 60 else "SKIP", f"match score {score}"
        con.execute("INSERT INTO jobs VALUES (?,?,?,?,?,?,?,?,?,?,?)", (
            jid, job.company, job.title, job.url, job.source, score, verdict,
            "FOUND", reason, datetime.now(timezone.utc).isoformat(), None))
        out.append({"id": jid, "company": job.company, "title": job.title, "url": job.url,
                    "score": score, "verdict": verdict, "reason": reason})
    con.commit(); con.close()
    return sorted(out, key=lambda x: x["score"], reverse=True)


def main():
    p = argparse.ArgumentParser(description="Truth-first remote job application agent")
    p.add_argument("--config", default=str(ROOT / "config.yaml"))
    p.add_argument("--greenhouse", action="append", default=[])
    p.add_argument("--lever", action="append", default=[])
    args = p.parse_args()
    cfg = load_config(args.config)
    jobs = []
    for board in args.greenhouse:
        try: jobs += greenhouse_jobs(board)
        except Exception as e: print(f"Greenhouse {board}: {e}")
    for site in args.lever:
        try: jobs += lever_jobs(site)
        except Exception as e: print(f"Lever {site}: {e}")
    results = process(jobs, cfg)
    print(json.dumps(results[:50], indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
