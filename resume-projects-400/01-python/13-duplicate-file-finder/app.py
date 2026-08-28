#!/usr/bin/env python3
"""Duplicate File Finder - a tested, standard-library portfolio mini-project."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def solve(data: dict) -> dict:
    from collections import defaultdict
    groups=defaultdict(list)
    for f in data["files"]: groups[f["sha256"]].append(f)
    duplicates=[g for g in groups.values() if len(g)>1]
    recoverable=sum(sum(x["size"] for x in g)-max(x["size"] for x in g) for g in duplicates)
    return {"duplicate_groups":[[x["path"] for x in g] for g in duplicates],"recoverable_bytes":recoverable}


def main() -> None:
    parser = argparse.ArgumentParser(description='Duplicate File Finder')
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
