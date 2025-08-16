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
        print("  python3 -m discernus run <experiment>     # Main CLI")
        print("  python3 -m discernus v8 run <experiment>  # V8.0 CLI")
        print("\nFor help:")
        print("  python3 -m discernus --help")
        print("  python3 -m discernus v8 --help")
        sys.exit(1)
    
    # Check if user wants v8.0 CLI
    if sys.argv[1] == "v8":
        if len(sys.argv) < 3:
            print("Discernus V8.0 CLI")
            print("\nUsage:")
            print("  python3 -m discernus v8 run <experiment>")
            print("  python3 -m discernus v8 validate <experiment>")
            sys.exit(1)
        
        # Import and run v8.0 CLI
        try:
            from discernus.cli_v8 import cli
            # Remove "v8" from argv so click can parse the rest
            sys.argv = [sys.argv[0]] + sys.argv[2:]
            cli()
        except ImportError as e:
            print(f"❌ Error importing V8.0 CLI: {e}")
            print("Make sure all dependencies are installed")
            sys.exit(1)
        except Exception as e:
            print(f"❌ V8.0 CLI error: {e}")
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
