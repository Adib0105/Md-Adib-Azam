from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory

from app import connect, dashboard, import_csv, lead_score

assert lead_score("Qualified", 10000, "2026-01-01", date(2026, 8, 16)) == 70
with TemporaryDirectory() as folder:
    database = connect(":memory:")
    count = import_csv(database, Path(__file__).with_name("sample_leads.csv"))
    rows = dashboard(database)
    assert count == 4
    assert rows[0]["stage"] == "Proposal"
    assert {row["name"] for row in rows} == {"Asha Sen", "Ravi Das", "Mina Ali", "Kabir Roy"}
    database.close()

print("Mini CRM tests passed")
