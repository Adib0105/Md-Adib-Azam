"""Run the automated tests for projects 11–25."""

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).parent
PROJECTS = [
    path
    for path in sorted(ROOT.iterdir())
    if path.is_dir()
    and path.name[:2].isdigit()
    and 11 <= int(path.name[:2]) <= 25
    and (path / "test_main.py").is_file()
]


def main() -> int:
    failures = []
    for project in PROJECTS:
        print(f"\n▶ {project.name}")
        result = subprocess.run([sys.executable, "test_main.py", "-v"], cwd=project)
        if result.returncode:
            failures.append(project.name)
    if failures:
        print("\nFailed:", ", ".join(failures))
        return 1
    print(f"\n✓ All {len(PROJECTS)} Python projects passed their tests.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
