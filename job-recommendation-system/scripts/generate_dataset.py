import argparse
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from services.data_service import generate_dataset
from config import ROOT

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate fictional jobs; does not modify an existing database."
    )
    parser.add_argument("--count", type=int, default=640)
    parser.add_argument("--date", type=date.fromisoformat, default=date.today())
    parser.add_argument("--output", type=Path, default=ROOT / "data" / "jobs.csv")
    args = parser.parse_args()
    if args.count < 1:
        parser.error("Count must be positive.")
    generate_dataset(args.output, count=args.count, reference_date=args.date)
    print(f"Wrote {args.count} synthetic jobs to {args.output}")
