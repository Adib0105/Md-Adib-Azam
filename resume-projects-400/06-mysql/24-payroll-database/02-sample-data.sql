-- Synthetic sample data for Payroll Database
INSERT INTO employees_payroll (display_name, reference_code) VALUES
('Employee A', 'PAYROLL-001'),
('Employee B', 'PAYROLL-002');

INSERT INTO pay_runs (payroll_entity_id, pay_status, net_pay, occurred_at, notes) VALUES
(1, 'paid', 38500, '2026-08-27 10:00:00', 'Synthetic portfolio row'),
(2, 'review', 29200, '2026-08-28 11:30:00', 'Synthetic portfolio row');
