#!/usr/bin/env python3
"""Student Grade Calculator - a tested, standard-library portfolio mini-project."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def solve(data: dict) -> dict:
    weights=data["weights"]
    if round(sum(weights.values()),6)!=1: raise ValueError("weights must total 1")
    results=[]
    for s in data["students"]:
        score=round(sum(s["scores"][k]*w for k,w in weights.items()),2)
        grade="A" if score>=90 else "B" if score>=80 else "C" if score>=70 else "D" if score>=60 else "F"
        results.append({"name":s["name"],"weighted_score":score,"grade":grade})
    return {"results":results,"class_average":round(sum(r["weighted_score"] for r in results)/len(results),2)}


def main() -> None:
    parser = argparse.ArgumentParser(description='Student Grade Calculator')
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
