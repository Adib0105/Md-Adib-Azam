#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from analytics_core import *

def analyze(rows):
    temps={r["month"]:f(r,"avg_temp_c") for r in rows};rain={r["month"]:f(r,"rain_mm") for r in rows};return result({"warmest_month":max(temps,key=temps.get),"wettest_month":max(rain,key=rain.get),"mean_temperature_c":round2(mean(temps.values()))},"Monthly rainfall (mm)",rain)

def main():
 root=Path(__file__).parent
 with (root/"data.csv").open(newline="",encoding="utf-8") as handle:rows=list(csv.DictReader(handle))
 output=analyze(rows);(root/"output").mkdir(exist_ok=True)
 (root/"output"/"summary.json").write_text(json.dumps(output["summary"],indent=2)+"\n")
 (root/"output"/"chart.svg").write_text(svg_bar(output["chart"]["title"],output["chart"]["data"]))
 print(json.dumps(output["summary"],indent=2))
if __name__=="__main__":main()
