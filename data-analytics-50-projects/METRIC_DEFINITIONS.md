# Source and metric contract

- Source: user attachment `Sample - Superstore (1)(2).csv`; source_superstore.csv preserves original bytes, SHA-256 in DATA_PROFILE.json. This is a sample retail dataset, not a claim of real client work. No fabricated rows or unrelated datasets.
- Grain: one sales line per Row ID. Order ID repeats legitimately. Product names are labels; group products by Product ID. City is paired with State.
- Dates: strict month/day/year parsing. Postal codes remain text. No records dropped or imputed. Clean file renames headers, normalizes dates, and adds documented date, discount-band, loss and ship-day fields.
- Sales: SUM(Sales) exactly as supplied; do not multiply by Quantity or apply Discount again. Profit: SUM(Profit). Margin: SUM(Profit)/SUM(Sales), not average row margin.
- Orders: COUNT DISTINCT Order ID. AOV: total Sales / distinct orders. Observed customer value covers only the supplied observation window, not lifetime-value prediction.
- Loss line: Profit < 0 on a row. Loss order: sum of Profit < 0 after grouping Order ID. These are different metrics.
- Shipping interval: Ship Date minus Order Date in calendar days, evaluated once per order. Dispatch interval is not delivery time or an SLA breach; delivery/commitment/cost data is absent.
- Discount bands: exactly zero, (0,0.2], (0.2,0.4], (0.4,1). Discount is a fraction, not percentage points. Associations do not establish causal discount effects.
- Cohorts: first observed purchase, not account signup. Retention denominator is original cohort customers; unobserved future periods remain absent, never zero-filled.
- Statistical results are illustrative under independent-order sampling assumptions. Repeated customers and a fixed historical sample limit population inference; intervals and p-values are exploratory, not randomized A/B evidence. No familywise confirmatory claims are made. Nonparametric methods do not eliminate dependence or confounding.
- Bootstrap uses paired order sales/profit, seed 42, 2000 resamples. Forecast uses final 12 months as untouched holdout; regression uses chronological 80/20 split. Order outliers use log1p(sales), median/MAD and |z|>3.5; no records deleted.
- RFM scores use tie-preserving rank-based quantiles. Ranking is descriptive, not a validated churn model. Basket associations use unique subcategories per order, minimum 20 co-occurrences; lift is not causal.
- Monetary units follow the uploaded dataset; no INR conversion or currency assertion is inferred from geography.
