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
    john_format: str | None = None


SIGNATURES = [
    HashSignature(
        name="MD5",
        length=32,
        pattern=re.compile(r"^[a-fA-F0-9]{32}$"),
        prevalence=0.9,
        hashcat_mode=0,
        john_format="raw-md5",
    ),
    HashSignature(
        name="SHA-1",
        length=40,
        pattern=re.compile(r"^[a-fA-F0-9]{40}$"),
        prevalence=0.8,
        hashcat_mode=100,
        john_format="raw-sha1",
    ),
    HashSignature(
        name="SHA-224",
        length=56,
        pattern=re.compile(r"^[a-fA-F0-9]{56}$"),
        prevalence=0.1,
        hashcat_mode=1300,
        john_format="raw-sha224",
    ),
    HashSignature(
        name="SHA-256",
        length=64,
        pattern=re.compile(r"^[a-fA-F0-9]{64}$"),
        prevalence=0.7,
        hashcat_mode=1400,
        john_format="raw-sha256",
    ),
    HashSignature(
        name="SHA-384",
        length=96,
        pattern=re.compile(r"^[a-fA-F0-9]{96}$"),
        prevalence=0.6,
        hashcat_mode=10800,
        john_format="raw-sha384",
    ),
    HashSignature(
        name="SHA-512",
        length=128,
        pattern=re.compile(r"^[a-fA-F0-9]{128}$"),
        prevalence=0.5,
        hashcat_mode=1700,
        john_format="raw-sha512",
    ),
    HashSignature(
        name="bcrypt",
        length=60,
        pattern=re.compile(r"^\$2[abxy]\$\d{2}\$[./A-Za-z0-9]{53}$"),
        prevalence=0.5,
        hashcat_mode=3200,
        john_format="bcrypt",
    ),
    HashSignature(
        name="NTLM",
        length=32,
        pattern=re.compile(r"^[a-fA-F0-9]{32}$"),
        prevalence=0.45,
        hashcat_mode=1000,
        john_format="nt",
    ),
    HashSignature(
        name="MD4",
        length=32,
        pattern=re.compile(r"^[a-fA-F0-9]{32}$"),
        prevalence=0.15,
        hashcat_mode=900,
        john_format="raw-md4",
    ),
]
# hashcat - m 0 hashes.txt rockyou.txt        # mode 0 = MD5
# hashcat - m 100 hashes.txt rockyou.txt      # mode 100 = SHA-1
# hashcat - m 1400 hashes.txt rockyou.txt     # mode 1400 = SHA-256
# hashcat - m 3200 hashes.txt rockyou.txt     # mode 3200 = bcrypt

# john --format=raw-md5 hashes.txt
# think of kali and cyber security club we used this in class to crack hashes. john --format=raw-sha1 hashes.txt