#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from analytics_core import *

def analyze(rows):
    variance={r["category"]:f(r,"budget")-f(r,"actual") for r in rows};actual={r["category"]:f(r,"actual") for r in rows};return result({"budget":sum(f(r,"budget") for r in rows),"actual":sum(actual.values()),"variance":sum(variance.values()),"overspent_categories":[k for k,v in variance.items() if v<0]},"Actual expense by category",actual)

def main():
 root=Path(__file__).parent
 with (root/"data.csv").open(newline="",encoding="utf-8") as handle:rows=list(csv.DictReader(handle))
 output=analyze(rows);(root/"output").mkdir(exist_ok=True)
 (root/"output"/"summary.json").write_text(json.dumps(output["summary"],indent=2)+"\n")
 (root/"output"/"chart.svg").write_text(svg_bar(output["chart"]["title"],output["chart"]["data"]))
 print(json.dumps(output["summary"],indent=2))
if __name__=="__main__":main()
