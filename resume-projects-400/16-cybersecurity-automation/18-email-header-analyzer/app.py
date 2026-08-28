#!/usr/bin/env python3
"""Email Header Analyzer - defensive, offline portfolio mini-project."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def analyze(data:dict)->dict:
    import re
    headers={k.lower():v for k,v in data["headers"].items()};auth=headers.get("authentication-results","").lower();checks={"spf_pass":"spf=pass" in auth,"dkim_pass":"dkim=pass" in auth,"dmarc_pass":"dmarc=pass" in auth};received=len(re.findall(r"\breceived\b"," ".join(headers.keys()),re.I));return {"authentication":checks,"all_pass":all(checks.values()),"received_header_count":received,"warning":"Headers can be forged; corroborate with mail-provider logs."}

def main()->None:
 parser=argparse.ArgumentParser(description='Email Header Analyzer')
 parser.add_argument("--input",type=Path,default=Path("sample.json"))
 args=parser.parse_args();print(json.dumps(analyze(json.loads(args.input.read_text())),indent=2))
if __name__=="__main__":main()
