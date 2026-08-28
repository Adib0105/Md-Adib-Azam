#!/usr/bin/env python3
"""Secure Backup Verifier - defensive, offline portfolio mini-project."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def analyze(data:dict)->dict:
    from datetime import datetime,timezone
    source={x["path"]:x["sha256"] for x in data["source_manifest"]};backup={x["path"]:x["sha256"] for x in data["backup_manifest"]};created=datetime.fromisoformat(data["backup_created_at"].replace("Z","+00:00"));now=datetime.fromisoformat(data["as_of"].replace("Z","+00:00"));return {"missing":sorted(source.keys()-backup.keys()),"hash_mismatches":sorted(k for k in source.keys()&backup.keys() if source[k]!=backup[k]),"extra":sorted(backup.keys()-source.keys()),"age_hours":round((now-created).total_seconds()/3600,1),"stale":(now-created).total_seconds()>data.get("max_age_hours",24)*3600}

def main()->None:
 parser=argparse.ArgumentParser(description='Secure Backup Verifier')
 parser.add_argument("--input",type=Path,default=Path("sample.json"))
 args=parser.parse_args();print(json.dumps(analyze(json.loads(args.input.read_text())),indent=2))
if __name__=="__main__":main()
