-- Synthetic sample data for CRM Lead Database
INSERT INTO leads (display_name, reference_code) VALUES
('Alpha Pvt Ltd', 'CRM-001'),
('Beta Stores', 'CRM-002');

INSERT INTO lead_activities (crm_entity_id, activity_type, engagement_score, occurred_at, notes) VALUES
(1, 'demo', 85, '2026-08-27 10:00:00', 'Synthetic portfolio row'),
(2, 'email', 40, '2026-08-28 11:30:00', 'Synthetic portfolio row');
