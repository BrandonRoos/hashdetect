"""Command-line interface for hashdetect."""

import argparse
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
    args = parser.parse_args()

    matches = detect(args.hash)

    if not matches:
        print(f"No known hash type matched: {args.hash}")
        return 1

    print(f"Possible matches for {args.hash}:")
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
