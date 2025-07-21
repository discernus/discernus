#!/usr/bin/env python3
"""
Environment Checker for Cursor Agents
=====================================

Quick script to verify the development environment is set up correctly.
Helps prevent the venv confusion dance that wastes Cursor usage.

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
    
    # Check if we're in virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if not in_venv:
        print("❌ NOT in virtual environment!")
        print("🔧 Fix: Run `source venv/bin/activate` first")
        return False
    
    print("✅ Virtual environment: ACTIVE")
    
    # Check if python executable is in project venv
    expected_venv_path = project_root / "venv" / "bin" / "python3"
    if not str(expected_venv_path) in python_path:
        print(f"⚠️  WARNING: Python path doesn't match expected venv")
        print(f"   Expected: {expected_venv_path}")
        print(f"   Actual:   {python_path}")
        return False
    
    print("✅ Python executable: Correct venv path")
    
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
        print("🔧 Fix: Run `source venv/bin/activate && pip install -r requirements.txt`")
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