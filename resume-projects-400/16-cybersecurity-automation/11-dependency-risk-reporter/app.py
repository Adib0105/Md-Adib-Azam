#!/usr/bin/env python3
"""Dependency Risk Reporter - defensive, offline portfolio mini-project."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def analyze(data:dict)->dict:
    advisories={(a["package"],a["affected_version"]):a for a in data["advisories"]};findings=[]
    for dep in data["dependencies"]:
     key=(dep["package"],dep["version"])
     if key in advisories:findings.append({**dep,"advisory":advisories[key]["id"],"severity":advisories[key]["severity"],"fixed_version":advisories[key].get("fixed_version")})
    return {"dependencies":len(data["dependencies"]),"findings":findings,"source":"user-supplied advisory snapshot"}

def main()->None:
 parser=argparse.ArgumentParser(description='Dependency Risk Reporter')
 parser.add_argument("--input",type=Path,default=Path("sample.json"))
 args=parser.parse_args();print(json.dumps(analyze(json.loads(args.input.read_text())),indent=2))
if __name__=="__main__":main()
