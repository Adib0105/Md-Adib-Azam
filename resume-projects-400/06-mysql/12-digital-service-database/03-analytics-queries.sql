-- Operational detail with the parent entity
SELECT
    m.reference_code,
    m.display_name,
    a.request_status,
    a.turnaround_hours,
    a.occurred_at
FROM service_requests AS a
JOIN service_customers AS m ON m.digital_service_entity_id = a.digital_service_entity_id
ORDER BY a.occurred_at DESC;

-- KPI summary (hours)
CREATE OR REPLACE VIEW vw_digital_service_status_summary AS
SELECT
    request_status,
    COUNT(*) AS event_count,
    ROUND(AVG(turnaround_hours), 2) AS average_turnaround_hours,
    ROUND(SUM(turnaround_hours), 2) AS total_turnaround_hours
FROM service_requests
GROUP BY request_status;

SELECT * FROM vw_digital_service_status_summary
ORDER BY event_count DESC, request_status;
