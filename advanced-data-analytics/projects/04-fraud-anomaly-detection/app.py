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
    rng=np.random.default_rng(104); n=8000
    amount=rng.lognormal(4.2,1,n); hour=rng.integers(0,24,n); velocity=rng.poisson(1.2,n); distance=rng.exponential(25,n); device_age=rng.exponential(300,n)
    fraud=((amount>np.quantile(amount,.985)) | ((hour<5)&(velocity>3)) | ((distance>100)&(device_age<5))).astype(int)
    flip=rng.choice(n,35,replace=False); fraud[flip]=1
    x=np.c_[np.log1p(amount),hour,velocity,np.log1p(distance),np.log1p(device_age)]
    score=-IsolationForest(n_estimators=180,contamination=.02,random_state=104).fit(RobustScaler().fit_transform(x)).score_samples(RobustScaler().fit_transform(x))
    k=max(1,int(.02*n)); flagged=np.argsort(score)[-k:]
    metrics={"pr_auc":round(average_precision_score(fraud,score),3),"recall_at_2_pct":round(float(fraud[flagged].sum()/fraud.sum()),3),"precision_at_2_pct":round(float(fraud[flagged].mean()),3),"fraud_amount_captured_pct":round(100*float(amount[flagged][fraud[flagged]==1].sum()/amount[fraud==1].sum()),2)}
    return save_result("fraud-anomaly-detection",metrics,["Investigate the top 2% anomaly queue with amount-weighted priority.","Retrain contamination thresholds when payment mix changes."],output_dir)

if __name__ == "__main__": print(json.dumps(run(),indent=2))
