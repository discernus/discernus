#!/usr/bin/env python3
"""
Add GPL v3 License Headers to Python Files

This script adds GPL v3 license headers to all Python files in the tools repository.
"""

import os
import re
from pathlib import Path

GPL_HEADER = '''#!/usr/bin/env python3
"""
{description}

Copyright (C) 2025  Discernus Team

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

'''

def extract_description(content):
    """Extract description from existing docstring or create a default one."""
    # Look for existing docstring
    docstring_match = re.search(r'"""([^"]+)"""', content, re.DOTALL)
    if docstring_match:
        desc = docstring_match.group(1).strip()
        # Take first line or first sentence
        first_line = desc.split('\n')[0].strip()
        if first_line:
            return first_line
    
    # Default description
    return "Discernus Development Tool"

def has_license_header(content):
    """Check if file already has a GPL license header."""
    return "GNU General Public License" in content and "Copyright" in content

def add_license_header(file_path):
    """Add GPL v3 license header to a Python file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if has_license_header(content):
        print(f"Skipping {file_path} - already has license header")
        return False
    
    # Extract description
    description = extract_description(content)
    
    # Remove existing shebang and docstring if present
    content = re.sub(r'^#!/usr/bin/env python3\s*\n', '', content)
    content = re.sub(r'^"""[^"]*"""\s*\n', '', content, flags=re.DOTALL)
    
    # Add new header
    new_content = GPL_HEADER.format(description=description) + content
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Added license header to {file_path}")
    return True

def main():
    """Add license headers to all Python files."""
    updated_count = 0
    
    # Find all Python files
    for py_file in Path('.').rglob('*.py'):
        # Skip this script itself
        if py_file.name == 'add_license_headers.py':
            continue
            
        if add_license_header(py_file):
            updated_count += 1
    
    print(f"\nUpdated {updated_count} files with GPL v3 license headers")

if __name__ == "__main__":
    main()
