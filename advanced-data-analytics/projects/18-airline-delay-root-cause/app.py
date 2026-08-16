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

from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.inspection import permutation_importance
from sklearn.metrics import mean_absolute_error, roc_auc_score


def run(output_dir=None):
    rng=np.random.default_rng(118); n=6500
    x=pd.DataFrame({"weather":rng.gamma(1.4,5,n),"late_aircraft":rng.gamma(1.7,8,n),"airport_load":rng.uniform(.3,1,n),"distance":rng.gamma(2,500,n),"turnaround":rng.normal(48,12,n),"crew_risk":rng.binomial(1,.08,n)})
    delay=np.maximum(0,2.4*x.weather+1.1*x.late_aircraft+36*np.maximum(x.airport_load-.72,0)+.02*x.distance-1.25*(x.turnaround-40)+24*x.crew_risk+rng.normal(0,10,n)); cut=5200
    model=HistGradientBoostingRegressor(max_iter=160,max_leaf_nodes=20,random_state=118).fit(x.iloc[:cut],delay[:cut]); pred=model.predict(x.iloc[cut:]); actual=delay[cut:]
    imp=permutation_importance(model,x.iloc[cut:],actual,n_repeats=4,random_state=118).importances_mean; top=x.columns[int(np.argmax(imp))]
    severe=actual>60; auc=roc_auc_score(severe,pred) if len(np.unique(severe))>1 else .5
    metrics={"mae_minutes":round(mean_absolute_error(actual,pred),2),"severe_delay_auc":round(auc,3),"on_time_rate_pct":round(100*float((actual<=15).mean()),2),"top_delay_driver":top,"p90_absolute_error":round(float(np.quantile(np.abs(actual-pred),.9)),2)}
    return save_result("airline-delay-root-cause",metrics,[f"Prioritize operational improvement around {top}.","Use severe-delay ranking for proactive passenger communication."],output_dir)

if __name__ == "__main__": print(json.dumps(run(),indent=2))
