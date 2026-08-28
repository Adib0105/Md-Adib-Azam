-- Helpdesk Database - MySQL 8
CREATE TABLE IF NOT EXISTS customers (
    helpdesk_entity_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    display_name VARCHAR(120) NOT NULL,
    reference_code VARCHAR(40) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS tickets (
    helpdesk_event_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    helpdesk_entity_id BIGINT UNSIGNED NOT NULL,
    ticket_status VARCHAR(30) NOT NULL,
    resolution_minutes DECIMAL(12,2) NOT NULL DEFAULT 0,
    occurred_at DATETIME NOT NULL,
    notes VARCHAR(255),
    CONSTRAINT fk_helpdesk_activity_master
        FOREIGN KEY (helpdesk_entity_id) REFERENCES customers (helpdesk_entity_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_helpdesk_resolution_minutes CHECK (resolution_minutes >= 0),
    INDEX idx_helpdesk_status_time (ticket_status, occurred_at),
    INDEX idx_helpdesk_master_time (helpdesk_entity_id, occurred_at)
) ENGINE=InnoDB;
