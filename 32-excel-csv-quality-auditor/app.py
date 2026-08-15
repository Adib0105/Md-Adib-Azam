from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path


EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def audit(rows: list[dict[str, str]], numeric_columns: set[str] | None = None) -> dict[str, object]:
    numeric_columns = numeric_columns or set()
    if not rows:
        return {"rows": 0, "columns": [], "missing": {}, "duplicate_rows": 0, "issues": []}

    columns = list(rows[0])
    missing = {
        column: sum(not row.get(column, "").strip() for row in rows)
        for column in columns
    }
    signatures = [tuple(row.get(column, "").strip().lower() for column in columns) for row in rows]
    duplicate_rows = sum(count - 1 for count in Counter(signatures).values() if count > 1)
    issues = []
    seen_emails: set[str] = set()

    for number, row in enumerate(rows, start=2):
        email = row.get("email", "").strip().lower()
        if email and not EMAIL.match(email):
            issues.append({"row": number, "column": "email", "issue": "invalid email"})
        if email in seen_emails:
            issues.append({"row": number, "column": "email", "issue": "duplicate email"})
        if email:
            seen_emails.add(email)
        for column in numeric_columns:
            value = row.get(column, "").strip()
            if value:
                try:
                    float(value)
                except ValueError:
                    issues.append({"row": number, "column": column, "issue": "not numeric"})

    completeness = round(
        100 * (len(rows) * len(columns) - sum(missing.values())) / (len(rows) * len(columns)),
        1,
    )
    return {
        "rows": len(rows),
        "columns": columns,
        "completeness_percent": completeness,
        "missing": missing,
        "duplicate_rows": duplicate_rows,
        "issues": issues,
    }


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as source:
        return list(csv.DictReader(source))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("--numeric", nargs="*", default=[])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit(read_csv(args.csv_file), set(args.numeric))
    report = json.dumps(result, indent=2)
    print(report)
    if args.output:
        args.output.write_text(report + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
