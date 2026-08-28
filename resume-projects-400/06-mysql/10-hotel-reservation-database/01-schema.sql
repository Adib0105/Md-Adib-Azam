-- Hotel Reservation Database - MySQL 8
CREATE TABLE IF NOT EXISTS guests (
    hotel_entity_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    display_name VARCHAR(120) NOT NULL,
    reference_code VARCHAR(40) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS reservations (
    hotel_event_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    hotel_entity_id BIGINT UNSIGNED NOT NULL,
    reservation_status VARCHAR(30) NOT NULL,
    room_nights DECIMAL(12,2) NOT NULL DEFAULT 0,
    occurred_at DATETIME NOT NULL,
    notes VARCHAR(255),
    CONSTRAINT fk_hotel_activity_master
        FOREIGN KEY (hotel_entity_id) REFERENCES guests (hotel_entity_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_hotel_room_nights CHECK (room_nights >= 0),
    INDEX idx_hotel_status_time (reservation_status, occurred_at),
    INDEX idx_hotel_master_time (hotel_entity_id, occurred_at)
) ENGINE=InnoDB;
