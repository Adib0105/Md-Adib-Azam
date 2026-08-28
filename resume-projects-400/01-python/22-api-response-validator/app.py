#!/usr/bin/env python3
"""API Response Validator - a tested, standard-library portfolio mini-project."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def solve(data: dict) -> dict:
    TYPE_MAP={"string":str,"number":(int,float),"boolean":bool,"array":list,"object":dict}
    errors=[]
    for field,expected in data["schema"].items():
        value=data["response"]
        for part in field.split("."):
            if not isinstance(value,dict) or part not in value: errors.append(f"missing: {field}"); value=None; break
            value=value[part]
        if value is not None and not isinstance(value,TYPE_MAP[expected]): errors.append(f"type: {field} expected {expected}")
    return {"valid":not errors,"errors":errors,"checked_fields":len(data["schema"])}


def main() -> None:
    parser = argparse.ArgumentParser(description='API Response Validator')
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
