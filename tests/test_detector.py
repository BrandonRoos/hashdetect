"""Tests for the hash detection logic."""

from hashdetect.detector import detect, Match


# Known test vectors: real hashes of known inputs.
MD5_PASSWORD = "5f4dcc3b5aa765d61d8327deb882cf99"
SHA1_ABC = "a9993e364706816aba3e25717850c26c9cd0d89d"
SHA256_ABC = "ba7816bf8f01cfea414140de5dae2223b00361a3396177a9cb410ff61f20015a"
BCRYPT_SAMPLE = "$2b$12$EXRkfkdmXn2gzds2SSitu.MW9.gAVqa9eLS1//RYtYCmB1eLHg.5y"


def test_detect_returns_matches():
    """A valid MD5-shaped hash should return at least one match."""
    matches = detect(MD5_PASSWORD)
    assert len(matches) > 0


def test_md5_is_top_candidate():
    """For a 32-hex hash, MD5 should rank first (highest prevalence)."""
    matches = detect(MD5_PASSWORD)
    assert matches[0].signature.name == "MD5"


def test_sha1_detected():
    """A 40-hex hash should be detected as SHA-1."""
    matches = detect(SHA1_ABC)
    names = [m.signature.name for m in matches]
    assert "SHA-1" in names


def test_sha256_detected():
    """A 64-hex hash should be detected as SHA-256."""
    matches = detect(SHA256_ABC)
    names = [m.signature.name for m in matches]
    assert "SHA-256" in names


def test_bcrypt_detected():
    """A bcrypt hash should be detected as bcrypt."""
    matches = detect(BCRYPT_SAMPLE)
    assert matches[0].signature.name == "bcrypt"


def test_no_match_for_garbage():
    """Input that matches no signature should return an empty list."""
    matches = detect("this is definitely not a hash")
    assert matches == []


def test_confidences_sum_to_one():
    """When multiple signatures match, their confidences should sum to ~1.0."""
    matches = detect(MD5_PASSWORD)
    total = sum(m.confidence for m in matches)
    assert abs(total - 1.0) < 0.0001


def test_matches_sorted_by_confidence():
    """Matches should be returned in descending confidence order."""
    matches = detect(MD5_PASSWORD)
    confidences = [m.confidence for m in matches]
    assert confidences == sorted(confidences, reverse=True)


def test_whitespace_is_stripped():
    """Leading/trailing whitespace should not prevent detection."""
    matches = detect(f"  {MD5_PASSWORD}  ")
    assert len(matches) > 0
