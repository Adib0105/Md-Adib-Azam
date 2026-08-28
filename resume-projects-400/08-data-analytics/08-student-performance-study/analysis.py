#!/usr/bin/env python3
from __future__ import annotations
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from analytics_core import *

def analyze(rows):
    subjects={};[(subjects.setdefault(r["subject"],[]).append(f(r,"score"))) for r in rows];averages={k:round2(mean(v)) for k,v in subjects.items()};corr=pearson([f(r,"study_hours") for r in rows],[f(r,"score") for r in rows]);return result({"subject_average":averages,"study_score_correlation":corr,"sample_size":len(rows)},"Average score by subject",averages)

def main():
 root=Path(__file__).parent
 with (root/"data.csv").open(newline="",encoding="utf-8") as handle:rows=list(csv.DictReader(handle))
 output=analyze(rows);(root/"output").mkdir(exist_ok=True)
 (root/"output"/"summary.json").write_text(json.dumps(output["summary"],indent=2)+"\n")
 (root/"output"/"chart.svg").write_text(svg_bar(output["chart"]["title"],output["chart"]["data"]))
 print(json.dumps(output["summary"],indent=2))
if __name__=="__main__":main()
