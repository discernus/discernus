# Auditing Tools

This directory contains tools for validating and auditing research run integrity and experimental provenance.

## Tools

### `validate_run_integrity.py`
**Purpose**: Comprehensive integrity validation of research run consistency  
**Usage**: `python3 scripts/auditing/validate_run_integrity.py <run_path> [options]`  
**Features**:
- Content-addressed hash verification
- Provenance chain validation
- Git repository integrity checks
- Comprehensive error reporting and logging
- Verbose mode for detailed diagnostics

**Example**:
```bash
python3 scripts/auditing/validate_run_integrity.py projects/simple_test/runs/20250804T175152Z --verbose
python3 scripts/auditing/validate_run_integrity.py projects/simple_test/runs/20250804T175152Z --check-git
```

### `README_validation.md`
**Purpose**: Documentation and guidelines for validation processes  
**Content**: Best practices and procedures for research validation

## Integration Status

✅ **ACTIVELY USED** - The `validate_run_integrity.py` script is referenced in:
- `discernus/core/provenance_organizer.py` for automated validation
- Makefile targets for manual validation workflows

## Use Cases

1. **Research Auditing**: Verify that research runs maintain complete integrity
2. **Provenance Validation**: Ensure all artifacts are properly content-addressed
3. **Git Integration**: Validate that research artifacts are properly committed
4. **Quality Assurance**: Automated checks for research reproducibility

## Dependencies

- Standard Python libraries (hashlib, json, subprocess)
- Git (for repository integrity checks)
- No external dependencies required

## Output

The validator provides:
- ✅ Success indicators for passed checks
- ❌ Error reports for integrity violations  
- ⚠️ Warnings for potential issues
- Detailed logs in verbose mode
- Exit codes for automation integration
