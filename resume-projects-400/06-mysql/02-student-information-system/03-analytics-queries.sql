-- Operational detail with the parent entity
SELECT
    m.reference_code,
    m.display_name,
    a.enrollment_status,
    a.final_score,
    a.occurred_at
FROM enrollments AS a
JOIN students AS m ON m.student_entity_id = a.student_entity_id
ORDER BY a.occurred_at DESC;

-- KPI summary (score)
CREATE OR REPLACE VIEW vw_student_status_summary AS
SELECT
    enrollment_status,
    COUNT(*) AS event_count,
    ROUND(AVG(final_score), 2) AS average_final_score,
    ROUND(SUM(final_score), 2) AS total_final_score
FROM enrollments
GROUP BY enrollment_status;

SELECT * FROM vw_student_status_summary
ORDER BY event_count DESC, enrollment_status;
