# Power BI Executive Profit Scorecard

Status: implementation pack; not a Desktop-validated PBIX.

1. Run `python run.py --all` in the collection root.
2. Import `datasets/superstore_clean.csv` as `superstore`. Set order_date and ship_date to Date; sales/profit/discount to decimal; quantity/ship_days to whole number; postal_code to Text.
3. Add the measures in measures.dax one at a time.
4. Create Calendar = CALENDAR(MIN(superstore[order_date]), MAX(superstore[order_date])). Mark Calendar as date table and relate Calendar[Date] (one) to superstore[order_date] (many), single direction.
5. Primary visual: use `region` and the exact dimensions/metrics in `results.csv`. Cards: Sales, Profit, Margin, Orders. Add region, segment and Calendar date slicers.
6. Add profit conditional colors (red negative, teal positive), clear-filter bookmark and drillthrough by the primary dimension.
7. Compare unfiltered Sales/Profit/Orders with ../DATA_PROFILE.json. Compare grouped output with results.csv. Distinct orders/customers across overlapping groups must not be added together.
8. Open report.html for the executed analytical reference; this is not a screenshot of Power BI.
