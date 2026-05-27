"""Hash signature definitions for hashdetect."""

from dataclasses import dataclass
import re


@dataclass
class HashSignature:
    """Describes one hash type we know how to detect."""
    name: str
    length: int
    pattern: re.Pattern
    prevalence: float
    hashcat_mode: int | None = None


SIGNATURES = [
    HashSignature(
        name="MD5",
        length=32,
        pattern=re.compile(r"^[a-fA-F0-9]{32}$"),
        prevalence=0.9,
        hashcat_mode=0,
    ),
]
