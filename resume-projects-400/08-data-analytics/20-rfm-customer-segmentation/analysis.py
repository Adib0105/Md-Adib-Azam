#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from analytics_core import *

def analyze(rows):
    def score(v,values,reverse=False):
     ordered=sorted(values,reverse=reverse);rank=ordered.index(v);return 5-min(4,int(rank*5/len(values)))
    rec=[f(r,"recency_days") for r in rows];freq=[f(r,"orders") for r in rows];money=[f(r,"revenue") for r in rows];customers=[]
    for r in rows:rs=score(f(r,"recency_days"),rec,True);fs=score(f(r,"orders"),freq);ms=score(f(r,"revenue"),money);customers.append({"customer":r["customer"],"rfm_score":rs*100+fs*10+ms,"segment":"champion" if rs>=4 and fs>=4 else "at risk" if rs<=2 else "regular"})
    segments=Counter(x["segment"] for x in customers);return result({"customers":customers,"segments":dict(segments)},"Customers by segment",dict(segments))

def main():
 root=Path(__file__).parent
 with (root/"data.csv").open(newline="",encoding="utf-8") as handle:rows=list(csv.DictReader(handle))
 output=analyze(rows);(root/"output").mkdir(exist_ok=True)
 (root/"output"/"summary.json").write_text(json.dumps(output["summary"],indent=2)+"\n")
 (root/"output"/"chart.svg").write_text(svg_bar(output["chart"]["title"],output["chart"]["data"]))
 print(json.dumps(output["summary"],indent=2))
if __name__=="__main__":main()
