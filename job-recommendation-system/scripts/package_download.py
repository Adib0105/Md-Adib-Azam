"""Export the committed JobMatch app at the ZIP root, without local runtime data."""

import argparse
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def git(*args, cwd=ROOT):
    return subprocess.check_output(
        ["git", "-C", str(cwd), *args], text=True, stderr=subprocess.PIPE
    ).strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", default="HEAD", help="Committed revision to export")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT.parent / "JobMatch-AI-ML-Fixed.zip",
        help="Destination ZIP path",
    )
    args = parser.parse_args()
    output = args.output.resolve()
    if output.suffix.lower() != ".zip":
        parser.error("The output filename must end in .zip.")
    try:
        repository = Path(git("rev-parse", "--show-toplevel")).resolve()
        commit = git(
            "rev-parse", "--verify", "--end-of-options", f"{args.ref}^{{commit}}"
        )
        project_path = ROOT.relative_to(repository).as_posix()
        tree = commit if project_path == "." else f"{commit}:{project_path}"
        app_path = "app.py" if project_path == "." else f"{project_path}/app.py"
        git("cat-file", "-e", f"{commit}:{app_path}")
        output.parent.mkdir(parents=True, exist_ok=True)
        git("archive", "--format=zip", f"--output={output}", tree, cwd=repository)
    except (OSError, subprocess.CalledProcessError, ValueError) as exc:
        detail = getattr(exc, "stderr", None) or str(exc)
        parser.exit(
            1, f"Packaging needs a Git checkout of JobMatch: {detail.strip()}\n"
        )
    with zipfile.ZipFile(output, "a", compression=zipfile.ZIP_DEFLATED) as archive:
        required = {
            "app.py",
            "requirements.txt",
            "start_windows.cmd",
            "setup_windows.cmd",
            "scripts/seed_database.py",
            "DOWNLOAD_RUN_GUIDE.txt",
        }
        missing = required - set(archive.namelist())
        if missing:
            parser.exit(
                1, f"Archive is missing app files: {', '.join(sorted(missing))}\n"
            )
        archive.writestr(
            "SOURCE_COMMIT.txt", f"Source commit: {commit}\nApp path: {project_path}\n"
        )
    print(f"Created {output} from {commit}")
    print("Extract All, then run start_windows.cmd from the extracted folder.")


if __name__ == "__main__":
    main()
