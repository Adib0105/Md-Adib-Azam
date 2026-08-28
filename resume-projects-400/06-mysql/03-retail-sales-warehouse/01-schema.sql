-- Retail Sales Warehouse - MySQL 8
CREATE TABLE IF NOT EXISTS products (
    retail_entity_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    display_name VARCHAR(120) NOT NULL,
    reference_code VARCHAR(40) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS sale_items (
    retail_event_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    retail_entity_id BIGINT UNSIGNED NOT NULL,
    sales_channel VARCHAR(30) NOT NULL,
    line_revenue DECIMAL(12,2) NOT NULL DEFAULT 0,
    occurred_at DATETIME NOT NULL,
    notes VARCHAR(255),
    CONSTRAINT fk_retail_activity_master
        FOREIGN KEY (retail_entity_id) REFERENCES products (retail_entity_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_retail_line_revenue CHECK (line_revenue >= 0),
    INDEX idx_retail_status_time (sales_channel, occurred_at),
    INDEX idx_retail_master_time (retail_entity_id, occurred_at)
) ENGINE=InnoDB;
