#!/usr/bin/env python3
"""Configuration Drift Monitor - defensive, offline portfolio mini-project."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def analyze(data:dict)->dict:
    flatten=lambda d,p="":{(p+k):v for k,v in d.items() if not isinstance(v,dict)}|{kk:vv for k,v in d.items() if isinstance(v,dict) for kk,vv in flatten(v,p+k+".").items()};base=flatten(data["baseline"]);current=flatten(data["current"]);return {"changed":{k:{"baseline":base[k],"current":current[k]} for k in base.keys()&current.keys() if base[k]!=current[k]},"missing":sorted(base.keys()-current.keys()),"added":sorted(current.keys()-base.keys()),"changes_applied":False}

def main()->None:
 parser=argparse.ArgumentParser(description='Configuration Drift Monitor')
 parser.add_argument("--input",type=Path,default=Path("sample.json"))
 args=parser.parse_args();print(json.dumps(analyze(json.loads(args.input.read_text())),indent=2))
if __name__=="__main__":main()
