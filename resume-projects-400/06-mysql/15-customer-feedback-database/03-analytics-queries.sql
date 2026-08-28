-- Operational detail with the parent entity
SELECT
    m.reference_code,
    m.display_name,
    a.sentiment_label,
    a.rating,
    a.occurred_at
FROM feedback_entries AS a
JOIN respondents AS m ON m.feedback_entity_id = a.feedback_entity_id
ORDER BY a.occurred_at DESC;

-- KPI summary (stars)
CREATE OR REPLACE VIEW vw_feedback_status_summary AS
SELECT
    sentiment_label,
    COUNT(*) AS event_count,
    ROUND(AVG(rating), 2) AS average_rating,
    ROUND(SUM(rating), 2) AS total_rating
FROM feedback_entries
GROUP BY sentiment_label;

SELECT * FROM vw_feedback_status_summary
ORDER BY event_count DESC, sentiment_label;
