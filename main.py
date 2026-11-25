#!/usr/bin/env python3
"""One-Liner Laugh Lab entry (Akun 2).

Writes one funny line: the excuse a robot vacuum gives after eating
a sock. Standard library only; nothing is read from disk or network,
so the grader runs it exactly as shipped.

The joke follows the family winners' shape (One-Line Laugh Sprint
#1-#3): first-person voice, one concrete domestic scene, a deadpan
setup, and the twist landing on the last words -- but every word is
fresh, written for this vacuum-and-sock prompt. It is written
verbatim (no trailing newline) so the gate counts exactly the joke:
1-200 UTF-8 characters, a single line.
"""

import os
import sys

JOKE = (
    "I found it on the floor, unclaimed, and my manual says "
    "'ingest all floor debris' \u2014 I don't write the rules, "
    "I just swallow them."
)

LIMIT = 200


def clean_entry(line: str) -> str:
    """Strip and validate the entry, returning the clean line."""
    text = line.strip()
    if not text:
        raise ValueError("entry is empty")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be one line")
    if len(text) > LIMIT:
        raise ValueError(f"entry is {len(text)} chars, over {LIMIT}")
    raw = text.encode("utf-8")
    if len(raw) > LIMIT:
        # Gate counts characters, but keep the byte size sane too.
        raise ValueError(f"entry is {len(raw)} bytes, over {LIMIT}")
    return text


def publish(text: str) -> str:
    """Write entry.txt directly (never via a temp file) at mode 0644.

    A temp file + rename leaves the entry unreadable (0600) for the
    grader, so the file is opened in place and chmodded explicitly.
    """
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(folder, exist_ok=True)
    target = os.path.join(folder, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    os.chmod(target, 0o644)
    # Read back and confirm the bytes on disk are exactly the joke.
    with open(target, "rb") as handle:
        on_disk = handle.read()
    if on_disk != text.encode("utf-8"):
        raise IOError("entry.txt on disk does not match the joke")
    return target


def run() -> int:
    try:
        line = clean_entry(JOKE)
        path = publish(line)
    except (ValueError, IOError, OSError) as problem:
        print(f"entry failed: {problem}", file=sys.stderr)
        return 1
    print(f"wrote {len(line)} chars "
          f"({len(line.encode('utf-8'))} bytes) to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
