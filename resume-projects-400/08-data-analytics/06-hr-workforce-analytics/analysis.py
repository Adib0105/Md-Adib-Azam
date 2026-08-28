#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from analytics_core import *

def analyze(rows):
    departments={};[(departments.setdefault(r["department"],[]).append(int(r["attrition"]))) for r in rows];rates={k:pct(sum(v),len(v)) for k,v in departments.items()};return result({"headcount":{k:len(v) for k,v in departments.items()},"attrition_rate_pct":rates,"overall_attrition_pct":pct(sum(int(r["attrition"]) for r in rows),len(rows))},"Attrition rate by department",rates)

def main():
 root=Path(__file__).parent
 with (root/"data.csv").open(newline="",encoding="utf-8") as handle:rows=list(csv.DictReader(handle))
 output=analyze(rows);(root/"output").mkdir(exist_ok=True)
 (root/"output"/"summary.json").write_text(json.dumps(output["summary"],indent=2)+"\n")
 (root/"output"/"chart.svg").write_text(svg_bar(output["chart"]["title"],output["chart"]["data"]))
 print(json.dumps(output["summary"],indent=2))
if __name__=="__main__":main()
