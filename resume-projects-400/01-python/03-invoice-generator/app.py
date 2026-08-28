#!/usr/bin/env python3
"""Invoice Generator - a tested, standard-library portfolio mini-project."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def solve(data: dict) -> dict:
    lines=[]
    for item in data["items"]:
        total=round(item["quantity"]*item["unit_price"],2)
        lines.append({**item,"line_total":total})
    subtotal=round(sum(x["line_total"] for x in lines),2)
    tax=round(subtotal*data.get("tax_rate",0),2)
    return {"invoice_no":data["invoice_no"],"items":lines,"subtotal":subtotal,"tax":tax,"grand_total":round(subtotal+tax,2)}


def main() -> None:
    parser = argparse.ArgumentParser(description='Invoice Generator')
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
