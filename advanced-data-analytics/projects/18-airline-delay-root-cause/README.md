# 18. Airline Delay Root-Cause Analytics

## Business problem

Forecasts delay minutes and ranks operational drivers with permutation importance.

## Analytics approach

Boosted regression, MAE, severe-delay AUC, driver ranking. The pipeline generates a deterministic, realistic dataset, trains or calculates the analytical model, evaluates decision-focused KPIs, and writes a machine-readable metrics file plus a management brief.

## Run

```bash
python advanced-data-analytics/projects/18-airline-delay-root-cause/app.py
```

## Deliverables

- Reproducible data simulation and analytical pipeline
- Model or decision metrics in `metrics.json`
- Actionable recommendations in `decision_brief.md`
- Smoke-tested execution through the collection CI
