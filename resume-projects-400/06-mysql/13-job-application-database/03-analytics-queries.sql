-- Operational detail with the parent entity
SELECT
    m.reference_code,
    m.display_name,
    a.application_status,
    a.fit_score,
    a.occurred_at
FROM applications AS a
JOIN candidates AS m ON m.job_application_entity_id = a.job_application_entity_id
ORDER BY a.occurred_at DESC;

-- KPI summary (score)
CREATE OR REPLACE VIEW vw_job_application_status_summary AS
SELECT
    application_status,
    COUNT(*) AS event_count,
    ROUND(AVG(fit_score), 2) AS average_fit_score,
    ROUND(SUM(fit_score), 2) AS total_fit_score
FROM applications
GROUP BY application_status;

SELECT * FROM vw_job_application_status_summary
ORDER BY event_count DESC, application_status;
