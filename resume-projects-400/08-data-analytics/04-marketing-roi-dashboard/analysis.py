#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from analytics_core import *

def analyze(rows):
    metrics={r["campaign"]:{"roas":round2(f(r,"revenue")/f(r,"spend")),"profit":f(r,"revenue")-f(r,"spend")} for r in rows};best=max(metrics,key=lambda x:metrics[x]["roas"]);return result({"campaigns":metrics,"best_roas_campaign":best,"total_profit":sum(x["profit"] for x in metrics.values())},"ROAS by campaign",{k:v["roas"] for k,v in metrics.items()})

def main():
 root=Path(__file__).parent
 with (root/"data.csv").open(newline="",encoding="utf-8") as handle:rows=list(csv.DictReader(handle))
 output=analyze(rows);(root/"output").mkdir(exist_ok=True)
 (root/"output"/"summary.json").write_text(json.dumps(output["summary"],indent=2)+"\n")
 (root/"output"/"chart.svg").write_text(svg_bar(output["chart"]["title"],output["chart"]["data"]))
 print(json.dumps(output["summary"],indent=2))
if __name__=="__main__":main()
