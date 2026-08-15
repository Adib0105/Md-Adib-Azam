import unittest

from main import split_sentences, summarize


class SummaryTests(unittest.TestCase):
    def test_summary_length(self):
        text = "Python is popular. Python supports automation. Rain fell today. Python has many libraries."
        result = summarize(text, 2)
        self.assertEqual(len(split_sentences(result)), 2)
        self.assertIn("Python", result)


if __name__ == "__main__":
    unittest.main()
