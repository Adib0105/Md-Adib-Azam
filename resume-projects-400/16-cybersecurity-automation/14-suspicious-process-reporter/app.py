#!/usr/bin/env python3
"""Suspicious Process Reporter - defensive, offline portfolio mini-project."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def analyze(data:dict)->dict:
    approved={(x["name"],x.get("path","")) for x in data["approved"]};findings=[]
    for p in data["processes"]:
     reasons=[]
     if (p["name"],p.get("path","")) not in approved:reasons.append("not in approved inventory")
     if p.get("user")=="root" and not p.get("requires_root",False):reasons.append("unexpected elevated user")
     if reasons:findings.append({"pid":p["pid"],"name":p["name"],"reasons":reasons})
    return {"processes":len(data["processes"]),"findings":findings,"action":"manual review only"}

def main()->None:
 parser=argparse.ArgumentParser(description='Suspicious Process Reporter')
 parser.add_argument("--input",type=Path,default=Path("sample.json"))
 args=parser.parse_args();print(json.dumps(analyze(json.loads(args.input.read_text())),indent=2))
if __name__=="__main__":main()
