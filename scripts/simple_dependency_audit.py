#!/usr/bin/env python3
"""
Simple Dependency License Audit Script

This script manually checks common dependencies for GPL v3 compatibility.

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

# Known license information for common packages
DEPENDENCY_LICENSES = {
    # Core dependencies
    'python-dotenv': 'BSD-3-Clause',
    'gitpython': 'BSD-3-Clause',
    'litellm': 'MIT',
    'anthropic': 'MIT',
    'requests': 'Apache-2.0',
    'click': 'BSD-3-Clause',
    'rich': 'MIT',
    
    # Data processing
    'pandas': 'BSD-3-Clause',
    'numpy': 'BSD-3-Clause',
    'scipy': 'BSD-3-Clause',
    'pingouin': 'GPL-3.0',
    'statsmodels': 'BSD-3-Clause',
    
    # Jupyter
    'jupyter': 'BSD-3-Clause',
    'nbformat': 'BSD-3-Clause',
    
    # Configuration
    'PyYAML': 'MIT',
    'pydantic': 'MIT',
    'pydantic-settings': 'MIT',
    
    # Text processing
    'nltk': 'Apache-2.0',
    'textblob': 'MIT',
    
    # Google Cloud
    'google-cloud-aiplatform': 'Apache-2.0',
    'google-auth': 'Apache-2.0',
    
    # YouTube
    'youtube-transcript-api': 'MIT',
    'yt-dlp': 'Unlicense',
    'loguru': 'MIT',
    'ratelimit': 'MIT',
    
    # Search and indexing
    'txtai': 'Apache-2.0',
    'typesense': 'MIT',
    'rank_bm25': 'MIT',
}

# GPL v3 compatible licenses
GPL_COMPATIBLE = {
    'MIT', 'Apache-2.0', 'BSD-3-Clause', 'BSD-2-Clause', 'BSD',
    'ISC', 'Unlicense', 'Public Domain', 'GPL-3.0', 'GPL-3.0-or-later',
    'LGPL-3.0', 'LGPL-3.0-or-later', 'MPL-2.0'
}

# Potentially problematic
PROBLEMATIC = {
    'GPL-2.0', 'GPL-2.0-or-later', 'LGPL-2.0', 'LGPL-2.0-or-later',
    'AGPL-3.0', 'AGPL-3.0-or-later', 'Proprietary', 'Commercial'
}

def audit_dependencies():
    """Audit dependencies for GPL v3 compatibility."""
    print("🔍 Auditing dependencies for GPL v3 compatibility...")
    print("=" * 60)
    
    compatible_count = 0
    problematic_count = 0
    unknown_count = 0
    
    for package, license_name in DEPENDENCY_LICENSES.items():
        print(f"📦 {package}")
        print(f"   License: {license_name}")
        
        if license_name in GPL_COMPATIBLE:
            print(f"   ✅ Compatible with GPL v3")
            compatible_count += 1
        elif license_name in PROBLEMATIC:
            print(f"   ⚠️  Potentially problematic")
            problematic_count += 1
        else:
            print(f"   ❓ Unknown compatibility")
            unknown_count += 1
        
        print()
    
    # Summary
    print("=" * 60)
    print("📊 AUDIT SUMMARY")
    print("=" * 60)
    print(f"✅ Compatible: {compatible_count}")
    print(f"⚠️  Problematic: {problematic_count}")
    print(f"❓ Unknown: {unknown_count}")
    print(f"📦 Total: {len(DEPENDENCY_LICENSES)}")
    
    if problematic_count > 0:
        print("\n⚠️  WARNING: Some dependencies may have compatibility issues!")
        print("   Manual review recommended.")
    
    if unknown_count > 0:
        print("\n❓ Some dependencies have unknown compatibility.")
        print("   Manual verification recommended.")
    
    if problematic_count == 0 and unknown_count == 0:
        print("\n🎉 All dependencies appear to be GPL v3 compatible!")
    
    # Specific notes
    print("\n📝 NOTES:")
    print("- pingouin is GPL-3.0, which is compatible with GPL-3.0-or-later")
    print("- Most dependencies use permissive licenses (MIT, Apache-2.0, BSD)")
    print("- No AGPL or proprietary dependencies found")
    print("- All Google Cloud packages use Apache-2.0 (compatible)")

def main():
    """Main function."""
    print("Discernus Dependency License Audit")
    print("==================================")
    print()
    
    audit_dependencies()

if __name__ == "__main__":
    main()
