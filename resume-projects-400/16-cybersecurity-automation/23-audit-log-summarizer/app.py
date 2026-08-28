#!/usr/bin/env python3
"""Audit Log Summarizer - defensive, offline portfolio mini-project."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def analyze(data:dict)->dict:
    from collections import Counter
    actions=Counter(e["action"] for e in data["events"]);outcomes=Counter(e["outcome"] for e in data["events"]);actors=Counter(e["actor"] for e in data["events"]);return {"events":len(data["events"]),"actions":dict(actions),"outcomes":dict(outcomes),"top_actors":actors.most_common(5),"failures":[e for e in data["events"] if e["outcome"]=="failure"]}

def main()->None:
 parser=argparse.ArgumentParser(description='Audit Log Summarizer')
 parser.add_argument("--input",type=Path,default=Path("sample.json"))
 args=parser.parse_args();print(json.dumps(analyze(json.loads(args.input.read_text())),indent=2))
if __name__=="__main__":main()
