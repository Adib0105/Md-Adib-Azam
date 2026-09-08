-- Dialect: SQLite 3.25+; run via analysis.py to load source data.
SELECT customer_id,COUNT(DISTINCT order_id) AS orders,SUM(sales) AS observed_sales,SUM(profit) AS observed_profit,MIN(order_date) AS first_order,MAX(order_date) AS last_order FROM superstore GROUP BY customer_id ORDER BY observed_sales DESC;
