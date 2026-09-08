-- Dialect: SQLite 3.25+; run via analysis.py to load source data.
SELECT city,state,SUM(sales) AS sales,SUM(profit) AS profit FROM superstore GROUP BY city,state ORDER BY profit;
