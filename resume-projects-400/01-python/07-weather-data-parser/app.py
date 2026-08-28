#!/usr/bin/env python3
"""Weather Data Parser - a tested, standard-library portfolio mini-project."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def solve(data: dict) -> dict:
    rows=data["readings"]
    temps=[r["temperature_c"] for r in rows]
    rain=sum(r.get("rain_mm",0) for r in rows)
    return {"days":len(rows),"mean_temperature_c":round(sum(temps)/len(temps),2),"min_temperature_c":min(temps),"max_temperature_c":max(temps),"total_rain_mm":round(rain,1)}


def main() -> None:
    parser = argparse.ArgumentParser(description='Weather Data Parser')
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
