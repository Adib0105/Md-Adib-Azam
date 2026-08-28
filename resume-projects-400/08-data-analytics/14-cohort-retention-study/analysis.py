#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from analytics_core import *

def analyze(rows):
    matrix={};by_index={}
    for r in rows:rate=pct(f(r,"active_users"),f(r,"starting_users"));matrix.setdefault(r["cohort"],{})[r["month_index"]]=rate;by_index.setdefault(r["month_index"],[]).append(rate)
    average={f"M{k}":round2(mean(v)) for k,v in sorted(by_index.items(),key=lambda x:int(x[0]))};return result({"retention_matrix_pct":matrix,"average_retention_pct":average},"Average retention by month",average)

def main():
 root=Path(__file__).parent
 with (root/"data.csv").open(newline="",encoding="utf-8") as handle:rows=list(csv.DictReader(handle))
 output=analyze(rows);(root/"output").mkdir(exist_ok=True)
 (root/"output"/"summary.json").write_text(json.dumps(output["summary"],indent=2)+"\n")
 (root/"output"/"chart.svg").write_text(svg_bar(output["chart"]["title"],output["chart"]["data"]))
 print(json.dumps(output["summary"],indent=2))
if __name__=="__main__":main()
