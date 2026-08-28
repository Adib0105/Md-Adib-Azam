#!/usr/bin/env python3
"""Password Strength Checker - a tested, standard-library portfolio mini-project."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def solve(data: dict) -> dict:
    password=data["password"]
    classes=sum(bool(__import__("re").search(p,password)) for p in [r"[a-z]",r"[A-Z]",r"\d",r"[^A-Za-z0-9]"])
    pool=[0,26,52,62,94][classes]
    entropy=round(len(password)*(__import__("math").log2(pool) if pool else 0),1)
    issues=[]
    if len(password)<12: issues.append("use at least 12 characters")
    if classes<3: issues.append("mix upper, lower, digits and symbols")
    return {"length":len(password),"character_classes":classes,"entropy_bits":entropy,"rating":"strong" if entropy>=60 and not issues else "needs-improvement","issues":issues}


def main() -> None:
    parser = argparse.ArgumentParser(description='Password Strength Checker')
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
