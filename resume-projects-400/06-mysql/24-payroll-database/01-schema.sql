-- Payroll Database - MySQL 8
CREATE TABLE IF NOT EXISTS employees_payroll (
    payroll_entity_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    display_name VARCHAR(120) NOT NULL,
    reference_code VARCHAR(40) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS pay_runs (
    payroll_event_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    payroll_entity_id BIGINT UNSIGNED NOT NULL,
    pay_status VARCHAR(30) NOT NULL,
    net_pay DECIMAL(12,2) NOT NULL DEFAULT 0,
    occurred_at DATETIME NOT NULL,
    notes VARCHAR(255),
    CONSTRAINT fk_payroll_activity_master
        FOREIGN KEY (payroll_entity_id) REFERENCES employees_payroll (payroll_entity_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_payroll_net_pay CHECK (net_pay >= 0),
    INDEX idx_payroll_status_time (pay_status, occurred_at),
    INDEX idx_payroll_master_time (payroll_entity_id, occurred_at)
) ENGINE=InnoDB;
