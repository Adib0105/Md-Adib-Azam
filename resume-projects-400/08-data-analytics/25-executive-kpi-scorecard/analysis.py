#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from analytics_core import *

def analyze(rows):
    scorecard=[]
    for r in rows:actual=f(r,"actual");target=f(r,"target");met=actual>=target if r["direction"]=="higher" else actual<=target;attainment=actual/target*100 if r["direction"]=="higher" else target/actual*100;scorecard.append({"kpi":r["kpi"],"actual":actual,"target":target,"met":met,"attainment_pct":round2(attainment)})
    return result({"scorecard":scorecard,"targets_met":sum(x["met"] for x in scorecard),"total_kpis":len(scorecard)},"KPI attainment (%)",{x["kpi"]:x["attainment_pct"] for x in scorecard})

def main():
 root=Path(__file__).parent
 with (root/"data.csv").open(newline="",encoding="utf-8") as handle:rows=list(csv.DictReader(handle))
 output=analyze(rows);(root/"output").mkdir(exist_ok=True)
 (root/"output"/"summary.json").write_text(json.dumps(output["summary"],indent=2)+"\n")
 (root/"output"/"chart.svg").write_text(svg_bar(output["chart"]["title"],output["chart"]["data"]))
 print(json.dumps(output["summary"],indent=2))
if __name__=="__main__":main()
