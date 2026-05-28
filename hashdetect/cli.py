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
    for signature in matches:
        print(f"  - {signature.name} (length {signature.length})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
