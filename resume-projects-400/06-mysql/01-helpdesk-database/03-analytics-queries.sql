-- Operational detail with the parent entity
SELECT
    m.reference_code,
    m.display_name,
    a.ticket_status,
    a.resolution_minutes,
    a.occurred_at
FROM tickets AS a
JOIN customers AS m ON m.helpdesk_entity_id = a.helpdesk_entity_id
ORDER BY a.occurred_at DESC;

-- KPI summary (minutes)
CREATE OR REPLACE VIEW vw_helpdesk_status_summary AS
SELECT
    ticket_status,
    COUNT(*) AS event_count,
    ROUND(AVG(resolution_minutes), 2) AS average_resolution_minutes,
    ROUND(SUM(resolution_minutes), 2) AS total_resolution_minutes
FROM tickets
GROUP BY ticket_status;

SELECT * FROM vw_helpdesk_status_summary
ORDER BY event_count DESC, ticket_status;
