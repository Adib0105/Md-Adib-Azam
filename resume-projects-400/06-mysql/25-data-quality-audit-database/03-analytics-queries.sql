-- Operational detail with the parent entity
SELECT
    m.reference_code,
    m.display_name,
    a.check_status,
    a.failed_rows,
    a.occurred_at
FROM quality_checks AS a
JOIN data_sources AS m ON m.quality_entity_id = a.quality_entity_id
ORDER BY a.occurred_at DESC;

-- KPI summary (rows)
CREATE OR REPLACE VIEW vw_quality_status_summary AS
SELECT
    check_status,
    COUNT(*) AS event_count,
    ROUND(AVG(failed_rows), 2) AS average_failed_rows,
    ROUND(SUM(failed_rows), 2) AS total_failed_rows
FROM quality_checks
GROUP BY check_status;

SELECT * FROM vw_quality_status_summary
ORDER BY event_count DESC, check_status;
