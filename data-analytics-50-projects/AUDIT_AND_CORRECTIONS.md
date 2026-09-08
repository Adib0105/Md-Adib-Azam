# Audit and corrections

Scope: prior 50-project collection, not unrelated projects in the repository.

| Finding | Correction |
|---|---|
| Five fabricated 8–10-row datasets presented as project evidence | Replaced with original attached 9,994-row Superstore; byte checksum retained |
| HR, CSAT, marketing, churn unavailable in new source | Replaced every incompatible business question; no invented fields |
| Excel only described formulas; no actual workbooks | Ten native formula-driven XLSX workbooks, source-derived inputs, charts and formula checks |
| README links used ../../datasets from one-level folders | Correct ../datasets and explicit runnable paths |
| Reorder calculation had no stock or lead-time data | Removed unsupported inventory decisions |
| Lifetime value was merely past customer sales | Renamed observed customer value |
| Product affinity query only grouped categories | Actual order basket pair counts, support, confidence and lift |
| Churn risk used actual churn as predictor (leakage) | Removed; replaced with descriptive RFM ranking |
| Forecast lacked claimed MAE/holdout evidence | Two baselines with held-out actuals, per-period errors and MAE summary |
| Multi-source claim used one source | Source-limited questions explicitly identified |
| Small-sample salary CI used normal critical value | Order-sales Student-t interval, limitations documented |
| Chi-square and CSAT tests omitted claimed p-values | Implemented appropriate tests with statistics, p-values and effect sizes |
| Advertised YoY measure missing | Supplied calendar relationship and blank-safe prior-year DAX |
| Validation checked only file presence | All 50 runs, SQL-vs-pandas checks, order grain, saved-output reconciliation and workbook checks |
| Claims implied completed Power BI/Tableau dashboards | Marked 12 projects as implementation packs; no PBIX/TWBX runtime validation claimed |

Original files removed from the active collection remain recoverable in Git history (prior commit 3bacc99edcc806ff22ad3c7ac0438f0d9c2d38c6). Unrelated repository files are unchanged except the two collection descriptions in root README.
