-- Student Information System - MySQL 8
CREATE TABLE IF NOT EXISTS students (
    student_entity_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    display_name VARCHAR(120) NOT NULL,
    reference_code VARCHAR(40) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS enrollments (
    student_event_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    student_entity_id BIGINT UNSIGNED NOT NULL,
    enrollment_status VARCHAR(30) NOT NULL,
    final_score DECIMAL(12,2) NOT NULL DEFAULT 0,
    occurred_at DATETIME NOT NULL,
    notes VARCHAR(255),
    CONSTRAINT fk_student_activity_master
        FOREIGN KEY (student_entity_id) REFERENCES students (student_entity_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_student_final_score CHECK (final_score >= 0),
    INDEX idx_student_status_time (enrollment_status, occurred_at),
    INDEX idx_student_master_time (student_entity_id, occurred_at)
) ENGINE=InnoDB;
