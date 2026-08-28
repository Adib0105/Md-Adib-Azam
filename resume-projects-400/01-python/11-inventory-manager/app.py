#!/usr/bin/env python3
"""Inventory Manager - a tested, standard-library portfolio mini-project."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def solve(data: dict) -> dict:
    alerts=[]; value=0
    for item in data["items"]:
        value+=item["quantity"]*item["unit_cost"]
        if item["quantity"]<=item["reorder_level"]:
            alerts.append({"sku":item["sku"],"order_quantity":max(item["target_stock"]-item["quantity"],0)})
    return {"inventory_value":round(value,2),"reorder_alerts":alerts,"sku_count":len(data["items"])}


def main() -> None:
    parser = argparse.ArgumentParser(description='Inventory Manager')
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
