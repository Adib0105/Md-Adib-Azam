-- Synthetic sample data for Job Application Database
INSERT INTO candidates (display_name, reference_code) VALUES
('Candidate A', 'JOB_APPLICATION-001'),
('Candidate B', 'JOB_APPLICATION-002');

INSERT INTO applications (job_application_entity_id, application_status, fit_score, occurred_at, notes) VALUES
(1, 'interview', 82, '2026-08-27 10:00:00', 'Synthetic portfolio row'),
(2, 'applied', 68, '2026-08-28 11:30:00', 'Synthetic portfolio row');
