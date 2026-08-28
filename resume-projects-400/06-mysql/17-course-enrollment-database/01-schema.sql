-- Course Enrollment Database - MySQL 8
CREATE TABLE IF NOT EXISTS courses (
    course_entity_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    display_name VARCHAR(120) NOT NULL,
    reference_code VARCHAR(40) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS course_enrollments (
    course_event_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    course_entity_id BIGINT UNSIGNED NOT NULL,
    completion_status VARCHAR(30) NOT NULL,
    progress_pct DECIMAL(12,2) NOT NULL DEFAULT 0,
    occurred_at DATETIME NOT NULL,
    notes VARCHAR(255),
    CONSTRAINT fk_course_activity_master
        FOREIGN KEY (course_entity_id) REFERENCES courses (course_entity_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_course_progress_pct CHECK (progress_pct >= 0),
    INDEX idx_course_status_time (completion_status, occurred_at),
    INDEX idx_course_master_time (course_entity_id, occurred_at)
) ENGINE=InnoDB;
