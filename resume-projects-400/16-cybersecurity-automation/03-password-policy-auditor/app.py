#!/usr/bin/env python3
"""Password Policy Auditor - defensive, offline portfolio mini-project."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def analyze(data:dict)->dict:
    import re,math
    p=data["password"];checks={"minimum_length":len(p)>=data.get("minimum_length",14),"uppercase":bool(re.search(r"[A-Z]",p)),"lowercase":bool(re.search(r"[a-z]",p)),"digit":bool(re.search(r"\d",p)),"symbol":bool(re.search(r"[^A-Za-z0-9]",p)),"not_common":p.lower() not in {x.lower() for x in data.get("blocked",[])}};classes=sum(checks[k] for k in ["uppercase","lowercase","digit","symbol"]);pool=[0,26,52,62,94][classes];entropy=round(len(p)*(math.log2(pool) if pool else 0),1);return {"compliant":all(checks.values()),"checks":checks,"estimated_entropy_bits":entropy}

def main()->None:
 parser=argparse.ArgumentParser(description='Password Policy Auditor')
 parser.add_argument("--input",type=Path,default=Path("sample.json"))
 args=parser.parse_args();print(json.dumps(analyze(json.loads(args.input.read_text())),indent=2))
if __name__=="__main__":main()
