-- Operational detail with the parent entity
SELECT
    m.reference_code,
    m.display_name,
    a.reservation_status,
    a.room_nights,
    a.occurred_at
FROM reservations AS a
JOIN guests AS m ON m.hotel_entity_id = a.hotel_entity_id
ORDER BY a.occurred_at DESC;

-- KPI summary (nights)
CREATE OR REPLACE VIEW vw_hotel_status_summary AS
SELECT
    reservation_status,
    COUNT(*) AS event_count,
    ROUND(AVG(room_nights), 2) AS average_room_nights,
    ROUND(SUM(room_nights), 2) AS total_room_nights
FROM reservations
GROUP BY reservation_status;

SELECT * FROM vw_hotel_status_summary
ORDER BY event_count DESC, reservation_status;
