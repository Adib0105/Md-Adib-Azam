#!/usr/bin/env python3
"""Security Header Auditor - defensive, offline portfolio mini-project."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def analyze(data:dict)->dict:
    required={"strict-transport-security":"Enable HSTS","content-security-policy":"Define a CSP","x-content-type-options":"Set nosniff","referrer-policy":"Set a restrictive policy"};headers={k.lower():v for k,v in data["headers"].items()};missing={k:fix for k,fix in required.items() if k not in headers};return {"present":sorted(set(required)&headers.keys()),"missing":missing,"score_pct":round(100*(len(required)-len(missing))/len(required),1)}

def main()->None:
 parser=argparse.ArgumentParser(description='Security Header Auditor')
 parser.add_argument("--input",type=Path,default=Path("sample.json"))
 args=parser.parse_args();print(json.dumps(analyze(json.loads(args.input.read_text())),indent=2))
if __name__=="__main__":main()
