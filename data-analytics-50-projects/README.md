# Superstore — 50 Audited Analytics Cases

**Md Adib Azam** · Excel · SQL · Python · Statistics · Power BI · Tableau

Rebuilt entirely from the user-supplied Superstore CSV. Source totals: **9,994 sales lines**, **5,009 orders**, **793 customers**, **2,297,200.86 Sales**, **286,397.02 Profit**. Period: 2014-01-03 to 2017-12-30.

## Honest deliverables

- 10 actual Excel workbooks: editable input rows, recalculating SUMIF summaries, margins, native charts and formula checks.
- 10 SQL cases: explicit analytical queries run against an automatically loaded SQLite database.
- 10 Python cases: quality, RFM, cohort retention, Pareto, holdout forecast, robust outliers, basket association, shipping quantiles, purchase cadence and loss hotspots.
- 8 statistics cases: full computed outputs with assumptions and limitations.
- 6 Power BI + 6 Tableau cases: executed reference results, measures/calculated fields and specific desktop build instructions. **These 12 are implementation packs, not completed native PBIX/TWBX dashboards.**
- Every case includes a results CSV, a readable HTML report, a business question and a reproducible command.

## Reproduce

```bash
python -m pip install -r requirements.txt
python run.py --all
python verify.py
```

Run any case via its analysis.py. View report.html locally after downloading the repository. Excel binaries are checked in; regeneration requires the documented artifact-tool environment in build_workbooks.mjs, not Python alone.

Original data: [source CSV](datasets/source_superstore.csv) · [provenance](DATA_PROFILE.json) · [definitions](METRIC_DEFINITIONS.md) · [audit](AUDIT_AND_CORRECTIONS.md) · [test evidence](VERIFICATION.json)

## Case index

| # | Case | Track | Status |
|---:|---|---|---|
| 01 | [Regional Sales and Margin](01-regional-sales-and-margin/) | Excel | Executed analysis |
| 02 | [Category Profit Contribution](02-category-profit-contribution/) | Excel | Executed analysis |
| 03 | [Subcategory Loss Exposure](03-subcategory-loss-exposure/) | Excel | Executed analysis |
| 04 | [Monthly Sales and Profit](04-monthly-sales-and-profit/) | Excel | Executed analysis |
| 05 | [Customer Segment Economics](05-customer-segment-economics/) | Excel | Executed analysis |
| 06 | [State Profitability Review](06-state-profitability-review/) | Excel | Executed analysis |
| 07 | [Shipping Mode Sales Mix](07-shipping-mode-sales-mix/) | Excel | Executed analysis |
| 08 | [Discount Band Economics](08-discount-band-economics/) | Excel | Executed analysis |
| 09 | [Annual Commercial Performance](09-annual-commercial-performance/) | Excel | Executed analysis |
| 10 | [Quarterly Trading Review](10-quarterly-trading-review/) | Excel | Executed analysis |
| 11 | [Order Value and Basket Size](11-order-value-and-basket-size/) | SQL | Executed analysis |
| 12 | [Customer Observed Value](12-customer-observed-value/) | SQL | Executed analysis |
| 13 | [Year over Year Sales Growth](13-year-over-year-sales-growth/) | SQL | Executed analysis |
| 14 | [State Rank within Region](14-state-rank-within-region/) | SQL | Executed analysis |
| 15 | [Rolling Three Month Sales](15-rolling-three-month-sales/) | SQL | Executed analysis |
| 16 | [Product Sales Concentration](16-product-sales-concentration/) | SQL | Executed analysis |
| 17 | [First Observed Purchase Cohorts](17-first-observed-purchase-cohorts/) | SQL | Executed analysis |
| 18 | [Order Level Shipping Intervals](18-order-level-shipping-intervals/) | SQL | Executed analysis |
| 19 | [Loss Making Order Audit](19-loss-making-order-audit/) | SQL | Executed analysis |
| 20 | [Repeat Purchase Gaps](20-repeat-purchase-gaps/) | SQL | Executed analysis |
| 21 | [Source Data Quality Audit](21-source-data-quality-audit/) | Python | Executed analysis |
| 22 | [Customer RFM Ranking](22-customer-rfm-ranking/) | Python | Executed analysis |
| 23 | [Annual Cohort Retention](23-annual-cohort-retention/) | Python | Executed analysis |
| 24 | [Product Pareto Analysis](24-product-pareto-analysis/) | Python | Executed analysis |
| 25 | [Holdout Sales Forecast Comparison](25-holdout-sales-forecast-comparison/) | Python | Executed analysis |
| 26 | [Robust Order Value Outliers](26-robust-order-value-outliers/) | Python | Executed analysis |
| 27 | [Subcategory Basket Association](27-subcategory-basket-association/) | Python | Executed analysis |
| 28 | [Shipping Interval Quantiles](28-shipping-interval-quantiles/) | Python | Executed analysis |
| 29 | [Customer Purchase Cadence](29-customer-purchase-cadence/) | Python | Executed analysis |
| 30 | [State Subcategory Loss Hotspots](30-state-subcategory-loss-hotspots/) | Python | Executed analysis |
| 31 | [Order Sales Mean Confidence Interval](31-order-sales-mean-confidence-interval/) | Statistics | Executed analysis |
| 32 | [Regional Profit Welch Comparison](32-regional-profit-welch-comparison/) | Statistics | Executed analysis |
| 33 | [Segment Loss Association Test](33-segment-loss-association-test/) | Statistics | Executed analysis |
| 34 | [Discount Profit Rank Correlation](34-discount-profit-rank-correlation/) | Statistics | Executed analysis |
| 35 | [Shipping Interval Kruskal Test](35-shipping-interval-kruskal-test/) | Statistics | Executed analysis |
| 36 | [Profit Margin Bootstrap Interval](36-profit-margin-bootstrap-interval/) | Statistics | Executed analysis |
| 37 | [Temporal Holdout Profit Regression](37-temporal-holdout-profit-regression/) | Statistics | Executed analysis |
| 38 | [Loss Order Wilson Interval](38-loss-order-wilson-interval/) | Statistics | Executed analysis |
| 39 | [Power BI Executive Profit Scorecard](39-power-bi-executive-profit-scorecard/) | Power BI | Desktop implementation pack |
| 40 | [Power BI Time Intelligence](40-power-bi-time-intelligence/) | Power BI | Desktop implementation pack |
| 41 | [Power BI Product Profit Matrix](41-power-bi-product-profit-matrix/) | Power BI | Desktop implementation pack |
| 42 | [Power BI Discount Exposure](42-power-bi-discount-exposure/) | Power BI | Desktop implementation pack |
| 43 | [Power BI Customer Portfolio](43-power-bi-customer-portfolio/) | Power BI | Desktop implementation pack |
| 44 | [Power BI Shipping Mix](44-power-bi-shipping-mix/) | Power BI | Desktop implementation pack |
| 45 | [Tableau City Profit Explorer](45-tableau-city-profit-explorer/) | Tableau | Desktop implementation pack |
| 46 | [Tableau Seasonal Sales Heatmap](46-tableau-seasonal-sales-heatmap/) | Tableau | Desktop implementation pack |
| 47 | [Tableau Customer Profit Scatter](47-tableau-customer-profit-scatter/) | Tableau | Desktop implementation pack |
| 48 | [Tableau Category Share Story](48-tableau-category-share-story/) | Tableau | Desktop implementation pack |
| 49 | [Tableau Discount Loss Heatmap](49-tableau-discount-loss-heatmap/) | Tableau | Desktop implementation pack |
| 50 | [Tableau Order Size Distribution](50-tableau-order-size-distribution/) | Tableau | Desktop implementation pack |

This is a sample-data learning portfolio, not a claim of client work or independently collected real-world data. Statistical findings are exploratory. The original attachment is preserved byte-for-byte; all normalization is in the separate clean file.
