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
from sklearn.metrics import mean_absolute_error, r2_score


def run(output_dir=None):
    rng=np.random.default_rng(119); n=5200
    x=pd.DataFrame({"area_sqft":rng.lognormal(7.2,.38,n),"bedrooms":rng.integers(1,6,n),"age":rng.exponential(14,n),"distance_km":rng.gamma(2,4,n),"amenity_score":rng.uniform(0,10,n),"floor":rng.integers(0,30,n)})
    price=900000+6200*x.area_sqft+480000*x.bedrooms-32000*x.age-180000*x.distance_km+240000*x.amenity_score+55000*x.floor+900*x.area_sqft*x.amenity_score+rng.normal(0,650000,n); cut=4200
    model=HistGradientBoostingRegressor(max_iter=180,l2_regularization=1,random_state=119).fit(x.iloc[:cut],price[:cut]); pred=model.predict(x.iloc[cut:]); actual=price[cut:]; imp=permutation_importance(model,x.iloc[cut:],actual,n_repeats=4,random_state=119).importances_mean; top=x.columns[int(np.argmax(imp))]
    luxury=actual>np.quantile(actual,.8); gap=abs(np.mean(np.abs(actual[luxury]-pred[luxury]))-np.mean(np.abs(actual[~luxury]-pred[~luxury])))
    metrics={"r2":round(r2_score(actual,pred),3),"mae_inr":round(mean_absolute_error(actual,pred),0),"mape_pct":round(100*float(np.mean(np.abs((actual-pred)/actual))),2),"top_price_driver":top,"luxury_error_gap_inr":round(float(gap),0)}
    return save_result("real-estate-explainability",metrics,[f"Expose {top} as a primary valuation driver in analyst review.","Maintain separate error thresholds for luxury listings."],output_dir)

if __name__ == "__main__": print(json.dumps(run(),indent=2))
