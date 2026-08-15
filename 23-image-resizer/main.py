import argparse
from pathlib import Path

from PIL import Image, ImageOps


SUPPORTED = {".jpg", ".jpeg", ".png", ".webp"}


def resize_image(source: Path, destination: Path, size: tuple[int, int], allow_upscale: bool = False) -> tuple[int, int]:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as image:
        image = ImageOps.exif_transpose(image)
        target = size if allow_upscale else (min(size[0], image.width), min(size[1], image.height))
        image.thumbnail(target, Image.Resampling.LANCZOS)
        image.save(destination)
        return image.size


def batch_resize(source: Path, destination: Path, size: tuple[int, int]) -> int:
    files = [source] if source.is_file() else [path for path in source.iterdir() if path.suffix.lower() in SUPPORTED]
    for path in files:
        resize_image(path, destination / path.name, size)
    return len(files)


def main() -> None:
    parser = argparse.ArgumentParser(description="Batch-resize images")
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--width", type=int, default=1200)
    parser.add_argument("--height", type=int, default=1200)
    args = parser.parse_args()
    print(f"Resized {batch_resize(args.source, args.destination, (args.width, args.height))} image(s)")


if __name__ == "__main__":
    main()
