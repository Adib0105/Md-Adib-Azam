#!/usr/bin/env python3
"""Secure Backup Verifier - portfolio project 09 for 16 cybersecurity automation."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

SAMPLE = [{"id": 1, "name": "Alpha", "value": 19}, {"id": 2, "name": "Beta", "value": 27}]

def analyze(records: list[dict]) -> dict:
    values = [float(row.get("value", 0)) for row in records]
    return {"project": "Secure Backup Verifier", "records": len(records), "total": round(sum(values), 2), "average": round(sum(values) / len(values), 2) if values else 0}

def main() -> None:
    parser = argparse.ArgumentParser(description="Secure Backup Verifier")
    parser.add_argument("--input", type=Path, help="Optional JSON input")
    args = parser.parse_args()
    records = json.loads(args.input.read_text()) if args.input else SAMPLE
    print(json.dumps(analyze(records), indent=2))

if __name__ == "__main__":
    main()
