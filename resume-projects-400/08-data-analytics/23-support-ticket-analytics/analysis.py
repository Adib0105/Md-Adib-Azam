#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from analytics_core import *

def analyze(rows):
    categories={}
    for r in rows:categories.setdefault(r["category"],[]).append(r)
    sla={k:pct(sum(int(x["sla_met"]) for x in v),len(v)) for k,v in categories.items()};volume={k:len(v) for k,v in categories.items()};return result({"ticket_volume":volume,"sla_by_category_pct":sla,"average_resolution_hours":{k:round2(mean(f(x,"resolution_hours") for x in v)) for k,v in categories.items()}},"Ticket volume by category",volume)

def main():
 root=Path(__file__).parent
 with (root/"data.csv").open(newline="",encoding="utf-8") as handle:rows=list(csv.DictReader(handle))
 output=analyze(rows);(root/"output").mkdir(exist_ok=True)
 (root/"output"/"summary.json").write_text(json.dumps(output["summary"],indent=2)+"\n")
 (root/"output"/"chart.svg").write_text(svg_bar(output["chart"]["title"],output["chart"]["data"]))
 print(json.dumps(output["summary"],indent=2))
if __name__=="__main__":main()
