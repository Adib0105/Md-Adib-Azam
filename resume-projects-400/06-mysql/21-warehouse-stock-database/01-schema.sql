-- Warehouse Stock Database - MySQL 8
CREATE TABLE IF NOT EXISTS warehouses (
    warehouse_entity_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    display_name VARCHAR(120) NOT NULL,
    reference_code VARCHAR(40) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS stock_balances (
    warehouse_event_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    warehouse_entity_id BIGINT UNSIGNED NOT NULL,
    stock_status VARCHAR(30) NOT NULL,
    on_hand_quantity DECIMAL(12,2) NOT NULL DEFAULT 0,
    occurred_at DATETIME NOT NULL,
    notes VARCHAR(255),
    CONSTRAINT fk_warehouse_activity_master
        FOREIGN KEY (warehouse_entity_id) REFERENCES warehouses (warehouse_entity_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_warehouse_on_hand_quantity CHECK (on_hand_quantity >= 0),
    INDEX idx_warehouse_status_time (stock_status, occurred_at),
    INDEX idx_warehouse_master_time (warehouse_entity_id, occurred_at)
) ENGINE=InnoDB;
