#!/usr/bin/env python3
"""CSV Cleaner - a tested, standard-library portfolio mini-project."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def solve(data: dict) -> dict:
    headers=[h.strip().lower().replace(" ","_") for h in data["headers"]]
    seen=set(); clean=[]; missing={"","na","n/a","null","none"}
    for raw in data["rows"]:
        row=[None if str(v).strip().casefold() in missing else str(v).strip() for v in raw]
        key=tuple(row)
        if key not in seen: seen.add(key); clean.append(dict(zip(headers,row)))
    return {"headers":headers,"rows":clean,"removed_duplicates":len(data["rows"])-len(clean)}


def main() -> None:
    parser = argparse.ArgumentParser(description='CSV Cleaner')
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
