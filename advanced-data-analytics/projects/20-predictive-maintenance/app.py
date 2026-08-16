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

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import average_precision_score, roc_auc_score


def run(output_dir=None):
    rng=np.random.default_rng(120); n=7000
    x=pd.DataFrame({"temperature":rng.normal(68,11,n),"vibration":rng.lognormal(-1,.55,n),"pressure":rng.normal(32,5,n),"runtime_hours":rng.exponential(2400,n),"error_count":rng.poisson(.8,n),"load":rng.beta(5,2,n)})
    z=-5+.075*(x.temperature-65)+3.5*x.vibration+.00045*x.runtime_hours+.45*x.error_count+1.3*x.load
    y=rng.binomial(1,1/(1+np.exp(-z))); cut=5600
    model=RandomForestClassifier(n_estimators=220,max_depth=9,class_weight="balanced",random_state=120,n_jobs=-1).fit(x.iloc[:cut],y[:cut]); score=model.predict_proba(x.iloc[cut:])[:,1]; actual=y[cut:]; k=int(.1*len(score)); flagged=np.argsort(score)[-k:]; recall=float(actual[flagged].sum()/max(actual.sum(),1))
    proactive_cost=k*3200; avoided=actual[flagged].sum()*28000*.7; net=float(avoided-proactive_cost)
    metrics={"roc_auc":round(roc_auc_score(actual,score),3),"pr_auc":round(average_precision_score(actual,score),3),"recall_at_10_pct_capacity":round(recall,3),"estimated_net_savings_inr":round(net,0),"machines_prioritized":k}
    return save_result("predictive-maintenance",metrics,["Inspect the top-risk 10% before the next production cycle.","Tune the threshold using downtime cost and technician capacity."],output_dir)

if __name__ == "__main__": print(json.dumps(run(),indent=2))
