-- Operational detail with the parent entity
SELECT
    m.reference_code,
    m.display_name,
    a.rental_status,
    a.rental_days,
    a.occurred_at
FROM rental_contracts AS a
JOIN vehicles AS m ON m.vehicle_entity_id = a.vehicle_entity_id
ORDER BY a.occurred_at DESC;

-- KPI summary (days)
CREATE OR REPLACE VIEW vw_vehicle_status_summary AS
SELECT
    rental_status,
    COUNT(*) AS event_count,
    ROUND(AVG(rental_days), 2) AS average_rental_days,
    ROUND(SUM(rental_days), 2) AS total_rental_days
FROM rental_contracts
GROUP BY rental_status;

SELECT * FROM vw_vehicle_status_summary
ORDER BY event_count DESC, rental_status;
