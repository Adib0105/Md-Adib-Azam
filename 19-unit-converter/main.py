import argparse


LINEAR_TO_BASE = {
    "m": ("length", 1.0), "km": ("length", 1000.0), "mi": ("length", 1609.344), "ft": ("length", 0.3048),
    "kg": ("weight", 1.0), "g": ("weight", 0.001), "lb": ("weight", 0.45359237),
}


def convert(value: float, source: str, target: str) -> float:
    source, target = source.lower(), target.lower()
    if source in {"c", "f", "k"} or target in {"c", "f", "k"}:
        if source not in {"c", "f", "k"} or target not in {"c", "f", "k"}:
            raise ValueError("Cannot mix temperature and linear units")
        celsius = value if source == "c" else (value - 32) * 5 / 9 if source == "f" else value - 273.15
        return celsius if target == "c" else celsius * 9 / 5 + 32 if target == "f" else celsius + 273.15
    if source not in LINEAR_TO_BASE or target not in LINEAR_TO_BASE:
        raise ValueError("Unsupported unit")
    source_kind, source_factor = LINEAR_TO_BASE[source]
    target_kind, target_factor = LINEAR_TO_BASE[target]
    if source_kind != target_kind:
        raise ValueError("Units belong to different categories")
    return value * source_factor / target_factor


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert common units")
    parser.add_argument("value", type=float)
    parser.add_argument("source")
    parser.add_argument("target")
    args = parser.parse_args()
    print(f"{convert(args.value, args.source, args.target):.4f} {args.target}")


if __name__ == "__main__":
    main()
