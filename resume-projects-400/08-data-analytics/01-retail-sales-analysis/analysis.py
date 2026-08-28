#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from analytics_core import *

def analyze(rows):
    by_category=group_sum(rows,"category","revenue");by_month=group_sum(rows,"month","revenue");months=list(by_month);growth=pct(by_month[months[-1]]-by_month[months[0]],by_month[months[0]]);return result({"total_revenue":sum(by_category.values()),"category_revenue":by_category,"first_to_last_month_growth_pct":growth},"Revenue by category",by_category)

def main():
 root=Path(__file__).parent
 with (root/"data.csv").open(newline="",encoding="utf-8") as handle:rows=list(csv.DictReader(handle))
 output=analyze(rows);(root/"output").mkdir(exist_ok=True)
 (root/"output"/"summary.json").write_text(json.dumps(output["summary"],indent=2)+"\n")
 (root/"output"/"chart.svg").write_text(svg_bar(output["chart"]["title"],output["chart"]["data"]))
 print(json.dumps(output["summary"],indent=2))
if __name__=="__main__":main()
