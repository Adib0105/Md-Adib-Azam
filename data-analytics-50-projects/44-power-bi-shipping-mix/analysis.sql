-- Dialect: SQLite 3.25+; run via analysis.py to load source data.
WITH o AS (SELECT order_id,region,ship_mode,MAX(ship_days) AS days FROM superstore GROUP BY order_id,region,ship_mode) SELECT region,ship_mode,COUNT(*) AS orders,AVG(days) AS mean_ship_days FROM o GROUP BY region,ship_mode ORDER BY region,mean_ship_days;
