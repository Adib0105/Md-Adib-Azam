-- Dialect: SQLite 3.25+; run via analysis.py to load source data.
SELECT order_id,customer_id,SUM(sales) AS sales,SUM(profit) AS profit,SUM(profit)/SUM(sales) AS margin FROM superstore GROUP BY order_id,customer_id HAVING SUM(profit)<0 ORDER BY profit;
