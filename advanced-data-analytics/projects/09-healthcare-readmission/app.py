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

from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import brier_score_loss, roc_auc_score


def run(output_dir=None):
    rng=np.random.default_rng(109); n=5500
    x=pd.DataFrame({"age":rng.integers(18,91,n),"prior_admissions":rng.poisson(1.1,n),"los":rng.gamma(2.2,2,n),"comorbidity":rng.integers(0,8,n),"medications":rng.poisson(5,n),"followup_days":rng.integers(1,35,n)})
    z=-3+.025*(x.age-50)+.48*x.prior_admissions+.19*x.comorbidity+.045*x.los-.055*x.followup_days
    y=rng.binomial(1,1/(1+np.exp(-z))); cut=4400
    model=HistGradientBoostingClassifier(max_iter=140,max_leaf_nodes=18,random_state=109).fit(x.iloc[:cut],y[:cut]); score=model.predict_proba(x.iloc[cut:])[:,1]; actual=y[cut:]; test=x.iloc[cut:]
    k=int(.2*len(score)); flagged=np.argsort(score)[-k:]; recall=float(actual[flagged].sum()/max(actual.sum(),1))
    young=test.age.to_numpy()<65; r1=actual[flagged][young[flagged]].mean() if young[flagged].any() else 0; r2=actual[flagged][~young[flagged]].mean() if (~young[flagged]).any() else 0
    metrics={"roc_auc":round(roc_auc_score(actual,score),3),"brier_score":round(brier_score_loss(actual,score),3),"recall_at_20_pct_capacity":round(recall,3),"flagged_risk_gap_by_age":round(float(abs(r1-r2)),3),"readmission_rate_pct":round(100*float(actual.mean()),2)}
    return save_result("healthcare-readmission",metrics,["Assign care-management slots by risk while retaining clinician review.","Monitor calibration and age-subgroup gaps before deployment."],output_dir)

if __name__ == "__main__": print(json.dumps(run(),indent=2))
