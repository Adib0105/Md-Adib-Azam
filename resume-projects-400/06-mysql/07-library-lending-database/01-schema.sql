-- Library Lending Database - MySQL 8
CREATE TABLE IF NOT EXISTS books (
    library_entity_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    display_name VARCHAR(120) NOT NULL,
    reference_code VARCHAR(40) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS loan_events (
    library_event_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    library_entity_id BIGINT UNSIGNED NOT NULL,
    loan_status VARCHAR(30) NOT NULL,
    loan_days DECIMAL(12,2) NOT NULL DEFAULT 0,
    occurred_at DATETIME NOT NULL,
    notes VARCHAR(255),
    CONSTRAINT fk_library_activity_master
        FOREIGN KEY (library_entity_id) REFERENCES books (library_entity_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_library_loan_days CHECK (loan_days >= 0),
    INDEX idx_library_status_time (loan_status, occurred_at),
    INDEX idx_library_master_time (library_entity_id, occurred_at)
) ENGINE=InnoDB;
