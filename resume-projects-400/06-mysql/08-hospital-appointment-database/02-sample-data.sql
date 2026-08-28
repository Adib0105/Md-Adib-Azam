-- Synthetic sample data for Hospital Appointment Database
INSERT INTO patients (display_name, reference_code) VALUES
('Patient A', 'HOSPITAL-001'),
('Patient B', 'HOSPITAL-002');

INSERT INTO appointments (hospital_entity_id, appointment_status, wait_minutes, occurred_at, notes) VALUES
(1, 'completed', 25, '2026-08-27 10:00:00', 'Synthetic portfolio row'),
(2, 'scheduled', 0, '2026-08-28 11:30:00', 'Synthetic portfolio row');
