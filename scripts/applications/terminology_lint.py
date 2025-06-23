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

# More precise patterns to avoid false positives
FORBIDDEN_PATTERNS = {
    'well': [
        # Technical usage patterns to flag (variable/class/function names with well)
        r'\bwell[_]+(name|id|definition|score|data|statistics|analysis|mapping)',
        r'\b[_]*well[_]*scores?\b',
        r'\b[_]*well[_]*data\b', 
        r'\b[_]*well[_]*definitions?\b',
        r'\b(narrative|gravity|moral|rhetorical)[_\s]+well\b',
        r'\b(create|define|generate)[_\s]+well\b',
        r'\bclass\s+\w*Well\b',
        r'\bdef\s+create_well\b',  # Only flag specific function patterns
        r'\bdef\s+\w*_well_\w*\b',  # Function names with well in middle
        # Variable assignments
        r'\b\w*well\w*\s*=',
        r'=\s*\w*well\w*\b',
    ],
    'dipole': [
        # Dipole is more specific, less likely to have false positives
        r'\bdipole\b',
    ],
    'gravity': [
        # Only flag "narrative gravity" contexts
        r'\bnarrative[_\s]+gravity\b',
        r'\bgravity[_\s]+(well|map|analysis|engine)',
        r'\bclass\s+\w*Gravity\b',
        r'\bdef\s+\w*gravity\w*\(',
    ]
}

# Patterns to exclude (legitimate English usage)
EXCLUSION_PATTERNS = [
    r'\bhow\s+well\b',         # "how well"
    r'\bas\s+well\s+as\b',     # "as well as"  
    r'\bworks?\s+well\b',      # "works well"
    r'\bvery\s+well\b',        # "very well"
    r'\bquite\s+well\b',       # "quite well"
    r'\bpretty\s+well\b',      # "pretty well"
    r'\bwell\s+with\b',        # "well with"
    r'\bwell\s+for\b',         # "well for"
    r'\bwell\s+in\b',          # "well in"
]

# Directories to exclude from linting
EXCLUDED_DIRS = {
    'deprecated/',
    'archive/',
    'docs_site/site/',
    '.git/',
    '__pycache__/',
    'venv/',
    'node_modules/',
}

# File patterns to exclude
EXCLUDED_FILES = {
    'CHANGELOG.md',
    'README.md',
    'HISTORY.md',  
}

def should_exclude_file(file_path: str) -> bool:
    """Check if file should be excluded from linting."""
    # Normalize path separators
    normalized_path = file_path.replace('\\', '/')
    
    # Check excluded directories
    for excluded_dir in EXCLUDED_DIRS:
        if normalized_path.startswith(excluded_dir) or f'/{excluded_dir}' in normalized_path:
            return True
    
    # Check excluded files
    file_name = Path(file_path).name
    if file_name in EXCLUDED_FILES:
        return True
        
    return False

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
            
            if current_file and not should_exclude_file(current_file):
                # Check against all forbidden patterns
                for term, patterns in FORBIDDEN_PATTERNS.items():
                    for pattern in patterns:
                        if re.search(pattern, line_content.lower()):
                            # Check if this is legitimate usage that should be excluded
                            if not has_legitimate_usage(line_content):
                                matches.append((current_file, line_number, line_content.rstrip(), term, pattern))
                            break  # Only report first match per line
            line_number += 1
        elif not line.startswith("-"):
            # This is a context line (unchanged)
            line_number += 1
    
    return matches

def has_legitimate_usage(line_content: str) -> bool:
    """Check if the line contains legitimate English usage of flagged terms."""
    line_lower = line_content.lower()
    for exclusion in EXCLUSION_PATTERNS:
        if re.search(exclusion, line_lower):
            return True
    return False

def main() -> int:
    matches = get_staged_changes()
    if matches:
        print("❌ Forbidden terminology detected in staged changes:")
        print("=" * 60)
        for path, line_num, text, term, pattern in matches:
            print(f"{path}:{line_num}: {text.strip()}")
            print(f"   ↳ Flagged '{term}' usage - See terminology strategy for alternatives")
            print()
        
        print("💡 To fix these issues:")
        print("   • Replace 'well' with 'coordinate' or 'anchor'")
        print("   • Replace 'dipole' with 'axis'") 
        print("   • Use 'Discernus Coordinate System' instead of 'narrative gravity'")
        print("   • See: branding/discernus_coordinates_renaming_guide.md")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
