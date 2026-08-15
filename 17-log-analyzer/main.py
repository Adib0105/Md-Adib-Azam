import argparse
import re
from collections import Counter
from pathlib import Path


LOG_PATTERN = re.compile(r"^\[(?P<timestamp>[^]]+)]\s+(?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL)\s+(?P<message>.+)$")


def parse_line(line: str) -> dict | None:
    match = LOG_PATTERN.match(line.strip())
    return match.groupdict() if match else None


def analyze(lines: list[str]) -> dict:
    entries = [entry for line in lines if (entry := parse_line(line))]
    levels = Counter(entry["level"] for entry in entries)
    errors = Counter(entry["message"] for entry in entries if entry["level"] in {"ERROR", "CRITICAL"})
    return {
        "parsed": len(entries),
        "ignored": len(lines) - len(entries),
        "levels": dict(levels),
        "top_errors": errors.most_common(5),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize application logs")
    parser.add_argument("log_file", type=Path)
    args = parser.parse_args()
    report = analyze(args.log_file.read_text(encoding="utf-8").splitlines())
    print(f"Parsed: {report['parsed']} | Ignored: {report['ignored']}")
    print("Levels:", report["levels"])
    print("Top errors:", report["top_errors"])


if __name__ == "__main__":
    main()
