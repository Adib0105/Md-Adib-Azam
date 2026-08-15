import argparse
import shutil
from pathlib import Path


CATEGORIES = {
    "Images": {".png", ".jpg", ".jpeg", ".gif", ".webp"},
    "Documents": {".pdf", ".docx", ".txt", ".xlsx", ".csv"},
    "Audio": {".mp3", ".wav", ".m4a"},
    "Video": {".mp4", ".mov", ".mkv"},
    "Archives": {".zip", ".rar", ".7z"},
}


def category_for(path: Path) -> str:
    suffix = path.suffix.lower()
    return next((name for name, endings in CATEGORIES.items() if suffix in endings), "Other")


def plan_moves(folder: Path) -> list[tuple[Path, Path]]:
    return [(item, folder / category_for(item) / item.name) for item in folder.iterdir() if item.is_file()]


def organize(folder: Path, apply: bool = False) -> list[tuple[Path, Path]]:
    moves = plan_moves(folder)
    if apply:
        for source, destination in moves:
            destination.parent.mkdir(exist_ok=True)
            shutil.move(str(source), str(destination))
    return moves


def main() -> None:
    parser = argparse.ArgumentParser(description="Preview or organize files by type")
    parser.add_argument("folder", type=Path)
    parser.add_argument("--apply", action="store_true", help="Perform the moves")
    args = parser.parse_args()
    for source, destination in organize(args.folder, args.apply):
        print(f"{source.name} -> {destination.parent.name}/")
    print("Changes applied." if args.apply else "Preview only; use --apply to move files.")


if __name__ == "__main__":
    main()
