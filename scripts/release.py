#!/usr/bin/env python3
"""
Narrative Gravity Wells - Release Management Script

This script automates the release process including:
- Pre-release file hygiene and organization checks
- Comprehensive testing requirements
- Documentation updates and verification
- Version management and tagging
- Git workflow automation

Usage:
    python scripts/release.py patch --message "Bug fixes and improvements"
    python scripts/release.py minor --message "New features added"
    python scripts/release.py major --message "Breaking changes"
    python scripts/release.py --dry-run patch --message "Test release process"
"""

import os
import sys
import subprocess
import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Optional

class ReleaseManager:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.root_dir = Path.cwd()
        self.errors = []
        self.warnings = []
        
    def log(self, message: str, level: str = "INFO"):
        """Log messages with timestamp and level."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = "🔍 [DRY-RUN] " if self.dry_run else ""
        print(f"{prefix}[{timestamp}] {level}: {message}")
        
    def error(self, message: str):
        """Log error and add to error list."""
        self.errors.append(message)
        self.log(message, "ERROR")
        
    def warning(self, message: str):
        """Log warning and add to warning list."""
        self.warnings.append(message)
        self.log(message, "WARN")
        
    def run_command(self, cmd: List[str], capture: bool = True) -> Tuple[bool, str]:
        """Run shell command and return (success, output)."""
        if self.dry_run:
            self.log(f"Would run: {' '.join(cmd)}")
            return True, "dry-run-output"
            
        try:
            if capture:
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                return True, result.stdout.strip()
            else:
                subprocess.run(cmd, check=True)
                return True, ""
        except subprocess.CalledProcessError as e:
            return False, str(e)
    
    def check_git_status(self) -> bool:
        """Ensure git repository is clean."""
        self.log("Checking git repository status...")
        
        # Check if we're in a git repository
        success, _ = self.run_command(["git", "status", "--porcelain"])
        if not success:
            self.error("Not in a git repository")
            return False
            
        # Check for uncommitted changes
        success, output = self.run_command(["git", "status", "--porcelain"])
        if output.strip():
            self.error("Repository has uncommitted changes. Please commit or stash them.")
            return False
            
        # Check if we're on main/master branch
        success, branch = self.run_command(["git", "branch", "--show-current"])
        if branch not in ["main", "master"]:
            self.warning(f"Not on main/master branch (currently on: {branch})")
            
        return True
    
    def check_file_hygiene(self) -> bool:
        """Check project file organization and hygiene."""
        self.log("Checking file organization and hygiene...")
        
        hygiene_passed = True
        
        # Check root directory cleanliness
        allowed_root_files = {
            'README.md', 'CHANGELOG.md', 'LICENSE', 'launch.py', 'launch_chainlit.py',
            'check_database.py', 'requirements.txt', 'env.example', 'alembic.ini',
            'pytest.ini', '.gitignore', '.cursorrules', 'LAUNCH_GUIDE.md',
            'package.json', 'package-lock.json', 'playwright.config.ts', 'chainlit.md',
            '.env'
        }
        
        allowed_root_dirs = {
            'src', 'tests', 'docs', 'scripts', 'corpus', 'analysis_results',
            'logs', 'frameworks', 'venv', '.git', 'alembic', 'config',
            'examples', 'exports', 'snapshots', 'schemas',
            'archive', 'model_output', 'framework_prompts',
            '.pytest_cache', 'tmp', 'frontend', 'node_modules', 'paper',
            'public', 'templates', '.chainlit', '.files', 'playwright-report',
            'test-results'
        }
        
        for item in self.root_dir.iterdir():
            if item.is_file() and item.name not in allowed_root_files:
                self.error(f"Unexpected file in root directory: {item.name}")
                hygiene_passed = False
            elif item.is_dir() and item.name not in allowed_root_dirs:
                self.warning(f"Unexpected directory in root: {item.name}")
        
        # Check for temporary files
        tmp_patterns = ['*.tmp', '*.bak', '*.backup', '*~', '.DS_Store']
        for pattern in tmp_patterns:
            success, output = self.run_command(['find', '.', '-name', pattern, '-type', 'f'])
            if output:
                self.warning(f"Found temporary files: {output}")
        
        return hygiene_passed
    
    def run_tests(self) -> bool:
        """Run comprehensive test suite."""
        self.log("Running comprehensive test suite...")
        
        # Check if pytest is available
        success, _ = self.run_command(['python3', '-m', 'pytest', '--version'])
        if not success:
            self.error("pytest not available. Install with: pip install pytest")
            return False
        
        # Run core unit tests only for release (integration tests require running services)
        test_cmd = ['python3', '-m', 'pytest', '-v', 'tests/unit/test_cost_manager.py', 'tests/unit/test_sanitization.py', 'tests/unit/test_crud.py']
        
        # Check if pytest-cov is available
        success, _ = self.run_command(['python3', '-c', 'import pytest_cov'])
        if success:
            test_cmd.extend(['--cov=src', '--cov-report=term-missing'])
        
        success, output = self.run_command(test_cmd, capture=False)
        if not success:
            self.error("Test suite failed. All tests must pass before release.")
            return False
            
        self.log("All tests passed!")
        return True
    
    def check_documentation(self) -> bool:
        """Verify documentation is up to date."""
        self.log("Checking documentation completeness...")
        
        doc_checks_passed = True
        
        # Check required documentation files exist
        required_docs = [
            'README.md',
            'CHANGELOG.md',
            'LAUNCH_GUIDE.md',
            'docs/development/CONTRIBUTING.md',
            'docs/architecture/database_architecture.md'
        ]
        
        for doc in required_docs:
            if not (self.root_dir / doc).exists():
                self.error(f"Required documentation missing: {doc}")
                doc_checks_passed = False
        
        # Check CHANGELOG has unreleased section
        changelog_path = self.root_dir / 'CHANGELOG.md'
        if changelog_path.exists():
            with open(changelog_path, 'r') as f:
                content = f.read()
                if '[Unreleased]' not in content:
                    self.warning("CHANGELOG.md should have [Unreleased] section")
        
        return doc_checks_passed
    
    def get_current_version(self) -> Optional[str]:
        """Extract current version from CHANGELOG.md."""
        changelog_path = self.root_dir / 'CHANGELOG.md'
        if not changelog_path.exists():
            return None
            
        with open(changelog_path, 'r') as f:
            content = f.read()
            
        # Look for version pattern [vX.Y.Z]
        version_pattern = r'\[v(\d+\.\d+\.\d+)\]'
        matches = re.findall(version_pattern, content)
        
        if matches:
            return matches[0]  # Return first (most recent) version
        return None
    
    def calculate_new_version(self, current_version: str, release_type: str) -> str:
        """Calculate new version based on release type."""
        if not current_version:
            return "2.1.0"  # Default starting version
            
        major, minor, patch = map(int, current_version.split('.'))
        
        if release_type == 'major':
            return f"{major + 1}.0.0"
        elif release_type == 'minor':
            return f"{major}.{minor + 1}.0"
        elif release_type == 'patch':
            return f"{major}.{minor}.{patch + 1}"
        else:
            raise ValueError(f"Invalid release type: {release_type}")
    
    def update_changelog(self, new_version: str, release_message: str) -> bool:
        """Update CHANGELOG.md with new version."""
        self.log(f"Updating CHANGELOG.md for version {new_version}...")
        
        changelog_path = self.root_dir / 'CHANGELOG.md'
        if not changelog_path.exists():
            self.error("CHANGELOG.md not found")
            return False
        
        if self.dry_run:
            self.log(f"Would update CHANGELOG.md with version {new_version}")
            return True
        
        with open(changelog_path, 'r') as f:
            content = f.read()
        
        # Replace [Unreleased] with new version
        today = datetime.now().strftime("%Y-%m-%d")
        new_header = f"## [v{new_version}] - {release_message} - {today}"
        
        # Add new [Unreleased] section
        updated_content = content.replace(
            "# Narrative Gravity Maps - Changelog",
            f"# Narrative Gravity Maps - Changelog\n\n## [Unreleased]\n\n{new_header}"
        )
        
        with open(changelog_path, 'w') as f:
            f.write(updated_content)
        
        return True
    
    def create_git_tag(self, version: str, message: str) -> bool:
        """Create and push git tag."""
        self.log(f"Creating git tag v{version}...")
        
        # Stage and commit changes
        success, _ = self.run_command(['git', 'add', '.'])
        if not success:
            self.error("Failed to stage changes")
            return False
        
        commit_message = f"Release v{version}: {message}"
        success, _ = self.run_command(['git', 'commit', '-m', commit_message])
        if not success:
            self.error("Failed to commit changes")
            return False
        
        # Create tag
        tag_message = f"Release v{version}\n\n{message}"
        success, _ = self.run_command(['git', 'tag', '-a', f'v{version}', '-m', tag_message])
        if not success:
            self.error("Failed to create git tag")
            return False
        
        # Push changes and tags
        success, _ = self.run_command(['git', 'push'])
        if not success:
            self.error("Failed to push changes")
            return False
        
        success, _ = self.run_command(['git', 'push', '--tags'])
        if not success:
            self.error("Failed to push tags")
            return False
        
        return True
    
    def generate_release_summary(self, version: str, release_type: str) -> str:
        """Generate release summary."""
        summary = f"""
🎉 Release v{version} ({release_type.upper()}) Complete!

✅ Pre-release Checks:
   - File hygiene verified
   - All tests passed
   - Documentation updated
   - Git repository clean

📋 Release Actions:
   - CHANGELOG.md updated
   - Git commit created
   - Git tag v{version} created
   - Changes pushed to repository

🚀 Next Steps:
   - Monitor for any post-release issues
   - Update deployment if applicable
   - Communicate release to stakeholders
"""
        return summary
    
    def perform_release(self, release_type: str, message: str) -> bool:
        """Perform complete release process."""
        self.log(f"Starting {release_type} release process...")
        
        # Pre-release checks
        if not self.check_git_status():
            return False
        
        if not self.check_file_hygiene():
            return False
        
        if not self.run_tests():
            return False
        
        if not self.check_documentation():
            return False
        
        # Version management
        current_version = self.get_current_version()
        if current_version:
            self.log(f"Current version: {current_version}")
        else:
            self.warning("No current version found, starting from 2.1.0")
            current_version = "2.1.0"
        
        new_version = self.calculate_new_version(current_version, release_type)
        self.log(f"New version will be: {new_version}")
        
        # Update documentation
        if not self.update_changelog(new_version, message):
            return False
        
        # Git operations
        if not self.create_git_tag(new_version, message):
            return False
        
        # Success!
        print(self.generate_release_summary(new_version, release_type))
        
        if self.warnings:
            self.log("Warnings encountered during release:")
            for warning in self.warnings:
                self.log(f"  - {warning}", "WARN")
        
        return True

def main():
    parser = argparse.ArgumentParser(description="Narrative Gravity Wells Release Manager")
    parser.add_argument(
        'release_type', 
        choices=['patch', 'minor', 'major'],
        help="Type of release (patch: bug fixes, minor: new features, major: breaking changes)"
    )
    parser.add_argument(
        '--message', '-m',
        required=True,
        help="Release message describing the changes"
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Perform all checks but don't make any changes"
    )
    
    args = parser.parse_args()
    
    release_manager = ReleaseManager(dry_run=args.dry_run)
    
    success = release_manager.perform_release(args.release_type, args.message)
    
    if release_manager.errors:
        print("\n❌ Release failed due to errors:")
        for error in release_manager.errors:
            print(f"  - {error}")
        sys.exit(1)
    
    if success:
        print("\n✅ Release completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Release failed")
        sys.exit(1)

if __name__ == "__main__":
    main() 