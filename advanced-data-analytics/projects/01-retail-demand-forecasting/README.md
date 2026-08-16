# 01. Retail Demand Forecasting

## Business problem

SKU-level time-series forecasting with lag, rolling, price and promotion signals.

## Analytics approach

Gradient boosting, temporal validation, WAPE, peak-demand planning. The pipeline generates a deterministic, realistic dataset, trains or calculates the analytical model, evaluates decision-focused KPIs, and writes a machine-readable metrics file plus a management brief.

## Run

```bash
python advanced-data-analytics/projects/01-retail-demand-forecasting/app.py
```

## Deliverables

- Reproducible data simulation and analytical pipeline
- Model or decision metrics in `metrics.json`
- Actionable recommendations in `decision_brief.md`
- Smoke-tested execution through the collection CI
