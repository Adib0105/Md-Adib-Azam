-- Operational detail with the parent entity
SELECT
    m.reference_code,
    m.display_name,
    a.sales_channel,
    a.line_revenue,
    a.occurred_at
FROM sale_items AS a
JOIN products AS m ON m.retail_entity_id = a.retail_entity_id
ORDER BY a.occurred_at DESC;

-- KPI summary (INR)
CREATE OR REPLACE VIEW vw_retail_status_summary AS
SELECT
    sales_channel,
    COUNT(*) AS event_count,
    ROUND(AVG(line_revenue), 2) AS average_line_revenue,
    ROUND(SUM(line_revenue), 2) AS total_line_revenue
FROM sale_items
GROUP BY sales_channel;

SELECT * FROM vw_retail_status_summary
ORDER BY event_count DESC, sales_channel;
