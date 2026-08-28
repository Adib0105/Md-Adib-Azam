-- Hospital Appointment Database - MySQL 8
CREATE TABLE IF NOT EXISTS patients (
    hospital_entity_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    display_name VARCHAR(120) NOT NULL,
    reference_code VARCHAR(40) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS appointments (
    hospital_event_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    hospital_entity_id BIGINT UNSIGNED NOT NULL,
    appointment_status VARCHAR(30) NOT NULL,
    wait_minutes DECIMAL(12,2) NOT NULL DEFAULT 0,
    occurred_at DATETIME NOT NULL,
    notes VARCHAR(255),
    CONSTRAINT fk_hospital_activity_master
        FOREIGN KEY (hospital_entity_id) REFERENCES patients (hospital_entity_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_hospital_wait_minutes CHECK (wait_minutes >= 0),
    INDEX idx_hospital_status_time (appointment_status, occurred_at),
    INDEX idx_hospital_master_time (hospital_entity_id, occurred_at)
) ENGINE=InnoDB;
