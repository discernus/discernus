# Discernus Gauntlet Test Results

**Purpose**: Results from systematic testing of the Discernus analysis pipeline across different experiment sizes and complexities.

**Test Date**: September 11, 2025
**Status**: Gauntlet testing paused due to critical bugs discovered

---

## Test Results Summary

### Tier 1 Tests (Small - 2-4 documents)
- ✅ **nano_test_20250911T153727Z** - 2 documents, ~2 minutes
- ✅ **micro_test_20250911T000619Z** - 4 documents, ~3 minutes

### Tier 2 Tests (Small - 4 documents)  
- ✅ **business_ethics_20250904T121503Z** - 4 documents, ~8 minutes
- ✅ **entman_framing_20250829T185822Z** - 4 documents, ~10 minutes

### Tier 3 Tests (Medium - 8 documents)
- ✅ **civic_character_20250910T223449Z** - 8 documents, ~21 minutes

### Tier 4 Tests (Large - 54 documents)
- ✅ **constitutional_health_20250911T181940Z** - 54 documents, ~2.5 hours

---

## Critical Issues Discovered

### 1. Intermittent Final Report Generation Failure
- **Symptom**: Draft reports created but not moved to outputs/final_report.md
- **Affected**: micro_test (first run), constitutional_health
- **Status**: Manual fix applied, root cause unknown

### 2. CSV Export Files Not Generated
- **Symptom**: No scores.csv, evidence.csv, metadata.csv in data/ directory
- **Affected**: All experiments
- **Status**: Core feature completely missing

### 3. Standalone Validation Command Failing
- **Symptom**: `discernus validate` fails with parsing errors
- **Affected**: All experiments
- **Status**: Orchestrator validation works, standalone broken

### 4. Frequent LLM Timeouts
- **Symptom**: Flash model timeouts every 12-15 documents
- **Affected**: civic_character, constitutional_health
- **Status**: Automatic fallback works, but increases costs

---

## Next Steps

**Sprint 17: Critical Bug Fixes** has been created to address these issues before resuming gauntlet testing.

**Remaining Tests**:
- vanderveen_presidential_pdaf (56 documents, 20+ minutes) - BLOCKED until bugs fixed

---

## Directory Structure

Each test directory contains:
- `outputs/` - Main results (final_report.md, statistics, evidence)
- `artifacts/` - Raw LLM responses and intermediate data
- `session_logs/` - Execution logs and performance metrics
- `data/` - CSV export files (currently empty due to bug)
- `statistical_package/` - Statistical analysis outputs
- `inputs/` - Input materials (framework, corpus, experiment)
- `provenance/` - Provenance tracking data
