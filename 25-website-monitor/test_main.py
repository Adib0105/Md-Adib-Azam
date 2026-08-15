import unittest

from main import check_url


class FakeResponse:
    status_code = 200
    status = 200

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def fake_opener(request, timeout):
    return FakeResponse()


class MonitorTests(unittest.TestCase):
    def test_success(self):
        result = check_url("https://example.com", opener=fake_opener)
        self.assertTrue(result["available"])
        self.assertEqual(result["status"], 200)


if __name__ == "__main__":
    unittest.main()
