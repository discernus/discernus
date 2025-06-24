#!/usr/bin/env python3
"""
License Audit Runner for Discernus Project
Convenient orchestration script for running complete license audits

Usage:
    python run_audit.py [--baseline baseline.json] [--policy policy.json] [--output-dir reports/]
    
Examples:
    python run_audit.py                                    # Quick audit
    python run_audit.py --baseline previous_audit.json    # Compare against baseline
    python run_audit.py --output-dir quarterly_audit/     # Organized output
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_command(cmd: list, description: str) -> tuple:
    """Run a command and return (returncode, stdout, stderr)."""
    print(f"🔍 {description}...", file=sys.stderr)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        print(f"❌ Error running {description}: {e}", file=sys.stderr)
        return 1, "", str(e)


def main():
    parser = argparse.ArgumentParser(description='Run comprehensive license audit')
    parser.add_argument('--baseline', help='Previous audit JSON file for comparison')
    parser.add_argument('--policy', help='License policy JSON file')
    parser.add_argument('--output-dir', default='audit_results', help='Output directory')
    parser.add_argument('--quick', action='store_true', help='Quick audit (no detailed investigation)')
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Generate timestamp for files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print("🎯 Starting License Audit Suite", file=sys.stderr)
    print(f"📁 Output directory: {output_dir}", file=sys.stderr)
    print("=" * 50, file=sys.stderr)
    
    results = {
        'audit_timestamp': timestamp,
        'outputs': [],
        'errors': []
    }
    
    # Step 1: Basic license check
    license_report = output_dir / f"license_report_{timestamp}.md"
    license_json = output_dir / f"license_data_{timestamp}.json"
    
    cmd = ["python3", "license_checker.py", "--output-format", "json"]
    returncode, stdout, stderr = run_command(cmd, "Running license checker")
    
    if returncode == 0:
        # Save JSON data
        with open(license_json, 'w') as f:
            f.write(stdout)
        results['outputs'].append(str(license_json))
        
        # Generate markdown report
        cmd = ["python3", "license_checker.py", "--output-format", "markdown", 
               "--output-file", str(license_report)]
        returncode, _, stderr = run_command(cmd, "Generating markdown report")
        
        if returncode == 0:
            results['outputs'].append(str(license_report))
        else:
            results['errors'].append(f"Markdown report generation: {stderr}")
    else:
        results['errors'].append(f"License checker: {stderr}")
        print(f"❌ License checker failed: {stderr}", file=sys.stderr)
    
    # Step 2: Baseline comparison (if provided)
    if args.baseline and Path(args.baseline).exists():
        diff_report = output_dir / f"dependency_changes_{timestamp}.md"
        
        cmd = ["python3", "dependency_diff.py", args.baseline, 
               "--output-format", "markdown", "--output-file", str(diff_report)]
        returncode, _, stderr = run_command(cmd, "Comparing against baseline")
        
        if returncode == 0:
            results['outputs'].append(str(diff_report))
        else:
            results['errors'].append(f"Dependency diff: {stderr}")
    
    # Step 3: Compliance check
    compliance_report = output_dir / f"compliance_report_{timestamp}.md"
    
    cmd_args = ["python3", "compliance_checker.py", 
                "--output-format", "markdown", "--output-file", str(compliance_report)]
    
    if args.policy and Path(args.policy).exists():
        cmd_args.extend(["--policy-file", args.policy])
    
    # Use the JSON data we just generated
    if license_json.exists():
        cmd_args.extend(["--input-file", str(license_json)])
    
    returncode, _, stderr = run_command(cmd_args, "Running compliance check")
    
    if returncode == 0:
        results['outputs'].append(str(compliance_report))
        print("✅ Compliance check passed", file=sys.stderr)
    elif returncode == 1:
        results['outputs'].append(str(compliance_report))
        results['errors'].append("❌ Compliance violations detected")
        print("❌ Compliance violations found - check report", file=sys.stderr)
    else:
        results['errors'].append(f"Compliance check error: {stderr}")
    
    # Step 4: Generate summary
    summary_file = output_dir / f"audit_summary_{timestamp}.md"
    
    with open(summary_file, 'w') as f:
        f.write(f"""# License Audit Summary
        
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Audit ID:** {timestamp}

## Generated Reports

""")
        
        for output_file in results['outputs']:
            f.write(f"- [`{Path(output_file).name}`]({Path(output_file).name})\n")
        
        if results['errors']:
            f.write(f"\n## Issues ({len(results['errors'])})\n\n")
            for error in results['errors']:
                f.write(f"- {error}\n")
        
        f.write(f"""
## Quick Commands

```bash
# View main license report
cat {license_report.name}

# Check compliance status
cat {compliance_report.name}
""")
        
        if args.baseline:
            f.write(f"""
# View dependency changes
cat {diff_report.name}
""")
        
        f.write(f"""
# Rerun audit
python run_audit.py --output-dir {args.output_dir}
```

## Next Steps

1. Review all generated reports
2. Address any compliance violations
3. Update THIRD_PARTY_LICENSES.md if needed
4. Save this audit as baseline for future comparisons:
   ```bash
   cp {license_json.name} baseline_audit.json
   ```
""")
    
    results['outputs'].append(str(summary_file))
    
    # Final summary
    print("=" * 50, file=sys.stderr)
    print("🎉 Audit Complete!", file=sys.stderr)
    print(f"📊 Generated {len(results['outputs'])} reports", file=sys.stderr)
    
    if results['errors']:
        print(f"⚠️  {len(results['errors'])} issues detected", file=sys.stderr)
        for error in results['errors']:
            print(f"   • {error}", file=sys.stderr)
    else:
        print("✅ No issues detected", file=sys.stderr)
    
    print(f"\n📁 All reports saved to: {output_dir}/", file=sys.stderr)
    print(f"📄 Start with: {summary_file.name}", file=sys.stderr)
    
    # Exit with error if there were compliance violations
    if any("Compliance violations" in error for error in results['errors']):
        sys.exit(1)


if __name__ == "__main__":
    main() 