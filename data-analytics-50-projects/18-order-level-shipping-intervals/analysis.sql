-- Dialect: SQLite 3.25+; run via analysis.py to load source data.
WITH o AS (SELECT order_id,ship_mode,MAX(ship_days) AS days FROM superstore GROUP BY order_id,ship_mode) SELECT ship_mode,COUNT(*) AS orders,AVG(days) AS mean_days,MIN(days) AS min_days,MAX(days) AS max_days FROM o GROUP BY ship_mode ORDER BY mean_days;
