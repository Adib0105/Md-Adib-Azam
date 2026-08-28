#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from analytics_core import *

def analyze(rows):
    n=len(rows);kpis={"aht_seconds":round2(mean(f(r,"aht_seconds") for r in rows)),"sla_pct":pct(sum(int(r["sla_met"]) for r in rows),n),"fcr_pct":pct(sum(int(r["first_contact_resolved"]) for r in rows),n),"csat":round2(mean(f(r,"csat") for r in rows))};return result(kpis,"Service KPI score",{"SLA %":kpis["sla_pct"],"FCR %":kpis["fcr_pct"],"CSAT x20":kpis["csat"]*20})

def main():
 root=Path(__file__).parent
 with (root/"data.csv").open(newline="",encoding="utf-8") as handle:rows=list(csv.DictReader(handle))
 output=analyze(rows);(root/"output").mkdir(exist_ok=True)
 (root/"output"/"summary.json").write_text(json.dumps(output["summary"],indent=2)+"\n")
 (root/"output"/"chart.svg").write_text(svg_bar(output["chart"]["title"],output["chart"]["data"]))
 print(json.dumps(output["summary"],indent=2))
if __name__=="__main__":main()
