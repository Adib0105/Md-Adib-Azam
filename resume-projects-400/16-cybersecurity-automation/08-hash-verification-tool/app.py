#!/usr/bin/env python3
"""Hash Verification Tool - defensive, offline portfolio mini-project."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def analyze(data:dict)->dict:
    import hashlib,hmac
    results=[]
    for item in data["items"]:
     actual=hashlib.sha256(item["content"].encode()).hexdigest();results.append({"name":item["name"],"actual_sha256":actual,"matches":hmac.compare_digest(actual,item["expected_sha256"])})
    return {"verified":sum(x["matches"] for x in results),"failed":[x["name"] for x in results if not x["matches"]],"results":results}

def main()->None:
 parser=argparse.ArgumentParser(description='Hash Verification Tool')
 parser.add_argument("--input",type=Path,default=Path("sample.json"))
 args=parser.parse_args();print(json.dumps(analyze(json.loads(args.input.read_text())),indent=2))
if __name__=="__main__":main()
