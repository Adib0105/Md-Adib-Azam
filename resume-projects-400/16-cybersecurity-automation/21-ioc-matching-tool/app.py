#!/usr/bin/env python3
"""IOC Matching Tool - defensive, offline portfolio mini-project."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def analyze(data:dict)->dict:
    watch={(x["type"],x["value"].lower()):x for x in data["watchlist"]};matches=[]
    for o in data["observables"]:
     key=(o["type"],o["value"].lower())
     if key in watch:matches.append({**o,"ioc_id":watch[key]["id"],"confidence":watch[key]["confidence"]})
    return {"observables":len(data["observables"]),"matches":matches,"note":"A match is an investigation lead, not automatic proof."}

def main()->None:
 parser=argparse.ArgumentParser(description='IOC Matching Tool')
 parser.add_argument("--input",type=Path,default=Path("sample.json"))
 args=parser.parse_args();print(json.dumps(analyze(json.loads(args.input.read_text())),indent=2))
if __name__=="__main__":main()
