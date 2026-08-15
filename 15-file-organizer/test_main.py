import tempfile
import unittest
from pathlib import Path

from main import category_for, organize


class OrganizerTests(unittest.TestCase):
    def test_preview_and_apply(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / "photo.JPG"
            source.write_text("demo")
            self.assertEqual(category_for(source), "Images")
            moves = organize(root)
            self.assertTrue(source.exists())
            organize(root, apply=True)
            self.assertTrue(moves[0][1].exists())


if __name__ == "__main__":
    unittest.main()
