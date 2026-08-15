from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


RECOMMENDATIONS = {
    "content-security-policy": "Define trusted sources with a Content-Security-Policy.",
    "strict-transport-security": "Enable HSTS with max-age of at least 31536000 on HTTPS.",
    "x-content-type-options": "Set X-Content-Type-Options to nosniff.",
    "referrer-policy": "Set a privacy-aware Referrer-Policy.",
    "permissions-policy": "Disable browser features the site does not need.",
}


def audit(headers: dict[str, str]) -> dict[str, object]:
    normalized = {key.lower(): str(value).strip() for key, value in headers.items()}
    checks = {}
    for header, recommendation in RECOMMENDATIONS.items():
        value = normalized.get(header, "")
        passed = bool(value)
        if header == "strict-transport-security" and value:
            match = re.search(r"max-age=(\d+)", value.lower())
            passed = bool(match and int(match.group(1)) >= 31_536_000)
        if header == "x-content-type-options" and value:
            passed = value.lower() == "nosniff"
        checks[header] = {
            "passed": passed,
            "value": value or "missing",
            "recommendation": "" if passed else recommendation,
        }
    passed_count = sum(item["passed"] for item in checks.values())
    return {
        "score": passed_count * 20,
        "passed": passed_count,
        "total": len(checks),
        "checks": checks,
        "scope": "Offline configuration review only",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("headers_json", type=Path)
    args = parser.parse_args()
    headers = json.loads(args.headers_json.read_text(encoding="utf-8"))
    print(json.dumps(audit(headers), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
