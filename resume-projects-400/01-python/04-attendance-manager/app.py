#!/usr/bin/env python3
"""Attendance Manager - a tested, standard-library portfolio mini-project."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def solve(data: dict) -> dict:
    threshold=data.get("threshold",75)
    results=[]
    for s in data["students"]:
        pct=round(100*s["present"]/s["classes"],2) if s["classes"] else 0
        results.append({"name":s["name"],"attendance_pct":pct,"eligible":pct>=threshold})
    return {"threshold":threshold,"students":results,"shortage":[r["name"] for r in results if not r["eligible"]]}


def main() -> None:
    parser = argparse.ArgumentParser(description='Attendance Manager')
    parser.add_argument("--input", type=Path, default=Path('sample.json'))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = solve(json.loads(args.input.read_text(encoding="utf-8")))
    rendered = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
