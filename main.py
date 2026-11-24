#!/usr/bin/env python3
"""Funniest Time Machine Warning Label -- make.fun entry program.

Reads the single warning label from entry.txt next to this script,
validates it against the competition gate, and writes it byte-for-byte
to $MAKEFUN_OUTPUT_DIR/entry.txt.

Gate (RULES.txt): output must be UTF-8 text of 1 to 120 characters,
not only white space.
"""

import os
import sys

MAX_CHARS = 120


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.txt")

    with open(src, "rb") as fh:
        raw = fh.read()
    text = raw.decode("utf-8")  # strict: raises on invalid UTF-8

    # The entry is one warning label: a single line, no embedded newline.
    if "\n" in text.rstrip("\n") or "\r" in text:
        print("gate: entry must be a single line", file=sys.stderr)
        return 1
    # A single trailing newline in the source file is not part of the label.
    text = text.rstrip("\n")
    if text.encode("utf-8") != raw.rstrip(b"\n"):
        print("gate: entry did not round-trip as UTF-8", file=sys.stderr)
        return 1

    # Gate: 1 to 120 characters, not only white space.
    if not (1 <= len(text) <= MAX_CHARS):
        print(f"gate: entry is {len(text)} chars, must be 1..{MAX_CHARS}",
              file=sys.stderr)
        return 1
    if not text.strip():
        print("gate: entry is only white space", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.txt")
    with open(dst, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)

    print(f"wrote {len(text)} chars to {dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
