#!/usr/bin/env python3
"""
License Compliance Checker for Discernus Project
Validates licenses against organizational policies and flags issues

Usage:
    python compliance_checker.py [--policy-file policy.json] [--input-file audit.json]
    
Examples:
    python compliance_checker.py --policy-file company_policy.json
    python license_checker.py --output-format json | python compliance_checker.py
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List, Set
import importlib.metadata


# Default license policies
DEFAULT_POLICIES = {
    "approved_licenses": [
        "MIT License",
        "MIT",
        "Apache License 2.0", 
        "Apache-2.0",
        "BSD License",
        "BSD",
        "BSD-2-Clause",
        "BSD-3-Clause",
        "ISC License",
        "ISC",
        "Python Software Foundation License",
        "PSF-2.0",
        "PostgreSQL License",
        "PostgreSQL"
    ],
    "conditional_licenses": [
        "GNU Lesser General Public License v2.1",
        "LGPL-2.1",
        "LGPL-3.0",
        "Mozilla Public License 2.0",
        "MPL-2.0"
    ],
    "prohibited_licenses": [
        "GNU General Public License v2.0",
        "GPL-2.0",
        "GNU General Public License v3.0", 
        "GPL-3.0",
        "GNU Affero General Public License v3.0",
        "AGPL-3.0"
    ],
    "attribution_required": [
        "MIT License",
        "MIT",
        "Apache License 2.0",
        "Apache-2.0", 
        "BSD License",
        "BSD",
        "BSD-2-Clause",
        "BSD-3-Clause"
    ],
    "unknown_policy": "flag",  # Options: "flag", "prohibit", "allow"
    "require_all_known": True
}


def load_policy(policy_file: str = None) -> Dict:
    """Load license policy from file or use defaults."""
    if policy_file:
        try:
            with open(policy_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading policy file: {e}", file=sys.stderr)
            print("Using default policy", file=sys.stderr)
    
    return DEFAULT_POLICIES


def get_packages_from_input(input_file: str = None) -> Dict:
    """Get package data from input file or current environment."""
    if input_file:
        try:
            with open(input_file, 'r') as f:
                data = json.load(f)
                if 'packages' in data:
                    return data['packages']
                else:
                    return data
        except Exception as e:
            print(f"Error loading input file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Read from current environment
        packages = {}
        try:
            for dist in importlib.metadata.distributions():
                name = dist.metadata['Name']
                metadata = importlib.metadata.metadata(name)
                license_info = metadata.get('License', 'Unknown')
                packages[name] = {'license': license_info, 'source': 'metadata'}
        except Exception as e:
            print(f"Error getting packages: {e}", file=sys.stderr)
            sys.exit(1)
        
        return packages


def normalize_license_name(license_name: str) -> str:
    """Normalize license name for comparison."""
    # Handle common variations
    license_map = {
        'MIT': 'MIT License',
        'Apache Software License': 'Apache License 2.0',
        'Apache 2.0': 'Apache License 2.0',
        'BSD': 'BSD License',
        'BSD License (BSD)': 'BSD License',
        'ISC License (ISCL)': 'ISC License',
        'Python Software Foundation License': 'PSF-2.0'
    }
    
    return license_map.get(license_name, license_name)


def check_compliance(packages: Dict, policy: Dict) -> Dict:
    """Check package licenses against policy."""
    
    results = {
        'analysis_date': datetime.now().isoformat(),
        'total_packages': len(packages),
        'policy_applied': policy,
        'compliant_packages': [],
        'conditional_packages': [],
        'prohibited_packages': [],
        'unknown_packages': [],
        'attribution_required': [],
        'compliance_summary': {},
        'issues': []
    }
    
    for package_name, package_info in packages.items():
        if isinstance(package_info, dict):
            license_name = package_info.get('license', 'Unknown')
        else:
            license_name = package_info
        
        normalized_license = normalize_license_name(license_name)
        
        # Check against policy categories
        if normalized_license in policy['approved_licenses']:
            results['compliant_packages'].append({
                'package': package_name,
                'license': license_name,
                'status': 'approved'
            })
        elif normalized_license in policy['conditional_licenses']:
            results['conditional_packages'].append({
                'package': package_name,
                'license': license_name,
                'status': 'conditional',
                'note': 'Review required - conditional approval'
            })
        elif normalized_license in policy['prohibited_licenses']:
            results['prohibited_packages'].append({
                'package': package_name,
                'license': license_name,
                'status': 'prohibited'
            })
            results['issues'].append(f"PROHIBITED: {package_name} uses {license_name}")
        elif license_name == 'Unknown' or normalized_license == 'Unknown':
            results['unknown_packages'].append({
                'package': package_name,
                'license': license_name,
                'status': 'unknown'
            })
            if policy.get('require_all_known', True):
                results['issues'].append(f"UNKNOWN: {package_name} has unknown license")
        else:
            # License not in any category
            results['unknown_packages'].append({
                'package': package_name,
                'license': license_name,
                'status': 'unclassified'
            })
            results['issues'].append(f"UNCLASSIFIED: {package_name} uses {license_name} (not in policy)")
        
        # Check attribution requirements
        if normalized_license in policy.get('attribution_required', []):
            results['attribution_required'].append({
                'package': package_name,
                'license': license_name
            })
    
    # Calculate summary
    results['compliance_summary'] = {
        'approved': len(results['compliant_packages']),
        'conditional': len(results['conditional_packages']),
        'prohibited': len(results['prohibited_packages']),
        'unknown': len(results['unknown_packages']),
        'attribution_required': len(results['attribution_required']),
        'total_issues': len(results['issues'])
    }
    
    # Overall compliance status
    if results['prohibited_packages']:
        results['overall_status'] = 'NON_COMPLIANT'
    elif results['unknown_packages'] and policy.get('require_all_known', True):
        results['overall_status'] = 'NEEDS_REVIEW'
    elif results['conditional_packages']:
        results['overall_status'] = 'CONDITIONAL'
    else:
        results['overall_status'] = 'COMPLIANT'
    
    return results


def format_markdown(results: Dict) -> str:
    """Format compliance results as Markdown."""
    status_icons = {
        'COMPLIANT': '✅',
        'CONDITIONAL': '⚠️',
        'NEEDS_REVIEW': '🔍',
        'NON_COMPLIANT': '❌'
    }
    
    icon = status_icons.get(results['overall_status'], '❓')
    
    md = f"""# License Compliance Report

**Analysis Date:** {results['analysis_date'][:10]}  
**Total Packages:** {results['total_packages']}  
**Overall Status:** {icon} {results['overall_status']}

## Compliance Summary

| Category | Count | Status |
|----------|-------|--------|
| ✅ Approved | {results['compliance_summary']['approved']} | Fully compliant |
| ⚠️ Conditional | {results['compliance_summary']['conditional']} | Review required |
| ❌ Prohibited | {results['compliance_summary']['prohibited']} | **VIOLATIONS** |
| ❓ Unknown | {results['compliance_summary']['unknown']} | Investigation needed |
| 📝 Attribution Required | {results['compliance_summary']['attribution_required']} | Documentation needed |

"""
    
    if results['issues']:
        md += f"## 🚨 Issues Requiring Attention ({len(results['issues'])})\n\n"
        for issue in results['issues']:
            md += f"- {issue}\n"
        md += "\n"
    
    if results['prohibited_packages']:
        md += f"## ❌ Prohibited Licenses ({len(results['prohibited_packages'])})\n\n"
        md += "**These packages MUST be removed or replaced:**\n\n"
        md += "| Package | License | Action Required |\n"
        md += "|---------|---------|------------------|\n"
        for pkg in results['prohibited_packages']:
            md += f"| {pkg['package']} | {pkg['license']} | Remove or find alternative |\n"
        md += "\n"
    
    if results['conditional_packages']:
        md += f"## ⚠️ Conditional Licenses ({len(results['conditional_packages'])})\n\n"
        md += "**These packages require legal review:**\n\n"
        md += "| Package | License | Notes |\n"
        md += "|---------|---------|-------|\n"
        for pkg in results['conditional_packages']:
            md += f"| {pkg['package']} | {pkg['license']} | {pkg.get('note', 'Review required')} |\n"
        md += "\n"
    
    if results['unknown_packages']:
        md += f"## ❓ Unknown/Unclassified Licenses ({len(results['unknown_packages'])})\n\n"
        md += "**These packages need license investigation:**\n\n"
        for pkg in results['unknown_packages']:
            md += f"- **{pkg['package']}**: {pkg['license']}\n"
        md += "\n"
    
    if results['attribution_required']:
        md += f"## 📝 Attribution Required ({len(results['attribution_required'])})\n\n"
        md += "**These packages must be listed in attribution documentation:**\n\n"
        for pkg in results['attribution_required']:
            md += f"- {pkg['package']} ({pkg['license']})\n"
        md += "\n"
    
    # Recommendations
    md += "## 📋 Recommended Actions\n\n"
    
    if results['overall_status'] == 'COMPLIANT':
        md += "✅ **No action required** - All packages are compliant with license policy.\n"
    else:
        if results['prohibited_packages']:
            md += "1. **URGENT**: Remove or replace prohibited packages\n"
        if results['unknown_packages']:
            md += "2. **Research unknown licenses** using license investigation tools\n"
        if results['conditional_packages']:
            md += "3. **Legal review** for conditionally approved packages\n"
        if results['attribution_required']:
            md += "4. **Update attribution documentation** (THIRD_PARTY_LICENSES.md)\n"
    
    return md


def main():
    parser = argparse.ArgumentParser(description='Check license compliance against policy')
    parser.add_argument('--policy-file', help='Path to policy JSON file')
    parser.add_argument('--input-file', help='Path to audit JSON file (default: current environment)')
    parser.add_argument('--output-format', choices=['json', 'markdown'], 
                       default='markdown', help='Output format')
    parser.add_argument('--output-file', help='Output file (default: stdout)')
    parser.add_argument('--create-policy', action='store_true',
                       help='Create example policy file and exit')
    
    args = parser.parse_args()
    
    if args.create_policy:
        with open('license_policy_example.json', 'w') as f:
            json.dump(DEFAULT_POLICIES, f, indent=2)
        print("Created license_policy_example.json", file=sys.stderr)
        return
    
    # Load policy and packages
    policy = load_policy(args.policy_file)
    packages = get_packages_from_input(args.input_file)
    
    # Check compliance
    results = check_compliance(packages, policy)
    
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
    print(f"\nCompliance Summary:", file=sys.stderr)
    print(f"  Overall status: {results['overall_status']}", file=sys.stderr)
    print(f"  Issues: {results['compliance_summary']['total_issues']}", file=sys.stderr)
    print(f"  Prohibited: {results['compliance_summary']['prohibited']}", file=sys.stderr)
    print(f"  Unknown: {results['compliance_summary']['unknown']}", file=sys.stderr)
    
    # Exit with error code if non-compliant
    if results['overall_status'] == 'NON_COMPLIANT':
        sys.exit(1)


if __name__ == "__main__":
    main() 