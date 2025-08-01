#!/usr/bin/env python3
"""
Environment Checker for Cursor Agents
=====================================

Quick script to verify the development environment is set up correctly.
No venv required - uses system Python with user-installed packages.
Includes detection of common agent confusion patterns.

Usage: python3 scripts/check_environment.py
"""

import sys
import os
import subprocess
from pathlib import Path

def check_python_commands():
    """Check for common Python command confusion patterns."""
    issues = []
    
    # Check if 'python' vs 'python3' confusion exists
    try:
        result = subprocess.run(['python', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            issues.append("⚠️  'python' command exists - use 'python3' instead")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass  # Good - 'python' doesn't exist
    
    # Check if we're using the right Python
    if not sys.executable.endswith('python3'):
        issues.append(f"⚠️  Using {sys.executable} - ensure it's python3")
    
    return issues

def check_macos_specifics():
    """Check for macOS-specific environment issues."""
    issues = []
    
    # Check if we're on macOS
    if sys.platform == "darwin":
        # Check for Homebrew Python
        if "/opt/homebrew" in sys.executable:
            issues.append("✅ Using Homebrew Python (macOS standard)")
        elif "/usr/bin" in sys.executable:
            issues.append("⚠️  Using system Python - consider Homebrew for better package management")
        
        # Check for common macOS Python issues
        if "Library/Python" in sys.executable:
            issues.append("✅ Using user-installed packages (macOS standard)")
    
    return issues

def check_common_agent_mistakes():
    """Check for patterns that indicate agent confusion."""
    issues = []
    
    # Check if we're in a venv (agents might try to create one)
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if in_venv:
        issues.append("⚠️  WARNING: Running in virtual environment")
        issues.append("   Note: We removed venv to eliminate agent confusion")
        issues.append("   System Python with user packages is preferred")
    else:
        issues.append("✅ Environment: System Python (no venv)")
    
    # Check for common directory confusion
    cwd = Path.cwd()
    if "venv" in str(cwd):
        issues.append("❌ ERROR: You're inside a venv directory!")
        issues.append("   Run: cd /Volumes/code/discernus")
    
    return issues

def check_environment():
    """Check if the environment is properly configured."""
    
    print("🔍 Environment Check")
    print("=" * 50)
    
    # Check if we're in the right directory
    project_root = Path.cwd()
    if not (project_root / "requirements.txt").exists():
        print("❌ Not in project root (no requirements.txt found)")
        print("🔧 Fix: cd /Volumes/code/discernus")
        return False
    
    print(f"✅ Project root: {project_root}")
    
    # Check Python version and location
    python_path = sys.executable
    print(f"🐍 Python executable: {python_path}")
    print(f"🐍 Python version: {sys.version.split()[0]}")
    
    # Check for common agent confusion patterns
    python_issues = check_python_commands()
    macos_issues = check_macos_specifics()
    agent_issues = check_common_agent_mistakes()
    
    all_issues = python_issues + macos_issues + agent_issues
    
    for issue in all_issues:
        print(issue)
    
    # Check key imports
    missing_packages = []
    
    try:
        import yaml
    except ImportError:
        missing_packages.append("PyYAML")
    
    try:
        import litellm
    except ImportError:
        missing_packages.append("litellm")
        
    try:
        import requests
    except ImportError:
        missing_packages.append("requests")
        
    try:
        from dotenv import load_dotenv
    except ImportError:
        missing_packages.append("python-dotenv")
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("🔧 Fix: python3 -m pip install --user --break-system-packages -r requirements.txt")
        return False
    
    print("✅ Core packages: Available")
    
    # Check .env file
    if not (project_root / ".env").exists():
        print("⚠️  WARNING: No .env file found")
        print("   API keys may not be loaded")
    else:
        print("✅ Environment file: Found")
    
    # Provide quick command reference
    print("\n💡 Quick Commands for Agents:")
    print("   python3 -m discernus.cli list")
    print("   make run EXPERIMENT=projects/simple_test")
    print("   make check")
    
    print("\n🎉 Environment check: ALL GOOD!")
    print("💡 Ready to run Discernus commands")
    return True

if __name__ == "__main__":
    success = check_environment()
    sys.exit(0 if success else 1) 