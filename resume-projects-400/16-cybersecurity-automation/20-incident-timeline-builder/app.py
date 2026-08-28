#!/usr/bin/env python3
"""Incident Timeline Builder - defensive, offline portfolio mini-project."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def analyze(data:dict)->dict:
    from datetime import datetime,timezone
    events=[]
    for e in data["events"]:
     dt=datetime.fromisoformat(e["timestamp"].replace("Z","+00:00")).astimezone(timezone.utc);events.append({**e,"timestamp_utc":dt.isoformat().replace("+00:00","Z")})
    events.sort(key=lambda x:x["timestamp_utc"]);return {"incident_id":data["incident_id"],"timeline":events,"first_event":events[0]["timestamp_utc"],"last_event":events[-1]["timestamp_utc"],"evidence_preserved":True}

def main()->None:
 parser=argparse.ArgumentParser(description='Incident Timeline Builder')
 parser.add_argument("--input",type=Path,default=Path("sample.json"))
 args=parser.parse_args();print(json.dumps(analyze(json.loads(args.input.read_text())),indent=2))
if __name__=="__main__":main()
