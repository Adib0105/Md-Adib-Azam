import argparse
import csv
from pathlib import Path


def clean_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    cleaned = []
    seen = set()
    for row in rows:
        normalized = {key.strip(): (value or "").strip() for key, value in row.items()}
        signature = tuple(normalized.items())
        if signature not in seen:
            seen.add(signature)
            cleaned.append(normalized)
    return cleaned


def clean_csv(source: Path, destination: Path) -> tuple[int, int]:
    with source.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    cleaned = clean_rows(rows)
    fieldnames = list(cleaned[0]) if cleaned else []
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned)
    return len(rows), len(cleaned)


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean and deduplicate a CSV file")
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    before, after = clean_csv(args.source, args.destination)
    print(f"Cleaned {before} rows -> {after} unique rows")


if __name__ == "__main__":
    main()
