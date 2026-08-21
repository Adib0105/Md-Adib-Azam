from __future__ import annotations

import argparse
import csv
import json
import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent
DB = ROOT / "jobs.db"
REPORTS = ROOT / "reports"


def run_discovery(config: str, greenhouse: list[str], lever: list[str]):
    cmd = [sys.executable, str(ROOT / "agent.py"), "--config", config]
    for x in greenhouse: cmd += ["--greenhouse", x]
    for x in lever: cmd += ["--lever", x]
    return subprocess.run(cmd, text=True, capture_output=True, check=False)


def export_queue(limit: int = 10):
    REPORTS.mkdir(exist_ok=True)
    if not DB.exists(): return []
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    rows = con.execute("""SELECT company,title,url,source,score,verdict,status,reason,discovered_at
        FROM jobs WHERE verdict='QUALIFIED' AND status='FOUND'
        ORDER BY score DESC, discovered_at DESC LIMIT ?""", (limit,)).fetchall()
    con.close()
    data = [dict(x) for x in rows]
    stamp = datetime.now().strftime("%Y-%m-%d")
    with open(REPORTS / f"queue-{stamp}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    with open(REPORTS / f"queue-{stamp}.csv", "w", newline="", encoding="utf-8") as f:
        if data:
            w = csv.DictWriter(f, fieldnames=data[0].keys()); w.writeheader(); w.writerows(data)
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=str(ROOT / "config.yaml"))
    ap.add_argument("--greenhouse", action="append", default=[])
    ap.add_argument("--lever", action="append", default=[])
    ap.add_argument("--limit", type=int, default=10)
    args = ap.parse_args()
    result = run_discovery(args.config, args.greenhouse, args.lever)
    if result.stdout: print(result.stdout)
    if result.stderr: print(result.stderr, file=sys.stderr)
    queue = export_queue(args.limit)
    print(f"Daily queue prepared: {len(queue)} qualified jobs")
    for i, x in enumerate(queue, 1): print(f"{i}. {x['company']} — {x['title']} ({x['score']}%)")

if __name__ == "__main__": main()
