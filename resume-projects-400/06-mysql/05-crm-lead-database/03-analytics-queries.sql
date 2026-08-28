-- Operational detail with the parent entity
SELECT
    m.reference_code,
    m.display_name,
    a.activity_type,
    a.engagement_score,
    a.occurred_at
FROM lead_activities AS a
JOIN leads AS m ON m.crm_entity_id = a.crm_entity_id
ORDER BY a.occurred_at DESC;

-- KPI summary (score)
CREATE OR REPLACE VIEW vw_crm_status_summary AS
SELECT
    activity_type,
    COUNT(*) AS event_count,
    ROUND(AVG(engagement_score), 2) AS average_engagement_score,
    ROUND(SUM(engagement_score), 2) AS total_engagement_score
FROM lead_activities
GROUP BY activity_type;

SELECT * FROM vw_crm_status_summary
ORDER BY event_count DESC, activity_type;
