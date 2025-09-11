#!/usr/bin/env python3
"""
Repository Organization Script

This script organizes the Discernus codebase into separate repositories
for open source release and private content.

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
import shutil
from pathlib import Path

# Repository structure
REPOS = {
    'discernus': {
        'path': '../discernus-repos/discernus',
        'description': 'Core Discernus platform (GPL v3)',
        'content': [
            'discernus/',
            'docs/',
            'frameworks/',
            'requirements.txt',
            'pyproject.toml',
            'Makefile',
            'README.md',
            'LICENSE',
            'COPYING',
            'DUAL_LICENSING.md',
            'CONTRIBUTING.md',
            '.github/',
            'scripts/add_license_headers.py',
            'scripts/audit_dependencies.py',
            'scripts/simple_dependency_audit.py',
        ]
    },
    'frameworks': {
        'path': '../discernus-repos/frameworks',
        'description': 'Community framework specifications (MIT)',
        'content': [
            'frameworks/',
            'docs/specifications/',
            'scripts/framework_researcher/',
            'scripts/framework_validation/',
        ]
    },
    'librarian': {
        'path': '../discernus-repos/librarian',
        'description': 'Framework management and discovery tools (GPL v3)',
        'content': [
            'discernus/librarian/',
            'scripts/auditing/',
        ]
    },
    'tools': {
        'path': '../discernus-repos/tools',
        'description': 'Development tools and utilities (MIT)',
        'content': [
            'scripts/cursor_tools/',
            'scripts/prompt_engineering/',
            'scripts/compliance_tools/',
            'scripts/auditing/',
        ]
    },
    'research': {
        'path': '../discernus-repos/research',
        'description': 'Open research examples and experiments (MIT)',
        'content': [
            'projects/micro_test_experiment/',
            'projects/nano_test_experiment/',
            'projects/simple_test/',
            'projects/business_ethics_experiment/',
            'projects/entman_framing_experiment/',
            'projects/lakoff_framing_experiment/',
        ]
    },
    'discernus-private': {
        'path': '../discernus-repos/discernus-private',
        'description': 'Private corpus, planning, and proprietary content',
        'content': [
            'corpus/',
            'scripts/corpus_tools/',
            'pm/',
            'projects/1a_caf_civic_character/',
            'projects/1b_chf_constitutional_health/',
            'projects/1c_ecf_emotional_climate/',
            'projects/2a_populist_rhetoric_study/',
            'projects/2b_cff_cohesive_flourishing/',
            'projects/2c_political_moral_analysis/',
            'projects/2d_trump_populism/',
            'projects/apdes/',
            'projects/bolsonaro_2018/',
            'projects/mlkmx/',
            'projects/vanderveen_presidential_pdaf/',
            'projects/vanderveen_presidential_pdaf_phase2/',
            'projects/zfreezer/',
        ]
    }
}

def create_repository_structure():
    """Create the repository directory structure."""
    print("🏗️  Creating repository structure...")
    
    for repo_name, repo_info in REPOS.items():
        repo_path = Path(repo_info['path'])
        repo_path.mkdir(parents=True, exist_ok=True)
        
        # Create README for each repo
        readme_content = f"""# {repo_name.title()}

{repo_info['description']}

## Repository Structure

This repository contains:
{chr(10).join(f"- {item}" for item in repo_info['content'])}

## License

See LICENSE file for details.

## Contributing

See CONTRIBUTING.md for guidelines.
"""
        
        with open(repo_path / 'README.md', 'w') as f:
            f.write(readme_content)
        
        print(f"✅ Created {repo_name} at {repo_path}")

def copy_content():
    """Copy content to appropriate repositories."""
    print("\n📁 Copying content to repositories...")
    
    for repo_name, repo_info in REPOS.items():
        repo_path = Path(repo_info['path'])
        print(f"\n📦 Processing {repo_name}...")
        
        for item in repo_info['content']:
            src_path = Path(item)
            dst_path = repo_path / item
            
            if src_path.exists():
                if src_path.is_dir():
                    try:
                        shutil.copytree(src_path, dst_path, dirs_exist_ok=True, ignore=shutil.ignore_patterns('*.json'))
                        print(f"  ✅ Copied directory: {item}")
                    except shutil.Error as e:
                        print(f"  ⚠️  Partial copy of directory: {item} (some files skipped)")
                else:
                    dst_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src_path, dst_path)
                    print(f"  ✅ Copied file: {item}")
            else:
                print(f"  ⚠️  Not found: {item}")

def create_license_files():
    """Create appropriate license files for each repository."""
    print("\n📄 Creating license files...")
    
    # MIT license for permissive repositories
    mit_license = """MIT License

Copyright (c) 2025 Discernus Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    
    # GPL v3 license (already exists)
    gpl_license_path = Path('LICENSE')
    
    # Copy licenses to appropriate repositories
    license_assignments = {
        'discernus': 'GPL-3.0',
        'frameworks': 'MIT',
        'librarian': 'GPL-3.0',
        'tools': 'MIT',
        'research': 'MIT',
        'discernus-private': 'PRIVATE'
    }
    
    for repo_name, license_type in license_assignments.items():
        repo_path = Path(REPOS[repo_name]['path'])
        
        if license_type == 'GPL-3.0':
            # Copy GPL v3 license
            shutil.copy2(gpl_license_path, repo_path / 'LICENSE')
            shutil.copy2('COPYING', repo_path / 'COPYING')
            print(f"  ✅ Added GPL v3 license to {repo_name}")
        elif license_type == 'MIT':
            # Create MIT license
            with open(repo_path / 'LICENSE', 'w') as f:
                f.write(mit_license)
            print(f"  ✅ Added MIT license to {repo_name}")
        elif license_type == 'PRIVATE':
            # Create private license notice
            private_notice = """PRIVATE REPOSITORY

This repository contains private and proprietary content.
Access is restricted to authorized personnel only.

Copyright (c) 2025 Discernus Team
All rights reserved.
"""
            with open(repo_path / 'LICENSE', 'w') as f:
                f.write(private_notice)
            print(f"  ✅ Added private license notice to {repo_name}")

def main():
    """Main function."""
    print("Discernus Repository Organization")
    print("=================================")
    print()
    
    create_repository_structure()
    copy_content()
    create_license_files()
    
    print("\n🎉 Repository organization complete!")
    print("\nNext steps:")
    print("1. Review the organized repositories")
    print("2. Initialize git repositories")
    print("3. Set up GitHub repositories")
    print("4. Update documentation and links")

if __name__ == "__main__":
    main()
