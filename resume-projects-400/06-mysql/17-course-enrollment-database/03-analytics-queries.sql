-- Operational detail with the parent entity
SELECT
    m.reference_code,
    m.display_name,
    a.completion_status,
    a.progress_pct,
    a.occurred_at
FROM course_enrollments AS a
JOIN courses AS m ON m.course_entity_id = a.course_entity_id
ORDER BY a.occurred_at DESC;

-- KPI summary (percent)
CREATE OR REPLACE VIEW vw_course_status_summary AS
SELECT
    completion_status,
    COUNT(*) AS event_count,
    ROUND(AVG(progress_pct), 2) AS average_progress_pct,
    ROUND(SUM(progress_pct), 2) AS total_progress_pct
FROM course_enrollments
GROUP BY completion_status;

SELECT * FROM vw_course_status_summary
ORDER BY event_count DESC, completion_status;
