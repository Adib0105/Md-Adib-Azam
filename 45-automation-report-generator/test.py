from datetime import date
from app import build_html, summarize

rows = [
    {"task_id": "1", "task": "A", "owner": "Asha", "priority": "High", "status": "Completed", "due_date": "2026-08-10"},
    {"task_id": "2", "task": "B", "owner": "Ravi", "priority": "High", "status": "Open", "due_date": "2026-08-15"},
]
result = summarize(rows, date(2026, 8, 16))
assert result["completion_percent"] == 50.0
assert result["overdue"] == 1
assert result["high_priority_open"] == 1
report = build_html(rows, result, date(2026, 8, 16))
assert "Operations report" in report
assert "class='overdue'" in report
print("Automation report generator tests passed")
