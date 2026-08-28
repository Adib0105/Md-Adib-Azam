-- Synthetic sample data for Expense Ledger Database
INSERT INTO cost_centres (display_name, reference_code) VALUES
('Operations', 'EXPENSE-001'),
('Marketing', 'EXPENSE-002');

INSERT INTO expense_entries (expense_entity_id, approval_status, expense_amount, occurred_at, notes) VALUES
(1, 'approved', 3200, '2026-08-27 10:00:00', 'Synthetic portfolio row'),
(2, 'pending', 1800, '2026-08-28 11:30:00', 'Synthetic portfolio row');
