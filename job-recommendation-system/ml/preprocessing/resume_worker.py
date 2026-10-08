"""Private worker protocol: bounded bytes in, bounded JSON out."""

import json
import sys


def main():
    try:
        import resource

        resource.setrlimit(resource.RLIMIT_CPU, (8, 8))
        resource.setrlimit(resource.RLIMIT_AS, (768 * 1024 * 1024, 768 * 1024 * 1024))
    except (ImportError, ValueError, OSError):
        pass  # Windows still has the parent timeout and document expansion bounds.
    from models.resume_parser import parse_resume, ResumeError, MAX_FILE_BYTES

    try:
        result = parse_resume(sys.argv[1], sys.stdin.buffer.read(MAX_FILE_BYTES + 1))
        from ml.preprocessing.resume_intelligence import analyze_resume

        result["intelligence"] = analyze_resume(result["text"], result)
    except ResumeError as error:
        result = {"error": str(error)}
    encoded = json.dumps(result, ensure_ascii=True)
    if len(encoded) > 256 * 1024:
        encoded = json.dumps(
            {"error": "Extracted resume exceeds the safe output limit."}
        )
    print(encoded)


if __name__ == "__main__":
    main()
