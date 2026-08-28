-- Synthetic sample data for Customer Feedback Database
INSERT INTO respondents (display_name, reference_code) VALUES
('Customer A', 'FEEDBACK-001'),
('Customer B', 'FEEDBACK-002');

INSERT INTO feedback_entries (feedback_entity_id, sentiment_label, rating, occurred_at, notes) VALUES
(1, 'positive', 5, '2026-08-27 10:00:00', 'Synthetic portfolio row'),
(2, 'negative', 2, '2026-08-28 11:30:00', 'Synthetic portfolio row');
