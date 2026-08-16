# 16. Portfolio Risk & Stress Testing

## Business problem

Estimates VaR/CVaR and compares historical, Monte Carlo and stressed losses.

## Analytics approach

Correlated simulation, VaR, expected shortfall, scenario analysis. The pipeline generates a deterministic, realistic dataset, trains or calculates the analytical model, evaluates decision-focused KPIs, and writes a machine-readable metrics file plus a management brief.

## Run

```bash
python advanced-data-analytics/projects/16-market-risk-stress-testing/app.py
```

## Deliverables

- Reproducible data simulation and analytical pipeline
- Model or decision metrics in `metrics.json`
- Actionable recommendations in `decision_brief.md`
- Smoke-tested execution through the collection CI
