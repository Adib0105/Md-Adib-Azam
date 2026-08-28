-- Synthetic sample data for Vehicle Rental Database
INSERT INTO vehicles (display_name, reference_code) VALUES
('Bike WB01', 'VEHICLE-001'),
('Car WB02', 'VEHICLE-002');

INSERT INTO rental_contracts (vehicle_entity_id, rental_status, rental_days, occurred_at, notes) VALUES
(1, 'returned', 4, '2026-08-27 10:00:00', 'Synthetic portfolio row'),
(2, 'active', 2, '2026-08-28 11:30:00', 'Synthetic portfolio row');
