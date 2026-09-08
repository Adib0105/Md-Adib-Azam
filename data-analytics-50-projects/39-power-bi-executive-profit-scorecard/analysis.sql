-- Dialect: SQLite 3.25+; run via analysis.py to load source data.
SELECT region,category,SUM(sales) AS sales,SUM(profit) AS profit,COUNT(DISTINCT order_id) AS orders FROM superstore GROUP BY region,category ORDER BY profit DESC;
