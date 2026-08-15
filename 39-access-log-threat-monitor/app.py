from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


LOG_PATTERN = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ \[[^\]]+\] "(?P<method>[A-Z]+) (?P<path>\S+) [^"]+" (?P<status>\d{3}) (?P<size>\S+)'
)
PROTECTED_PATHS = ("/admin", "/login", "/wp-login.php", "/.env")


def parse_line(line: str) -> dict[str, object] | None:
    match = LOG_PATTERN.match(line)
    if not match:
        return None
    data = match.groupdict()
    return {
        "ip": data["ip"],
        "method": data["method"],
        "path": data["path"],
        "status": int(data["status"]),
    }


def analyze(lines: list[str], threshold: int = 3) -> dict[str, object]:
    records = [record for line in lines if (record := parse_line(line))]
    error_counts = Counter(
        record["ip"] for record in records if record["status"] in {401, 403, 404}
    )
    protected_counts = Counter(
        record["ip"]
        for record in records
        if any(record["path"].startswith(path) for path in PROTECTED_PATHS)
    )
    alerts = []
    for ip, count in error_counts.items():
        if count >= threshold:
            alerts.append({"ip": ip, "type": "repeated access errors", "count": count})
    for ip, count in protected_counts.items():
        if count >= threshold:
            alerts.append({"ip": ip, "type": "protected path activity", "count": count})
    return {
        "parsed_requests": len(records),
        "status_counts": dict(Counter(record["status"] for record in records)),
        "top_sources": Counter(record["ip"] for record in records).most_common(5),
        "alerts": alerts,
        "note": "Alerts are review signals, not proof of malicious activity.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("log_file", type=Path)
    parser.add_argument("--threshold", type=int, default=3)
    args = parser.parse_args()
    lines = args.log_file.read_text(encoding="utf-8").splitlines()
    print(json.dumps(analyze(lines, args.threshold), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
