#!/usr/bin/env python3
"""
Dependency License Audit Script

This script audits all dependencies in pyproject.toml for GPL v3 compatibility.

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

import json
import subprocess
import sys
from pathlib import Path

# GPL v3 compatible licenses
GPL_COMPATIBLE_LICENSES = {
    'MIT',
    'Apache-2.0',
    'Apache Software License',
    'BSD',
    'BSD-3-Clause',
    'BSD-2-Clause',
    'ISC',
    'Python Software Foundation License',
    'PSF',
    'Public Domain',
    'Unlicense',
    'CC0',
    'GPL-3.0',
    'GPL-3.0-or-later',
    'LGPL-3.0',
    'LGPL-3.0-or-later',
    'MPL-2.0',
    'Mozilla Public License 2.0',
}

# Potentially problematic licenses (need manual review)
PROBLEMATIC_LICENSES = {
    'GPL-2.0',
    'GPL-2.0-or-later',
    'LGPL-2.0',
    'LGPL-2.0-or-later',
    'AGPL-3.0',
    'AGPL-3.0-or-later',
    'Proprietary',
    'Commercial',
    'Unknown',
}

def get_package_license(package_name):
    """Get the license for a package using pip-licenses."""
    try:
        result = subprocess.run(
            ['pip-licenses', '--format=json', '--with-urls', '--with-description'],
            capture_output=True,
            text=True,
            check=True
        )
        
        packages = json.loads(result.stdout)
        
        for pkg in packages:
            if pkg['Name'].lower() == package_name.lower():
                return {
                    'license': pkg.get('License', 'Unknown'),
                    'url': pkg.get('URL', ''),
                    'description': pkg.get('Description', '')
                }
        
        return {'license': 'Unknown', 'url': '', 'description': ''}
        
    except (subprocess.CalledProcessError, json.JSONDecodeError, FileNotFoundError):
        return {'license': 'Unknown', 'url': '', 'description': ''}

def audit_dependencies():
    """Audit all dependencies for GPL v3 compatibility."""
    print("🔍 Auditing dependencies for GPL v3 compatibility...")
    print("=" * 60)
    
    # Read pyproject.toml
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        print("❌ pyproject.toml not found")
        return
    
    # Parse dependencies from pyproject.toml
    dependencies = []
    
    with open(pyproject_path, 'r') as f:
        content = f.read()
        
        # Extract dependencies from the file
        in_dependencies = False
        for line in content.split('\n'):
            line = line.strip()
            
            if line.startswith('dependencies = ['):
                in_dependencies = True
                continue
            elif in_dependencies and line.startswith(']'):
                break
            elif in_dependencies and line.startswith('"'):
                # Extract package name (remove version constraints)
                package_line = line.strip('",')
                if '>=' in package_line:
                    package_name = package_line.split('>=')[0].strip('"')
                elif '==' in package_line:
                    package_name = package_line.split('==')[0].strip('"')
                elif '~=' in package_line:
                    package_name = package_line.split('~=')[0].strip('"')
                else:
                    package_name = package_line.strip('"')
                
                if package_line and not package_line.startswith('#'):
                    dependencies.append(package_name)
    
    print(f"Found {len(dependencies)} dependencies to audit")
    print()
    
    # Audit each dependency
    compatible_count = 0
    problematic_count = 0
    unknown_count = 0
    
    for dep in dependencies:
        print(f"📦 {dep}")
        
        license_info = get_package_license(dep)
        license_name = license_info['license']
        
        if license_name in GPL_COMPATIBLE_LICENSES:
            print(f"   ✅ Compatible: {license_name}")
            compatible_count += 1
        elif license_name in PROBLEMATIC_LICENSES:
            print(f"   ⚠️  Problematic: {license_name}")
            problematic_count += 1
        else:
            print(f"   ❓ Unknown/Other: {license_name}")
            unknown_count += 1
        
        if license_info['url']:
            print(f"   🔗 URL: {license_info['url']}")
        
        print()
    
    # Summary
    print("=" * 60)
    print("📊 AUDIT SUMMARY")
    print("=" * 60)
    print(f"✅ Compatible: {compatible_count}")
    print(f"⚠️  Problematic: {problematic_count}")
    print(f"❓ Unknown/Other: {unknown_count}")
    print(f"📦 Total: {len(dependencies)}")
    
    if problematic_count > 0:
        print("\n⚠️  WARNING: Some dependencies have potentially problematic licenses!")
        print("   Manual review recommended for GPL v3 compliance.")
    
    if unknown_count > 0:
        print("\n❓ Some dependencies have unknown licenses.")
        print("   Manual verification recommended.")
    
    if problematic_count == 0 and unknown_count == 0:
        print("\n🎉 All dependencies appear to be GPL v3 compatible!")

def main():
    """Main function."""
    print("Discernus Dependency License Audit")
    print("==================================")
    print()
    
    # Check if pip-licenses is available
    try:
        subprocess.run(['pip-licenses', '--help'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ pip-licenses not found. Installing...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'pip-licenses'], check=True)
            print("✅ pip-licenses installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install pip-licenses")
            return
    
    audit_dependencies()

if __name__ == "__main__":
    main()
