-- Product Affinity SQL
-- Import ../../datasets/retail_sales.csv as table `retail_sales` before running.

SELECT category, COUNT(DISTINCT customer_id) customers, COUNT(*) orders, SUM(units) units, ROUND(SUM(units*unit_price*(1-discount)),2) revenue FROM retail_sales GROUP BY category ORDER BY revenue DESC;
