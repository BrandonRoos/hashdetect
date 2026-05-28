# Lessons Learned — building hashdetect

Notes on the errors I hit while building this project and what I took away
from each. Written as I go, for future reference.

## Git & GitHub

**Pushing to GitHub was blocked: `GH007: Your push would publish a private
email address`.**
GitHub was protecting my real email from ending up in public commit history.
Fix: set git to use GitHub's noreply email
(`git config --global user.email "ID+username@users.noreply.github.com"`), then
rewrite the existing commit with `git commit --amend --reset-author --no-edit`
and push again.
_Lesson: set the right git email **before** making commits on a new machine.
GitHub only checks the most recent commit, so older bad commits can slip
through if pushed in a batch._

**PowerShell wouldn't run the venv activation script: "running scripts is
disabled on this system."**
Windows blocks scripts by default. Fix:
`Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`.
_Lesson: this is a one-time, per-user Windows setting, not a per-project thing._

**OneDrive is a bad place for git repos.**
OneDrive constantly syncs the thousands of small files in `.git`, causing lock
conflicts and possible corruption. Moved projects out to
`C:\Users\me\projects` and used GitHub itself as the "sync across devices"
mechanism.
_Lesson: let git/GitHub handle versioning; don't layer another sync tool on top._

## Python

**`ModuleNotFoundError: No module named 'hashdetect'` when running
`python hashdetect/cli.py`.**
Running a file directly puts that file's folder first on the import path, so the
package couldn't see itself. Fix: run as a module instead —
`python -m hashdetect.cli` (or `python -m hashdetect`).
_Lesson: for any project where files import each other, use `python -m`, not
`python file.py`._

**`NameError: name 'HashSignaturue' is not defined`.**
A typo — `HashSignaturue` instead of `HashSignature`. Python doesn't catch this
until the line actually runs (no compile step like Java).
_Lesson: read tracebacks **bottom-up** — the last line is the real error. Watch
the VS Code PROBLEMS tab; it flags these before you even run the code._

**Ten errors in the PROBLEMS tab from one unclosed bracket.**
A single missing/misplaced `)` made everything after it unparseable, so the
editor reported a cascade of fake errors.
_Lesson: fix the **first** (topmost / earliest) error; the rest often vanish.
Use the editor's bracket-matching to find unclosed pairs._

**A SHA-256 hash was reported as "no match."**
The test string had an extra character (65 chars instead of 64). The tool was
right to reject it — the bug was in my input, not my code. Confirmed with
`python -c "print(len(s))"`.
_Lesson: when output is surprising, suspect the **input** before the code.
Most bugs are bad data, not bad logic._

## Tooling

**The `isort` extension kept crashing on startup.**
It was trying to load a tool that wasn't installed in the fresh venv. Harmless
noise; dismissed it.
_Lesson: not every red message is something I broke. Read it, decide if it
actually matters, move on._

## General takeaways

- Commit when something **works**, not when it's "done." Small, frequent commits
  with clear messages beat rare giant ones.
- `git status` is free and safe — run it constantly.
- The debug loop is always the same: error → read the message → fix → re-run.
- Modular structure (data / logic / interface in separate files) meant adding
  new features rarely touched unrelated code.
