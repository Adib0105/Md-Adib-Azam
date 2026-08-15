"""Run every project analysis and report a concise pass/fail summary."""

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).parent
PROJECTS = sorted(path for path in ROOT.iterdir() if path.is_dir() and path.name[:2].isdigit())


def main() -> int:
    failures = []
    for project in PROJECTS:
        print(f"\n▶ {project.name}")
        result = subprocess.run([sys.executable, "analysis.py"], cwd=project)
        if result.returncode:
            failures.append(project.name)

    if failures:
        print("\nFailed:", ", ".join(failures))
        return 1

    print(f"\n✓ All {len(PROJECTS)} projects completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
