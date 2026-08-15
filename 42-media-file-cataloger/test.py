import base64
from pathlib import Path
from tempfile import TemporaryDirectory

from app import catalog, image_dimensions

PNG_1X1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
)
with TemporaryDirectory() as folder:
    root = Path(folder)
    (root / "pixel.png").write_bytes(PNG_1X1)
    (root / "notes.txt").write_text("ignore")
    assert image_dimensions(root / "pixel.png") == (1, 1)
    rows = catalog(root)
    assert len(rows) == 1
    assert rows[0]["path"] == "pixel.png"
    assert len(rows[0]["sha256"]) == 64

print("Media cataloger tests passed")
