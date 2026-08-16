# 09. Hospital Readmission Risk

## Business problem

Predicts 30-day readmission and audits subgroup performance for deployment safety.

## Analytics approach

Gradient boosting, calibration, recall@capacity, subgroup gap. The pipeline generates a deterministic, realistic dataset, trains or calculates the analytical model, evaluates decision-focused KPIs, and writes a machine-readable metrics file plus a management brief.

## Run

```bash
python advanced-data-analytics/projects/09-healthcare-readmission/app.py
```

## Deliverables

- Reproducible data simulation and analytical pipeline
- Model or decision metrics in `metrics.json`
- Actionable recommendations in `decision_brief.md`
- Smoke-tested execution through the collection CI
