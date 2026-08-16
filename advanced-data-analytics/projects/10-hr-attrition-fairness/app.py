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

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def run(output_dir=None):
    rng=np.random.default_rng(110); n=4800
    gender=rng.integers(0,2,n); x=pd.DataFrame({"tenure":rng.exponential(5,n),"salary_ratio":rng.normal(1,.2,n),"overtime":rng.binomial(1,.32,n),"satisfaction":rng.uniform(1,5,n),"manager_changes":rng.poisson(.45,n),"commute":rng.gamma(2,8,n)})
    z=-1.8-.18*x.tenure-.55*(x.salary_ratio-1)+.95*x.overtime-.5*(x.satisfaction-3)+.35*x.manager_changes+.018*x.commute
    y=rng.binomial(1,1/(1+np.exp(-z))); cut=3800
    model=make_pipeline(StandardScaler(),LogisticRegression(max_iter=700)).fit(x.iloc[:cut],y[:cut]); score=model.predict_proba(x.iloc[cut:])[:,1]; actual=y[cut:]; g=gender[cut:]; pred=score>=np.quantile(score,.8)
    positive_gap=abs(pred[g==0].mean()-pred[g==1].mean()); tpr=[]
    for group in (0,1): tpr.append(((pred)&(actual==1)&(g==group)).sum()/max(((actual==1)&(g==group)).sum(),1))
    metrics={"roc_auc":round(roc_auc_score(actual,score),3),"attrition_rate_pct":round(100*float(actual.mean()),2),"demographic_parity_gap":round(float(positive_gap),3),"equal_opportunity_gap":round(float(abs(tpr[0]-tpr[1])),3),"high_risk_recall":round(float(actual[pred].sum()/max(actual.sum(),1)),3)}
    return save_result("hr-attrition-fairness",metrics,["Use predictions for workload and manager interventions, never automatic employment decisions.","Audit opportunity gaps every model refresh."],output_dir)

if __name__ == "__main__": print(json.dumps(run(),indent=2))
