#!/usr/bin/env python3
"""Phishing URL Heuristic Checker - defensive, offline portfolio mini-project."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def analyze(data:dict)->dict:
    from urllib.parse import urlparse
    results=[]
    for raw in data["urls"]:
     p=urlparse(raw);host=p.hostname or "";reasons=[]
     if p.scheme!="https":reasons.append("not HTTPS")
     if "@" in raw:reasons.append("@ in URL")
     if host.replace(".","").isdigit():reasons.append("IP-literal host")
     if len(host.split("."))>data.get("max_labels",4):reasons.append("many subdomains")
     if any(w in (p.path+"?"+p.query).lower() for w in ["verify-account","urgent-login","update-password"]):reasons.append("credential-themed path")
     results.append({"url":raw,"risk_score":len(reasons),"reasons":reasons,"manual_review":bool(reasons)})
    return {"results":results,"limitation":"Heuristics are not proof that a site is malicious."}

def main()->None:
 parser=argparse.ArgumentParser(description='Phishing URL Heuristic Checker')
 parser.add_argument("--input",type=Path,default=Path("sample.json"))
 args=parser.parse_args();print(json.dumps(analyze(json.loads(args.input.read_text())),indent=2))
if __name__=="__main__":main()
