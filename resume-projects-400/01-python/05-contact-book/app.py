#!/usr/bin/env python3
"""Contact Book - a tested, standard-library portfolio mini-project."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def solve(data: dict) -> dict:
    seen=set(); contacts=[]
    for c in data["contacts"]:
        phone="".join(ch for ch in c["phone"] if ch.isdigit())
        key=(c["name"].casefold().strip(),phone)
        if key not in seen:
            seen.add(key); contacts.append({"name":c["name"].strip(),"phone":phone,"email":c.get("email","").lower()})
    query=data.get("query","").casefold()
    return {"contacts":contacts,"matches":[c for c in contacts if query in c["name"].casefold()]}


def main() -> None:
    parser = argparse.ArgumentParser(description='Contact Book')
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
