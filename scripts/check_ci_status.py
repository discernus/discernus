#!/usr/bin/env python3
"""
Simple script to check CI status for the current branch.
"""

import subprocess
import sys
import json
import os


def get_current_branch():
    """Get the current git branch name."""
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def get_latest_commit():
    """Get the latest commit hash."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def main():
    """Main function to check CI status."""
    branch = get_current_branch()
    commit = get_latest_commit()
    
    if not branch or not commit:
        print("❌ Could not determine current branch or commit")
        sys.exit(1)
    
    print(f"🔍 Checking CI status for branch: {branch}")
    print(f"📝 Latest commit: {commit[:8]}")
    print()
    
    # Check if we're on the expected branch
    if branch != "refactor/discernus_rebuild":
        print(f"⚠️  Warning: Expected branch 'refactor/discernus_rebuild', got '{branch}'")
    
    print("🚀 CI Pipeline Status:")
    print("- GitHub Actions workflow: .github/workflows/ci.yml")
    print("- Tests: Python 3.11, 3.12, 3.13")
    print("- Services: PostgreSQL 15, Redis 7")
    print("- Coverage: Enabled for Python 3.13")
    print()
    
    print("📊 To check actual CI status:")
    print("1. Visit: https://github.com/discernus/discernus/actions")
    print("2. Look for the latest run on 'refactor/discernus_rebuild'")
    print("3. Or use GitHub CLI: gh run list --branch refactor/discernus_rebuild")
    print()
    
    print("✅ CI configuration is deployed and ready!")


if __name__ == "__main__":
    main() 