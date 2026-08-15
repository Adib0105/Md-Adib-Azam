import hashlib
import tempfile
import unittest
from pathlib import Path

from main import build_manifest, sha256_file


class ChecksumTests(unittest.TestCase):
    def test_checksum_and_manifest(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            path = root / "hello.txt"
            path.write_bytes(b"hello")
            expected = hashlib.sha256(b"hello").hexdigest()
            self.assertEqual(sha256_file(path), expected)
            self.assertEqual(build_manifest(root), [("hello.txt", expected)])


if __name__ == "__main__":
    unittest.main()
