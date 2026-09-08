-- Dialect: SQLite 3.25+; run via analysis.py to load source data.
SELECT order_id,COUNT(*) AS lines,SUM(quantity) AS units,SUM(sales) AS order_sales,SUM(profit) AS order_profit FROM superstore GROUP BY order_id ORDER BY order_sales DESC;
