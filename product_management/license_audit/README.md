# License Audit Documentation

This folder contains all documentation and materials from the comprehensive open source license audit conducted on June 24, 2025.

## Contents

### Primary Documentation
- **`LICENSE_AUDIT_REPORT_2025-06-24.md`** - Complete technical audit report with detailed findings, statistics, and compliance analysis
- **`AUDIT_PROCESS_DOCUMENTATION.md`** - Comprehensive methodology documentation describing the audit process, tools used, and investigation techniques

### Scripts
**Note:** No persistent scripts were retained. The audit used temporary Python scripts for package enumeration and license detection, which were created and removed during the investigation process to avoid cluttering the repository.

## Audit Summary

- **Date Conducted:** June 24, 2025
- **Packages Audited:** 261 total dependencies
- **Compliance Rate:** 100% (Perfect compliance achieved)
- **Unknown Packages Resolved:** 18 packages successfully investigated
- **Risk Level:** None - all licenses permit commercial use

## Key Achievements

✅ **Perfect Compliance:** All 261 packages now have verified licenses  
✅ **Commercial Ready:** All licenses permit commercial use and distribution  
✅ **Zero Unknown Packages:** Complete license resolution achieved  
✅ **Industry Leading:** Exceeds typical 85-90% industry compliance rates  

## Related Files

- **`/THIRD_PARTY_LICENSES.md`** (in project root) - Public-facing attribution document for compliance and distribution

## Next Steps

- **Next Review Due:** September 2025
- **Recommended:** Add automated license scanning to CI/CD pipeline
- **Monitoring:** Track new dependency additions for license compliance

---

**Audit Methodology:** Manual investigation with automated discovery  
**Verification Standard:** Minimum 2-source verification for all packages  
**Quality Assurance:** Cross-referenced against SPDX license database 

# License Audit Tools

This directory contains automated tools for conducting comprehensive open source license audits of the Discernus project.

## Quick Start

### Simple Audit
```bash
python run_audit.py
```

### Full Audit with Baseline Comparison
```bash
# First run - create baseline
python license_checker.py --output-format json > baseline_audit.json

# Future runs - compare against baseline
python run_audit.py --baseline baseline_audit.json --output-dir quarterly_audit/
```

---

## Scripts Overview

### 1. `run_audit.py` 🎯 **Main Orchestrator**
**Purpose:** One-stop script that runs complete license audits with all tools

**Usage:**
```bash
python run_audit.py [options]
```

**Options:**
- `--baseline FILE` - Compare against previous audit JSON
- `--policy FILE` - Use custom license policy  
- `--output-dir DIR` - Output directory (default: audit_results)
- `--quick` - Quick audit mode

**Output:** Complete audit suite with timestamped reports

---

### 2. `license_checker.py` 🔍 **Core License Scanner**
**Purpose:** Analyzes all installed packages and extracts license information

**Usage:**
```bash
python license_checker.py [--output-format FORMAT] [--output-file FILE]
```

**Examples:**
```bash
# Quick markdown report
python license_checker.py

# JSON data for other tools
python license_checker.py --output-format json > audit_data.json

# CSV for spreadsheet analysis
python license_checker.py --output-format csv > licenses.csv
```

**Output:** License analysis with compliance statistics

---

### 3. `dependency_diff.py` 📊 **Change Detector**
**Purpose:** Compares current dependencies against previous audits to identify changes

**Usage:**
```bash
python dependency_diff.py <baseline_file> [options]
```

**Examples:**
```bash
# Compare against last audit
python dependency_diff.py previous_audit.json

# Generate JSON diff data
python dependency_diff.py baseline.json --output-format json
```

**Output:** Added/removed packages and license changes

---

### 4. `compliance_checker.py` ✅ **Policy Validator**
**Purpose:** Validates licenses against organizational policies and flags violations

**Usage:**
```bash
python compliance_checker.py [options]
```

**Examples:**
```bash
# Check with default policy
python compliance_checker.py

# Use custom policy
python compliance_checker.py --policy-file company_policy.json

# Check specific audit data
python compliance_checker.py --input-file audit_data.json

# Create example policy file
python compliance_checker.py --create-policy
```

**Output:** Compliance report with violations and recommendations

---

## Typical Workflow

### Initial Setup (First Audit)
```bash
# 1. Run comprehensive audit
python run_audit.py --output-dir initial_audit/

# 2. Save baseline for future comparisons
cp initial_audit/license_data_*.json baseline_audit.json

# 3. Create organizational policy (optional)
python compliance_checker.py --create-policy
# Edit license_policy_example.json as needed
```

### Regular Audits (Quarterly/Before Releases)
```bash
# Run audit with change detection
python run_audit.py --baseline baseline_audit.json --output-dir quarterly_audit/

# Update baseline if changes are acceptable
cp quarterly_audit/license_data_*.json baseline_audit.json
```

### Investigating Specific Issues
```bash
# Check only unknown licenses
python license_checker.py | grep "Unknown"

# Validate against strict policy
python compliance_checker.py --policy-file strict_policy.json

# Check what changed since last week
python dependency_diff.py weekly_baseline.json
```

---

## Output Files Explained

### License Report (`license_report_*.md`)
- Summary of all packages and their licenses
- Compliance statistics
- List of unknown packages requiring investigation

### Dependency Changes (`dependency_changes_*.md`)
- Packages added/removed since baseline
- License changes in existing packages
- Impact assessment and recommendations

### Compliance Report (`compliance_report_*.md`)
- Policy violations and issues
- Packages requiring legal review
- Attribution requirements
- Action items prioritized by risk

### Audit Summary (`audit_summary_*.md`)
- Overview of all generated reports
- Quick commands for viewing results
- Next steps and recommendations

---

## License Policy Configuration

### Default Policy Categories

**✅ Approved Licenses:**
- MIT License
- Apache-2.0
- BSD variants
- ISC License
- PSF-2.0 (Python)
- PostgreSQL License

**⚠️ Conditional Licenses:**
- LGPL-2.1/3.0 (libraries only)
- MPL-2.0 (Mozilla)

**❌ Prohibited Licenses:**
- GPL-2.0/3.0 (viral copyleft)
- AGPL-3.0 (network copyleft)

### Custom Policy File Format

```json
{
  "approved_licenses": ["MIT License", "Apache-2.0", "BSD License"],
  "conditional_licenses": ["LGPL-2.1"],
  "prohibited_licenses": ["GPL-2.0", "GPL-3.0"],
  "attribution_required": ["MIT License", "Apache-2.0", "BSD License"],
  "require_all_known": true
}
```

---

## Integration with CI/CD

### GitHub Actions Example
```yaml
- name: License Audit
  run: |
    cd product_management/license_audit
    python run_audit.py --baseline baseline.json
    # Fail build if compliance violations
    if [ $? -ne 0 ]; then exit 1; fi
```

### Pre-Commit Hook
```bash
#!/bin/bash
cd product_management/license_audit
python compliance_checker.py --input-file <(python license_checker.py --output-format json)
```

---

## Troubleshooting

### Common Issues

**"Unknown" licenses detected:**
```bash
# Get more details about unknown packages
python license_checker.py --output-format json | jq '.unknown_packages[]'

# Manual investigation needed - check PyPI and GitHub
```

**Script fails with import errors:**
```bash
# Ensure you're in the correct Python environment
which python
pip list | grep importlib

# Run in project virtual environment
source ../../../venv/bin/activate  # Adjust path as needed
```

**Baseline comparison shows many changes:**
```bash
# Check if virtual environment changed
python dependency_diff.py baseline.json | grep "Added Packages"

# Update baseline after reviewing changes
cp audit_results/license_data_*.json new_baseline.json
```

---

## Advanced Usage

### Filtering Results
```bash
# Only show non-compliant packages
python compliance_checker.py --output-format json | jq '.prohibited_packages[]'

# Export specific license types
python license_checker.py --output-format csv | grep "MIT License"
```

### Automation Scripts
```bash
# Weekly check for new packages
python dependency_diff.py weekly_baseline.json | grep "Added Packages" && \
  echo "New packages detected - audit required"

# Pre-release compliance gate
python compliance_checker.py || echo "❌ Cannot release - license violations"
```

---

## File History

- **June 24, 2025:** Initial script suite created
- Scripts replace manual license investigation process
- Based on methodology from comprehensive manual audit achieving 100% compliance

---

## Support

For questions about these tools:
1. Check the comprehensive audit report: `LICENSE_AUDIT_REPORT_2025-06-24.md`
2. Review methodology: `AUDIT_PROCESS_DOCUMENTATION.md`
3. Test with: `python run_audit.py --quick` 