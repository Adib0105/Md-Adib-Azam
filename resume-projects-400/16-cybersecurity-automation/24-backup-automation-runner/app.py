#!/usr/bin/env python3
"""Backup Automation Runner - defensive, offline portfolio mini-project."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def analyze(data:dict)->dict:
    from datetime import datetime,timedelta
    now=datetime.fromisoformat(data["as_of"]);cutoff=now-timedelta(days=data["retention_days"]);expired=[b["name"] for b in data["existing_backups"] if datetime.fromisoformat(b["created_at"])<cutoff];steps=[{"action":"verify source","path":p} for p in data["source_paths"]]+[{"action":"create archive","destination":data["destination"]},{"action":"write checksum"},{"action":"verify archive"}];return {"plan":steps,"retention_candidates":expired,"dry_run":True,"files_deleted":0}

def main()->None:
 parser=argparse.ArgumentParser(description='Backup Automation Runner')
 parser.add_argument("--input",type=Path,default=Path("sample.json"))
 args=parser.parse_args();print(json.dumps(analyze(json.loads(args.input.read_text())),indent=2))
if __name__=="__main__":main()
