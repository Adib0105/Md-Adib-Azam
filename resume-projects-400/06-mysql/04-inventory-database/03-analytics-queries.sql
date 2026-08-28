-- Operational detail with the parent entity
SELECT
    m.reference_code,
    m.display_name,
    a.movement_type,
    a.quantity,
    a.occurred_at
FROM stock_movements AS a
JOIN stock_items AS m ON m.inventory_entity_id = a.inventory_entity_id
ORDER BY a.occurred_at DESC;

-- KPI summary (units)
CREATE OR REPLACE VIEW vw_inventory_status_summary AS
SELECT
    movement_type,
    COUNT(*) AS event_count,
    ROUND(AVG(quantity), 2) AS average_quantity,
    ROUND(SUM(quantity), 2) AS total_quantity
FROM stock_movements
GROUP BY movement_type;

SELECT * FROM vw_inventory_status_summary
ORDER BY event_count DESC, movement_type;
