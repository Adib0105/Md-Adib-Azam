-- Synthetic sample data for Event Registration Database
INSERT INTO events (display_name, reference_code) VALUES
('AI Workshop', 'EVENT-001'),
('Career Webinar', 'EVENT-002');

INSERT INTO event_registrations (event_entity_id, payment_status, tickets, occurred_at, notes) VALUES
(1, 'paid', 2, '2026-08-27 10:00:00', 'Synthetic portfolio row'),
(2, 'pending', 1, '2026-08-28 11:30:00', 'Synthetic portfolio row');
