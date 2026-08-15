import unittest

from main import check_password


class PasswordTests(unittest.TestCase):
    def test_strong_password(self):
        self.assertEqual(check_password("Blue-River_492!")["rating"], "Strong")

    def test_weak_password_has_suggestions(self):
        result = check_password("abc")
        self.assertLess(result["score"], 4)
        self.assertTrue(result["suggestions"])


if __name__ == "__main__":
    unittest.main()
