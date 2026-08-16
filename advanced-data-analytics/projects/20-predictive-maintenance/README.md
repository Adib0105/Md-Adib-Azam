# 20. Predictive Maintenance Economics

## Business problem

Prioritizes machines likely to fail and estimates avoidable maintenance cost.

## Analytics approach

Random forest, PR-AUC, recall@10%, cost-benefit simulation. The pipeline generates a deterministic, realistic dataset, trains or calculates the analytical model, evaluates decision-focused KPIs, and writes a machine-readable metrics file plus a management brief.

## Run

```bash
python advanced-data-analytics/projects/20-predictive-maintenance/app.py
```

## Deliverables

- Reproducible data simulation and analytical pipeline
- Model or decision metrics in `metrics.json`
- Actionable recommendations in `decision_brief.md`
- Smoke-tested execution through the collection CI
