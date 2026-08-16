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

from scipy.stats import ks_2samp
from sklearn.calibration import CalibratedClassifierCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def run(output_dir=None):
    rng = np.random.default_rng(103); n = 6000
    x = pd.DataFrame({"income": rng.lognormal(10.7,.45,n), "debt_ratio": rng.beta(2,5,n), "utilization": rng.beta(2.2,2.8,n), "delinquencies": rng.poisson(.35,n), "age": rng.integers(21,70,n), "credit_history": rng.integers(1,25,n)})
    z = -3.2 - .000018*x.income + 2.6*x.debt_ratio + 2*x.utilization + .75*x.delinquencies - .02*x.credit_history
    y = rng.binomial(1, 1/(1+np.exp(-z)))
    cut = 4800
    base = make_pipeline(StandardScaler(), LogisticRegression(max_iter=800, C=.7))
    model = CalibratedClassifierCV(base, method="sigmoid", cv=3).fit(x.iloc[:cut], y[:cut])
    pd_hat = model.predict_proba(x.iloc[cut:])[:,1]; actual=y[cut:]
    ks = ks_2samp(pd_hat[actual==1], pd_hat[actual==0]).statistic
    exposure = rng.uniform(20_000, 500_000, len(actual)); lgd = .45
    metrics = {"roc_auc": round(roc_auc_score(actual,pd_hat),3), "ks_statistic": round(ks,3), "brier_score": round(brier_score_loss(actual,pd_hat),3), "expected_loss_inr": round(float((exposure*lgd*pd_hat).sum()),0), "high_risk_share_pct": round(100*float((pd_hat>.35).mean()),2)}
    return save_result("credit-risk-scorecard", metrics, ["Apply manual review to the high-PD band instead of a single hard decline rule.", "Track calibration monthly before using predicted PD for pricing."], output_dir)

if __name__ == "__main__": print(json.dumps(run(), indent=2))
