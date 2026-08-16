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

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error


def run(output_dir=None):
    rng=np.random.default_rng(112); hours=24*180; t=np.arange(hours); temp=27+7*np.sin(2*np.pi*t/(24*90))+3*np.sin(2*np.pi*t/24)+rng.normal(0,1.5,hours)
    load=900+190*np.sin(2*np.pi*(t-8)/24)+4.5*(temp-24)**2+90*(t%168<120)+rng.normal(0,35,hours)
    df=pd.DataFrame({"temp":temp,"hour_sin":np.sin(2*np.pi*t/24),"hour_cos":np.cos(2*np.pi*t/24),"week_sin":np.sin(2*np.pi*t/168),"trend":t/hours,"load":load})
    df["lag24"]=df.load.shift(24); df["lag168"]=df.load.shift(168); df=df.dropna(); cut=int(.8*len(df)); train,test=df.iloc[:cut],df.iloc[cut:]; features=[c for c in df if c!="load"]
    model=GradientBoostingRegressor(n_estimators=160,max_depth=3,loss="huber",random_state=112).fit(train[features],train.load); pred=model.predict(test[features]); residual=train.load-model.predict(train[features]); q=np.quantile(np.abs(residual),.9)
    peak=test.load>=np.quantile(test.load,.9); metrics={"mape_pct":round(100*float(np.mean(np.abs((test.load-pred)/test.load))),2),"rmse_mw":round(float(np.sqrt(mean_squared_error(test.load,pred))),2),"peak_rmse_mw":round(float(np.sqrt(mean_squared_error(test.load[peak],pred[peak]))),2),"prediction_interval_coverage_pct":round(100*float((np.abs(test.load-pred)<=q).mean()),2)}
    return save_result("energy-load-forecasting",metrics,["Use peak-error monitoring for capacity decisions, not only average MAPE.","Recalibrate residual intervals when temperature distribution shifts."],output_dir)

if __name__ == "__main__": print(json.dumps(run(),indent=2))
