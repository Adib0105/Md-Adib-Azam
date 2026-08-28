#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from analytics_core import *

def analyze(rows):
    a,b=rows;ra=f(a,"conversions")/f(a,"visitors");rb=f(b,"conversions")/f(b,"visitors");p=(f(a,"conversions")+f(b,"conversions"))/(f(a,"visitors")+f(b,"visitors"));se=(p*(1-p)*(1/f(a,"visitors")+1/f(b,"visitors")))**.5;z=(rb-ra)/se;return result({"control_rate_pct":round2(ra*100),"treatment_rate_pct":round2(rb*100),"relative_lift_pct":round2((rb-ra)/ra*100),"z_score":round2(z),"note":"Approximate test; check experiment design before causal claims."},"Conversion rate by variant",{a["variant"]:ra*100,b["variant"]:rb*100})

def main():
 root=Path(__file__).parent
 with (root/"data.csv").open(newline="",encoding="utf-8") as handle:rows=list(csv.DictReader(handle))
 output=analyze(rows);(root/"output").mkdir(exist_ok=True)
 (root/"output"/"summary.json").write_text(json.dumps(output["summary"],indent=2)+"\n")
 (root/"output"/"chart.svg").write_text(svg_bar(output["chart"]["title"],output["chart"]["data"]))
 print(json.dumps(output["summary"],indent=2))
if __name__=="__main__":main()
