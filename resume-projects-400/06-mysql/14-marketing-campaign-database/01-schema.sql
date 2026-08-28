-- Marketing Campaign Database - MySQL 8
CREATE TABLE IF NOT EXISTS campaigns (
    campaign_entity_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    display_name VARCHAR(120) NOT NULL,
    reference_code VARCHAR(40) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS campaign_events (
    campaign_event_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    campaign_entity_id BIGINT UNSIGNED NOT NULL,
    event_type VARCHAR(30) NOT NULL,
    attributed_revenue DECIMAL(12,2) NOT NULL DEFAULT 0,
    occurred_at DATETIME NOT NULL,
    notes VARCHAR(255),
    CONSTRAINT fk_campaign_activity_master
        FOREIGN KEY (campaign_entity_id) REFERENCES campaigns (campaign_entity_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_campaign_attributed_revenue CHECK (attributed_revenue >= 0),
    INDEX idx_campaign_status_time (event_type, occurred_at),
    INDEX idx_campaign_master_time (campaign_entity_id, occurred_at)
) ENGINE=InnoDB;
