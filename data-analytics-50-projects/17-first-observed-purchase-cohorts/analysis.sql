-- Dialect: SQLite 3.25+; run via analysis.py to load source data.
WITH firsts AS (SELECT customer_id,MIN(order_year) AS cohort FROM superstore GROUP BY customer_id) SELECT f.cohort,COUNT(DISTINCT s.customer_id) AS customers,COUNT(DISTINCT s.order_id) AS orders,SUM(s.sales) AS sales FROM superstore s JOIN firsts f USING(customer_id) GROUP BY f.cohort ORDER BY f.cohort;
