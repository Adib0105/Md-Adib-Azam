# 19. Real Estate Price Explainability

## Business problem

Predicts property prices and audits error by market segment.

## Analytics approach

Nonlinear regression, permutation importance, segment error audit. The pipeline generates a deterministic, realistic dataset, trains or calculates the analytical model, evaluates decision-focused KPIs, and writes a machine-readable metrics file plus a management brief.

## Run

```bash
python advanced-data-analytics/projects/19-real-estate-explainability/app.py
```

## Deliverables

- Reproducible data simulation and analytical pipeline
- Model or decision metrics in `metrics.json`
- Actionable recommendations in `decision_brief.md`
- Smoke-tested execution through the collection CI
