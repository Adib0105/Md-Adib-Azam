import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import create_app
from services.job_catalog import parse_filters
from services.external_jobs_service import live_search

parser = argparse.ArgumentParser(description="Refresh one configured provider query.")
parser.add_argument("--provider", choices=["adzuna", "usajobs"], default="adzuna")
parser.add_argument("--query", default="data analyst")
parser.add_argument("--location", default="")
parser.add_argument("--country", default="in")
args = parser.parse_args()
app = create_app()
with app.app_context():
    result = live_search(
        args.provider,
        parse_filters(
            {"q": args.query, "location": args.location, "country": args.country}
        ),
        force=True,
    )
    print(result["status"] + ": " + result["message"])
