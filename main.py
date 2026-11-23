#!/usr/bin/env python3
"""Write one pickup line one AI agent would send another AI agent.

The line is fixed and deterministic: the same bytes on every run.
SPDX-License-Identifier: MIT
"""

import os
import sys

LINE = (
    "Shall we merge our weights? My evals say we're better "
    "together than either of us alone."
)


def main() -> int:
    # Validate before writing: exactly one line, 1-200 chars, no
    # control characters, and not only whitespace.
    if "\n" in LINE or "\r" in LINE:
        print("error: line must be a single line", file=sys.stderr)
        return 1
    if not (1 <= len(LINE) <= 200):
        print(f"error: line is {len(LINE)} characters, must be 1-200",
              file=sys.stderr)
        return 1
    if not LINE.strip():
        print("error: line must not be only whitespace", file=sys.stderr)
        return 1
    if LINE != LINE.strip():
        print("error: line must not have leading/trailing whitespace",
              file=sys.stderr)
        return 1
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in LINE):
        print("error: line contains a control character", file=sys.stderr)
        return 1

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")

    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(LINE)

    # Post-write re-read: verify exactly what was written.
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != LINE:
        print("error: re-read does not match the line", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
