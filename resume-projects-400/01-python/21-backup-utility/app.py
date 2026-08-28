#!/usr/bin/env python3
"""Backup Utility - a tested, standard-library portfolio mini-project."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def solve(data: dict) -> dict:
    from datetime import datetime,timedelta
    files=sorted(data["files"],key=lambda x:x["path"])
    manifest=[{"path":x["path"],"size":x["size"],"sha256":x["sha256"]} for x in files]
    cutoff=datetime.fromisoformat(data["as_of"])-timedelta(days=data.get("retention_days",30))
    expired=[b["name"] for b in data.get("backups",[]) if datetime.fromisoformat(b["created_at"])<cutoff]
    return {"manifest":manifest,"total_bytes":sum(x["size"] for x in files),"expired_backups":expired,"destructive_actions":False}


def main() -> None:
    parser = argparse.ArgumentParser(description='Backup Utility')
    parser.add_argument("--input", type=Path, default=Path('sample.json'))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = solve(json.loads(args.input.read_text(encoding="utf-8")))
    rendered = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
