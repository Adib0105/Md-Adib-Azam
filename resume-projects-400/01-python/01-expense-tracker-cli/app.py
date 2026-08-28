#!/usr/bin/env python3
"""Expense Tracker CLI - a tested, standard-library portfolio mini-project."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def solve(data: dict) -> dict:
    transactions = data["transactions"]
    income = sum(x["amount"] for x in transactions if x["type"] == "income")
    expenses = sum(x["amount"] for x in transactions if x["type"] == "expense")
    by_category = {}
    for row in transactions:
        if row["type"] == "expense":
            by_category[row["category"]] = round(by_category.get(row["category"], 0) + row["amount"], 2)
    return {"income": income, "expenses": expenses, "balance": round(income-expenses, 2), "expense_by_category": by_category}


def main() -> None:
    parser = argparse.ArgumentParser(description='Expense Tracker CLI')
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
