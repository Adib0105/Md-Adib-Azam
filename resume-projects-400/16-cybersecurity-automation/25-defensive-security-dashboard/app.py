#!/usr/bin/env python3
"""Defensive Security Dashboard - defensive, offline portfolio mini-project."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def analyze(data:dict)->dict:
    from collections import Counter
    severity_order={"critical":0,"high":1,"medium":2,"low":3};counts=Counter(f["severity"] for f in data["findings"]);queue=sorted(data["findings"],key=lambda x:(severity_order.get(x["severity"],9),x.get("due","9999")));score=sum({"critical":10,"high":7,"medium":4,"low":1}.get(x["severity"],0) for x in data["findings"]);return {"finding_counts":dict(counts),"risk_points":score,"remediation_queue":queue,"closed_pct":round(100*sum(f.get("status")=="closed" for f in data["findings"])/len(data["findings"]),1) if data["findings"] else 0}

def main()->None:
 parser=argparse.ArgumentParser(description='Defensive Security Dashboard')
 parser.add_argument("--input",type=Path,default=Path("sample.json"))
 args=parser.parse_args();print(json.dumps(analyze(json.loads(args.input.read_text())),indent=2))
if __name__=="__main__":main()
