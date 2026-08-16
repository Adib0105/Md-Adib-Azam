# 12. Energy Load Forecasting

## Business problem

Forecasts hourly electricity demand and validates peak-load and interval performance.

## Analytics approach

Cyclical features, boosting, MAPE, prediction-interval coverage. The pipeline generates a deterministic, realistic dataset, trains or calculates the analytical model, evaluates decision-focused KPIs, and writes a machine-readable metrics file plus a management brief.

## Run

```bash
python advanced-data-analytics/projects/12-energy-load-forecasting/app.py
```

## Deliverables

- Reproducible data simulation and analytical pipeline
- Model or decision metrics in `metrics.json`
- Actionable recommendations in `decision_brief.md`
- Smoke-tested execution through the collection CI
