#!/usr/bin/env python3
"""
Environment Checker for Cursor Agents
=====================================

Quick script to verify the development environment is set up correctly.
No venv required - uses system Python with user-installed packages.

Usage: python3 scripts/check_environment.py
"""

import sys
import os
from pathlib import Path

def check_environment():
    """Check if the environment is properly configured."""
    
    print("🔍 Environment Check")
    print("=" * 50)
    
    # Check if we're in the right directory
    project_root = Path.cwd()
    if not (project_root / "requirements.txt").exists():
        print("❌ Not in project root (no requirements.txt found)")
        return False
    
    print(f"✅ Project root: {project_root}")
    
    # Check Python version and location
    python_path = sys.executable
    print(f"🐍 Python executable: {python_path}")
    print(f"🐍 Python version: {sys.version.split()[0]}")
    
    # Check if we're using system Python (no venv required)
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if in_venv:
        print("⚠️  WARNING: Running in virtual environment")
        print("   Note: We removed venv to eliminate agent confusion")
        print("   System Python with user packages is preferred")
    else:
        print("✅ Environment: System Python (no venv)")
    
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
        print("🔧 Fix: Run `python3 -m pip install --user --break-system-packages -r requirements.txt`")
        return False
    
    print("✅ Core packages: Available")
    
    # Check .env file
    if not (project_root / ".env").exists():
        print("⚠️  WARNING: No .env file found")
        print("   API keys may not be loaded")
    else:
        print("✅ Environment file: Found")
    
    print("\n🎉 Environment check: ALL GOOD!")
    print("💡 Ready to run Discernus commands")
    return True

if __name__ == "__main__":
    success = check_environment()
    sys.exit(0 if success else 1) 