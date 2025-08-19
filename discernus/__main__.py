#!/usr/bin/env python3
"""
Discernus Package Entry Point
============================

This file allows running the discernus package as a module:
    python3 -m discernus

It provides access to both CLI versions:
- Main CLI: python3 -m discernus run <experiment>
- V8.0 CLI: python3 -m discernus v8 run <experiment>
"""

import sys
from pathlib import Path

def main():
    """Main entry point for the discernus package."""
    if len(sys.argv) < 2:
        print("Discernus CLI - Computational Social Science Research Platform")
        print("\nUsage:")
        print("  python3 -m discernus run <experiment>     # Run experiment")
        print("  python3 -m discernus validate <experiment> # Validate experiment")
        print("  python3 -m discernus list                 # List experiments")
        print("\nFor help:")
        print("  python3 -m discernus --help")
        sys.exit(1)
    
    # Main CLI only (v8 CLI deprecated)
    if sys.argv[1] == "v8":
        print("❌ V8.0 CLI has been deprecated")
        print("Use: python3 -m discernus run <experiment>")
        sys.exit(1)
    else:
        # Import and run main CLI
        try:
            from discernus.cli import main
            main()
        except ImportError as e:
            print(f"❌ Error importing main CLI: {e}")
            print("Make sure all dependencies are installed")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Main CLI error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
