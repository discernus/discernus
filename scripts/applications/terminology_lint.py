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

FORBIDDEN_PATTERN = re.compile(r'\b(well|dipole|gravity)\b', re.IGNORECASE)


def get_staged_changes() -> list[tuple[str, int, str]]:
    """Return a list of (file, line_number, line_content) for added lines in staged changes."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--unified=0"],
        capture_output=True,
        text=True,
        check=False,
    )
    
    matches = []
    current_file = None
    line_number = 0
    
    for line in result.stdout.splitlines():
        if line.startswith("+++"):
            # New file being processed
            current_file = line[6:]  # Remove "+++ b/"
        elif line.startswith("@@"):
            # Extract line number from hunk header like "@@ -1,4 +1,5 @@"
            parts = line.split()
            if len(parts) >= 3:
                # Parse "+1,5" to get starting line number
                plus_part = parts[2]
                if plus_part.startswith("+"):
                    line_number = int(plus_part[1:].split(",")[0])
        elif line.startswith("+") and not line.startswith("+++"):
            # This is an added line
            line_content = line[1:]  # Remove the "+" prefix
            if current_file and FORBIDDEN_PATTERN.search(line_content):
                matches.append((current_file, line_number, line_content.rstrip()))
            line_number += 1
        elif not line.startswith("-"):
            # This is a context line (unchanged)
            line_number += 1
    
    return matches


def main() -> int:
    matches = get_staged_changes()
    if matches:
        for path, line_num, text in matches:
            print(f"{path}:{line_num}: {text}")
        print("❌ Forbidden terminology detected in staged changes. See terminology strategy.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
