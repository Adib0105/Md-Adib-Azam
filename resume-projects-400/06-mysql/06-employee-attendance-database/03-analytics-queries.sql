-- Operational detail with the parent entity
SELECT
    m.reference_code,
    m.display_name,
    a.attendance_status,
    a.worked_minutes,
    a.occurred_at
FROM attendance_events AS a
JOIN employees AS m ON m.attendance_entity_id = a.attendance_entity_id
ORDER BY a.occurred_at DESC;

-- KPI summary (minutes)
CREATE OR REPLACE VIEW vw_attendance_status_summary AS
SELECT
    attendance_status,
    COUNT(*) AS event_count,
    ROUND(AVG(worked_minutes), 2) AS average_worked_minutes,
    ROUND(SUM(worked_minutes), 2) AS total_worked_minutes
FROM attendance_events
GROUP BY attendance_status;

SELECT * FROM vw_attendance_status_summary
ORDER BY event_count DESC, attendance_status;
