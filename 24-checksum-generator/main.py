import argparse
import hashlib
from pathlib import Path


def sha256_file(path: Path, chunk_size: int = 65536) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest(folder: Path) -> list[tuple[str, str]]:
    return [(str(path.relative_to(folder)), sha256_file(path)) for path in sorted(folder.rglob("*")) if path.is_file()]


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate SHA-256 file checksums")
    parser.add_argument("path", type=Path)
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    if args.path.is_file():
        print(sha256_file(args.path), args.path)
        return
    rows = build_manifest(args.path)
    output = "\n".join(f"{checksum}  {name}" for name, checksum in rows)
    if args.manifest:
        args.manifest.write_text(output + "\n", encoding="utf-8")
        print(f"Saved {len(rows)} checksums to {args.manifest}")
    else:
        print(output)


if __name__ == "__main__":
    main()
