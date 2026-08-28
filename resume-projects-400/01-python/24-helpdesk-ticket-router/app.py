#!/usr/bin/env python3
"""Helpdesk Ticket Router - a tested, standard-library portfolio mini-project."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def solve(data: dict) -> dict:
    text=(data["subject"]+" "+data["message"]).lower()
    rules={"billing":["refund","payment","invoice"],"technical":["error","login","bug","password"],"delivery":["late","delivery","tracking"]}
    scores={team:sum(word in text for word in words) for team,words in rules.items()}
    team=max(scores,key=scores.get) if max(scores.values()) else "general"
    urgent=any(w in text for w in ["urgent","blocked","cannot access","security"])
    priority="P1" if urgent and data.get("affected_users",1)>5 else "P2" if urgent else "P3"
    return {"team":team,"priority":priority,"rule_scores":scores,"requires_human_review":team=="general"}


def main() -> None:
    parser = argparse.ArgumentParser(description='Helpdesk Ticket Router')
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
