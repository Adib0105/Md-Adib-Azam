# 05. Inventory & Service-Level Optimizer

## Business problem

Optimizes reorder points using demand uncertainty, lead time and holding cost.

## Analytics approach

Monte Carlo simulation, safety stock, stockout risk, cost trade-offs. The pipeline generates a deterministic, realistic dataset, trains or calculates the analytical model, evaluates decision-focused KPIs, and writes a machine-readable metrics file plus a management brief.

## Run

```bash
python advanced-data-analytics/projects/05-inventory-optimization/app.py
```

## Deliverables

- Reproducible data simulation and analytical pipeline
- Model or decision metrics in `metrics.json`
- Actionable recommendations in `decision_brief.md`
- Smoke-tested execution through the collection CI
