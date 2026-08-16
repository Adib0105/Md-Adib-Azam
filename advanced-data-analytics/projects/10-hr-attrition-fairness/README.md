# 10. HR Attrition & Fairness Audit

## Business problem

Predicts employee attrition while reporting demographic parity and opportunity gaps.

## Analytics approach

Explainable logistic model, ROC-AUC, fairness diagnostics. The pipeline generates a deterministic, realistic dataset, trains or calculates the analytical model, evaluates decision-focused KPIs, and writes a machine-readable metrics file plus a management brief.

## Run

```bash
python advanced-data-analytics/projects/10-hr-attrition-fairness/app.py
```

## Deliverables

- Reproducible data simulation and analytical pipeline
- Model or decision metrics in `metrics.json`
- Actionable recommendations in `decision_brief.md`
- Smoke-tested execution through the collection CI
