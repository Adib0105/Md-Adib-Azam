#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from analytics_core import *

def analyze(rows):
    ratings=Counter(int(r["rating"]) for r in rows);low=Counter(r["theme"] for r in rows if int(r["rating"])<=2);return result({"average_rating":round2(mean(int(r["rating"]) for r in rows)),"rating_distribution":dict(sorted(ratings.items())),"low_rating_themes":dict(low)},"Review count by rating",{str(k):v for k,v in sorted(ratings.items())})

def main():
 root=Path(__file__).parent
 with (root/"data.csv").open(newline="",encoding="utf-8") as handle:rows=list(csv.DictReader(handle))
 output=analyze(rows);(root/"output").mkdir(exist_ok=True)
 (root/"output"/"summary.json").write_text(json.dumps(output["summary"],indent=2)+"\n")
 (root/"output"/"chart.svg").write_text(svg_bar(output["chart"]["title"],output["chart"]["data"]))
 print(json.dumps(output["summary"],indent=2))
if __name__=="__main__":main()
