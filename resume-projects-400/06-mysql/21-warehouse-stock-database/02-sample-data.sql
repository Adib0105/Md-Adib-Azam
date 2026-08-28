-- Synthetic sample data for Warehouse Stock Database
INSERT INTO warehouses (display_name, reference_code) VALUES
('Howrah WH', 'WAREHOUSE-001'),
('Kolkata WH', 'WAREHOUSE-002');

INSERT INTO stock_balances (warehouse_entity_id, stock_status, on_hand_quantity, occurred_at, notes) VALUES
(1, 'healthy', 120, '2026-08-27 10:00:00', 'Synthetic portfolio row'),
(2, 'low', 8, '2026-08-28 11:30:00', 'Synthetic portfolio row');
