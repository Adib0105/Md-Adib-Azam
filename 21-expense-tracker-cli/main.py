import argparse
import json
from collections import defaultdict
from datetime import date
from decimal import Decimal
from pathlib import Path


def load_expenses(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []


def save_expenses(path: Path, expenses: list[dict]) -> None:
    path.write_text(json.dumps(expenses, indent=2), encoding="utf-8")


def add_expense(expenses: list[dict], amount: str, category: str, note: str = "", spent_on: str | None = None) -> dict:
    value = Decimal(amount)
    if value <= 0:
        raise ValueError("Amount must be positive")
    entry = {
        "amount": str(value.quantize(Decimal("0.01"))),
        "category": category.strip().title(),
        "note": note.strip(),
        "date": spent_on or date.today().isoformat(),
    }
    expenses.append(entry)
    return entry


def category_totals(expenses: list[dict]) -> dict[str, Decimal]:
    totals = defaultdict(Decimal)
    for expense in expenses:
        totals[expense["category"]] += Decimal(expense["amount"])
    return dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))


def main() -> None:
    parser = argparse.ArgumentParser(description="JSON expense tracker")
    parser.add_argument("--file", type=Path, default=Path("expenses.json"))
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add")
    add.add_argument("amount")
    add.add_argument("category")
    add.add_argument("--note", default="")
    add.add_argument("--date")
    commands.add_parser("report")
    args = parser.parse_args()
    expenses = load_expenses(args.file)
    if args.command == "add":
        add_expense(expenses, args.amount, args.category, args.note, args.date)
        save_expenses(args.file, expenses)
        print("Expense saved.")
    else:
        totals = category_totals(expenses)
        for category, total in totals.items():
            print(f"{category}: ₹{total:,.2f}")
        print(f"Total: ₹{sum(totals.values(), Decimal()):,.2f}")


if __name__ == "__main__":
    main()
