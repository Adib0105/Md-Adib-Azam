-- Support SLA Analytics - MySQL 8
CREATE TABLE IF NOT EXISTS support_teams (
    support_sla_entity_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    display_name VARCHAR(120) NOT NULL,
    reference_code VARCHAR(40) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS sla_measurements (
    support_sla_event_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    support_sla_entity_id BIGINT UNSIGNED NOT NULL,
    sla_status VARCHAR(30) NOT NULL,
    first_response_minutes DECIMAL(12,2) NOT NULL DEFAULT 0,
    occurred_at DATETIME NOT NULL,
    notes VARCHAR(255),
    CONSTRAINT fk_support_sla_activity_master
        FOREIGN KEY (support_sla_entity_id) REFERENCES support_teams (support_sla_entity_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_support_sla_first_response_minutes CHECK (first_response_minutes >= 0),
    INDEX idx_support_sla_status_time (sla_status, occurred_at),
    INDEX idx_support_sla_master_time (support_sla_entity_id, occurred_at)
) ENGINE=InnoDB;
