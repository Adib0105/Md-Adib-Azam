-- Synthetic sample data for Data Quality Audit Database
INSERT INTO data_sources (display_name, reference_code) VALUES
('CRM Import', 'QUALITY-001'),
('Sales Export', 'QUALITY-002');

INSERT INTO quality_checks (quality_entity_id, check_status, failed_rows, occurred_at, notes) VALUES
(1, 'passed', 0, '2026-08-27 10:00:00', 'Synthetic portfolio row'),
(2, 'failed', 14, '2026-08-28 11:30:00', 'Synthetic portfolio row');
