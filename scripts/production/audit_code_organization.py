#!/usr/bin/env python3
"""
Audit Code Organization

Shows current code organization and recommends what should go where
based on the new production/experimental/deprecated structure.

Usage:
    python3 scripts/production/audit_code_organization.py
"""

import os
from pathlib import Path
from collections import defaultdict

def analyze_file(file_path):
    """Analyze a file to determine if it's production-ready, experimental, or deprecated."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for deprecated markers
        deprecated_markers = [
            "# DEPRECATED",
            "# TODO: Remove", 
            "# OBSOLETE",
            "_old",
            "_backup",
            ".bak",
            "archive",
            "BROKEN",
            "NOT WORKING"
        ]
        
        # Check for experimental markers
        experimental_markers = [
            "# TODO",
            "# FIXME",
            "# EXPERIMENTAL",
            "# PROTOTYPE",
            "# TEST",
            "# DRAFT",
            "print(",  # Debug prints suggest experimental
            "temp",
            "tmp",
            "test_",
            "demo_"
        ]
        
        # Check for production markers
        production_markers = [
            '"""',  # Proper docstrings
            "class ",  # Proper classes
            "def ",   # Proper functions
            "__init__",
            "import ",
            "from ",
            "# Production",
            "# STABLE"
        ]
        
        content_lower = content.lower()
        
        # Count markers
        deprecated_count = sum(1 for marker in deprecated_markers if marker.lower() in content_lower)
        experimental_count = sum(1 for marker in experimental_markers if marker.lower() in content_lower)
        production_count = sum(1 for marker in production_markers if marker.lower() in content_lower)
        
        # Determine classification
        if deprecated_count > 0:
            return "deprecated"
        elif experimental_count > production_count or "TODO" in content:
            return "experimental"  
        elif production_count > 5:  # Has substantial production markers
            return "production"
        else:
            return "unknown"
            
    except Exception:
        return "unknown"

def audit_directory(directory_path, max_depth=3):
    """Audit files in a directory."""
    results = defaultdict(list)
    
    for root, dirs, files in os.walk(directory_path):
        # Limit depth
        depth = root.replace(str(directory_path), '').count(os.sep)
        if depth >= max_depth:
            dirs[:] = []  # Don't recurse deeper
            
        for file in files:
            if file.endswith(('.py', '.md')):
                file_path = Path(root) / file
                classification = analyze_file(file_path)
                relative_path = file_path.relative_to(Path('.'))
                results[classification].append(str(relative_path))
    
    return results

def main():
    """Main audit function."""
    print("📋 CODE ORGANIZATION AUDIT")
    print("=" * 60)
    print("Analyzing current codebase organization...")
    
    # Current project structure
    current_locations = {
        "scripts/": "Scripts directory",
        "src/": "Source code",
        "docs/": "Documentation", 
        "tests/": "Test files"
    }
    
    all_results = defaultdict(list)
    
    for location, description in current_locations.items():
        if Path(location).exists():
            print(f"\n🔍 Analyzing {description} ({location})")
            results = audit_directory(Path(location))
            
            for classification, files in results.items():
                all_results[classification].extend(files)
                if files:
                    print(f"  {classification.upper()}: {len(files)} files")
    
    print(f"\n📊 OVERALL CLASSIFICATION RESULTS:")
    print("=" * 40)
    
    # Production candidates
    if all_results['production']:
        print(f"\n✅ PRODUCTION CANDIDATES ({len(all_results['production'])}):")
        print("Should stay in src/ and scripts/production/")
        for file in sorted(all_results['production'][:10]):  # Show first 10
            print(f"  ✓ {file}")
        if len(all_results['production']) > 10:
            print(f"  ... and {len(all_results['production']) - 10} more")
    
    # Experimental candidates  
    if all_results['experimental']:
        print(f"\n🧪 EXPERIMENTAL CANDIDATES ({len(all_results['experimental'])}):")
        print("Should move to experimental/ or sandbox/")
        for file in sorted(all_results['experimental'][:10]):  # Show first 10
            print(f"  🧪 {file}")
        if len(all_results['experimental']) > 10:
            print(f"  ... and {len(all_results['experimental']) - 10} more")
    
    # Deprecated candidates
    if all_results['deprecated']:
        print(f"\n🗑️ DEPRECATED CANDIDATES ({len(all_results['deprecated'])}):")
        print("Should move to deprecated/")
        for file in sorted(all_results['deprecated']):
            print(f"  🗑️ {file}")
    
    # Unknown files
    if all_results['unknown']:
        print(f"\n❓ NEEDS MANUAL REVIEW ({len(all_results['unknown'])}):")
        print("Requires human judgment")
        for file in sorted(all_results['unknown'][:5]):  # Show first 5
            print(f"  ❓ {file}")
        if len(all_results['unknown']) > 5:
            print(f"  ... and {len(all_results['unknown']) - 5} more")
    
    print(f"\n🎯 RECOMMENDATIONS:")
    print("=" * 40)
    
    # Generate specific recommendations
    total_files = sum(len(files) for files in all_results.values())
    production_pct = len(all_results['production']) / total_files * 100 if total_files else 0
    experimental_pct = len(all_results['experimental']) / total_files * 100 if total_files else 0
    
    print(f"Total files analyzed: {total_files}")
    print(f"Production-ready: {production_pct:.1f}%")
    print(f"Experimental: {experimental_pct:.1f}%")
    
    if experimental_pct > 30:
        print("\n⚠️  HIGH EXPERIMENTAL CODE RATIO")
        print("   Consider cleaning up or promoting experimental code")
    
    if len(all_results['deprecated']) > 5:
        print("\n🗑️ DEPRECATED CODE CLEANUP NEEDED")
        print("   Move deprecated files to deprecated/ directory")
    
    print(f"\n📋 NEXT STEPS:")
    print("1. Review experimental candidates for promotion potential")
    print("2. Move deprecated files to deprecated/ directory")
    print("3. Clean up or organize experimental code in experimental/")
    print("4. Ensure production code has proper documentation")
    
    print(f"\n🔗 See docs/CODE_ORGANIZATION_STANDARDS.md for detailed guidelines")

if __name__ == "__main__":
    main() 