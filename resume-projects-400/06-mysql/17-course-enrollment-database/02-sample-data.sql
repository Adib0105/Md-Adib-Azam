-- Synthetic sample data for Course Enrollment Database
INSERT INTO courses (display_name, reference_code) VALUES
('Python Essentials', 'COURSE-001'),
('Data Analytics', 'COURSE-002');

INSERT INTO course_enrollments (course_entity_id, completion_status, progress_pct, occurred_at, notes) VALUES
(1, 'completed', 100, '2026-08-27 10:00:00', 'Synthetic portfolio row'),
(2, 'active', 65, '2026-08-28 11:30:00', 'Synthetic portfolio row');
