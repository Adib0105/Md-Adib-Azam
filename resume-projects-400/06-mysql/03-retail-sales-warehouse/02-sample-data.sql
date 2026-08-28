-- Synthetic sample data for Retail Sales Warehouse
INSERT INTO products (display_name, reference_code) VALUES
('Wireless Mouse', 'RETAIL-001'),
('Keyboard', 'RETAIL-002');

INSERT INTO sale_items (retail_entity_id, sales_channel, line_revenue, occurred_at, notes) VALUES
(1, 'online', 1398, '2026-08-27 10:00:00', 'Synthetic portfolio row'),
(2, 'store', 1299, '2026-08-28 11:30:00', 'Synthetic portfolio row');
