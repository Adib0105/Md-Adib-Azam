#!/usr/bin/env python3
"""Task Scheduler - a tested, standard-library portfolio mini-project."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def solve(data: dict) -> dict:
    from datetime import date
    today=date.fromisoformat(data["today"]); output=[]
    for task in data["tasks"]:
        due=date.fromisoformat(task["due"]); days=(due-today).days
        status="done" if task.get("done") else "overdue" if days<0 else "due-soon" if days<=3 else "upcoming"
        output.append({**task,"days_remaining":days,"status":status})
    return {"tasks":sorted(output,key=lambda x:(x["done"],x["due"])),"overdue":sum(x["status"]=="overdue" for x in output)}


def main() -> None:
    parser = argparse.ArgumentParser(description='Task Scheduler')
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
