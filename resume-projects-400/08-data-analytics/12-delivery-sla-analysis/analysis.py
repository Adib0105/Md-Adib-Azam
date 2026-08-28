#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from analytics_core import *

def analyze(rows):
    couriers={}
    for r in rows:couriers.setdefault(r["courier"],[]).append(f(r,"actual_days")<=f(r,"promised_days"))
    rates={k:pct(sum(v),len(v)) for k,v in couriers.items()};delays=[f(r,"actual_days")-f(r,"promised_days") for r in rows];return result({"on_time_by_courier_pct":rates,"average_delay_days":round2(mean(delays))},"On-time delivery by courier",rates)

def main():
 root=Path(__file__).parent
 with (root/"data.csv").open(newline="",encoding="utf-8") as handle:rows=list(csv.DictReader(handle))
 output=analyze(rows);(root/"output").mkdir(exist_ok=True)
 (root/"output"/"summary.json").write_text(json.dumps(output["summary"],indent=2)+"\n")
 (root/"output"/"chart.svg").write_text(svg_bar(output["chart"]["title"],output["chart"]["data"]))
 print(json.dumps(output["summary"],indent=2))
if __name__=="__main__":main()
