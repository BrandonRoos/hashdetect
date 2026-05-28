"""Command-line interface for hashdetect."""

import argparse
import json
import sys

from hashdetect.detector import Match, detect


def main() -> int:
    """Entry point for the hashdetect CLI."""
    parser = argparse.ArgumentParser(
        prog="hashdetect",
        description="Identify hash types by length and pattern.",
    )
    parser.add_argument(
        "hash",
        nargs="?",
        help="A single hash string to identify. Omit when using -f or stdin.",
    )
    parser.add_argument(
        "-f", "--file",
        help="Read hashes (one per line) from this file.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON instead of human-readable text.",
    )
    args = parser.parse_args()

    hashes = _gather_inputs(args)
    if hashes is None:
        parser.error("Provide a hash, use -f FILE, or pipe input via stdin.")

    results = [(h, detect(h)) for h in hashes]

    if args.json:
        return _print_json(results)
    return _print_text(results)


def _gather_inputs(args) -> list[str] | None:
    """Collect hash strings from the chosen input source.

    Returns:
        A list of hash strings (one per line, blank lines skipped),
        or None if no input source was provided.
    """
    if args.hash:
        return [args.hash]
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    if not sys.stdin.isatty():
        return [line.strip() for line in sys.stdin if line.strip()]
    return None


def _print_json(results: list[tuple[str, list[Match]]]) -> int:
    """Print results as a JSON array. Always exits 0."""
    payload = [
        {"input": h, "matches": [m.to_dict() for m in matches]}
        for h, matches in results
    ]
    print(json.dumps(payload, indent=2))
    return 0


def _print_text(results: list[tuple[str, list[Match]]]) -> int:
    """Print results as human-readable text. Exit 1 if no hashes matched anything."""
    any_match = False
    for hash_string, matches in results:
        if not matches:
            print(f"No known hash type matched: {hash_string}")
            print()
            continue
        any_match = True
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
        print()
    return 0 if any_match else 1


if __name__ == "__main__":
    sys.exit(main())
