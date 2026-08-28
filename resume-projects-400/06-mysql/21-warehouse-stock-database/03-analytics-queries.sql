-- Operational detail with the parent entity
SELECT
    m.reference_code,
    m.display_name,
    a.stock_status,
    a.on_hand_quantity,
    a.occurred_at
FROM stock_balances AS a
JOIN warehouses AS m ON m.warehouse_entity_id = a.warehouse_entity_id
ORDER BY a.occurred_at DESC;

-- KPI summary (units)
CREATE OR REPLACE VIEW vw_warehouse_status_summary AS
SELECT
    stock_status,
    COUNT(*) AS event_count,
    ROUND(AVG(on_hand_quantity), 2) AS average_on_hand_quantity,
    ROUND(SUM(on_hand_quantity), 2) AS total_on_hand_quantity
FROM stock_balances
GROUP BY stock_status;

SELECT * FROM vw_warehouse_status_summary
ORDER BY event_count DESC, stock_status;
