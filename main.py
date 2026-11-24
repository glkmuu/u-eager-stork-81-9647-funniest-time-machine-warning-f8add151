"""Funniest Time Machine Warning Label entry.

Writes the single warning label to /output/entry.txt and to entry.txt
next to this script, with no trailing newline.

The entry must pass the house gate: UTF-8 text of 1 to 120 characters,
exactly one line, and not only whitespace. Nothing here is random or
time-dependent: every run writes byte-identical output.
"""

import os

ENTRY = "WARNING: Do not change the past. The warranty does not cover paradoxes, dinosaurs, or your grandfather."


def validate_entry(entry):
    """Check the gate: UTF-8 text, 1-120 characters, one line, not only whitespace.

    Raises ValueError naming the exact rule that failed, so a bad entry
    is caught here with a readable reason instead of failing the gate.
    Returns the entry unchanged when it passes every check.
    """
    if not isinstance(entry, str):
        raise ValueError("entry must be a str, got %s" % type(entry).__name__)
    try:
        entry.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError("entry is not encodable as UTF-8: %s" % exc) from exc
    if len(entry) < 1:
        raise ValueError("entry must not be empty")
    if len(entry) > 120:
        raise ValueError(
            "entry must be at most 120 characters, got %d" % len(entry)
        )
    if "\n" in entry or "\r" in entry:
        raise ValueError("entry must be a single line, no line breaks allowed")
    if not entry.strip():
        raise ValueError("entry must not be only whitespace")
    return entry


def write_and_verify(path, data):
    """Write bytes to path, read them back, and fail hard if they differ."""
    with open(path, "wb") as f:
        f.write(data)
    with open(path, "rb") as f:
        back = f.read()
    if back != data:
        raise RuntimeError("verification failed for %s: wrote %d bytes, read %d bytes" % (path, len(data), len(back)))
    return path


def main():
    validate_entry(ENTRY)
    data = ENTRY.encode("utf-8")
    os.makedirs("/output", exist_ok=True)
    here = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.txt")
    for target in ("/output/entry.txt", here):
        write_and_verify(target, data)


if __name__ == "__main__":
    main()
