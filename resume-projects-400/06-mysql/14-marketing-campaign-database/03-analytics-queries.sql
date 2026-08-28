-- Operational detail with the parent entity
SELECT
    m.reference_code,
    m.display_name,
    a.event_type,
    a.attributed_revenue,
    a.occurred_at
FROM campaign_events AS a
JOIN campaigns AS m ON m.campaign_entity_id = a.campaign_entity_id
ORDER BY a.occurred_at DESC;

-- KPI summary (INR)
CREATE OR REPLACE VIEW vw_campaign_status_summary AS
SELECT
    event_type,
    COUNT(*) AS event_count,
    ROUND(AVG(attributed_revenue), 2) AS average_attributed_revenue,
    ROUND(SUM(attributed_revenue), 2) AS total_attributed_revenue
FROM campaign_events
GROUP BY event_type;

SELECT * FROM vw_campaign_status_summary
ORDER BY event_count DESC, event_type;
