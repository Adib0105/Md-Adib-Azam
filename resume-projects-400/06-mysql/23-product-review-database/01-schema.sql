-- Product Review Database - MySQL 8
CREATE TABLE IF NOT EXISTS reviewed_products (
    review_entity_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    display_name VARCHAR(120) NOT NULL,
    reference_code VARCHAR(40) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS product_reviews (
    review_event_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    review_entity_id BIGINT UNSIGNED NOT NULL,
    moderation_status VARCHAR(30) NOT NULL,
    rating DECIMAL(12,2) NOT NULL DEFAULT 0,
    occurred_at DATETIME NOT NULL,
    notes VARCHAR(255),
    CONSTRAINT fk_review_activity_master
        FOREIGN KEY (review_entity_id) REFERENCES reviewed_products (review_entity_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_review_rating CHECK (rating >= 0),
    INDEX idx_review_status_time (moderation_status, occurred_at),
    INDEX idx_review_master_time (review_entity_id, occurred_at)
) ENGINE=InnoDB;
