-- Dialect: SQLite 3.25+; run via analysis.py to load source data.
SELECT region,segment,COUNT(DISTINCT customer_id) AS customers,SUM(sales) AS sales,SUM(profit) AS profit FROM superstore GROUP BY region,segment ORDER BY sales DESC;
