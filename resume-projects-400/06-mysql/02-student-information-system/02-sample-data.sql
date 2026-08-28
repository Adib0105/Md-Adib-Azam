-- Synthetic sample data for Student Information System
INSERT INTO students (display_name, reference_code) VALUES
('Asha Singh', 'STUDENT-001'),
('Kabir Ali', 'STUDENT-002');

INSERT INTO enrollments (student_entity_id, enrollment_status, final_score, occurred_at, notes) VALUES
(1, 'completed', 88, '2026-08-27 10:00:00', 'Synthetic portfolio row'),
(2, 'active', 0, '2026-08-28 11:30:00', 'Synthetic portfolio row');
