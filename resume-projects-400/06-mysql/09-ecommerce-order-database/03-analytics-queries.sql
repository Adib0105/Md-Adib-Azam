-- Operational detail with the parent entity
SELECT
    m.reference_code,
    m.display_name,
    a.fulfilment_status,
    a.line_total,
    a.occurred_at
FROM order_lines AS a
JOIN orders AS m ON m.ecommerce_entity_id = a.ecommerce_entity_id
ORDER BY a.occurred_at DESC;

-- KPI summary (INR)
CREATE OR REPLACE VIEW vw_ecommerce_status_summary AS
SELECT
    fulfilment_status,
    COUNT(*) AS event_count,
    ROUND(AVG(line_total), 2) AS average_line_total,
    ROUND(SUM(line_total), 2) AS total_line_total
FROM order_lines
GROUP BY fulfilment_status;

SELECT * FROM vw_ecommerce_status_summary
ORDER BY event_count DESC, fulfilment_status;
