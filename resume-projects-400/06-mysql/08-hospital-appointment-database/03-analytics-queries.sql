-- Operational detail with the parent entity
SELECT
    m.reference_code,
    m.display_name,
    a.appointment_status,
    a.wait_minutes,
    a.occurred_at
FROM appointments AS a
JOIN patients AS m ON m.hospital_entity_id = a.hospital_entity_id
ORDER BY a.occurred_at DESC;

-- KPI summary (minutes)
CREATE OR REPLACE VIEW vw_hospital_status_summary AS
SELECT
    appointment_status,
    COUNT(*) AS event_count,
    ROUND(AVG(wait_minutes), 2) AS average_wait_minutes,
    ROUND(SUM(wait_minutes), 2) AS total_wait_minutes
FROM appointments
GROUP BY appointment_status;

SELECT * FROM vw_hospital_status_summary
ORDER BY event_count DESC, appointment_status;
