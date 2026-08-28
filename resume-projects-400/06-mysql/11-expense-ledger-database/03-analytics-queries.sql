-- Operational detail with the parent entity
SELECT
    m.reference_code,
    m.display_name,
    a.approval_status,
    a.expense_amount,
    a.occurred_at
FROM expense_entries AS a
JOIN cost_centres AS m ON m.expense_entity_id = a.expense_entity_id
ORDER BY a.occurred_at DESC;

-- KPI summary (INR)
CREATE OR REPLACE VIEW vw_expense_status_summary AS
SELECT
    approval_status,
    COUNT(*) AS event_count,
    ROUND(AVG(expense_amount), 2) AS average_expense_amount,
    ROUND(SUM(expense_amount), 2) AS total_expense_amount
FROM expense_entries
GROUP BY approval_status;

SELECT * FROM vw_expense_status_summary
ORDER BY event_count DESC, approval_status;
