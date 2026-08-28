#!/usr/bin/env python3
"""Personal Budget Planner - a tested, standard-library portfolio mini-project."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def solve(data: dict) -> dict:
    budgets=data["budgets"]; spent={}
    for x in data["expenses"]: spent[x["category"]]=spent.get(x["category"],0)+x["amount"]
    variance={k:round(budgets[k]-spent.get(k,0),2) for k in budgets}
    income=data["income"]; total=sum(spent.values())
    return {"spent_by_category":spent,"variance":variance,"overspent":[k for k,v in variance.items() if v<0],"savings_rate":round((income-total)/income*100,2) if income else 0}


def main() -> None:
    parser = argparse.ArgumentParser(description='Personal Budget Planner')
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
