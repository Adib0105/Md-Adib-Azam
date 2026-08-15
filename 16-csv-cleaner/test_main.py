import unittest

from main import clean_rows


class CleanerTests(unittest.TestCase):
    def test_strip_and_deduplicate(self):
        rows = [{" name ": " Adib ", "city": " Kolkata "}, {" name ": "Adib", "city": "Kolkata"}]
        self.assertEqual(clean_rows(rows), [{"name": "Adib", "city": "Kolkata"}])


if __name__ == "__main__":
    unittest.main()
