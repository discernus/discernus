#!/usr/bin/env python3
"""
Dependency Difference Checker for Discernus Project
Compares current dependencies against a previous audit to identify changes

Usage:
    python dependency_diff.py <previous_audit_json> [--output-format markdown|json]
    
Examples:
    python dependency_diff.py previous_audit.json --output-format markdown
    python license_checker.py --output-format json > baseline.json
    python dependency_diff.py baseline.json
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List, Set
import importlib.metadata


def get_current_packages() -> Dict[str, str]:
    """Get current installed packages with versions."""
    packages = {}
    try:
        for dist in importlib.metadata.distributions():
            name = dist.metadata['Name']
            version = dist.metadata['Version']
            packages[name] = version
    except Exception as e:
        print(f"Error getting current packages: {e}", file=sys.stderr)
    
    return packages


def load_previous_audit(file_path: str) -> Dict:
    """Load previous audit data from JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading previous audit: {e}", file=sys.stderr)
        sys.exit(1)


def analyze_differences(current_packages: Dict[str, str], previous_audit: Dict) -> Dict:
    """Analyze differences between current and previous package sets."""
    
    # Extract previous packages (handle different JSON structures)
    if 'packages' in previous_audit:
        # From license_checker.py output
        previous_packages = set(previous_audit['packages'].keys())
        previous_licenses = previous_audit['packages']
    else:
        # Simple package list
        previous_packages = set(previous_audit.keys())
        previous_licenses = previous_audit
    
    current_package_names = set(current_packages.keys())
    
    # Calculate differences
    added_packages = current_package_names - previous_packages
    removed_packages = previous_packages - current_package_names
    common_packages = current_package_names & previous_packages
    
    # Check for license changes in common packages
    license_changes = {}
    if isinstance(previous_licenses, dict):
        for pkg in common_packages:
            if pkg in previous_licenses:
                if isinstance(previous_licenses[pkg], dict):
                    # From license_checker.py format
                    prev_license = previous_licenses[pkg].get('license', 'Unknown')
                else:
                    # Simple format
                    prev_license = previous_licenses[pkg]
                
                # Get current license
                try:
                    metadata = importlib.metadata.metadata(pkg)
                    current_license = metadata.get('License', 'Unknown')
                    
                    if current_license != prev_license and prev_license != 'Unknown':
                        license_changes[pkg] = {
                            'previous': prev_license,
                            'current': current_license
                        }
                except:
                    pass
    
    results = {
        'analysis_date': datetime.now().isoformat(),
        'previous_audit_date': previous_audit.get('audit_date', 'Unknown'),
        'current_total': len(current_packages),
        'previous_total': len(previous_packages),
        'added_packages': sorted(list(added_packages)),
        'removed_packages': sorted(list(removed_packages)),
        'license_changes': license_changes,
        'unchanged_packages': len(common_packages) - len(license_changes),
        'summary': {
            'packages_added': len(added_packages),
            'packages_removed': len(removed_packages),
            'licenses_changed': len(license_changes),
            'total_changes': len(added_packages) + len(removed_packages) + len(license_changes)
        }
    }
    
    return results


def format_markdown(results: Dict) -> str:
    """Format results as Markdown."""
    md = f"""# Dependency Change Report

**Analysis Date:** {results['analysis_date'][:10]}  
**Previous Audit:** {results['previous_audit_date'][:10] if results['previous_audit_date'] != 'Unknown' else 'Unknown'}  
**Current Packages:** {results['current_total']}  
**Previous Packages:** {results['previous_total']}  

## Summary

| Change Type | Count |
|-------------|-------|
| Packages Added | {results['summary']['packages_added']} |
| Packages Removed | {results['summary']['packages_removed']} |
| License Changes | {results['summary']['licenses_changed']} |
| **Total Changes** | **{results['summary']['total_changes']}** |
| Unchanged | {results['unchanged_packages']} |

"""
    
    if results['added_packages']:
        md += f"## ➕ Added Packages ({len(results['added_packages'])})\n\n"
        md += "**⚠️ License audit required for these new packages:**\n\n"
        for pkg in results['added_packages']:
            md += f"- {pkg}\n"
        md += "\n"
    
    if results['removed_packages']:
        md += f"## ➖ Removed Packages ({len(results['removed_packages'])})\n\n"
        for pkg in results['removed_packages']:
            md += f"- {pkg}\n"
        md += "\n"
    
    if results['license_changes']:
        md += f"## 🔄 License Changes ({len(results['license_changes'])})\n\n"
        md += "**⚠️ Review required for license changes:**\n\n"
        md += "| Package | Previous License | Current License |\n"
        md += "|---------|------------------|------------------|\n"
        for pkg, change in results['license_changes'].items():
            md += f"| {pkg} | {change['previous']} | {change['current']} |\n"
        md += "\n"
    
    if results['summary']['total_changes'] == 0:
        md += "## ✅ No Changes Detected\n\nAll packages and licenses remain the same since the previous audit.\n"
    else:
        md += "## 📋 Recommended Actions\n\n"
        if results['added_packages']:
            md += "1. **Audit new packages**: Research licenses for all added packages\n"
        if results['license_changes']:
            md += "2. **Review license changes**: Verify compatibility of changed licenses\n"
        if results['added_packages'] or results['license_changes']:
            md += "3. **Update documentation**: Refresh THIRD_PARTY_LICENSES.md\n"
            md += "4. **Legal review**: Consider legal consultation for significant changes\n"
    
    return md


def main():
    parser = argparse.ArgumentParser(description='Compare dependencies against previous audit')
    parser.add_argument('previous_audit', help='Path to previous audit JSON file')
    parser.add_argument('--output-format', choices=['json', 'markdown'], 
                       default='markdown', help='Output format')
    parser.add_argument('--output-file', help='Output file (default: stdout)')
    
    args = parser.parse_args()
    
    # Load data
    current_packages = get_current_packages()
    previous_audit = load_previous_audit(args.previous_audit)
    
    # Analyze differences
    results = analyze_differences(current_packages, previous_audit)
    
    # Format output
    if args.output_format == 'json':
        output = json.dumps(results, indent=2)
    else:
        output = format_markdown(results)
    
    # Write output
    if args.output_file:
        with open(args.output_file, 'w') as f:
            f.write(output)
        print(f"Report written to {args.output_file}", file=sys.stderr)
    else:
        print(output)
    
    # Print summary to stderr
    print(f"\nChange Summary:", file=sys.stderr)
    print(f"  Packages added: {results['summary']['packages_added']}", file=sys.stderr)
    print(f"  Packages removed: {results['summary']['packages_removed']}", file=sys.stderr)
    print(f"  License changes: {results['summary']['licenses_changed']}", file=sys.stderr)
    print(f"  Total changes: {results['summary']['total_changes']}", file=sys.stderr)


if __name__ == "__main__":
    main() 