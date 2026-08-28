-- Operational detail with the parent entity
SELECT
    m.reference_code,
    m.display_name,
    a.loan_status,
    a.loan_days,
    a.occurred_at
FROM loan_events AS a
JOIN books AS m ON m.library_entity_id = a.library_entity_id
ORDER BY a.occurred_at DESC;

-- KPI summary (days)
CREATE OR REPLACE VIEW vw_library_status_summary AS
SELECT
    loan_status,
    COUNT(*) AS event_count,
    ROUND(AVG(loan_days), 2) AS average_loan_days,
    ROUND(SUM(loan_days), 2) AS total_loan_days
FROM loan_events
GROUP BY loan_status;

SELECT * FROM vw_library_status_summary
ORDER BY event_count DESC, loan_status;
