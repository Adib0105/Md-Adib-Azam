#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from analytics_core import *

def analyze(rows):
    baskets={};[(baskets.setdefault(r["order"],set()).add(r["product"])) for r in rows];pairs=Counter()
    for basket in baskets.values():
     for pair in combinations(sorted(basket),2):pairs[" + ".join(pair)]+=1
    return result({"orders":len(baskets),"pair_counts":dict(pairs),"top_pair":pairs.most_common(1)[0][0]},"Product pair frequency",dict(pairs))

def main():
 root=Path(__file__).parent
 with (root/"data.csv").open(newline="",encoding="utf-8") as handle:rows=list(csv.DictReader(handle))
 output=analyze(rows);(root/"output").mkdir(exist_ok=True)
 (root/"output"/"summary.json").write_text(json.dumps(output["summary"],indent=2)+"\n")
 (root/"output"/"chart.svg").write_text(svg_bar(output["chart"]["title"],output["chart"]["data"]))
 print(json.dumps(output["summary"],indent=2))
if __name__=="__main__":main()
