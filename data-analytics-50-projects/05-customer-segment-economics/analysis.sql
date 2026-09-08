-- Dialect: SQLite 3.25+; run via analysis.py to load source data.
SELECT segment AS dimension, SUM(sales) AS sales, SUM(profit) AS profit, SUM(quantity) AS quantity, SUM(profit)/SUM(sales) AS margin FROM superstore GROUP BY segment ORDER BY segment;
