-- Dialect: SQLite 3.25+; run via analysis.py to load source data.
SELECT order_year,substr(order_month,6,2) AS month_number,SUM(sales) AS sales,SUM(profit) AS profit FROM superstore GROUP BY order_year,month_number ORDER BY order_year,month_number;
