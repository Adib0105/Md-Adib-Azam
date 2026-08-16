# 03. Credit Risk Scorecard

## Business problem

Produces calibrated probability-of-default estimates and portfolio expected loss.

## Analytics approach

Logistic scorecard, KS statistic, Brier score, PD bands. The pipeline generates a deterministic, realistic dataset, trains or calculates the analytical model, evaluates decision-focused KPIs, and writes a machine-readable metrics file plus a management brief.

## Run

```bash
python advanced-data-analytics/projects/03-credit-risk-scorecard/app.py
```

## Deliverables

- Reproducible data simulation and analytical pipeline
- Model or decision metrics in `metrics.json`
- Actionable recommendations in `decision_brief.md`
- Smoke-tested execution through the collection CI
