# Research Run Integrity Validation

## Quick Start for Auditors

The `validate_run_integrity.py` script provides comprehensive cryptographic validation of Discernus research runs.

### Basic Usage

```bash
# Navigate to the Discernus repository root
cd /path/to/discernus

# Validate a research run (basic check)
python3 scripts/validate_run_integrity.py projects/simple_test/runs/20250804T175152Z

# Detailed validation with verbose output
python3 scripts/validate_run_integrity.py projects/simple_test/runs/20250804T175152Z --verbose

# Include Git history validation
python3 scripts/validate_run_integrity.py projects/simple_test/runs/20250804T175152Z --check-git
```

### What Gets Validated

1. **Manifest Structure** - Ensures run metadata is complete and well-formed
2. **Results Files** - Verifies expected output files exist and are substantial
3. **Symlink Integrity** - Confirms all artifact links point to existing files
4. **Hash Integrity** - Validates cryptographic hashes match file contents
5. **Provenance Chain** - Verifies dependency relationships are complete
6. **Git History** (optional) - Confirms run exists in repository history

### Exit Codes

- `0` - All validations passed, run has cryptographic integrity
- `1` - One or more validations failed, investigation required

### Example Output

```
🔍 Discernus Research Run Integrity Validator
📁 Validating: projects/simple_test/runs/20250804T175152Z
🕐 Started: Mon Aug  4 18:21:54 EDT 2025
============================================================

📋 Manifest Structure:
----------------------------------------
✅ Manifest validation passed

📋 Results Files:
----------------------------------------
✅ Results files validation passed

📋 Symlink Integrity:
----------------------------------------
✅ All 6 symlinks verified

📋 Hash Integrity:
----------------------------------------
✅ All 6 content-addressed artifacts verified

📋 Provenance Chain:
----------------------------------------
✅ Provenance chain validated for 0 artifacts

============================================================
🎯 VALIDATION SUMMARY
✅ Checks Passed: 5/5

🎉 INTEGRITY VERIFICATION: PASSED
   This research run has cryptographic integrity.
   All artifacts are tamper-evident and traceable.
```

### Integration with Academic Workflows

This validation script can be integrated into:
- **Peer review processes** - Validate submitted research before review
- **Replication studies** - Verify integrity before attempting reproduction
- **Audit procedures** - Automated first-pass integrity checking
- **CI/CD pipelines** - Continuous validation of research outputs

### Technical Details

The script validates that:
- All content-addressed filenames match their SHA-256 hash prefixes
- Symlinks correctly point to shared cache artifacts
- Dependency chains are complete and traceable
- No artifacts have been tampered with or corrupted
- Research runs are properly documented and preserved

This provides mathematical proof of research integrity and enables trustworthy computational social science.