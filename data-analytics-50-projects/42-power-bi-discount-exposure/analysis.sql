-- Dialect: SQLite 3.25+; run via analysis.py to load source data.
SELECT region,discount_band,COUNT(*) AS lines,SUM(sales) AS sales,SUM(profit) AS profit,1.0*SUM(loss_flag)/COUNT(*) AS loss_line_rate FROM superstore GROUP BY region,discount_band ORDER BY region,discount_band;
