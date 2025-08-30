# Coherence Validation Test Results

## Test Overview
This directory contains a test of the new coherence validation system implemented in `DATA-003`. The test demonstrates that the system correctly catches missing grouping variables and statistical validity issues.

## Test Setup
1. **Original Experiment**: Copied from `projects/simple_test_pdaf/`
2. **Modified Experiment**: Added `Data Grouping and Custom Variable Mapping` section that references:
   - `political_era` grouping variable
   - `speaker_category` grouping variable
3. **Corpus Manifest**: Initially missing these grouping variables

## Test Results

### Test 1: Missing Grouping Variables (FAILED - As Expected)
**Command**: `python3 -m discernus.cli validate --strict`

**Result**: ❌ Coherence validation failed
**Blocking Issues**:
- The experiment requires statistical analysis using the grouping variables 'political_era' and 'speaker_category', but these variables are not defined in the corpus manifest's metadata for any document.
- The experiment specification does not provide a mapping to derive these variables from existing metadata fields.

**Validation Working**: ✅ The system correctly identified that the experiment referenced grouping variables that didn't exist in the corpus manifest.

### Test 2: Corrected Grouping Variables (FAILED - Statistical Validity Issues)
**Action**: Added missing grouping variables to corpus manifest:
- `political_era`: pre_obama, trump_era, post_trump
- `speaker_category`: institutional_establishment, populist_conservative, populist_progressive

**Result**: ❌ Coherence validation failed (different reason)
**Blocking Issues**:
- ANOVA requires n≥2 per group, but pre_obama (n=1) and trump_era (n=1) groups are too small
- T-tests cannot be performed between categories with insufficient sample sizes
- Correlation analysis impossible with n=1 groups

**Validation Working**: ✅ The system now correctly identified statistical validity issues rather than missing variable issues.

### Test 3: Dry Run Validation (PASSED - As Expected)
**Command**: `python3 -m discernus.cli validate --dry-run`

**Result**: ✅ Basic validation only (no coherence validation)
**Behavior**: The `--dry-run` flag correctly skips the expensive coherence validation step.

## Test Conclusions

### ✅ **Coherence Validation System Working Correctly**

1. **Missing Variable Detection**: The system correctly identifies when experiments reference grouping variables that don't exist in corpus manifests.

2. **Statistical Validity Checking**: Once variables are present, the system validates statistical requirements (group sizes, test appropriateness).

3. **Clear Error Messages**: The system provides specific, actionable feedback about what needs to be fixed.

4. **Proper Flag Behavior**: The `--dry-run` flag correctly skips expensive validation steps.

### 🔧 **Implementation Status**

The new coherence validation system from `DATA-003` is **fully functional** and correctly:

- Enforces the requirement that all grouping variables referenced in experiments must exist in corpus manifests
- Validates statistical executability requirements
- Provides clear, actionable error messages
- Integrates properly with the existing CLI validation system

### 📋 **Next Steps for Full Test**

To create a fully valid test case, the experiment specification should be updated to:
1. Remove requests for ANOVA with insufficient group sizes
2. Replace inferential tests with descriptive analysis appropriate for N=4
3. Designate single-document groups as baselines rather than analysis groups

This would demonstrate that the validation passes when all requirements are met.
