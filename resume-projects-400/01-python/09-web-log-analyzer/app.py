#!/usr/bin/env python3
"""Web Log Analyzer - a tested, standard-library portfolio mini-project."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def solve(data: dict) -> dict:
    import re, collections
    pattern=re.compile(r'(?P<ip>\S+) .*? "(?P<method>[A-Z]+) (?P<path>\S+) [^"]+" (?P<status>\d{3})')
    parsed=[m.groupdict() for line in data["lines"] if (m:=pattern.search(line))]
    statuses=collections.Counter(x["status"] for x in parsed); ips=collections.Counter(x["ip"] for x in parsed)
    return {"parsed":len(parsed),"status_counts":dict(statuses),"top_ips":ips.most_common(3),"error_paths":[x["path"] for x in parsed if int(x["status"])>=400]}


def main() -> None:
    parser = argparse.ArgumentParser(description='Web Log Analyzer')
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
