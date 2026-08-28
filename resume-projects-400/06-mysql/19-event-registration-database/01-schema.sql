-- Event Registration Database - MySQL 8
CREATE TABLE IF NOT EXISTS events (
    event_entity_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    display_name VARCHAR(120) NOT NULL,
    reference_code VARCHAR(40) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS event_registrations (
    event_event_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    event_entity_id BIGINT UNSIGNED NOT NULL,
    payment_status VARCHAR(30) NOT NULL,
    tickets DECIMAL(12,2) NOT NULL DEFAULT 0,
    occurred_at DATETIME NOT NULL,
    notes VARCHAR(255),
    CONSTRAINT fk_event_activity_master
        FOREIGN KEY (event_entity_id) REFERENCES events (event_entity_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_event_tickets CHECK (tickets >= 0),
    INDEX idx_event_status_time (payment_status, occurred_at),
    INDEX idx_event_master_time (event_entity_id, occurred_at)
) ENGINE=InnoDB;
