#!/usr/bin/env python3
"""
License Checker Script for Discernus Project
Automatically analyzes all installed packages and their licenses

Usage:
    python license_checker.py [--output-format json|markdown|csv]
    
Examples:
    python license_checker.py --output-format markdown > license_report.md
    python license_checker.py --output-format json > license_data.json
"""

import argparse
import importlib.metadata
import json
import sys
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple


def get_package_license(package_name: str) -> Tuple[str, str]:
    """
    Get license information for a package.
    Returns (license, source) tuple.
    """
    try:
        metadata = importlib.metadata.metadata(package_name)
        
        # Try license field first
        license_info = metadata.get('License', '').strip()
        
        # If license field is empty/unknown, check classifiers
        if not license_info or license_info.lower() in ['unknown', 'none', '']:
            classifiers = metadata.get_all('Classifier', [])
            license_classifiers = [c for c in classifiers if c.startswith('License ::')]
            
            if license_classifiers:
                # Extract license from classifier like "License :: OSI Approved :: MIT License"
                license_parts = license_classifiers[0].split(' :: ')
                if len(license_parts) >= 3:
                    license_info = license_parts[-1]
                    return license_info, "classifier"
        
        if license_info and license_info.lower() not in ['unknown', 'none', '']:
            return license_info, "metadata"
        
        return "Unknown", "none"
        
    except Exception as e:
        return f"Error: {str(e)}", "error"


def get_all_packages() -> List[str]:
    """Get list of all installed packages."""
    try:
        # Get all installed packages
        packages = [dist.metadata['Name'] for dist in importlib.metadata.distributions()]
        return sorted(packages)
    except Exception as e:
        print(f"Error getting package list: {e}", file=sys.stderr)
        return []


def analyze_licenses() -> Dict:
    """Analyze licenses of all installed packages."""
    packages = get_all_packages()
    
    results = {
        'audit_date': datetime.now().isoformat(),
        'total_packages': len(packages),
        'packages': {},
        'license_summary': defaultdict(int),
        'unknown_packages': [],
        'error_packages': []
    }
    
    print(f"Analyzing {len(packages)} packages...", file=sys.stderr)
    
    for i, package in enumerate(packages):
        if i % 50 == 0:  # Progress indicator
            print(f"Progress: {i}/{len(packages)}", file=sys.stderr)
            
        license_info, source = get_package_license(package)
        
        results['packages'][package] = {
            'license': license_info,
            'source': source
        }
        
        # Categorize results
        if license_info == "Unknown":
            results['unknown_packages'].append(package)
        elif license_info.startswith("Error:"):
            results['error_packages'].append(package)
        else:
            results['license_summary'][license_info] += 1
    
    # Calculate compliance rate
    unknown_count = len(results['unknown_packages']) + len(results['error_packages'])
    results['compliance_rate'] = ((len(packages) - unknown_count) / len(packages)) * 100
    
    return results


def format_markdown(results: Dict) -> str:
    """Format results as Markdown."""
    md = f"""# License Audit Report
**Date:** {results['audit_date'][:10]}  
**Total Packages:** {results['total_packages']}  
**Compliance Rate:** {results['compliance_rate']:.1f}%

## License Summary

| License | Count | Percentage |
|---------|-------|------------|
"""
    
    # Sort licenses by count (descending)
    sorted_licenses = sorted(results['license_summary'].items(), key=lambda x: x[1], reverse=True)
    
    for license_name, count in sorted_licenses:
        percentage = (count / results['total_packages']) * 100
        md += f"| {license_name} | {count} | {percentage:.1f}% |\n"
    
    if results['unknown_packages']:
        md += f"\n## Unknown Licenses ({len(results['unknown_packages'])} packages)\n\n"
        for pkg in sorted(results['unknown_packages']):
            md += f"- {pkg}\n"
    
    if results['error_packages']:
        md += f"\n## Error Packages ({len(results['error_packages'])} packages)\n\n"
        for pkg in sorted(results['error_packages']):
            md += f"- {pkg}\n"
    
    return md


def format_csv(results: Dict) -> str:
    """Format results as CSV."""
    csv = "Package,License,Source\n"
    
    for package, info in sorted(results['packages'].items()):
        # Escape quotes in license names
        license_clean = info['license'].replace('"', '""')
        csv += f'"{package}","{license_clean}","{info["source"]}"\n'
    
    return csv


def main():
    parser = argparse.ArgumentParser(description='Check licenses of all installed packages')
    parser.add_argument('--output-format', choices=['json', 'markdown', 'csv'], 
                       default='markdown', help='Output format')
    parser.add_argument('--output-file', help='Output file (default: stdout)')
    
    args = parser.parse_args()
    
    # Run analysis
    results = analyze_licenses()
    
    # Format output
    if args.output_format == 'json':
        output = json.dumps(results, indent=2)
    elif args.output_format == 'markdown':
        output = format_markdown(results)
    elif args.output_format == 'csv':
        output = format_csv(results)
    
    # Write output
    if args.output_file:
        with open(args.output_file, 'w') as f:
            f.write(output)
        print(f"Report written to {args.output_file}", file=sys.stderr)
    else:
        print(output)
    
    # Print summary to stderr
    print(f"\nSummary:", file=sys.stderr)
    print(f"  Total packages: {results['total_packages']}", file=sys.stderr)
    print(f"  Compliance rate: {results['compliance_rate']:.1f}%", file=sys.stderr)
    print(f"  Unknown licenses: {len(results['unknown_packages'])}", file=sys.stderr)
    print(f"  Errors: {len(results['error_packages'])}", file=sys.stderr)


if __name__ == "__main__":
    main() 