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
