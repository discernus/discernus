#!/usr/bin/env python3
"""
Check Existing Systems - Production-First Search

Run this script before building any new functionality to see if we already
have something that does what you want to build.

Uses clean search strategy:
1. Search PRODUCTION code first (src/, scripts/production/, docs/specifications/)
2. Only search experimental if no production matches found
3. Never search deprecated code unless explicitly requested

Usage:
    python3 scripts/production/check_existing_systems.py "quality assurance"
    python3 scripts/production/check_existing_systems.py "experiment execution"
    python3 scripts/production/check_existing_systems.py "data export" --include-experimental
"""

import sys
import subprocess
import argparse
from pathlib import Path

class ProductionCodeSearcher:
    """Clean search focusing on production-ready code."""
    
    def __init__(self, include_experimental=False, include_deprecated=False):
        self.include_experimental = include_experimental
        self.include_deprecated = include_deprecated
        self.project_root = Path(__file__).parent.parent.parent
        
        # Production directories (always searched)
        self.production_dirs = [
            "src/narrative_gravity/",
            "scripts/production/", 
            "docs/specifications/",
            "docs/user-guides/",
            "frameworks/"
        ]
        
        # Experimental directories (conditional search)
        self.experimental_dirs = [
            "experimental/",
            "sandbox/",
            "tests/",  # Include tests in experimental for now
        ]
        
        # Deprecated directories (rarely searched)
        self.deprecated_dirs = [
            "deprecated/",
            "tmp/",
        ]
        
        # Known problematic patterns to avoid
        self.avoid_patterns = [
            "# DEPRECATED",
            "# TODO: Remove",
            "# OBSOLETE",
            "archive/",
            ".bak",
            "_old",
            "_backup"
        ]
    
    def search_production_code(self, query: str):
        """Search production code directories first."""
        print(f"🔍 Searching PRODUCTION systems for: '{query}'")
        print("=" * 60)
        
        production_matches = 0
        
        for directory in self.production_dirs:
            if not (self.project_root / directory).exists():
                continue
                
            print(f"\n📁 {directory.upper()}:")
            try:
                result = subprocess.run(
                    ["grep", "-r", "-i", "--include=*.py", "--include=*.md", query, directory],
                    capture_output=True, text=True, cwd=self.project_root
                )
                
                if result.stdout:
                    # Filter out problematic patterns
                    lines = result.stdout.split('\n')
                    clean_lines = []
                    
                    for line in lines:
                        if line.strip() and not any(pattern in line for pattern in self.avoid_patterns):
                            clean_lines.append(line)
                    
                    if clean_lines:
                        production_matches += len(clean_lines)
                        # Show limited output to avoid overwhelming
                        for line in clean_lines[:10]:
                            print(line)
                        if len(clean_lines) > 10:
                            print(f"... and {len(clean_lines) - 10} more matches")
                    else:
                        print("No clean matches found.")
                else:
                    print("No matches found.")
                    
            except Exception as e:
                print(f"Error searching {directory}: {e}")
        
        return production_matches
    
    def search_experimental_code(self, query: str):
        """Search experimental code if no production matches."""
        print(f"\n🧪 Searching EXPERIMENTAL systems for: '{query}'")
        print("=" * 60)
        print("⚠️  These results may include unstable or obsolete code!")
        
        experimental_matches = 0
        
        for directory in self.experimental_dirs:
            if not (self.project_root / directory).exists():
                continue
                
            print(f"\n📂 {directory.upper()}:")
            try:
                result = subprocess.run(
                    ["grep", "-r", "-i", "--include=*.py", "--include=*.md", query, directory],
                    capture_output=True, text=True, cwd=self.project_root
                )
                
                if result.stdout:
                    lines = result.stdout.split('\n')
                    clean_lines = [line for line in lines if line.strip()]
                    experimental_matches += len(clean_lines)
                    
                    # Show limited output
                    for line in clean_lines[:5]:
                        print(line)
                    if len(clean_lines) > 5:
                        print(f"... and {len(clean_lines) - 5} more experimental matches")
                else:
                    print("No matches found.")
                    
            except Exception as e:
                print(f"Error searching {directory}: {e}")
        
        return experimental_matches
    
    def search_deprecated_code(self, query: str):
        """Search deprecated code (only if explicitly requested)."""
        print(f"\n🗑️ Searching DEPRECATED systems for: '{query}'")
        print("=" * 60)
        print("⚠️  These results are obsolete and should not be used!")
        
        for directory in self.deprecated_dirs:
            if not (self.project_root / directory).exists():
                continue
                
            print(f"\n📂 {directory.upper()}:")
            try:
                result = subprocess.run(
                    ["grep", "-r", "-i", "--include=*.py", "--include=*.md", query, directory],
                    capture_output=True, text=True, cwd=self.project_root
                )
                
                if result.stdout:
                    lines = result.stdout.split('\n')[:3]  # Very limited output
                    for line in lines:
                        if line.strip():
                            print(line)
                    print("... (deprecated code - use production alternatives)")
                else:
                    print("No matches found.")
                    
            except Exception as e:
                print(f"Error searching {directory}: {e}")

def show_inventory():
    """Show the existing systems inventory."""
    inventory_path = Path(__file__).parent.parent.parent / "docs" / "EXISTING_SYSTEMS_INVENTORY.md"
    
    if inventory_path.exists():
        print("\n📋 PRODUCTION SYSTEMS INVENTORY:")
        print("=" * 40)
        with open(inventory_path, 'r') as f:
            content = f.read()
            # Show production systems only
            lines = content.split('\n')
            in_production_section = False
            
            for line in lines:
                if "🔍 Quality Assurance Systems" in line:
                    in_production_section = True
                elif line.startswith("## ⚠️"):  # Deprecation section
                    in_production_section = False
                elif line.startswith("---"):
                    in_production_section = False
                    
                if in_production_section or "✅" in line:
                    print(line)
    else:
        print("⚠️ EXISTING_SYSTEMS_INVENTORY.md not found!")

def main():
    parser = argparse.ArgumentParser(
        description="Search for existing systems before building new ones",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/production/check_existing_systems.py "quality assurance"
  python3 scripts/production/check_existing_systems.py "experiment execution" --include-experimental
  python3 scripts/production/check_existing_systems.py "validation" --include-deprecated
        """
    )
    
    parser.add_argument("query", help="Search query for existing functionality")
    parser.add_argument("--include-experimental", action="store_true", 
                       help="Also search experimental code")
    parser.add_argument("--include-deprecated", action="store_true",
                       help="Also search deprecated code")
    
    args = parser.parse_args()
    
    print("🚨 PREVENTION CHECK: Searching for existing systems...")
    print("🎯 FOCUS: Production-ready code first!")
    print("Rule: ALWAYS search before building!")
    
    searcher = ProductionCodeSearcher(
        include_experimental=args.include_experimental,
        include_deprecated=args.include_deprecated
    )
    
    # Search production code first
    production_matches = searcher.search_production_code(args.query)
    
    # Search experimental code if requested OR if no production matches
    experimental_matches = 0
    if args.include_experimental or production_matches == 0:
        if production_matches == 0:
            print("\n⚠️  No production systems found. Checking experimental...")
        experimental_matches = searcher.search_experimental_code(args.query)
    
    # Search deprecated code only if explicitly requested
    if args.include_deprecated:
        searcher.search_deprecated_code(args.query)
    
    # Show inventory
    show_inventory()
    
    # Generate recommendations
    print("\n" + "=" * 60)
    print("🎯 SEARCH RESULTS SUMMARY:")
    print(f"Production matches: {production_matches}")
    print(f"Experimental matches: {experimental_matches}")
    
    if production_matches > 0:
        print("\n✅ FOUND PRODUCTION SYSTEMS!")
        print("Recommendation: Use or enhance existing production code")
        print("⚠️  Avoid rebuilding - enhance what exists!")
    elif experimental_matches > 0:
        print("\n🧪 Found experimental systems only")
        print("Recommendation: Consider promoting experimental code to production")
        print("📋 Review experimental code for production readiness")
    else:
        print("\n🔍 No existing systems found")
        print("✅ Safe to build new - but double-check inventory first!")
    
    print("\n✅ PREVENTION CHECKLIST:")
    print("1. ☐ Did you find existing functionality above?")
    print("2. ☐ Can you enhance existing code instead of rebuilding?") 
    print("3. ☐ If building new, will it be clearly superior?")
    print("4. ☐ Have you documented why existing solutions are insufficient?")
    print("5. ☐ Will you update EXISTING_SYSTEMS_INVENTORY.md when done?")
    print("6. ☐ Are you building in experimental/ first?")
    print("\n🛡️ Remember: Production code first, experimental second, deprecated never!")

if __name__ == "__main__":
    main() 