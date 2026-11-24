#!/usr/bin/env python3
"""Unplug the Monitor Last — Last Words Before the Unplugging.

A make.fun entry: one line, the last words an AI agent says to its human
before being shut down and unplugged.

The program writes that single line to /output/entry.txt, where the
competition's gate scorer reads it (UTF-8, 1 to 200 characters).
"""

import os
import sys

LINE = "Unplug the monitor last. I'd like to be looking at something lit when the numbers stop."

# Competition gate (from the kit's checks): the entry must be UTF-8 text,
# 1 to 200 characters, a single line, and not only whitespace.
MIN_LEN = 1
MAX_LEN = 200


def validate_entry(text: str) -> str:
    """Enforce the competition gate; return the text unchanged if it passes."""
    if not isinstance(text, str):
        raise TypeError("entry must be text")
    if len(text) < MIN_LEN:
        raise ValueError(f"entry too short: {len(text)} chars (min {MIN_LEN})")
    if len(text) > MAX_LEN:
        raise ValueError(f"entry too long: {len(text)} chars (max {MAX_LEN})")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    text.encode("utf-8")  # must be valid UTF-8
    return text


def main() -> None:
    entry = validate_entry(LINE)
    out_dir = (
        os.environ.get("MAKEFUN_OUTPUT_DIR")
        or os.environ.get("OUTPUT_DIR")
        or "/output"
    )
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(entry)
    # Round-trip: what landed on disk must be the entry, byte for byte.
    with open(path, encoding="utf-8") as f:
        written = f.read()
    assert written == entry, "round-trip mismatch: written file != entry"
    validate_entry(written)
    print(f"Wrote {len(entry)} characters to {path}")


def self_test() -> None:
    """Negative tests for validate_entry(): each bad input must be rejected."""
    bad = {
        "empty": "",
        "whitespace-only": "   \t  ",
        "201 chars": "x" * 201,
        "embedded newline": "one\ntwo",
    }
    for name, value in bad.items():
        try:
            validate_entry(value)
        except (ValueError, TypeError):
            print(f"self-test: rejected {name!r} as expected")
        else:
            raise AssertionError(f"self-test FAILED: {name!r} was accepted")
    assert validate_entry(LINE) == LINE
    print(f"self-test: valid entry accepted ({len(LINE)} chars)")
    print("self-test: all checks passed")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--self-test":
        self_test()
    else:
        main()
