-- Synthetic sample data for Helpdesk Database
INSERT INTO customers (display_name, reference_code) VALUES
('Acme Retail', 'HELPDESK-001'),
('Bright Foods', 'HELPDESK-002');

INSERT INTO tickets (helpdesk_entity_id, ticket_status, resolution_minutes, occurred_at, notes) VALUES
(1, 'closed', 45, '2026-08-27 10:00:00', 'Synthetic portfolio row'),
(2, 'open', 0, '2026-08-28 11:30:00', 'Synthetic portfolio row');
