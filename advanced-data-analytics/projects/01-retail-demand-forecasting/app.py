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
from sklearn.metrics import mean_absolute_error, mean_squared_error


def run(output_dir=None):
    rng = np.random.default_rng(101)
    days, skus = 420, 12
    rows = []
    for sku in range(skus):
        base = rng.uniform(35, 120)
        for day in range(days):
            promo = rng.binomial(1, 0.14)
            price = rng.normal(100 - sku * 1.5, 4)
            season = 12 * np.sin(2 * np.pi * day / 7) + 18 * np.sin(2 * np.pi * day / 365)
            demand = max(0, base + season + promo * 28 - 0.7 * (price - 90) + rng.normal(0, 8))
            rows.append((sku, day, price, promo, demand))
    df = pd.DataFrame(rows, columns=["sku", "day", "price", "promo", "demand"])
    for lag in (1, 7, 14, 28):
        df[f"lag_{lag}"] = df.groupby("sku")["demand"].shift(lag)
    df["rolling_7"] = df.groupby("sku")["demand"].transform(lambda s: s.shift(1).rolling(7).mean())
    df["dow_sin"] = np.sin(2 * np.pi * df.day / 7)
    df["dow_cos"] = np.cos(2 * np.pi * df.day / 7)
    df = df.dropna()
    train, test = df[df.day < 336], df[df.day >= 336]
    features = [c for c in df.columns if c not in {"demand"}]
    model = GradientBoostingRegressor(n_estimators=120, max_depth=3, random_state=101).fit(train[features], train.demand)
    pred = np.clip(model.predict(test[features]), 0, None)
    err = test.demand.to_numpy() - pred
    metrics = {
        "wape_pct": round(100 * np.abs(err).sum() / test.demand.sum(), 2),
        "mae_units": round(mean_absolute_error(test.demand, pred), 2),
        "rmse_units": round(np.sqrt(mean_squared_error(test.demand, pred)), 2),
        "peak_bias_pct": round(100 * err[test.demand.to_numpy() >= np.quantile(test.demand, .9)].mean() / test.demand.mean(), 2),
    }
    return save_result("retail-demand-forecasting", metrics, ["Use SKU-level forecasts for replenishment instead of portfolio averages.", "Review promotions with persistent positive forecast residuals."], output_dir)


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
