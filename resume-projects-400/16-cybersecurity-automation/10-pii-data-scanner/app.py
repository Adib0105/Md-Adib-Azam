#!/usr/bin/env python3
"""PII Data Scanner - defensive, offline portfolio mini-project."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def analyze(data:dict)->dict:
    import re
    patterns={"email":r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b","phone":r"(?<!\d)(?:\+91[- ]?)?[6-9]\d{9}(?!\d)","pan":r"\b[A-Z]{5}\d{4}[A-Z]\b"};findings=[]
    for name,pattern in patterns.items():
     for m in re.finditer(pattern,data["text"]):findings.append({"type":name,"start":m.start(),"end":m.end(),"redacted":m.group(0)[:2]+"***"})
    return {"finding_count":len(findings),"findings":findings,"content_echoed":False}

def main()->None:
 parser=argparse.ArgumentParser(description='PII Data Scanner')
 parser.add_argument("--input",type=Path,default=Path("sample.json"))
 args=parser.parse_args();print(json.dumps(analyze(json.loads(args.input.read_text())),indent=2))
if __name__=="__main__":main()
