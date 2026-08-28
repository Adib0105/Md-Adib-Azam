#!/usr/bin/env python3
"""File Integrity Monitor - defensive, offline portfolio mini-project."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def analyze(data:dict)->dict:
    trusted={x["path"]:x["sha256"] for x in data["trusted"]};current={x["path"]:x["sha256"] for x in data["current"]};return {"added":sorted(current.keys()-trusted.keys()),"deleted":sorted(trusted.keys()-current.keys()),"changed":sorted(k for k in trusted.keys()&current.keys() if trusted[k]!=current[k]),"unchanged":sum(trusted[k]==current[k] for k in trusted.keys()&current.keys())}

def main()->None:
 parser=argparse.ArgumentParser(description='File Integrity Monitor')
 parser.add_argument("--input",type=Path,default=Path("sample.json"))
 args=parser.parse_args();print(json.dumps(analyze(json.loads(args.input.read_text())),indent=2))
if __name__=="__main__":main()
