#!/usr/bin/env python3
"""URL Health Monitor - a tested, standard-library portfolio mini-project."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def solve(data: dict) -> dict:
    from urllib.parse import urlparse
    checks=[]
    for row in data["checks"]:
        parsed=urlparse(row["url"])
        valid=parsed.scheme in {"http","https"} and bool(parsed.netloc)
        healthy=valid and 200<=row.get("status",0)<400 and row.get("latency_ms",99999)<=data.get("max_latency_ms",2000)
        checks.append({**row,"valid_url":valid,"healthy":healthy})
    return {"healthy":sum(x["healthy"] for x in checks),"total":len(checks),"checks":checks}


def main() -> None:
    parser = argparse.ArgumentParser(description='URL Health Monitor')
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
