"""Command-line interface for hashdetect."""

import argparse
import json
import sys

from hashdetect.detector import detect


def main() -> int:
    """Entry point for the hashdetect CLI."""
    parser = argparse.ArgumentParser(
        prog="hashdetect",
        description="Identify hash types by length and pattern.",
    )
    parser.add_argument(
        "hash",
        help="The hash string to identify.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON instead of human-readable text.",
    )
    args = parser.parse_args()

    matches = detect(args.hash)

    if args.json:
        return _print_json(args.hash, matches)
    return _print_text(args.hash, matches)


def _print_json(hash_string: str, matches: list) -> int:
    """Print results as JSON. Always exit 0; absence of matches is empty list."""
    payload = {
        "input": hash_string,
        "matches": [m.to_dict() for m in matches],
    }
    print(json.dumps(payload, indent=2))
    return 0


def _print_text(hash_string: str, matches: list) -> int:
    """Print results as human-readable text. Exit 1 if no matches."""
    if not matches:
        print(f"No known hash type matched: {hash_string}")
        return 1

    print(f"Possible matches for {hash_string}:")
    for match in matches:
        sig = match.signature
        confidence_pct = round(match.confidence * 100)
        hashcat = f"hashcat {sig.hashcat_mode}" if sig.hashcat_mode is not None else "hashcat n/a"
        john = f"john {sig.john_format}" if sig.john_format is not None else "john n/a"
        print(
            f"  - {sig.name:<8} "
            f"(confidence {confidence_pct}%, "
            f"length {sig.length}, "
            f"{hashcat}, {john})"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
