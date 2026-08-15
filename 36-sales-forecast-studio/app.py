from __future__ import annotations

import argparse
import csv
import json
from datetime import date
from pathlib import Path


def linear_forecast(values: list[float], periods: int) -> list[float]:
    if len(values) < 2:
        raise ValueError("At least two observations are required.")
    n = len(values)
    mean_x = (n - 1) / 2
    mean_y = sum(values) / n
    denominator = sum((x - mean_x) ** 2 for x in range(n))
    slope = sum((x - mean_x) * (y - mean_y) for x, y in enumerate(values)) / denominator
    intercept = mean_y - slope * mean_x
    return [round(intercept + slope * (n + step), 2) for step in range(periods)]


def moving_average(values: list[float], window: int = 3) -> float:
    if not values:
        raise ValueError("No observations supplied.")
    selected = values[-min(window, len(values)):]
    return round(sum(selected) / len(selected), 2)


def holdout_mae(values: list[float]) -> float:
    if len(values) < 5:
        return 0.0
    train, actual = values[:-2], values[-2:]
    predicted = linear_forecast(train, 2)
    return round(sum(abs(a - p) for a, p in zip(actual, predicted)) / 2, 2)


def add_months(value: str, count: int) -> str:
    current = date.fromisoformat(value + "-01")
    month_index = current.year * 12 + current.month - 1 + count
    year, month_zero = divmod(month_index, 12)
    return f"{year:04d}-{month_zero + 1:02d}"


def analyze(rows: list[dict[str, str]], periods: int) -> dict[str, object]:
    values = [float(row["sales"]) for row in rows]
    last_month = rows[-1]["month"]
    future = linear_forecast(values, periods)
    return {
        "observations": len(values),
        "moving_average_3": moving_average(values, 3),
        "holdout_mae": holdout_mae(values),
        "forecast": [
            {"month": add_months(last_month, step + 1), "sales": amount}
            for step, amount in enumerate(future)
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("--periods", type=int, default=3)
    args = parser.parse_args()
    with args.csv_file.open(newline="", encoding="utf-8") as source:
        rows = list(csv.DictReader(source))
    print(json.dumps(analyze(rows, args.periods), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
