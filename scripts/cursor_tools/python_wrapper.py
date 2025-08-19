#!/usr/bin/env python3
"""
Python Command Wrapper for Cursor Agents
========================================

This script helps agents avoid python vs python3 confusion and provides
helpful error messages for common macOS environment issues.

Usage: python3 scripts/python_wrapper.py <command> [args...]
"""

import sys
import subprocess
import os
from pathlib import Path

def check_python_command():
    """Check if we're using the right Python command."""
    if not sys.executable.endswith('python3'):
        print("❌ ERROR: Not using python3!")
        print(f"   Current: {sys.executable}")
        print("   Fix: Use 'python3' instead of 'python'")
        return False
    return True

def check_macos_environment():
    """Check for macOS-specific environment issues."""
    if sys.platform == "darwin":
        # Check if we're using Homebrew Python
        if "/opt/homebrew" in sys.executable:
            print("✅ Using Homebrew Python (macOS standard)")
        elif "/usr/bin" in sys.executable:
            print("⚠️  Using system Python - consider Homebrew for better package management")
        
        # Check for user-installed packages
        if "Library/Python" in sys.executable:
            print("✅ Using user-installed packages (macOS standard)")
    
    return True

def run_command(command_args):
    """Run the specified command with proper error handling."""
    try:
        # Run the command
        result = subprocess.run(command_args, check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed with exit code {e.returncode}")
        return e.returncode
    except FileNotFoundError as e:
        print(f"❌ Command not found: {e}")
        print("💡 Common fixes:")
        print("   - Use 'python3' instead of 'python'")
        print("   - Install missing packages: python3 -m pip install --user --break-system-packages -r requirements.txt")
        print("   - Check if you're in the right directory: cd /Volumes/code/discernus")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1

def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("❌ Usage: python3 scripts/python_wrapper.py <command> [args...]")
        print("💡 Examples:")
        print("   python3 scripts/python_wrapper.py -m discernus.cli list")
        print("   python3 scripts/python_wrapper.py scripts/check_environment.py")
        return 1
    
    # Check environment
    if not check_python_command():
        return 1
    
    check_macos_environment()
    
    # Get command arguments
    command_args = sys.argv[1:]
    
    print(f"🚀 Running: {' '.join(command_args)}")
    print("=" * 50)
    
    # Run the command
    return run_command(command_args)

if __name__ == "__main__":
    sys.exit(main()) 