-- Synthetic sample data for Restaurant Order Database
INSERT INTO menu_items (display_name, reference_code) VALUES
('Biryani', 'RESTAURANT-001'),
('Cold Drink', 'RESTAURANT-002');

INSERT INTO order_items (restaurant_entity_id, kitchen_status, line_total, occurred_at, notes) VALUES
(1, 'served', 720, '2026-08-27 10:00:00', 'Synthetic portfolio row'),
(2, 'preparing', 120, '2026-08-28 11:30:00', 'Synthetic portfolio row');
