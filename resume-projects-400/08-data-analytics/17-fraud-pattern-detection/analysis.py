#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from analytics_core import *

def analyze(rows):
    values=[f(r,"amount") for r in rows];mu=mean(values);sd=stdev(values);scored=[{"transaction":r["transaction"],"amount":f(r,"amount"),"z_score":round2((f(r,"amount")-mu)/sd),"flag":abs((f(r,"amount")-mu)/sd)>=2} for r in rows];return result({"mean":round2(mu),"standard_deviation":round2(sd),"flagged":[x for x in scored if x["flag"]],"method":"z-score >= 2; review only, not proof of fraud"},"Transaction amount",{r["transaction"]:f(r,"amount") for r in rows})

def main():
 root=Path(__file__).parent
 with (root/"data.csv").open(newline="",encoding="utf-8") as handle:rows=list(csv.DictReader(handle))
 output=analyze(rows);(root/"output").mkdir(exist_ok=True)
 (root/"output"/"summary.json").write_text(json.dumps(output["summary"],indent=2)+"\n")
 (root/"output"/"chart.svg").write_text(svg_bar(output["chart"]["title"],output["chart"]["data"]))
 print(json.dumps(output["summary"],indent=2))
if __name__=="__main__":main()
