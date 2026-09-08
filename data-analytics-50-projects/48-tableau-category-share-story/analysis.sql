-- Dialect: SQLite 3.25+; run via analysis.py to load source data.
WITH a AS (SELECT order_year,category,SUM(sales) AS sales FROM superstore GROUP BY order_year,category) SELECT *,sales/SUM(sales) OVER(PARTITION BY order_year) AS annual_share FROM a ORDER BY order_year,category;
