-- Dialect: SQLite 3.25+; run via analysis.py to load source data.
WITH a AS (SELECT region,state,SUM(sales) AS sales,SUM(profit) AS profit FROM superstore GROUP BY region,state) SELECT *,DENSE_RANK() OVER(PARTITION BY region ORDER BY sales DESC) AS regional_rank FROM a ORDER BY region,regional_rank;
