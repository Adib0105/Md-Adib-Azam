-- Dialect: SQLite 3.25+; run via analysis.py to load source data.
WITH a AS (SELECT order_year,SUM(sales) AS sales,SUM(profit) AS profit FROM superstore GROUP BY order_year), b AS (SELECT *,LAG(sales) OVER(ORDER BY order_year) AS prior_sales FROM a) SELECT *,sales/NULLIF(prior_sales,0)-1 AS yoy_growth FROM b ORDER BY order_year;
