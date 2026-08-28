-- CRM Lead Database - MySQL 8
CREATE TABLE IF NOT EXISTS leads (
    crm_entity_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    display_name VARCHAR(120) NOT NULL,
    reference_code VARCHAR(40) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS lead_activities (
    crm_event_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    crm_entity_id BIGINT UNSIGNED NOT NULL,
    activity_type VARCHAR(30) NOT NULL,
    engagement_score DECIMAL(12,2) NOT NULL DEFAULT 0,
    occurred_at DATETIME NOT NULL,
    notes VARCHAR(255),
    CONSTRAINT fk_crm_activity_master
        FOREIGN KEY (crm_entity_id) REFERENCES leads (crm_entity_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_crm_engagement_score CHECK (engagement_score >= 0),
    INDEX idx_crm_status_time (activity_type, occurred_at),
    INDEX idx_crm_master_time (crm_entity_id, occurred_at)
) ENGINE=InnoDB;
