import unittest
from decimal import Decimal

from main import add_expense, category_totals


class ExpenseTests(unittest.TestCase):
    def test_add_and_report(self):
        expenses = []
        add_expense(expenses, "100.50", "food", spent_on="2026-08-16")
        add_expense(expenses, "49.50", "Food", spent_on="2026-08-16")
        self.assertEqual(category_totals(expenses)["Food"], Decimal("150.00"))


if __name__ == "__main__":
    unittest.main()
