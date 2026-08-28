#!/usr/bin/env python3
"""SSL Expiry Monitor - portfolio project 17 for 16 cybersecurity automation."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

SAMPLE = [{"id": 1, "name": "Alpha", "value": 27}, {"id": 2, "name": "Beta", "value": 35}]

def analyze(records: list[dict]) -> dict:
    values = [float(row.get("value", 0)) for row in records]
    return {"project": "SSL Expiry Monitor", "records": len(records), "total": round(sum(values), 2), "average": round(sum(values) / len(values), 2) if values else 0}

def main() -> None:
    parser = argparse.ArgumentParser(description="SSL Expiry Monitor")
    parser.add_argument("--input", type=Path, help="Optional JSON input")
    args = parser.parse_args()
    records = json.loads(args.input.read_text()) if args.input else SAMPLE
    print(json.dumps(analyze(records), indent=2))

if __name__ == "__main__":
    main()
