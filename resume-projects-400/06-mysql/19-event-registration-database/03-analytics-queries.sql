-- Operational detail with the parent entity
SELECT
    m.reference_code,
    m.display_name,
    a.payment_status,
    a.tickets,
    a.occurred_at
FROM event_registrations AS a
JOIN events AS m ON m.event_entity_id = a.event_entity_id
ORDER BY a.occurred_at DESC;

-- KPI summary (count)
CREATE OR REPLACE VIEW vw_event_status_summary AS
SELECT
    payment_status,
    COUNT(*) AS event_count,
    ROUND(AVG(tickets), 2) AS average_tickets,
    ROUND(SUM(tickets), 2) AS total_tickets
FROM event_registrations
GROUP BY payment_status;

SELECT * FROM vw_event_status_summary
ORDER BY event_count DESC, payment_status;
