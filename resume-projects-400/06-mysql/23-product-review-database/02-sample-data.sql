-- Synthetic sample data for Product Review Database
INSERT INTO reviewed_products (display_name, reference_code) VALUES
('Headset', 'REVIEW-001'),
('Keyboard', 'REVIEW-002');

INSERT INTO product_reviews (review_entity_id, moderation_status, rating, occurred_at, notes) VALUES
(1, 'published', 4, '2026-08-27 10:00:00', 'Synthetic portfolio row'),
(2, 'pending', 3, '2026-08-28 11:30:00', 'Synthetic portfolio row');
