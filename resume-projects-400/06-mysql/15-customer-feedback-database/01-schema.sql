-- Customer Feedback Database - MySQL 8
CREATE TABLE IF NOT EXISTS respondents (
    feedback_entity_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    display_name VARCHAR(120) NOT NULL,
    reference_code VARCHAR(40) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS feedback_entries (
    feedback_event_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    feedback_entity_id BIGINT UNSIGNED NOT NULL,
    sentiment_label VARCHAR(30) NOT NULL,
    rating DECIMAL(12,2) NOT NULL DEFAULT 0,
    occurred_at DATETIME NOT NULL,
    notes VARCHAR(255),
    CONSTRAINT fk_feedback_activity_master
        FOREIGN KEY (feedback_entity_id) REFERENCES respondents (feedback_entity_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_feedback_rating CHECK (rating >= 0),
    INDEX idx_feedback_status_time (sentiment_label, occurred_at),
    INDEX idx_feedback_master_time (feedback_entity_id, occurred_at)
) ENGINE=InnoDB;
