# Provenance Validation Reference

**Quick reference for validating Discernus research run integrity**

## Validation Script Usage

### Basic Commands

```bash
# Quick integrity check (recommended for all audits)
python3 scripts/validate_run_integrity.py projects/experiment/runs/20250804T175152Z

# Verbose output showing all validation steps
python3 scripts/validate_run_integrity.py projects/experiment/runs/20250804T175152Z --verbose

# Include Git history validation
python3 scripts/validate_run_integrity.py projects/experiment/runs/20250804T175152Z --check-git
```

### Exit Codes

- **0**: All validations passed, run has integrity
- **1**: One or more validations failed, investigation required

## Validation Checks

### 1. Manifest Structure
**Validates**: Run metadata completeness and format
```bash
✅ Manifest validation passed
```
**Checks**:
- Required fields present in `run_metadata`
- Performance metrics show completion
- Execution record is well-formed

### 2. Results Files
**Validates**: Expected output files exist and are substantial
```bash
✅ Results files validation passed
```
**Checks**:
- `final_report.md` exists and has content
- `scores.csv`, `evidence.csv`, `metadata.csv` present
- File sizes are reasonable (not empty)

### 3. Symlink Integrity
**Validates**: All artifact links point to existing files
```bash
✅ All 6 symlinks verified
```
**Checks**:
- Symlinks in `artifacts/` resolve correctly
- Target files exist in shared cache
- No broken links in provenance chain

### 4. Hash Integrity
**Validates**: Content matches expected SHA-256 hashes
```bash
✅ All 6 content-addressed artifacts verified
```
**Checks**:
- Filename hash prefixes match actual file content
- SHA-256 computation validates against 8-character prefix
- No content corruption detected

### 5. Provenance Chain
**Validates**: Complete dependency relationships
```bash
✅ Provenance chain validated for 0 artifacts
```
**Checks**:
- Dependencies listed in artifact metadata exist
- Recursive dependency resolution complete
- No missing links in provenance graph

### 6. Git History (Optional)
**Validates**: Run exists in Git repository history
```bash
✅ Found 1 Git commits referencing this run
```
**Checks**:
- Git log contains references to run ID
- Commit history shows research preservation
- Repository integrity maintained

## Example Output

### Successful Validation
```
🔍 Discernus Research Run Integrity Validator
📁 Validating: projects/simple_test/runs/20250804T175152Z
🕐 Started: Mon Aug  4 18:21:54 EDT 2025
============================================================

📋 Manifest Structure:
✅ Manifest validation passed

📋 Results Files:
✅ Results files validation passed

📋 Symlink Integrity:
✅ All 6 symlinks verified

📋 Hash Integrity:
✅ All 6 content-addressed artifacts verified

📋 Provenance Chain:
✅ Provenance chain validated for 0 artifacts

============================================================
🎯 VALIDATION SUMMARY
✅ Checks Passed: 5/5

🎉 INTEGRITY VERIFICATION: PASSED
   This research run has consistent content-addressed integrity.
   All artifacts match expected hashes and are traceable.
```

### Failed Validation
```
🔍 Discernus Research Run Integrity Validator
📁 Validating: projects/experiment/runs/20250804T175152Z
============================================================

📋 Hash Integrity:
❌ ERROR: Found 2 hash mismatches:
  analysis_response_185f5e58.json: expected 185f5e58, got a1b2c3d4

📋 Symlink Integrity:
❌ ERROR: Found 1 broken symlinks:
  artifacts/missing_file.json → ../../shared_cache/artifacts/missing_file.json (missing)

============================================================
🎯 VALIDATION SUMMARY
✅ Checks Passed: 3/5
❌ Errors: 3
   • Found 2 hash mismatches
   • Found 1 broken symlinks
   • Git validation failed

⚠️  INTEGRITY VERIFICATION: FAILED
   Issues detected that require investigation.
```

## Manual Verification Commands

### Hash Verification
```bash
# Verify specific artifact integrity
sha256sum artifacts/analysis_results/analysis_response_185f5e58.json
# Should start with: 185f5e58...

# Check all statistical results
sha256sum artifacts/statistical_results/*.json
```

### Git History Check
```bash
# Find commits referencing this run
git log --oneline --grep="20250804T175152Z"

# Check repository status
git status

# Verify run is committed
git ls-files projects/experiment/runs/20250804T175152Z/
```

### Symlink Validation
```bash
# Check all symlinks resolve
find artifacts/ -type l -exec ls -la {} \;

# Verify shared cache exists
ls -la projects/experiment/shared_cache/artifacts/

# Test specific symlink
readlink artifacts/analysis_results/analysis_response_185f5e58.json
```

### Dependency Chain Check
```bash
# Examine provenance metadata
cat artifacts/provenance.json | jq '.'

# Check for dependency information
grep -r "dependencies" artifacts/*/

# Validate artifact registry
ls -la projects/experiment/shared_cache/artifacts/ | wc -l
```

## Troubleshooting

### Common Validation Failures

**Hash Mismatches**:
```
❌ ERROR: analysis_response_185f5e58.json: expected 185f5e58, got a1b2c3d4
```
**Cause**: File content changed after creation  
**Fix**: Check for file corruption, re-run analysis if needed

**Broken Symlinks**:
```
❌ ERROR: artifacts/missing_file.json → ../../shared_cache/missing_file.json (missing)
```
**Cause**: Shared cache artifact deleted or moved  
**Fix**: Check shared cache integrity, restore from backup

**Git History Missing**:
```
⚠️  WARNING: Run 20250804T175152Z not found in Git history
```
**Cause**: Run not committed to Git (auto-commit disabled or failed)  
**Fix**: Manually commit run directory

**Empty Results Files**:
```
⚠️  WARNING: Empty results files: ['scores.csv', 'evidence.csv']
```
**Cause**: Analysis or synthesis pipeline failure  
**Fix**: Check logs for errors, re-run experiment

### Recovery Procedures

**Restore Missing Artifacts**:
1. Check if artifacts exist elsewhere: `find . -name "*185f5e58*"`
2. Verify shared cache: `ls projects/experiment/shared_cache/artifacts/`
3. Re-run analysis if artifacts are truly missing
4. Validate after recovery: `python3 scripts/validate_run_integrity.py [path]`

**Fix Git Issues**:
1. Add run manually: `git add projects/experiment/runs/20250804T175152Z`
2. Commit: `git commit -m "Recover run 20250804T175152Z"`
3. Validate: `python3 scripts/validate_run_integrity.py [path] --check-git`

**Repair Symlinks**:
1. Check target exists: `ls ../../shared_cache/artifacts/[hash].json`
2. Recreate symlink: `ln -sf ../../shared_cache/artifacts/[hash].json artifacts/[dir]/[file]`
3. Validate: `python3 scripts/validate_run_integrity.py [path]`

## Integration with Workflows

### Academic Submission Checklist
```bash
# Before paper submission
for run in projects/my_study/runs/*/; do
    echo "Validating $run"
    python3 scripts/validate_run_integrity.py "$run" --check-git
done
```

### Collaboration Workflow
```bash
# Before sharing with collaborators
python3 scripts/validate_run_integrity.py projects/shared_study/runs/20250804T175152Z

# After receiving shared work
git pull
python3 scripts/validate_run_integrity.py projects/shared_study/runs/20250804T175152Z --verbose
```

### Backup Verification
```bash
# Verify backup integrity
for backup_run in backup/projects/*/runs/*/; do
    python3 scripts/validate_run_integrity.py "$backup_run"
done
```

## Advanced Usage

### Custom Validation Scripts
```python
#!/usr/bin/env python3
"""Custom validation for specific research requirements"""

import json
from pathlib import Path
import subprocess
import sys

def validate_research_standards(run_path):
    """Validate custom research standards"""
    run_path = Path(run_path)
    
    # Load manifest
    manifest = json.loads((run_path / "manifest.json").read_text())
    
    # Custom checks
    assert manifest["costs"]["total_cost_usd"] < 10.00, "Cost too high"
    assert len(manifest.get("corpus_files", [])) >= 5, "Insufficient corpus size"
    
    # Run standard validation
    result = subprocess.run([
        "python3", "scripts/validate_run_integrity.py", 
        str(run_path), "--check-git"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Standard validation failed:")
        print(result.stdout)
        sys.exit(1)
    
    print("✅ All validations passed (including custom checks)")

if __name__ == "__main__":
    validate_research_standards(sys.argv[1])
```

### Batch Validation
```bash
#!/bin/bash
# Validate all runs in a project

PROJECT_PATH="projects/my_study"
FAILED_RUNS=()

echo "🔍 Validating all runs in $PROJECT_PATH"

for run_dir in "$PROJECT_PATH"/runs/*/; do
    if [ -d "$run_dir" ]; then
        run_id=$(basename "$run_dir")
        echo "Validating $run_id..."
        
        if python3 scripts/validate_run_integrity.py "$run_dir" --check-git > /dev/null 2>&1; then
            echo "✅ $run_id: PASSED"
        else
            echo "❌ $run_id: FAILED"
            FAILED_RUNS+=("$run_id")
        fi
    fi
done

echo
echo "🎯 BATCH VALIDATION SUMMARY"
echo "Total runs validated: $(find "$PROJECT_PATH"/runs/ -maxdepth 1 -type d | wc -l | tr -d ' ')"
echo "Failed runs: ${#FAILED_RUNS[@]}"

if [ ${#FAILED_RUNS[@]} -gt 0 ]; then
    echo "Failed run IDs:"
    printf '  • %s\n' "${FAILED_RUNS[@]}"
    exit 1
else
    echo "✅ All runs passed validation"
fi
```

## Performance Notes

### Validation Speed
- **Quick check**: ~2-5 seconds per run
- **Verbose check**: ~5-10 seconds per run  
- **Git history check**: +2-3 seconds per run
- **Large runs (>100MB)**: May take 30+ seconds for hash verification

### Optimization Tips
- Use quick validation for routine checks
- Save verbose validation for debugging
- Batch validate multiple runs in parallel
- Skip Git validation for local-only workflows

## Conclusion

The validation system provides **comprehensive integrity checking** for Discernus research runs. Use it regularly to:

- ✅ **Verify research integrity** before submission
- ✅ **Debug issues** with verbose output
- ✅ **Prepare for peer review** with complete validation
- ✅ **Ensure collaboration quality** when sharing work
- ✅ **Maintain backup integrity** over time

**Default workflow**: Run quick validation before any important milestone, use verbose validation for troubleshooting.