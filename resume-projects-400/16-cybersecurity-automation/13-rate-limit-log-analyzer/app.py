#!/usr/bin/env python3
"""Rate Limit Log Analyzer - defensive, offline portfolio mini-project."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def analyze(data:dict)->dict:
    from collections import Counter
    limited=[e for e in data["events"] if int(e["status"])==429];clients=Counter(e["client"] for e in limited);threshold=data.get("threshold",2);return {"rate_limited_events":len(limited),"clients_over_threshold":{k:v for k,v in clients.items() if v>=threshold},"recommendations":["Review client retry backoff","Confirm server limit policy","Avoid automatic blocking without context"]}

def main()->None:
 parser=argparse.ArgumentParser(description='Rate Limit Log Analyzer')
 parser.add_argument("--input",type=Path,default=Path("sample.json"))
 args=parser.parse_args();print(json.dumps(analyze(json.loads(args.input.read_text())),indent=2))
if __name__=="__main__":main()
