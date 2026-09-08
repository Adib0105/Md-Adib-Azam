-- Dialect: SQLite 3.25+; run via analysis.py to load source data.
WITH dates AS (SELECT DISTINCT customer_id,order_date FROM superstore), a AS (SELECT *,LAG(order_date) OVER(PARTITION BY customer_id ORDER BY order_date) AS prior_date FROM dates) SELECT *,julianday(order_date)-julianday(prior_date) AS gap_days FROM a WHERE prior_date IS NOT NULL ORDER BY customer_id,order_date;
