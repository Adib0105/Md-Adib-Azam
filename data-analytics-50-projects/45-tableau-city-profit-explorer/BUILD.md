# Tableau City Profit Explorer

Status: implementation pack; not a Desktop-validated TWBX.

Connect to datasets/superstore_clean.csv as Text File. Confirm date and numeric types; postal_code remains string. Add calculated fields individually. Use `city` as the primary dimension and `results.csv` as the precise target output.

Suggested design: seasonal and discount projects use square marks with year/month or subcategory/discount axes; customer scatter uses customer_id on Detail, SUM(sales) on Columns, SUM(profit) on Rows; city explorer uses city + state together; category share uses category bars and Category Share computed across category, partitioned by year. Order-size analysis must use a distinct-order table, not repeated line-level LOD values: connect directly to results.csv for the validated output.

Use a 1200x800 dashboard, Sales/Profit/Margin cards, region and segment filters, descriptive tooltips and a reset action. FIXED LOD runs before ordinary dimension filters; promote intended filters to context or use direct aggregates. Reconcile with DATA_PROFILE.json and results.csv. report.html is an executed analytical reference, not a Tableau screenshot.
