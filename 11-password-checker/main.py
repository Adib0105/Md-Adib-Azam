"""Local password-strength checks. Passwords are never stored or transmitted."""

import argparse
import re


def check_password(password: str) -> dict:
    checks = {
        "12+ characters": len(password) >= 12,
        "uppercase letter": bool(re.search(r"[A-Z]", password)),
        "lowercase letter": bool(re.search(r"[a-z]", password)),
        "number": bool(re.search(r"\d", password)),
        "symbol": bool(re.search(r"[^A-Za-z0-9]", password)),
        "no long repetition": not bool(re.search(r"(.)\1{2,}", password)),
    }
    score = sum(checks.values())
    labels = {0: "Very weak", 1: "Very weak", 2: "Weak", 3: "Fair", 4: "Good", 5: "Strong", 6: "Strong"}
    return {
        "score": score,
        "maximum": len(checks),
        "rating": labels[score],
        "suggestions": [f"Add or improve: {name}" for name, passed in checks.items() if not passed],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Check password strength locally")
    parser.add_argument("password")
    args = parser.parse_args()
    result = check_password(args.password)
    print(f"{result['rating']} — {result['score']}/{result['maximum']}")
    for suggestion in result["suggestions"]:
        print("-", suggestion)


if __name__ == "__main__":
    main()
