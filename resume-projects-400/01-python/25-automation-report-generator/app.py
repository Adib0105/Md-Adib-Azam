#!/usr/bin/env python3
"""Automation Report Generator - a tested, standard-library portfolio mini-project."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def solve(data: dict) -> dict:
    import html
    runs=data["runs"]; passed=sum(r["status"]=="success" for r in runs); rate=round(100*passed/len(runs),1) if runs else 0
    rows="".join(f"<tr><td>{html.escape(r['task'])}</td><td>{html.escape(r['status'])}</td><td>{r['duration_s']}</td></tr>" for r in runs)
    report=f"<h1>Automation Report</h1><p>Success rate: {rate}%</p><table><tr><th>Task</th><th>Status</th><th>Seconds</th></tr>{rows}</table>"
    return {"success_rate":rate,"failures":[r["task"] for r in runs if r["status"]!="success"],"html":report}


def main() -> None:
    parser = argparse.ArgumentParser(description='Automation Report Generator')
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
