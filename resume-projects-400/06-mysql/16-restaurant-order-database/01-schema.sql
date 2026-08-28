-- Restaurant Order Database - MySQL 8
CREATE TABLE IF NOT EXISTS menu_items (
    restaurant_entity_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    display_name VARCHAR(120) NOT NULL,
    reference_code VARCHAR(40) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS order_items (
    restaurant_event_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    restaurant_entity_id BIGINT UNSIGNED NOT NULL,
    kitchen_status VARCHAR(30) NOT NULL,
    line_total DECIMAL(12,2) NOT NULL DEFAULT 0,
    occurred_at DATETIME NOT NULL,
    notes VARCHAR(255),
    CONSTRAINT fk_restaurant_activity_master
        FOREIGN KEY (restaurant_entity_id) REFERENCES menu_items (restaurant_entity_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_restaurant_line_total CHECK (line_total >= 0),
    INDEX idx_restaurant_status_time (kitchen_status, occurred_at),
    INDEX idx_restaurant_master_time (restaurant_entity_id, occurred_at)
) ENGINE=InnoDB;
