-- Vehicle Rental Database - MySQL 8
CREATE TABLE IF NOT EXISTS vehicles (
    vehicle_entity_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    display_name VARCHAR(120) NOT NULL,
    reference_code VARCHAR(40) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS rental_contracts (
    vehicle_event_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    vehicle_entity_id BIGINT UNSIGNED NOT NULL,
    rental_status VARCHAR(30) NOT NULL,
    rental_days DECIMAL(12,2) NOT NULL DEFAULT 0,
    occurred_at DATETIME NOT NULL,
    notes VARCHAR(255),
    CONSTRAINT fk_vehicle_activity_master
        FOREIGN KEY (vehicle_entity_id) REFERENCES vehicles (vehicle_entity_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_vehicle_rental_days CHECK (rental_days >= 0),
    INDEX idx_vehicle_status_time (rental_status, occurred_at),
    INDEX idx_vehicle_master_time (vehicle_entity_id, occurred_at)
) ENGINE=InnoDB;
