#!/usr/bin/env python3
"""Library Management System - a tested, standard-library portfolio mini-project."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def solve(data: dict) -> dict:
    from datetime import date
    books={b["id"]:{**b,"borrower":None,"due":None} for b in data["books"]}
    for event in data["events"]:
        b=books[event["book_id"]]
        if event["action"]=="borrow": b.update(borrower=event["member"],due=event["due"])
        elif event["action"]=="return": b.update(borrower=None,due=None)
    today=date.fromisoformat(data["today"])
    overdue=[b for b in books.values() if b["due"] and date.fromisoformat(b["due"])<today]
    return {"books":list(books.values()),"available":sum(b["borrower"] is None for b in books.values()),"overdue":overdue}


def main() -> None:
    parser = argparse.ArgumentParser(description='Library Management System')
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
