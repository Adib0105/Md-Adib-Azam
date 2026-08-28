-- Synthetic sample data for Marketing Campaign Database
INSERT INTO campaigns (display_name, reference_code) VALUES
('Search Launch', 'CAMPAIGN-001'),
('Social Retargeting', 'CAMPAIGN-002');

INSERT INTO campaign_events (campaign_entity_id, event_type, attributed_revenue, occurred_at, notes) VALUES
(1, 'conversion', 12000, '2026-08-27 10:00:00', 'Synthetic portfolio row'),
(2, 'click', 0, '2026-08-28 11:30:00', 'Synthetic portfolio row');
