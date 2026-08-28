-- Synthetic sample data for Subscription Billing Database
INSERT INTO plans (display_name, reference_code) VALUES
('Starter', 'SUBSCRIPTION-001'),
('Professional', 'SUBSCRIPTION-002');

INSERT INTO subscriptions (subscription_entity_id, subscription_status, monthly_amount, occurred_at, notes) VALUES
(1, 'active', 499, '2026-08-27 10:00:00', 'Synthetic portfolio row'),
(2, 'past_due', 1499, '2026-08-28 11:30:00', 'Synthetic portfolio row');
