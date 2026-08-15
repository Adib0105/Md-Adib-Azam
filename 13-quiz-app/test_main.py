import unittest

from main import QUESTIONS, calculate_score, normalize_answer


class QuizTests(unittest.TestCase):
    def test_score(self):
        self.assertEqual(calculate_score(QUESTIONS, ["B", "a", " b "]), 3)

    def test_normalization(self):
        self.assertEqual(normalize_answer(" A "), "a")


if __name__ == "__main__":
    unittest.main()
