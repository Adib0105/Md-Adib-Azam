#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from analytics_core import *

def analyze(rows):
    suppliers={}
    for r in rows:suppliers.setdefault(r["supplier"],[]).append(int(r["on_time"])==1 and int(r["in_full"])==1)
    otif={k:pct(sum(v),len(v)) for k,v in suppliers.items()};return result({"otif_by_supplier_pct":otif,"overall_otif_pct":pct(sum(sum(v) for v in suppliers.values()),len(rows)),"best_supplier":max(otif,key=otif.get)},"OTIF by supplier",otif)

def main():
 root=Path(__file__).parent
 with (root/"data.csv").open(newline="",encoding="utf-8") as handle:rows=list(csv.DictReader(handle))
 output=analyze(rows);(root/"output").mkdir(exist_ok=True)
 (root/"output"/"summary.json").write_text(json.dumps(output["summary"],indent=2)+"\n")
 (root/"output"/"chart.svg").write_text(svg_bar(output["chart"]["title"],output["chart"]["data"]))
 print(json.dumps(output["summary"],indent=2))
if __name__=="__main__":main()
