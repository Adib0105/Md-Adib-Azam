import unittest

from main import convert


class ConverterTests(unittest.TestCase):
    def test_conversions(self):
        self.assertAlmostEqual(convert(1, "km", "m"), 1000)
        self.assertAlmostEqual(convert(32, "f", "c"), 0)
        self.assertAlmostEqual(convert(1, "kg", "lb"), 2.20462, places=4)

    def test_invalid_category(self):
        with self.assertRaises(ValueError):
            convert(1, "km", "kg")


if __name__ == "__main__":
    unittest.main()
