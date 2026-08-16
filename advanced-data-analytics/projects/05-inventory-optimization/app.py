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

from scipy.stats import norm


def run(output_dir=None):
    rng=np.random.default_rng(105); skus=250
    daily_mean=rng.lognormal(2.7,.65,skus); daily_sd=np.sqrt(daily_mean)*rng.uniform(1,2,skus); lead=rng.integers(2,18,skus); unit_cost=rng.uniform(80,2500,skus)
    z=norm.ppf(.95); safety=z*daily_sd*np.sqrt(lead); reorder=daily_mean*lead+safety
    simulations=1200
    demand=rng.normal(daily_mean[:,None]*lead[:,None],daily_sd[:,None]*np.sqrt(lead[:,None]),(skus,simulations)).clip(0)
    stockout=demand>reorder[:,None]; service=1-stockout.mean()
    holding=float((safety*unit_cost*.18).sum()); shortage=float((np.maximum(demand-reorder[:,None],0).mean(axis=1)*unit_cost*1.6).sum())
    baseline=daily_mean*lead
    baseline_service=1-float((demand>baseline[:,None]).mean())
    metrics={"optimized_service_level_pct":round(100*service,2),"baseline_service_level_pct":round(100*baseline_service,2),"annual_safety_stock_cost_inr":round(holding,0),"expected_shortage_cost_inr":round(shortage,0),"reorder_capital_inr":round(float((reorder*unit_cost).sum()),0)}
    return save_result("inventory-optimization",metrics,["Adopt SKU-specific reorder points based on lead-time uncertainty.","Review expensive slow movers before applying a uniform 95% service target."],output_dir)

if __name__ == "__main__": print(json.dumps(run(),indent=2))
