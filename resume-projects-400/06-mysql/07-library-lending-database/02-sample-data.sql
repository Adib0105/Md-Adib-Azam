-- Synthetic sample data for Library Lending Database
INSERT INTO books (display_name, reference_code) VALUES
('Python Basics', 'LIBRARY-001'),
('SQL Guide', 'LIBRARY-002');

INSERT INTO loan_events (library_entity_id, loan_status, loan_days, occurred_at, notes) VALUES
(1, 'returned', 7, '2026-08-27 10:00:00', 'Synthetic portfolio row'),
(2, 'overdue', 18, '2026-08-28 11:30:00', 'Synthetic portfolio row');
