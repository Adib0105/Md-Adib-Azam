from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


STOP_WORDS = {
    "and", "the", "with", "for", "that", "this", "from", "are", "our",
    "you", "your", "will", "have", "has", "into", "using", "who", "but",
    "not", "all", "any", "job", "role", "work", "team", "years", "year",
}


def tokenize(text: str) -> list[str]:
    return [
        token
        for token in re.findall(r"[a-z0-9+#.]+", text.lower())
        if len(token) > 2 and token not in STOP_WORDS
    ]


def match_resume(resume_text: str, job_text: str) -> dict[str, object]:
    resume_terms = set(tokenize(resume_text))
    job_counts = Counter(tokenize(job_text))
    if not job_counts:
        raise ValueError("The job description has no useful keywords.")

    total_weight = sum(job_counts.values())
    matched_weight = sum(
        count for term, count in job_counts.items() if term in resume_terms
    )
    ranked = sorted(
        job_counts,
        key=lambda term: (-job_counts[term], term),
    )
    matched = [term for term in ranked if term in resume_terms]
    missing = [term for term in ranked if term not in resume_terms]
    score = round(matched_weight * 100 / total_weight, 1)

    if score >= 75:
        verdict = "strong match"
    elif score >= 50:
        verdict = "good foundation"
    else:
        verdict = "needs tailoring"

    return {
        "match_score": score,
        "verdict": verdict,
        "matched_keywords": matched[:15],
        "missing_keywords": missing[:12],
        "recommendation": (
            "Add only skills you genuinely have; support them with project evidence."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare a resume with a job.")
    parser.add_argument("resume", type=Path)
    parser.add_argument("job", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = match_resume(
        args.resume.read_text(encoding="utf-8"),
        args.job.read_text(encoding="utf-8"),
    )
    output = json.dumps(result, indent=2)
    print(output)
    if args.output:
        args.output.write_text(output + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
