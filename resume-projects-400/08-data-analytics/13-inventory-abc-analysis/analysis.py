#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from analytics_core import *

def analyze(rows):
    items=sorted([{"sku":r["sku"],"value":f(r,"annual_units")*f(r,"unit_cost")} for r in rows],key=lambda x:x["value"],reverse=True);total=sum(x["value"] for x in items);running=0
    for x in items:running+=x["value"];share=running/total;x["class"]="A" if share<=.8 else "B" if share<=.95 else "C"
    counts=Counter(x["class"] for x in items);return result({"total_consumption_value":total,"items":items,"class_counts":dict(counts)},"Inventory value by SKU",{x["sku"]:x["value"] for x in items})

def main():
 root=Path(__file__).parent
 with (root/"data.csv").open(newline="",encoding="utf-8") as handle:rows=list(csv.DictReader(handle))
 output=analyze(rows);(root/"output").mkdir(exist_ok=True)
 (root/"output"/"summary.json").write_text(json.dumps(output["summary"],indent=2)+"\n")
 (root/"output"/"chart.svg").write_text(svg_bar(output["chart"]["title"],output["chart"]["data"]))
 print(json.dumps(output["summary"],indent=2))
if __name__=="__main__":main()
