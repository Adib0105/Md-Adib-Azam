-- Synthetic sample data for Digital Service Database
INSERT INTO service_customers (display_name, reference_code) VALUES
('Customer A', 'DIGITAL_SERVICE-001'),
('Customer B', 'DIGITAL_SERVICE-002');

INSERT INTO service_requests (digital_service_entity_id, request_status, turnaround_hours, occurred_at, notes) VALUES
(1, 'closed', 8, '2026-08-27 10:00:00', 'Synthetic portfolio row'),
(2, 'processing', 20, '2026-08-28 11:30:00', 'Synthetic portfolio row');
