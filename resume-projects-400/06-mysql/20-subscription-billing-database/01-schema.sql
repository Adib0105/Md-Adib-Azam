-- Subscription Billing Database - MySQL 8
CREATE TABLE IF NOT EXISTS plans (
    subscription_entity_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    display_name VARCHAR(120) NOT NULL,
    reference_code VARCHAR(40) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS subscriptions (
    subscription_event_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    subscription_entity_id BIGINT UNSIGNED NOT NULL,
    subscription_status VARCHAR(30) NOT NULL,
    monthly_amount DECIMAL(12,2) NOT NULL DEFAULT 0,
    occurred_at DATETIME NOT NULL,
    notes VARCHAR(255),
    CONSTRAINT fk_subscription_activity_master
        FOREIGN KEY (subscription_entity_id) REFERENCES plans (subscription_entity_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_subscription_monthly_amount CHECK (monthly_amount >= 0),
    INDEX idx_subscription_status_time (subscription_status, occurred_at),
    INDEX idx_subscription_master_time (subscription_entity_id, occurred_at)
) ENGINE=InnoDB;
