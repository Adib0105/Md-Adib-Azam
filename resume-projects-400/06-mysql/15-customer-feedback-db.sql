-- Customer Feedback DB: MySQL 8 schema, sample data, analytics view and index.
CREATE TABLE IF NOT EXISTS project_15_records (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  customer_name VARCHAR(100) NOT NULL,
  status ENUM('open','pending','closed') NOT NULL DEFAULT 'open',
  amount DECIMAL(12,2) NOT NULL DEFAULT 0 CHECK (amount >= 0),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_15_status_created (status, created_at)
);
INSERT INTO project_15_records (customer_name,status,amount) VALUES ('Alpha','open',115),('Beta','closed',215);
CREATE OR REPLACE VIEW v_project_15_records_summary AS SELECT status, COUNT(*) AS records, SUM(amount) AS total_amount, AVG(amount) AS avg_amount FROM project_15_records GROUP BY status;
SELECT * FROM v_project_15_records_summary ORDER BY total_amount DESC;
