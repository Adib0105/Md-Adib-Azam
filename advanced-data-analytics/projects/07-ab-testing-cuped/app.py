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

from scipy.stats import ttest_ind


def run(output_dir=None):
    rng=np.random.default_rng(107); n=7000
    pre=rng.gamma(2.4,22,n); group=rng.integers(0,2,n); noise=rng.normal(0,18,n)
    outcome=15+.72*pre+group*2.6+noise
    theta=np.cov(outcome,pre,ddof=1)[0,1]/np.var(pre,ddof=1); adjusted=outcome-theta*(pre-pre.mean())
    a,b=adjusted[group==0],adjusted[group==1]; effect=b.mean()-a.mean(); p=ttest_ind(a,b,equal_var=False).pvalue
    boots=np.array([rng.choice(b,len(b)).mean()-rng.choice(a,len(a)).mean() for _ in range(1500)])
    raw_var=np.var(outcome); reduction=1-np.var(adjusted)/raw_var
    metrics={"cuped_uplift":round(float(effect),3),"uplift_pct":round(100*float(effect/a.mean()),2),"p_value":round(float(p),5),"ci_95_low":round(float(np.quantile(boots,.025)),3),"ci_95_high":round(float(np.quantile(boots,.975)),3),"variance_reduction_pct":round(100*float(reduction),2)}
    return save_result("ab-testing-cuped",metrics,["Ship only if the confidence interval and business threshold both pass.","Reuse a stable pre-period covariate to reduce required sample size."],output_dir)

if __name__ == "__main__": print(json.dumps(run(),indent=2))
