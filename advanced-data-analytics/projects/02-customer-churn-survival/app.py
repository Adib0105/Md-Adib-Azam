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
from sklearn.metrics import average_precision_score, roc_auc_score


def run(output_dir=None):
    rng = np.random.default_rng(102)
    n = 5000
    x = pd.DataFrame({
        "tenure": rng.integers(1, 73, n), "monthly_fee": rng.normal(70, 20, n).clip(15),
        "tickets": rng.poisson(1.8, n), "usage_drop": rng.normal(.05, .18, n),
        "late_payments": rng.poisson(.6, n), "contract_months": rng.choice([1, 12, 24], n, p=[.55, .3, .15]),
    })
    logit = -2.4 - .025*x.tenure + .018*(x.monthly_fee-60) + .42*x.tickets + 2.8*x.usage_drop + .5*x.late_payments - .05*x.contract_months
    y = rng.binomial(1, 1/(1+np.exp(-logit)))
    cut = 4000
    model = HistGradientBoostingClassifier(max_iter=130, max_leaf_nodes=15, random_state=102).fit(x.iloc[:cut], y[:cut])
    score = model.predict_proba(x.iloc[cut:])[:, 1]
    actual = y[cut:]
    k = max(1, len(score)//10)
    idx = np.argsort(score)[-k:]
    lift = actual[idx].mean() / max(actual.mean(), 1e-9)
    saved_value = float((x.iloc[cut:].monthly_fee.to_numpy()[idx] * 6 * actual[idx] * .28).sum())
    metrics = {"roc_auc": round(roc_auc_score(actual, score), 3), "pr_auc": round(average_precision_score(actual, score), 3), "lift_at_10_pct": round(lift, 2), "campaign_value_inr": round(saved_value * 83, 0)}
    return save_result("customer-churn-survival", metrics, ["Contact the highest-risk decile with contract-specific offers.", "Prioritize usage-drop and repeated-ticket journeys for service recovery."], output_dir)

if __name__ == "__main__": print(json.dumps(run(), indent=2))
