#!/usr/bin/env python3
"""Access Log Threat Monitor - defensive, offline portfolio mini-project."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def analyze(data:dict)->dict:
    import re,collections
    pattern=re.compile(r'(?P<ip>\S+) "(?P<method>[A-Z]+) (?P<path>\S+)" (?P<status>\d{3}) "(?P<agent>[^"]*)"');events=[m.groupdict() for line in data["lines"] if (m:=pattern.search(line))];ip_errors=collections.Counter(e["ip"] for e in events if int(e["status"])>=400);findings=[]
    for e in events:
     reasons=[];low=(e["path"]+" "+e["agent"]).lower()
     if any(x in low for x in ["/.env","/wp-admin","sqlmap","nikto"]):reasons.append("sensitive path or scanner signature")
     if ip_errors[e["ip"]]>=data.get("error_threshold",3):reasons.append("repeated errors")
     if reasons:findings.append({**e,"reasons":reasons})
    return {"events":len(events),"findings":findings,"review_only":True}

def main()->None:
 parser=argparse.ArgumentParser(description='Access Log Threat Monitor')
 parser.add_argument("--input",type=Path,default=Path("sample.json"))
 args=parser.parse_args();print(json.dumps(analyze(json.loads(args.input.read_text())),indent=2))
if __name__=="__main__":main()
