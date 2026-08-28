-- Expense Ledger Database - MySQL 8
CREATE TABLE IF NOT EXISTS cost_centres (
    expense_entity_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    display_name VARCHAR(120) NOT NULL,
    reference_code VARCHAR(40) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS expense_entries (
    expense_event_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    expense_entity_id BIGINT UNSIGNED NOT NULL,
    approval_status VARCHAR(30) NOT NULL,
    expense_amount DECIMAL(12,2) NOT NULL DEFAULT 0,
    occurred_at DATETIME NOT NULL,
    notes VARCHAR(255),
    CONSTRAINT fk_expense_activity_master
        FOREIGN KEY (expense_entity_id) REFERENCES cost_centres (expense_entity_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_expense_expense_amount CHECK (expense_amount >= 0),
    INDEX idx_expense_status_time (approval_status, occurred_at),
    INDEX idx_expense_master_time (expense_entity_id, occurred_at)
) ENGINE=InnoDB;
