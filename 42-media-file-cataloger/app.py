from __future__ import annotations

import argparse
import csv
import hashlib
import struct
from pathlib import Path


MEDIA_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".mp4", ".mov", ".wav", ".mp3"}


def checksum(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def image_dimensions(path: Path) -> tuple[int | None, int | None]:
    with path.open("rb") as source:
        header = source.read(24)
        if header.startswith(b"\x89PNG\r\n\x1a\n") and len(header) >= 24:
            return struct.unpack(">II", header[16:24])
        if header[:6] in {b"GIF87a", b"GIF89a"}:
            return struct.unpack("<HH", header[6:10])
        if header.startswith(b"\xff\xd8"):
            source.seek(2)
            while True:
                marker_start = source.read(1)
                if not marker_start:
                    break
                if marker_start != b"\xff":
                    continue
                marker = source.read(1)
                while marker == b"\xff":
                    marker = source.read(1)
                if marker in {b"\xd8", b"\xd9"}:
                    continue
                length_data = source.read(2)
                if len(length_data) != 2:
                    break
                length = struct.unpack(">H", length_data)[0]
                if marker and marker[0] in range(0xC0, 0xC4):
                    data = source.read(5)
                    if len(data) == 5:
                        height, width = struct.unpack(">HH", data[1:5])
                        return width, height
                    break
                source.seek(length - 2, 1)
    return None, None


def catalog(folder: Path) -> list[dict[str, object]]:
    rows = []
    for path in sorted(folder.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in MEDIA_EXTENSIONS:
            continue
        width, height = image_dimensions(path)
        rows.append({
            "path": path.relative_to(folder).as_posix(),
            "extension": path.suffix.lower(),
            "size_bytes": path.stat().st_size,
            "width": width or "",
            "height": height or "",
            "sha256": checksum(path),
        })
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", type=Path)
    parser.add_argument("--output", type=Path, default=Path("media_catalog.csv"))
    args = parser.parse_args()
    rows = catalog(args.folder)
    with args.output.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=["path", "extension", "size_bytes", "width", "height", "sha256"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Cataloged {len(rows)} files into {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
