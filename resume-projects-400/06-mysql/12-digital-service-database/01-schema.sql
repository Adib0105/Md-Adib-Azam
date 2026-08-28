-- Digital Service Database - MySQL 8
CREATE TABLE IF NOT EXISTS service_customers (
    digital_service_entity_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    display_name VARCHAR(120) NOT NULL,
    reference_code VARCHAR(40) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS service_requests (
    digital_service_event_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    digital_service_entity_id BIGINT UNSIGNED NOT NULL,
    request_status VARCHAR(30) NOT NULL,
    turnaround_hours DECIMAL(12,2) NOT NULL DEFAULT 0,
    occurred_at DATETIME NOT NULL,
    notes VARCHAR(255),
    CONSTRAINT fk_digital_service_activity_master
        FOREIGN KEY (digital_service_entity_id) REFERENCES service_customers (digital_service_entity_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_digital_service_turnaround_hours CHECK (turnaround_hours >= 0),
    INDEX idx_digital_service_status_time (request_status, occurred_at),
    INDEX idx_digital_service_master_time (digital_service_entity_id, occurred_at)
) ENGINE=InnoDB;
