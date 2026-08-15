import tempfile
import unittest
from pathlib import Path

from PIL import Image

from main import resize_image


class ImageTests(unittest.TestCase):
    def test_aspect_ratio(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "source.png"
            destination = Path(folder) / "out.png"
            Image.new("RGB", (800, 400), "blue").save(source)
            self.assertEqual(resize_image(source, destination, (200, 200)), (200, 100))
            self.assertTrue(destination.exists())


if __name__ == "__main__":
    unittest.main()
