#!/usr/bin/env python3
"""Bulk File Renamer - a tested, standard-library portfolio mini-project."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def solve(data: dict) -> dict:
    used=set(); plan=[]
    for index,name in enumerate(data["files"],start=data.get("start",1)):
        ext=Path(name).suffix.lower()
        target=f'{data.get("prefix","file")}-{index:03d}{ext}'
        if target in used: raise ValueError("rename collision")
        used.add(target); plan.append({"from":name,"to":target})
    return {"plan":plan,"undo":[{"from":x["to"],"to":x["from"]} for x in reversed(plan)]}


def main() -> None:
    parser = argparse.ArgumentParser(description='Bulk File Renamer')
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
