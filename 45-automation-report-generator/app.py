from __future__ import annotations

import argparse
import csv
import html
from collections import Counter
from datetime import date
from pathlib import Path


def summarize(rows: list[dict[str, str]], as_of: date) -> dict[str, object]:
    completed = sum(row["status"].lower() == "completed" for row in rows)
    overdue_rows = [
        row for row in rows
        if row["status"].lower() != "completed" and date.fromisoformat(row["due_date"]) < as_of
    ]
    return {
        "total": len(rows),
        "completed": completed,
        "completion_percent": round(100 * completed / len(rows), 1) if rows else 0,
        "overdue": len(overdue_rows),
        "high_priority_open": sum(
            row["priority"].lower() == "high" and row["status"].lower() != "completed"
            for row in rows
        ),
        "by_owner": dict(Counter(row["owner"] for row in rows if row["status"].lower() != "completed")),
        "overdue_ids": [row["task_id"] for row in overdue_rows],
    }


def build_html(rows: list[dict[str, str]], summary: dict[str, object], as_of: date) -> str:
    cards = [
        ("Total tasks", summary["total"]),
        ("Completed", f"{summary['completion_percent']}%"),
        ("Overdue", summary["overdue"]),
        ("High priority open", summary["high_priority_open"]),
    ]
    card_html = "".join(
        f"<article><span>{html.escape(str(label))}</span><strong>{html.escape(str(value))}</strong></article>"
        for label, value in cards
    )
    overdue_ids = set(summary["overdue_ids"])
    row_html = "".join(
        "<tr class='" + ("overdue" if row["task_id"] in overdue_ids else "") + "'>" +
        "".join(f"<td>{html.escape(row[column])}</td>" for column in ["task_id", "task", "owner", "priority", "status", "due_date"]) +
        "</tr>"
        for row in rows
    )
    owner_html = "".join(
        f"<li><span>{html.escape(owner)}</span><strong>{count} open</strong></li>"
        for owner, count in sorted(summary["by_owner"].items())
    )
    return f"""<!doctype html>
    <html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Operations Report</title><style>
    :root{{--ink:#162031;--muted:#69778c;--blue:#246bfd;--paper:#f4f7fb;--danger:#b42318}}
    *{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font-family:system-ui,sans-serif}}
    main{{width:min(1100px,92%);margin:auto;padding:48px 0}}h1{{font-size:clamp(2.4rem,6vw,4.5rem);margin:0}}.sub{{color:var(--muted)}}
    .cards{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:28px 0}}article,.panel{{background:white;border:1px solid #dfe5ee;border-radius:16px;padding:20px}}
    article span{{color:var(--muted);font-size:.8rem}}article strong{{display:block;font-size:2rem;color:var(--blue);margin-top:8px}}
    .layout{{display:grid;grid-template-columns:1fr 260px;gap:16px}}.table{{overflow:auto}}table{{border-collapse:collapse;width:100%;min-width:720px}}th,td{{padding:13px;text-align:left;border-bottom:1px solid #e7ebf1}}th{{font-size:.75rem;text-transform:uppercase;color:var(--muted)}}.overdue td{{color:var(--danger)}}ul{{list-style:none;padding:0}}li{{display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid #e7ebf1}}
    @media(max-width:760px){{.cards{{grid-template-columns:repeat(2,1fr)}}.layout{{grid-template-columns:1fr}}}}
    </style></head><body><main><h1>Operations report</h1><p class="sub">Status as of {as_of.isoformat()}</p>
    <section class="cards">{card_html}</section><section class="layout"><div class="panel table"><table><thead><tr><th>ID</th><th>Task</th><th>Owner</th><th>Priority</th><th>Status</th><th>Due</th></tr></thead><tbody>{row_html}</tbody></table></div>
    <aside class="panel"><h2>Open by owner</h2><ul>{owner_html}</ul></aside></section></main></body></html>"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("tasks_csv", type=Path)
    parser.add_argument("--as-of", type=date.fromisoformat, default=date.today())
    parser.add_argument("--output", type=Path, default=Path("operations_report.html"))
    args = parser.parse_args()
    with args.tasks_csv.open(newline="", encoding="utf-8") as source:
        rows = list(csv.DictReader(source))
    summary = summarize(rows, args.as_of)
    args.output.write_text(build_html(rows, summary, args.as_of), encoding="utf-8")
    print(f"Saved report: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
