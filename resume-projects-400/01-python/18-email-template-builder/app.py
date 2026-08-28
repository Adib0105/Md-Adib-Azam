#!/usr/bin/env python3
"""Email Template Builder - a tested, standard-library portfolio mini-project."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def solve(data: dict) -> dict:
    import re
    template=data["template"]; values=data["values"]
    required=set(re.findall(r"{{\s*([a-zA-Z0-9_]+)\s*}}",template))
    missing=sorted(required-values.keys())
    rendered=template
    for key,value in values.items(): rendered=re.sub(r"{{\s*"+re.escape(key)+r"\s*}}",str(value),rendered)
    return {"rendered":rendered,"required_fields":sorted(required),"missing_fields":missing,"complete":not missing}


def main() -> None:
    parser = argparse.ArgumentParser(description='Email Template Builder')
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
