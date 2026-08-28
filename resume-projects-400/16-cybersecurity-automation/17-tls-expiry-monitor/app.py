#!/usr/bin/env python3
"""TLS Expiry Monitor - defensive, offline portfolio mini-project."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def analyze(data:dict)->dict:
    from datetime import date
    today=date.fromisoformat(data["today"]);results=[]
    for cert in data["certificates"]:
     days=(date.fromisoformat(cert["not_after"])-today).days;results.append({**cert,"days_remaining":days,"status":"expired" if days<0 else "critical" if days<=7 else "warning" if days<=30 else "ok"})
    return {"certificates":results,"requires_action":[x["host"] for x in results if x["status"]!="ok"],"network_connection":False}

def main()->None:
 parser=argparse.ArgumentParser(description='TLS Expiry Monitor')
 parser.add_argument("--input",type=Path,default=Path("sample.json"))
 args=parser.parse_args();print(json.dumps(analyze(json.loads(args.input.read_text())),indent=2))
if __name__=="__main__":main()
