-- Ecommerce Order Database - MySQL 8
CREATE TABLE IF NOT EXISTS orders (
    ecommerce_entity_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    display_name VARCHAR(120) NOT NULL,
    reference_code VARCHAR(40) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS order_lines (
    ecommerce_event_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    ecommerce_entity_id BIGINT UNSIGNED NOT NULL,
    fulfilment_status VARCHAR(30) NOT NULL,
    line_total DECIMAL(12,2) NOT NULL DEFAULT 0,
    occurred_at DATETIME NOT NULL,
    notes VARCHAR(255),
    CONSTRAINT fk_ecommerce_activity_master
        FOREIGN KEY (ecommerce_entity_id) REFERENCES orders (ecommerce_entity_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_ecommerce_line_total CHECK (line_total >= 0),
    INDEX idx_ecommerce_status_time (fulfilment_status, occurred_at),
    INDEX idx_ecommerce_master_time (ecommerce_entity_id, occurred_at)
) ENGINE=InnoDB;
