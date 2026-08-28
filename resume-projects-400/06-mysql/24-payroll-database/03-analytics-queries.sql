-- Operational detail with the parent entity
SELECT
    m.reference_code,
    m.display_name,
    a.pay_status,
    a.net_pay,
    a.occurred_at
FROM pay_runs AS a
JOIN employees_payroll AS m ON m.payroll_entity_id = a.payroll_entity_id
ORDER BY a.occurred_at DESC;

-- KPI summary (INR)
CREATE OR REPLACE VIEW vw_payroll_status_summary AS
SELECT
    pay_status,
    COUNT(*) AS event_count,
    ROUND(AVG(net_pay), 2) AS average_net_pay,
    ROUND(SUM(net_pay), 2) AS total_net_pay
FROM pay_runs
GROUP BY pay_status;

SELECT * FROM vw_payroll_status_summary
ORDER BY event_count DESC, pay_status;
