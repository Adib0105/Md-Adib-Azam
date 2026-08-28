-- Operational detail with the parent entity
SELECT
    m.reference_code,
    m.display_name,
    a.sla_status,
    a.first_response_minutes,
    a.occurred_at
FROM sla_measurements AS a
JOIN support_teams AS m ON m.support_sla_entity_id = a.support_sla_entity_id
ORDER BY a.occurred_at DESC;

-- KPI summary (minutes)
CREATE OR REPLACE VIEW vw_support_sla_status_summary AS
SELECT
    sla_status,
    COUNT(*) AS event_count,
    ROUND(AVG(first_response_minutes), 2) AS average_first_response_minutes,
    ROUND(SUM(first_response_minutes), 2) AS total_first_response_minutes
FROM sla_measurements
GROUP BY sla_status;

SELECT * FROM vw_support_sla_status_summary
ORDER BY event_count DESC, sla_status;
