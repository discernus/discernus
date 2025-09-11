#!/usr/bin/env python3
"""
Script to add GPL v3 license headers to Python source files.

This script adds the standard GPL v3 license header to all Python files
in the discernus package that don't already have it.

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

import os
import re
from pathlib import Path

# GPL v3 license header template
LICENSE_HEADER = '''Copyright (C) 2025  Discernus Team

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.'''

def has_license_header(content):
    """Check if the file already has a GPL license header."""
    return "GNU General Public License" in content and "Copyright (C) 2025" in content

def add_license_to_file(file_path):
    """Add GPL v3 license header to a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip if already has license header
        if has_license_header(content):
            print(f"✓ {file_path} already has license header")
            return False
        
        # Find the end of the docstring or shebang
        lines = content.split('\n')
        insert_line = 0
        
        # Skip shebang if present
        if lines[0].startswith('#!'):
            insert_line = 1
        
        # Find end of docstring
        in_docstring = False
        docstring_quotes = None
        
        for i, line in enumerate(lines[insert_line:], insert_line):
            stripped = line.strip()
            
            if not in_docstring:
                # Look for start of docstring
                if stripped.startswith('"""') or stripped.startswith("'''"):
                    in_docstring = True
                    docstring_quotes = '"""' if stripped.startswith('"""') else "'''"
                    # Check if docstring ends on same line
                    if stripped.count(docstring_quotes) >= 2:
                        insert_line = i + 1
                        break
                elif stripped and not stripped.startswith('#'):
                    # No docstring, insert after shebang or at beginning
                    insert_line = i
                    break
            else:
                # Look for end of docstring
                if docstring_quotes in line:
                    insert_line = i + 1
                    break
        
        # Insert license header
        license_lines = LICENSE_HEADER.split('\n')
        new_lines = lines[:insert_line] + [''] + license_lines + [''] + lines[insert_line:]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        print(f"✓ Added license header to {file_path}")
        return True
        
    except Exception as e:
        print(f"✗ Error processing {file_path}: {e}")
        return False

def main():
    """Add license headers to all Python files in the discernus package."""
    discernus_dir = Path("discernus")
    
    if not discernus_dir.exists():
        print("Error: discernus directory not found")
        return
    
    python_files = list(discernus_dir.rglob("*.py"))
    
    print(f"Found {len(python_files)} Python files")
    
    updated_count = 0
    for file_path in python_files:
        if add_license_to_file(file_path):
            updated_count += 1
    
    print(f"\nUpdated {updated_count} files with license headers")

if __name__ == "__main__":
    main()
