#!/usr/bin/env python3
"""HTTP Configuration Checker - defensive, offline portfolio mini-project."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def analyze(data:dict)->dict:
    findings=[];cfg=data["configuration"]
    for cookie in cfg.get("cookies",[]):
     if not cookie.get("secure"):findings.append({"control":"Secure cookie","cookie":cookie["name"],"severity":"high"})
     if not cookie.get("http_only"):findings.append({"control":"HttpOnly cookie","cookie":cookie["name"],"severity":"medium"})
     if cookie.get("same_site") not in {"Lax","Strict","None"}:findings.append({"control":"SameSite cookie","cookie":cookie["name"],"severity":"medium"})
    if not cfg.get("http_to_https_redirect"):findings.append({"control":"HTTP to HTTPS redirect","severity":"high"})
    return {"findings":findings,"passed":not findings}

def main()->None:
 parser=argparse.ArgumentParser(description='HTTP Configuration Checker')
 parser.add_argument("--input",type=Path,default=Path("sample.json"))
 args=parser.parse_args();print(json.dumps(analyze(json.loads(args.input.read_text())),indent=2))
if __name__=="__main__":main()
