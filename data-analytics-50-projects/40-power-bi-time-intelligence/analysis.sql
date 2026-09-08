-- Dialect: SQLite 3.25+; run via analysis.py to load source data.
SELECT order_year,SUM(sales) AS sales,SUM(profit) AS profit,COUNT(DISTINCT order_id) AS orders FROM superstore GROUP BY order_year ORDER BY order_year;
