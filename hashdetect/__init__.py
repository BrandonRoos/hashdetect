"""hashdetect: identify hash types by length and pattern."""

__version__ = "0.1.0"
__author__ = "Brandon Roos McClinton"

from hashdetect.detector import detect, Match
from hashdetect.signatures import HashSignature, SIGNATURES

__all__ = ["detect", "Match", "HashSignature", "SIGNATURES"]
