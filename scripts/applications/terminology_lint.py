#!/usr/bin/env python3
"""Terminology Lint - Production Compliance

Checks staged changes for legacy terminology such as "well", "dipole", or
"gravity". Intended for use as a pre-commit hook to enforce the new
cartographic vocabulary outlined in the Discernus Terminology Strategy.
"""

import re
import subprocess
import sys
from pathlib import Path

FORBIDDEN_PATTERN = re.compile(r"well|dipole|gravity", re.IGNORECASE)


def get_staged_files() -> list[str]:
    """Return a list of staged files to check."""
    result = subprocess.run(
        [
            "git",
            "diff",
            "--cached",
            "--name-only",
            f"-G{FORBIDDEN_PATTERN.pattern}",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    return [f for f in result.stdout.splitlines() if f and Path(f).is_file()]


def find_matches(files: list[str]) -> list[tuple[str, int, str]]:
    """Scan the given files for forbidden terms."""
    matches = []
    for path in files:
        try:
            with open(path, "r", encoding="utf-8") as fh:
                for idx, line in enumerate(fh, start=1):
                    if FORBIDDEN_PATTERN.search(line):
                        matches.append((path, idx, line.rstrip()))
        except Exception:
            # Skip binary or unreadable files
            continue
    return matches


def main() -> int:
    files = get_staged_files()
    if not files:
        return 0

    matches = find_matches(files)
    if matches:
        for path, idx, text in matches:
            print(f"{path}:{idx}: {text}")
        print("❌ Forbidden terminology detected. See terminology strategy.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
