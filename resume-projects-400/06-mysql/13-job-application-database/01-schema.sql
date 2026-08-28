-- Job Application Database - MySQL 8
CREATE TABLE IF NOT EXISTS candidates (
    job_application_entity_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    display_name VARCHAR(120) NOT NULL,
    reference_code VARCHAR(40) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS applications (
    job_application_event_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    job_application_entity_id BIGINT UNSIGNED NOT NULL,
    application_status VARCHAR(30) NOT NULL,
    fit_score DECIMAL(12,2) NOT NULL DEFAULT 0,
    occurred_at DATETIME NOT NULL,
    notes VARCHAR(255),
    CONSTRAINT fk_job_application_activity_master
        FOREIGN KEY (job_application_entity_id) REFERENCES candidates (job_application_entity_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_job_application_fit_score CHECK (fit_score >= 0),
    INDEX idx_job_application_status_time (application_status, occurred_at),
    INDEX idx_job_application_master_time (job_application_entity_id, occurred_at)
) ENGINE=InnoDB;
