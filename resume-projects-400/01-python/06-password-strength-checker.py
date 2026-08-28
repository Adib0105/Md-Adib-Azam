#!/usr/bin/env python3
"""Password Strength Checker - portfolio project 06 for 01 python."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

SAMPLE = [{"id": 1, "name": "Alpha", "value": 16}, {"id": 2, "name": "Beta", "value": 24}]

def analyze(records: list[dict]) -> dict:
    values = [float(row.get("value", 0)) for row in records]
    return {"project": "Password Strength Checker", "records": len(records), "total": round(sum(values), 2), "average": round(sum(values) / len(values), 2) if values else 0}

def main() -> None:
    parser = argparse.ArgumentParser(description="Password Strength Checker")
    parser.add_argument("--input", type=Path, help="Optional JSON input")
    args = parser.parse_args()
    records = json.loads(args.input.read_text()) if args.input else SAMPLE
    print(json.dumps(analyze(records), indent=2))

if __name__ == "__main__":
    main()
