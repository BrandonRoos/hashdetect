# hashdetect

A command-line tool that identifies common hash types by their length and
structure, ranks the candidates by confidence, and can export results as JSON.

Given an unknown hash, `hashdetect` tells you what it's most likely to be —
and, because many hash types share the same shape, it shows *all* plausible
matches ranked by how common each type is in the wild. It also prints the
[hashcat](https://hashcat.net/hashcat/) mode and
[John the Ripper](https://www.openwall.com/john/) format for each match, so you
can move straight from identification to cracking workflows.

## Features

- Detects 9 common hash types: MD5, SHA-1, SHA-224, SHA-256, SHA-384, SHA-512,
  NTLM, MD4, and bcrypt.
- Ranks ambiguous matches by confidence (e.g. a 32-character hex string could
  be MD5, NTLM, or MD4 — all three are shown, highest-likelihood first).
- Human-readable output by default; machine-readable JSON with `--json`.
- Accepts a single hash, a file of hashes, or piped input from stdin.
- Prints hashcat mode and John the Ripper format for each match.
- Proper exit codes for use in shell scripts.

## Installation

Requires Python 3.10 or newer.

```bash
# Clone the repository
git clone https://github.com/BrandonRoos/hashdetect.git
cd hashdetect

# Create and activate a virtual environment
python -m venv .venv
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate

# Install dependencies (only needed to run the tests)
pip install -r requirements.txt
```

The tool itself uses only the Python standard library, so no dependencies are
required just to run it.

## Usage

### Identify a single hash

```bash
python -m hashdetect 5f4dcc3b5aa765d61d8327deb882cf99
```

```
Possible matches for 5f4dcc3b5aa765d61d8327deb882cf99:
  - MD5      (confidence 60%, length 32, hashcat 0, john raw-md5)
  - NTLM     (confidence 30%, length 32, hashcat 1000, john nt)
  - MD4      (confidence 10%, length 32, hashcat 900, john raw-md4)
```
### Read hashes from a file

One hash per line:

```bash
python -m hashdetect -f hashes.txt
```

### Read from stdin (pipe)

```bash
# macOS / Linux
cat hashes.txt | python -m hashdetect

# Windows PowerShell
type hashes.txt | python -m hashdetect
```

### JSON output

Add `--json` to any of the above for structured output:

```bash
python -m hashdetect 5f4dcc3b5aa765d61d8327deb882cf99 --json
```

```json
[
  {
    "input": "5f4dcc3b5aa765d61d8327deb882cf99",
    "matches": [
      { "name": "MD5",  "confidence": 0.6, "length": 32, "hashcat_mode": 0,    "john_format": "raw-md5" },
      { "name": "NTLM", "confidence": 0.3, "length": 32, "hashcat_mode": 1000, "john_format": "nt" },
      { "name": "MD4",  "confidence": 0.1, "length": 32, "hashcat_mode": 900,  "john_format": "raw-md4" }
    ]
  }
]
```

### Help

```bash
python -m hashdetect --help
```

## How it works

Detection happens in two ways:

1. **Structural matching.** Hashes with a distinctive shape — like bcrypt's
   `$2b$12$...` format — are matched by a regular expression that captures their
   exact structure. These matches are unambiguous.

2. **Length and character-set matching.** Most raw hashes are just hex strings
   of a fixed length. A 64-character hex string, for example, could be SHA-256,
   but also SHA3-256, BLAKE2s, and others. `hashdetect` returns every signature
   that fits and ranks them.

Confidence is computed from a *prevalence* score assigned to each hash type
(how often it appears in practice). Each match's confidence is its prevalence
divided by the total prevalence of all matching types, so the scores for a given
input always sum to 100%.

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | At least one match found (or JSON mode, which always exits 0) |
| 1 | No known hash type matched the input (text mode) |
| 2 | No input provided (no hash, no `-f`, no piped stdin) |

## Limitations

`hashdetect` identifies hashes by **shape, not content**. It cannot verify that
a string is genuinely a hash of a given type — only that it *could* be, based on
length and pattern. A 32-character hex string is reported as a possible MD5
because it has the right form, not because the tool has confirmed it was produced
by MD5. Treat the output as a ranked set of hypotheses, not a definitive answer.

## Running the tests

```bash
pytest
```

## Disclaimer

This tool is intended for legitimate security work — penetration testing,
forensics, CTFs, and education — on systems and data you own or are authorized
to test. You are responsible for complying with all applicable laws.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE)
file for details.
