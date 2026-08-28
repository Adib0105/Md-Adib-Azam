#!/usr/bin/env python3
"""Firewall Rule Auditor - defensive, offline portfolio mini-project."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def analyze(data:dict)->dict:
    import ipaddress
    findings=[]
    for rule in data["rules"]:
     reasons=[];network=ipaddress.ip_network(rule["source"],strict=False)
     if network.prefixlen==0:reasons.append("source allows all addresses")
     if rule["port"]=="any":reasons.append("port allows any service")
     if not rule.get("justification","").strip():reasons.append("missing justification")
     if reasons:findings.append({"rule_id":rule["id"],"reasons":reasons})
    return {"rules":len(data["rules"]),"findings":findings,"changes_applied":False}

def main()->None:
 parser=argparse.ArgumentParser(description='Firewall Rule Auditor')
 parser.add_argument("--input",type=Path,default=Path("sample.json"))
 args=parser.parse_args();print(json.dumps(analyze(json.loads(args.input.read_text())),indent=2))
if __name__=="__main__":main()
