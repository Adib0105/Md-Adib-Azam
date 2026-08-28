#!/usr/bin/env python3
"""DNS Record Checker - defensive, offline portfolio mini-project."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def analyze(data:dict)->dict:
    normalize=lambda rows:{(r["type"],r["name"],r["value"].rstrip(".").lower()) for r in rows};expected=normalize(data["expected"]);observed=normalize(data["observed"]);return {"missing":[list(x) for x in sorted(expected-observed)],"unexpected":[list(x) for x in sorted(observed-expected)],"matching":len(expected&observed),"live_query_performed":False}

def main()->None:
 parser=argparse.ArgumentParser(description='DNS Record Checker')
 parser.add_argument("--input",type=Path,default=Path("sample.json"))
 args=parser.parse_args();print(json.dumps(analyze(json.loads(args.input.read_text())),indent=2))
if __name__=="__main__":main()
