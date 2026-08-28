#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from analytics_core import *

def analyze(rows):
    ordered=sorted(rows,key=lambda r:int(r["stage_order"]));steps=[];data={};prev=None
    for r in ordered:
     users=int(r["users"]);data[r["stage"]]=users
     if prev:steps.append({"from":prev["stage"],"to":r["stage"],"conversion_pct":pct(users,int(prev["users"])),"drop_off":int(prev["users"])-users})
     prev=r
    return result({"overall_conversion_pct":pct(int(ordered[-1]["users"]),int(ordered[0]["users"])),"steps":steps},"Users by funnel stage",data)

def main():
 root=Path(__file__).parent
 with (root/"data.csv").open(newline="",encoding="utf-8") as handle:rows=list(csv.DictReader(handle))
 output=analyze(rows);(root/"output").mkdir(exist_ok=True)
 (root/"output"/"summary.json").write_text(json.dumps(output["summary"],indent=2)+"\n")
 (root/"output"/"chart.svg").write_text(svg_bar(output["chart"]["title"],output["chart"]["data"]))
 print(json.dumps(output["summary"],indent=2))
if __name__=="__main__":main()
