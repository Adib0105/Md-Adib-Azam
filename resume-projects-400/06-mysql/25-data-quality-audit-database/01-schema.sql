-- Data Quality Audit Database - MySQL 8
CREATE TABLE IF NOT EXISTS data_sources (
    quality_entity_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    display_name VARCHAR(120) NOT NULL,
    reference_code VARCHAR(40) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS quality_checks (
    quality_event_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    quality_entity_id BIGINT UNSIGNED NOT NULL,
    check_status VARCHAR(30) NOT NULL,
    failed_rows DECIMAL(12,2) NOT NULL DEFAULT 0,
    occurred_at DATETIME NOT NULL,
    notes VARCHAR(255),
    CONSTRAINT fk_quality_activity_master
        FOREIGN KEY (quality_entity_id) REFERENCES data_sources (quality_entity_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_quality_failed_rows CHECK (failed_rows >= 0),
    INDEX idx_quality_status_time (check_status, occurred_at),
    INDEX idx_quality_master_time (quality_entity_id, occurred_at)
) ENGINE=InnoDB;
