from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

PORTFOLIO = Path(__file__).resolve().parents[2]
if str(PORTFOLIO) not in sys.path:
    sys.path.insert(0, str(PORTFOLIO))
from portfolio_core import save_result

from sklearn.ensemble import IsolationForest
from sklearn.metrics import average_precision_score
from sklearn.preprocessing import RobustScaler


def run(output_dir=None):
    rng=np.random.default_rng(117); cells=500; periods=18; n=cells*periods
    cell=np.repeat(np.arange(cells),periods); throughput=rng.normal(42,7,n); drop=rng.beta(1.5,35,n); latency=rng.normal(38,8,n); utilization=rng.beta(5,2,n); handover=rng.beta(18,2,n); label=np.zeros(n,dtype=int)
    bad_cells=rng.choice(cells,22,replace=False); bad=np.isin(cell,bad_cells)&(np.tile(np.arange(periods),cells)>10); throughput[bad]-=22; drop[bad]+=.12; latency[bad]+=45; handover[bad]-=.18; label[bad]=1
    x=np.c_[throughput,drop,latency,utilization,handover]; scaled=RobustScaler().fit_transform(x); score=-IsolationForest(n_estimators=180,contamination=.035,random_state=117).fit(scaled).score_samples(scaled); k=int(.035*n); flagged=np.argsort(score)[-k:]
    detected=len(set(cell[flagged])&set(bad_cells)); metrics={"pr_auc":round(average_precision_score(label,score),3),"event_recall_at_capacity":round(float(label[flagged].sum()/label.sum()),3),"precision_at_capacity":round(float(label[flagged].mean()),3),"degraded_cells_detected":detected,"degraded_cells_total":len(bad_cells)}
    return save_result("telecom-kpi-anomalies",metrics,["Dispatch field checks to repeatedly flagged cells, not isolated events.","Rebaseline KPI distributions after capacity upgrades."],output_dir)

if __name__ == "__main__": print(json.dumps(run(),indent=2))
