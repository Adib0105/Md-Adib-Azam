-- Dialect: SQLite 3.25+; run via analysis.py to load source data.
SELECT category,sub_category,SUM(sales) AS sales,SUM(profit) AS profit,SUM(profit)/SUM(sales) AS margin FROM superstore GROUP BY category,sub_category ORDER BY profit;
