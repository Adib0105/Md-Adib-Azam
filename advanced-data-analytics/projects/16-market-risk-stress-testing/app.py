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


def run(output_dir=None):
    rng=np.random.default_rng(116); assets=6; weights=np.array([.24,.2,.18,.16,.12,.1]); vol=np.array([.012,.016,.011,.02,.014,.018]); corr=np.full((assets,assets),.28); np.fill_diagonal(corr,1); cov=np.outer(vol,vol)*corr
    returns=rng.multivariate_normal(np.full(assets,.00035),cov,1500); portfolio=returns@weights; losses=-portfolio; var=np.quantile(losses,.99); cvar=losses[losses>=var].mean()
    sims=rng.multivariate_normal(returns.mean(0),np.cov(returns,rowvar=False),30000)@weights; capital=10_000_000; stress=np.array([-.08,-.12,-.06,-.18,-.1,-.14])@weights
    metrics={"historical_var_99_inr":round(float(var*capital),0),"expected_shortfall_99_inr":round(float(cvar*capital),0),"monte_carlo_loss_probability_pct":round(100*float((sims<0).mean()),2),"stress_loss_inr":round(float(-stress*capital),0),"annualized_volatility_pct":round(100*float(np.std(portfolio)*np.sqrt(252)),2)}
    return save_result("market-risk-stress-testing",metrics,["Size risk limits from expected shortfall as well as VaR.","Treat the stress scenario as a capital-planning input, not a forecast."],output_dir)

if __name__ == "__main__": print(json.dumps(run(),indent=2))
