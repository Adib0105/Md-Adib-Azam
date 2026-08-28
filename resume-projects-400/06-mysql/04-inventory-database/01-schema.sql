-- Inventory Database - MySQL 8
CREATE TABLE IF NOT EXISTS stock_items (
    inventory_entity_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    display_name VARCHAR(120) NOT NULL,
    reference_code VARCHAR(40) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS stock_movements (
    inventory_event_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    inventory_entity_id BIGINT UNSIGNED NOT NULL,
    movement_type VARCHAR(30) NOT NULL,
    quantity DECIMAL(12,2) NOT NULL DEFAULT 0,
    occurred_at DATETIME NOT NULL,
    notes VARCHAR(255),
    CONSTRAINT fk_inventory_activity_master
        FOREIGN KEY (inventory_entity_id) REFERENCES stock_items (inventory_entity_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_inventory_quantity CHECK (quantity >= 0),
    INDEX idx_inventory_status_time (movement_type, occurred_at),
    INDEX idx_inventory_master_time (inventory_entity_id, occurred_at)
) ENGINE=InnoDB;
