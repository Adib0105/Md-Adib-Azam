-- Dialect: SQLite 3.25+; run via analysis.py to load source data.
SELECT discount_band AS dimension, SUM(sales) AS sales, SUM(profit) AS profit, SUM(quantity) AS quantity, SUM(profit)/SUM(sales) AS margin FROM superstore GROUP BY discount_band ORDER BY discount_band;
