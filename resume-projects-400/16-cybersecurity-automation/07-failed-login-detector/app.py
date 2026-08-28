#!/usr/bin/env python3
"""Failed Login Detector - defensive, offline portfolio mini-project."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def analyze(data:dict)->dict:
    from collections import Counter
    failures=[e for e in data["events"] if e["result"]=="failed"];by_user=Counter(e["user"] for e in failures);by_source=Counter(e["source"] for e in failures);threshold=data.get("threshold",3);return {"failed_events":len(failures),"users_over_threshold":{k:v for k,v in by_user.items() if v>=threshold},"sources_over_threshold":{k:v for k,v in by_source.items() if v>=threshold},"note":"Review context before blocking."}

def main()->None:
 parser=argparse.ArgumentParser(description='Failed Login Detector')
 parser.add_argument("--input",type=Path,default=Path("sample.json"))
 args=parser.parse_args();print(json.dumps(analyze(json.loads(args.input.read_text())),indent=2))
if __name__=="__main__":main()
