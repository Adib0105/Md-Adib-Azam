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

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


def run(output_dir=None):
    rng=np.random.default_rng(108); n=3500
    recency=rng.exponential(55,n).clip(0,365); frequency=rng.lognormal(2.1,.7,n); monetary=rng.lognormal(5.1,.8,n); margin=rng.uniform(.18,.55,n); churn=np.clip(.04+.0015*recency-.002*frequency,.03,.8)
    clv=frequency*monetary*margin/np.maximum(churn,.03)
    x=np.c_[np.log1p(recency),np.log1p(frequency),np.log1p(monetary),margin]
    labels=KMeans(n_clusters=5,n_init=15,random_state=108).fit_predict(StandardScaler().fit_transform(x))
    seg=pd.DataFrame({"segment":labels,"clv":clv,"recency":recency}).groupby("segment").agg(size=("clv","size"),mean_clv=("clv","mean"),recency=("recency","mean"))
    best=int(seg.mean_clv.idxmax()); high_share=float(clv[labels==best].sum()/clv.sum())
    metrics={"silhouette_score":round(float(silhouette_score(StandardScaler().fit_transform(x),labels)),3),"segments":int(seg.shape[0]),"highest_value_segment":best,"high_value_clv_share_pct":round(100*high_share,2),"portfolio_clv_inr":round(float(clv.sum()),0)}
    return save_result("customer-segmentation-clv",metrics,[f"Build premium retention journeys for segment {best}.","Use predicted CLV, not revenue alone, for acquisition bid ceilings."],output_dir)

if __name__ == "__main__": print(json.dumps(run(),indent=2))
