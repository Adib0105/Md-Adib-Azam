#!/usr/bin/env python3
"""Security Checklist Generator - defensive, offline portfolio mini-project."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def analyze(data:dict)->dict:
    controls=[("MFA enabled",data["mfa"],"high"),("Backups tested",data["backup_tested"],"high"),("Automatic updates",data["auto_updates"],"medium"),("Least privilege review",data["least_privilege_reviewed"],"medium"),("Logging enabled",data["logging"],"high")];missing=[{"control":name,"priority":priority} for name,passed,priority in controls if not passed];return {"passed":sum(passed for _,passed,_ in controls),"total":len(controls),"missing":sorted(missing,key=lambda x:0 if x["priority"]=="high" else 1)}

def main()->None:
 parser=argparse.ArgumentParser(description='Security Checklist Generator')
 parser.add_argument("--input",type=Path,default=Path("sample.json"))
 args=parser.parse_args();print(json.dumps(analyze(json.loads(args.input.read_text())),indent=2))
if __name__=="__main__":main()
