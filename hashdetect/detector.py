"""Hash detection logic with confidence scoring."""

from dataclasses import dataclass

from hashdetect.signatures import SIGNATURES, HashSignature


@dataclass
class Match:
    """A signature that matched the input, with its computed confidence."""
    signature: HashSignature
    confidence: float


def detect(hash_string: str) -> list[Match]:
    """Identify the hash type(s) of the input string with confidence scores.

    Args:
        hash_string: The candidate hash string to identify.

    Returns:
        A list of Match objects, sorted by confidence descending.
        Empty if nothing matched.
    """
    hash_string = hash_string.strip()

    matching_signatures = [
        sig for sig in SIGNATURES if sig.pattern.match(hash_string)
    ]

    if not matching_signatures:
        return []

    total_prevalence = sum(sig.prevalence for sig in matching_signatures)

    matches = [
        Match(signature=sig, confidence=sig.prevalence / total_prevalence)
        for sig in matching_signatures
    ]

    matches.sort(key=lambda m: m.confidence, reverse=True)

    return matches

    # for sig in SIGNATURES:
    #     if sig.pattern.match(hash_string):
    #         yield Match(signature=sig, confidence=sig.prevalence)
