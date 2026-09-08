-- Dialect: SQLite 3.25+; run via analysis.py to load source data.
WITH a AS (SELECT product_id,SUM(sales) AS sales FROM superstore GROUP BY product_id) SELECT *,SUM(sales) OVER(ORDER BY sales DESC,product_id ROWS UNBOUNDED PRECEDING)/SUM(sales) OVER() AS cumulative_share FROM a ORDER BY sales DESC,product_id;
