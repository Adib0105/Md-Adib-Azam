-- Employee Attendance Database - MySQL 8
CREATE TABLE IF NOT EXISTS employees (
    attendance_entity_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    display_name VARCHAR(120) NOT NULL,
    reference_code VARCHAR(40) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS attendance_events (
    attendance_event_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    attendance_entity_id BIGINT UNSIGNED NOT NULL,
    attendance_status VARCHAR(30) NOT NULL,
    worked_minutes DECIMAL(12,2) NOT NULL DEFAULT 0,
    occurred_at DATETIME NOT NULL,
    notes VARCHAR(255),
    CONSTRAINT fk_attendance_activity_master
        FOREIGN KEY (attendance_entity_id) REFERENCES employees (attendance_entity_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_attendance_worked_minutes CHECK (worked_minutes >= 0),
    INDEX idx_attendance_status_time (attendance_status, occurred_at),
    INDEX idx_attendance_master_time (attendance_entity_id, occurred_at)
) ENGINE=InnoDB;
