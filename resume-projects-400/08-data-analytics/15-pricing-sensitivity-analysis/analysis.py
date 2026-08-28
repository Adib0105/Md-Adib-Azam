#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from analytics_core import *

def analyze(rows):
    products={}
    for r in rows:products.setdefault(r["product"],[]).append(r)
    elasticity={}
    for product,obs in products.items():
     a,b=obs;dq=(f(b,"quantity")-f(a,"quantity"))/mean([f(a,"quantity"),f(b,"quantity")]);dp=(f(b,"price")-f(a,"price"))/mean([f(a,"price"),f(b,"price")]);elasticity[product]=round2(dq/dp)
    return result({"midpoint_elasticity":elasticity,"interpretation":{k:("elastic" if abs(v)>1 else "inelastic") for k,v in elasticity.items()}},"Absolute elasticity by product",{k:abs(v) for k,v in elasticity.items()})

def main():
 root=Path(__file__).parent
 with (root/"data.csv").open(newline="",encoding="utf-8") as handle:rows=list(csv.DictReader(handle))
 output=analyze(rows);(root/"output").mkdir(exist_ok=True)
 (root/"output"/"summary.json").write_text(json.dumps(output["summary"],indent=2)+"\n")
 (root/"output"/"chart.svg").write_text(svg_bar(output["chart"]["title"],output["chart"]["data"]))
 print(json.dumps(output["summary"],indent=2))
if __name__=="__main__":main()
