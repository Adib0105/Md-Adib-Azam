-- Dialect: SQLite 3.25+; run via analysis.py to load source data.
SELECT customer_id,COUNT(DISTINCT order_id) AS orders,SUM(sales) AS sales,SUM(profit) AS profit FROM superstore GROUP BY customer_id ORDER BY sales DESC;
