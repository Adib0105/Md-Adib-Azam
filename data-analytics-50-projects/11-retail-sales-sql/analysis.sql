-- Retail Sales Analysis with SQL
-- Import ../../datasets/retail_sales.csv as table `retail_sales` before running.

SELECT region, ROUND(SUM(units*unit_price*(1-discount)),2) net_sales, COUNT(*) orders, ROUND(AVG(units*unit_price*(1-discount)),2) aov, DENSE_RANK() OVER(ORDER BY SUM(units*unit_price*(1-discount)) DESC) sales_rank FROM retail_sales GROUP BY region ORDER BY sales_rank;
