-- Customer Lifetime Value SQL
-- Import ../../datasets/retail_sales.csv as table `retail_sales` before running.

SELECT customer_id, COUNT(*) orders, SUM(units) units, ROUND(SUM(units*unit_price*(1-discount)),2) lifetime_value, MAX(date) last_order FROM retail_sales GROUP BY customer_id ORDER BY lifetime_value DESC;
