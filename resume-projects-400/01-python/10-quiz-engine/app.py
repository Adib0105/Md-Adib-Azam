#!/usr/bin/env python3
"""Quiz Engine - a tested, standard-library portfolio mini-project."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def solve(data: dict) -> dict:
    answers=data["answers"]; score=0; review=[]
    for q in data["questions"]:
        chosen=answers.get(q["id"]); correct=chosen==q["answer"]; score+=correct
        review.append({"id":q["id"],"correct":correct,"chosen":chosen,"answer":q["answer"],"explanation":q["explanation"]})
    return {"score":score,"out_of":len(review),"percentage":round(100*score/len(review),1),"review":review}


def main() -> None:
    parser = argparse.ArgumentParser(description='Quiz Engine')
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
