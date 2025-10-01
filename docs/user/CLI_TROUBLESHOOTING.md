# CLI Troubleshooting Guide

## Overview

This guide helps resolve common CLI issues and provides clear guidance on proper usage patterns for the Discernus CLI.

## Common Issues & Solutions

### 1. Phase Dependency Errors

**Problem**: `Phase dependency validation failed: Critical artifacts missing`

**Cause**: Attempting to run a phase that requires artifacts from previous phases that haven't been completed.

**Solutions**:
- **Fresh Run**: Start from an earlier phase that has all required dependencies
- **Resume Run**: Use `--resume` flag to copy artifacts from a completed run

**Examples**:
```bash
# ❌ This fails - statistical phase needs analysis artifacts
discernus run projects/my_experiment --from statistical --to statistical

# ✅ This works - start from analysis to create required artifacts
discernus run projects/my_experiment --from analysis --to statistical

# ✅ This works - resume from a completed run
discernus run projects/my_experiment --from statistical --to statistical --resume
```

### 2. Resume Artifact Copying

**Problem**: Resume only copies some phases, missing required artifacts

**Cause**: The source run doesn't have all required phases completed

**Solutions**:
- Check what phases are completed in the source run
- Use a different source run that has more phases completed
- Start from an earlier phase in the current run

**Examples**:
```bash
# Check available runs
ls projects/my_experiment/runs/

# Use a specific run that has more phases completed
discernus run projects/my_experiment --from synthesis --to synthesis --run-dir 20250101_120000
```

### 3. Skip Validation Issues

**Problem**: `Failed to populate CAS hashes: 'NoneType' object has no attribute 'log_agent_event'`

**Cause**: The `--skip-validation` flag has compatibility issues with the current audit system

**Solutions**:
- Avoid using `--skip-validation` flag
- Use normal validation (default behavior)
- If validation is slow, consider using a smaller test corpus

### 4. Error Message Interpretation

**Clear Error Messages**: The CLI provides specific, actionable error messages:

```
❌ Phase dependency validation failed: Critical artifacts missing for requested execution:
  • score_extraction (needed for statistical)
  • statistical_analysis (needed for evidence)
  • baseline_statistics (needed for synthesis)

This may indicate the run is incomplete or corrupted.
Try running from an earlier phase or check the source run integrity.
```

**What this means**:
- The statistical phase needs `score_extraction` from analysis
- The evidence phase needs `statistical_analysis` and `baseline_statistics` from statistical
- The synthesis phase needs all of the above

**How to fix**:
- Run from analysis to create score_extraction
- Or resume from a run that has these artifacts

## Best Practices

### 1. Development Workflow

```bash
# 1. Start with validation
discernus run projects/my_experiment --from validation --to validation

# 2. Test individual phases
discernus run projects/my_experiment --from analysis --to analysis
discernus run projects/my_experiment --from statistical --to statistical

# 3. Run full pipeline
discernus run projects/my_experiment --from validation --to synthesis
```

### 2. Resume Workflow

```bash
# 1. Check available runs
ls projects/my_experiment/runs/

# 2. Resume from a specific phase
discernus run projects/my_experiment --from statistical --to synthesis --resume

# 3. Use specific run if needed
discernus run projects/my_experiment --from synthesis --to synthesis --run-dir 20250101_120000
```

### 3. Debugging

```bash
# Enable verbose tracing
discernus run projects/my_experiment --verbose-trace

# Filter tracing to specific components
discernus run projects/my_experiment --trace-filter statistical --trace-filter analysis

# Check costs
discernus costs projects/my_experiment --detailed
```

## Phase Dependencies

Understanding phase dependencies is crucial for successful CLI usage:

```
validation → analysis → statistical → evidence → synthesis
```

**Critical Artifacts**:
- **statistical**: needs `score_extraction` from analysis
- **evidence**: needs `score_extraction`, `statistical_analysis`, `baseline_statistics`
- **synthesis**: needs `score_extraction`, `statistical_analysis`, `baseline_statistics`, `curated_evidence`

## Troubleshooting Checklist

1. **Check phase dependencies**: Ensure all required phases are completed
2. **Verify resume source**: Make sure the source run has the required phases
3. **Avoid skip-validation**: Don't use `--skip-validation` flag
4. **Check error messages**: Read the specific error messages for guidance
5. **Use appropriate start phase**: Start from the earliest phase that has all dependencies
6. **Verify experiment structure**: Ensure `experiment.md` exists and is valid

## Common Commands

```bash
# Basic usage
discernus run projects/my_experiment

# Specific phases
discernus run projects/my_experiment --from analysis --to statistical

# Resume from existing run
discernus run projects/my_experiment --from statistical --to synthesis --resume

# Use specific run directory
discernus run projects/my_experiment --from synthesis --to synthesis --run-dir 20250101_120000

# Check costs
discernus costs projects/my_experiment

# Resume command (alternative to --resume flag)
discernus resume projects/my_experiment --from statistical --to synthesis
```

## Getting Help

If you encounter issues not covered in this guide:

1. Check the error message carefully - it usually provides specific guidance
2. Verify your experiment structure and phase dependencies
3. Try running from an earlier phase
4. Use the resume functionality with a completed run
5. Check the audit logs in `runs/*/logs/` for detailed information
