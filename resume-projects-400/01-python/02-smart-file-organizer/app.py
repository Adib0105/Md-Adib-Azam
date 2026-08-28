#!/usr/bin/env python3
"""Smart File Organizer - a tested, standard-library portfolio mini-project."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def solve(data: dict) -> dict:
    groups = {}
    for name in data["files"]:
        ext = Path(name).suffix.lower().lstrip(".") or "no-extension"
        destination = f"{ext}/{Path(name).name}"
        groups.setdefault(ext, []).append(destination)
    return {"move_plan": groups, "files": sum(map(len, groups.values())), "dry_run": True}


def main() -> None:
    parser = argparse.ArgumentParser(description='Smart File Organizer')
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
