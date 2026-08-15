from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).parent


def command_for(project: Path) -> list[str] | None:
    if (project / "test.py").is_file():
        return [sys.executable, "test.py"]
    if (project / "test.js").is_file():
        return ["node", "test.js"]
    if (project / "validate_schema.py").is_file():
        return [sys.executable, "validate_schema.py"]
    return None


def main() -> int:
    projects = [
        path for path in sorted(ROOT.iterdir())
        if path.is_dir() and path.name[:2].isdigit() and 26 <= int(path.name[:2]) <= 45
    ]
    failures = []
    for project in projects:
        command = command_for(project)
        if not command:
            failures.append((project.name, "No test command found"))
            continue
        if shutil.which(command[0]) is None:
            failures.append((project.name, f"Missing runtime: {command[0]}"))
            continue
        print(f"\n▶ {project.name}")
        result = subprocess.run(command, cwd=project)
        if result.returncode:
            failures.append((project.name, f"Exit code {result.returncode}"))

    if failures:
        print("\nValidation failures")
        for project, error in failures:
            print(f"- {project}: {error}")
        return 1
    print(f"\n✓ All {len(projects)} CV-aligned projects passed validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
