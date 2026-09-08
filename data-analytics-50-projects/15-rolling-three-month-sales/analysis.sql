-- Dialect: SQLite 3.25+; run via analysis.py to load source data.
WITH a AS (SELECT order_month,SUM(sales) AS sales FROM superstore GROUP BY order_month) SELECT *,CASE WHEN ROW_NUMBER() OVER(ORDER BY order_month)>=3 THEN AVG(sales) OVER(ORDER BY order_month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) END AS trailing_3_month_sales FROM a ORDER BY order_month;
