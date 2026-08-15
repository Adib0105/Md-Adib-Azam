import unittest

from main import analyze, parse_line


class LogTests(unittest.TestCase):
    def test_parse_and_summary(self):
        lines = [
            "[2026-08-16 10:00:00] INFO Started",
            "[2026-08-16 10:01:00] ERROR Database unavailable",
            "invalid",
        ]
        self.assertEqual(parse_line(lines[0])["level"], "INFO")
        report = analyze(lines)
        self.assertEqual(report["levels"]["ERROR"], 1)
        self.assertEqual(report["ignored"], 1)


if __name__ == "__main__":
    unittest.main()
