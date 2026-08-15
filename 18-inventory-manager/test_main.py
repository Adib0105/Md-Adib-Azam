import sqlite3
import unittest

from main import add_product, adjust_stock, init_db, low_stock


class InventoryTests(unittest.TestCase):
    def test_inventory_flow(self):
        connection = sqlite3.connect(":memory:")
        init_db(connection)
        add_product(connection, "SKU1", "Notebook", 4, 120)
        self.assertEqual(adjust_stock(connection, "SKU1", 2), 6)
        self.assertEqual(low_stock(connection, 5), [])
        with self.assertRaises(ValueError):
            adjust_stock(connection, "SKU1", -7)
        connection.close()


if __name__ == "__main__":
    unittest.main()
