-- Dialect: SQLite 3.25+; run via analysis.py to load source data.
SELECT sub_category,discount_band,SUM(sales) AS sales,SUM(profit) AS profit,1.0*SUM(loss_flag)/COUNT(*) AS loss_line_rate FROM superstore GROUP BY sub_category,discount_band ORDER BY sub_category,discount_band;
