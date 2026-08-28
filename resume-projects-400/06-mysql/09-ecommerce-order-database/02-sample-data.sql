-- Synthetic sample data for Ecommerce Order Database
INSERT INTO orders (display_name, reference_code) VALUES
('ORD-1001', 'ECOMMERCE-001'),
('ORD-1002', 'ECOMMERCE-002');

INSERT INTO order_lines (ecommerce_entity_id, fulfilment_status, line_total, occurred_at, notes) VALUES
(1, 'shipped', 2499, '2026-08-27 10:00:00', 'Synthetic portfolio row'),
(2, 'pending', 899, '2026-08-28 11:30:00', 'Synthetic portfolio row');
