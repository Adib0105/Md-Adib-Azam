"""Run from cron/Task Scheduler; no hidden background service is installed."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import create_app
from services.alert_service import process_due_alerts

app = create_app()
with app.app_context():
    print(f"Processed {process_due_alerts()} due alerts.")
