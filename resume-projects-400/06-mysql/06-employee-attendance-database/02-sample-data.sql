-- Synthetic sample data for Employee Attendance Database
INSERT INTO employees (display_name, reference_code) VALUES
('Asha Singh', 'ATTENDANCE-001'),
('Kabir Ali', 'ATTENDANCE-002');

INSERT INTO attendance_events (attendance_entity_id, attendance_status, worked_minutes, occurred_at, notes) VALUES
(1, 'present', 480, '2026-08-27 10:00:00', 'Synthetic portfolio row'),
(2, 'late', 420, '2026-08-28 11:30:00', 'Synthetic portfolio row');
