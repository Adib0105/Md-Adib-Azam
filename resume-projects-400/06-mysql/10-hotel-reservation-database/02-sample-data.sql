-- Synthetic sample data for Hotel Reservation Database
INSERT INTO guests (display_name, reference_code) VALUES
('Asha Singh', 'HOTEL-001'),
('Kabir Ali', 'HOTEL-002');

INSERT INTO reservations (hotel_entity_id, reservation_status, room_nights, occurred_at, notes) VALUES
(1, 'checked_out', 3, '2026-08-27 10:00:00', 'Synthetic portfolio row'),
(2, 'confirmed', 2, '2026-08-28 11:30:00', 'Synthetic portfolio row');
