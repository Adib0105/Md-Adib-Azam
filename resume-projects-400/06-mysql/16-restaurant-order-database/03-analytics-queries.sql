-- Operational detail with the parent entity
SELECT
    m.reference_code,
    m.display_name,
    a.kitchen_status,
    a.line_total,
    a.occurred_at
FROM order_items AS a
JOIN menu_items AS m ON m.restaurant_entity_id = a.restaurant_entity_id
ORDER BY a.occurred_at DESC;

-- KPI summary (INR)
CREATE OR REPLACE VIEW vw_restaurant_status_summary AS
SELECT
    kitchen_status,
    COUNT(*) AS event_count,
    ROUND(AVG(line_total), 2) AS average_line_total,
    ROUND(SUM(line_total), 2) AS total_line_total
FROM order_items
GROUP BY kitchen_status;

SELECT * FROM vw_restaurant_status_summary
ORDER BY event_count DESC, kitchen_status;
