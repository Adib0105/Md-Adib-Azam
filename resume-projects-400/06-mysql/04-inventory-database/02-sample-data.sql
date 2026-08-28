-- Synthetic sample data for Inventory Database
INSERT INTO stock_items (display_name, reference_code) VALUES
('SKU-A1', 'INVENTORY-001'),
('SKU-B2', 'INVENTORY-002');

INSERT INTO stock_movements (inventory_entity_id, movement_type, quantity, occurred_at, notes) VALUES
(1, 'receipt', 40, '2026-08-27 10:00:00', 'Synthetic portfolio row'),
(2, 'issue', 12, '2026-08-28 11:30:00', 'Synthetic portfolio row');
