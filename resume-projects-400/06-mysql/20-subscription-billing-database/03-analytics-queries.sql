-- Operational detail with the parent entity
SELECT
    m.reference_code,
    m.display_name,
    a.subscription_status,
    a.monthly_amount,
    a.occurred_at
FROM subscriptions AS a
JOIN plans AS m ON m.subscription_entity_id = a.subscription_entity_id
ORDER BY a.occurred_at DESC;

-- KPI summary (INR)
CREATE OR REPLACE VIEW vw_subscription_status_summary AS
SELECT
    subscription_status,
    COUNT(*) AS event_count,
    ROUND(AVG(monthly_amount), 2) AS average_monthly_amount,
    ROUND(SUM(monthly_amount), 2) AS total_monthly_amount
FROM subscriptions
GROUP BY subscription_status;

SELECT * FROM vw_subscription_status_summary
ORDER BY event_count DESC, subscription_status;
