"""Hash detection logic."""

from hashdetect.signatures import SIGNATURES, HashSignature


def detect(hash_string: str) -> list[HashSignature]:
    """Return all signatures whose pattern matches the input string.

    Args:
        hash_string: The candidate hash string to identify.

    Returns:
        A list of HashSignature objects that match. Empty list if no match.
    """
    hash_string = hash_string.strip()
    matches = []
    for signature in SIGNATURES:
        if signature.pattern.match(hash_string):
            matches.append(signature)
    return matches
