-- Synthetic sample data for Support SLA Analytics
INSERT INTO support_teams (display_name, reference_code) VALUES
('L1 Support', 'SUPPORT_SLA-001'),
('Email Support', 'SUPPORT_SLA-002');

INSERT INTO sla_measurements (support_sla_entity_id, sla_status, first_response_minutes, occurred_at, notes) VALUES
(1, 'met', 20, '2026-08-27 10:00:00', 'Synthetic portfolio row'),
(2, 'breached', 180, '2026-08-28 11:30:00', 'Synthetic portfolio row');
