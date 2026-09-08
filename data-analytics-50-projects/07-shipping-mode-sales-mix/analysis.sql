-- Dialect: SQLite 3.25+; run via analysis.py to load source data.
SELECT ship_mode AS dimension, SUM(sales) AS sales, SUM(profit) AS profit, SUM(quantity) AS quantity, SUM(profit)/SUM(sales) AS margin FROM superstore GROUP BY ship_mode ORDER BY ship_mode;
