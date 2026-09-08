-- Regional Performance Ranking SQL
-- Import ../../datasets/retail_sales.csv as table `retail_sales` before running.

WITH r AS (SELECT region,SUM(units*unit_price*(1-discount)) net_sales,AVG(discount) avg_discount,COUNT(*) orders FROM retail_sales GROUP BY region) SELECT *,DENSE_RANK() OVER(ORDER BY net_sales DESC) region_rank,ROUND(100.0*orders/SUM(orders) OVER(),1) order_share_pct FROM r ORDER BY region_rank;
