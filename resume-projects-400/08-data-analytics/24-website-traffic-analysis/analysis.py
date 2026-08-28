#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from analytics_core import *

def analyze(rows):
    metrics={r["channel"]:{"conversion_rate_pct":pct(f(r,"conversions"),f(r,"sessions")),"bounce_rate_pct":pct(f(r,"bounces"),f(r,"sessions"))} for r in rows};best=max(metrics,key=lambda x:metrics[x]["conversion_rate_pct"]);return result({"channel_metrics":metrics,"best_conversion_channel":best,"total_sessions":sum(f(r,"sessions") for r in rows)},"Conversion rate by channel",{k:v["conversion_rate_pct"] for k,v in metrics.items()})

def main():
 root=Path(__file__).parent
 with (root/"data.csv").open(newline="",encoding="utf-8") as handle:rows=list(csv.DictReader(handle))
 output=analyze(rows);(root/"output").mkdir(exist_ok=True)
 (root/"output"/"summary.json").write_text(json.dumps(output["summary"],indent=2)+"\n")
 (root/"output"/"chart.svg").write_text(svg_bar(output["chart"]["title"],output["chart"]["data"]))
 print(json.dumps(output["summary"],indent=2))
if __name__=="__main__":main()
