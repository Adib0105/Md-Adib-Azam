from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path


CATEGORY_RULES = {
    "billing": {"charged", "payment", "refund", "invoice", "billing"},
    "account": {"account", "profile", "email", "verification"},
    "login": {"login", "password", "otp", "sign in", "locked"},
    "delivery": {"delivery", "shipment", "tracking", "courier", "late"},
    "technical": {"error", "crash", "bug", "loading", "not working"},
}
URGENT_WORDS = {"urgent", "immediately", "blocked", "critical", "today"}
NEGATIVE_WORDS = {"angry", "bad", "terrible", "frustrated", "disappointed"}


def classify(message: str) -> dict[str, str]:
    text = message.lower()
    scores = {
        category: sum(term in text for term in terms)
        for category, terms in CATEGORY_RULES.items()
    }
    category = max(scores, key=scores.get)
    if scores[category] == 0:
        category = "general"

    urgent = any(word in text for word in URGENT_WORDS)
    negative = any(word in text for word in NEGATIVE_WORDS)
    priority = "high" if urgent or negative else "normal"
    return {
        "category": category,
        "priority": priority,
        "tone": "negative" if negative else "neutral",
    }


def process(input_path: Path, output_path: Path) -> Counter:
    with input_path.open(newline="", encoding="utf-8") as source:
        rows = list(csv.DictReader(source))
    enriched = []
    for row in rows:
        enriched.append({**row, **classify(row.get("message", ""))})

    fieldnames = list(enriched[0]) if enriched else [
        "ticket_id", "message", "category", "priority", "tone"
    ]
    with output_path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(enriched)
    return Counter(row["category"] for row in enriched)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, default=Path("enriched_tickets.csv"))
    args = parser.parse_args()
    summary = process(args.input, args.output)
    print("Category summary")
    for category, count in summary.most_common():
        print(f"- {category}: {count}")
    print(f"Saved: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
