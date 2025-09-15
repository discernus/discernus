# Inbox - Raw Backlog Items

**Purpose**: Raw capture of backlog items without organization or sprint planning. Items here will be groomed into organized sprints later.

**Usage**:

- "inbox this" → append new items here with minimal formatting
- "groom our sprints" → move all items from here to sprints.md with proper organization

---

## Items Moved to Sprints

**Note**: The following items have been organized into focused sprints and moved from this inbox:

- **Sprint 11**: Statistical Preparation & CSV Export (6 items)
- **Sprint 12**: Provenance System Restoration (4 items)
- **Sprint 13**: Code Quality & Architecture Cleanup (4 items)
- **Sprint 14**: Open Source Strategy & Licensing (6 items)
- **Sprint 15**: Academic Quality & Documentation (7 items)
- **Sprint 16**: Alpha Release Preparation (6 items)

**Total Items Organized**: 33 items moved to sprints

---

## Items Moved to Content Development

**Note**: The following research and content development items have been moved to content.md:

- **APDES Collection Issues**: 8 items (Issues #344, #343, #342, #341, #340, #339, #338, #337, #336)
- **Research & Development Issues**: 7 items (Issues #381, #279, #274, #240, #113, #109, #91, #29)

**Total Research Items Moved**: 15 items moved to content.md

---

## Items Moved to Later.md

**Note**: The following items have been moved to later.md for post-alpha development:

- **Potential Alpha Items**: 4 items (Issues #311, #233, #244, #230)
- **Research & Investigation**: 2 items (Issues #214, #213)
- **Platform Maturation**: 2 items (Issues #107, #60)
- **Backward Compatibility**: 1 item (Issue #232)

**Total Later.md Items**: 9 items moved to later.md

---

## Summary

**Sprint Grooming Complete**: Successfully organized all backlog items into focused areas:

- **Sprints**: 33 items organized into 6 focused sprints (Sprints 11-16)
- **Content Development**: 15 research items moved to content.md for future content development
- **Later.md**: 9 items moved to later.md for post-alpha development

**Total Items Processed**: 57 items

**Next Steps**: 
1. Begin execution of Sprint 16 (Alpha Release Preparation) as critical priority
2. Consider Sprint 11 (Statistical Preparation & CSV Export) as next priority after alpha release
3. Plan content development activities for post-alpha phase

**Inbox Status**: EMPTY - All items have been organized and moved to appropriate locations

---

## New Items (Post-Grooming)

### Bug: Intermittent Final Report Generation Failure

**Issue**: During gauntlet testing, first micro_test_experiment run failed to create final_report.md in outputs directory.

**Confirmed Facts**:
- **Nano test**: ✅ Final report created correctly in outputs
- **Micro test (first run)**: ❌ **NO final report in outputs** - only draft report in artifacts
- **Micro test (second run)**: ✅ Final report created correctly in outputs
- **1a_caf_civic_character**: ✅ Final report created correctly in outputs
- **1b_chf_constitutional_health**: ❌ **NO final report in outputs** - only draft report in artifacts, no assets.json
- **Manual fix applied**: Copied draft report to final_report.md for failed runs

**What We Know**:
- **Intermittent issue**: System works sometimes, fails other times
- **Draft report always created**: Draft synthesis report consistently appears in artifacts
- **Final report placement inconsistent**: Sometimes moved to outputs, sometimes not
- **No error messages**: System reports success even when final report missing
- **Archive works**: Archive process completes successfully regardless

**What We Don't Know**:
- **Trigger conditions**: What causes the intermittent failure?
- **Timing dependency**: Is it related to processing time or race conditions?
- **Cache interaction**: Does shared cache state affect final report creation?
- **Framework complexity**: Is it related to derived metrics or statistical analysis?
- **Logging gap**: No "Save final report" messages in logs when it should work

**Investigation Needed**:
- Test with different experiment sizes to identify pattern
- Check orchestrator logs for final report creation messages
- Verify assets structure consistency between successful/failed runs
- Test with different frameworks to isolate cause

**Priority**: Medium - Intermittent but real issue that should be fixed before alpha release

### Bug: Standalone Validation Command Failing

**Issue**: `discernus validate` command fails with parsing error on valid experiments.

**Symptoms**:
- **Standalone validation**: `discernus validate nano_test_experiment` fails with "Could not parse or reformat LLM response: Expecting value: line 1 column 1 (char 0)"
- **Orchestrator validation**: Works correctly during `discernus run` process
- **Experiments valid**: nano and micro tests run successfully despite validation error
- **Consistent failure**: Validation fails on clean state experiments

**Root Cause Analysis**:
- **Validator bug**: Standalone validation command has parsing issue
- **Orchestrator works**: Built-in validation during run process functions correctly
- **LLM response parsing**: Validation agent cannot parse LLM response format
- **Not experiment issue**: Same experiments work fine when run through orchestrator

**Impact**:
- **Severity**: Low - Core functionality works, just standalone validation broken
- **User Impact**: Users cannot validate experiments before running them
- **Workaround**: Run experiments directly - orchestrator validation works

**Investigation Needed**:
- Check validation agent LLM response parsing logic
- Compare standalone vs orchestrator validation code paths
- Test with different experiment types to confirm scope

**Priority**: Low - Non-blocking since orchestrator validation works

### Bug: CSV Export Files Not Generated

**Issue**: CSV export files (scores.csv, evidence.csv, metadata.csv) are not being created in the data/ directory despite being documented as a core feature.

**Symptoms**:
- **Data directory empty**: Only README.md present, no CSV files
- **Consistent across experiments**: Affects all recent runs (nano, micro, civic character, constitutional health)
- **Documentation mismatch**: data/README.md describes CSV files that don't exist
- **No error messages**: System reports success without indicating CSV generation failure

**Expected Behavior**:
- **scores.csv**: Analysis scores and derived metrics
- **evidence.csv**: Supporting quotes and evidence  
- **metadata.csv**: Document and run metadata
- **Statistical package**: Import scripts and examples

**What We Know**:
- **README exists**: data/README.md describes expected CSV files
- **Directory created**: data/ directory is created but remains empty
- **No error logging**: No indication of CSV generation failure
- **Affects all runs**: Consistent across different experiment types and sizes

**What We Don't Know**:
- **Root cause**: Why CSV generation is not happening
- **Code location**: Where CSV generation should occur in pipeline
- **Dependencies**: What triggers CSV file creation
- **Timing**: When in pipeline CSV generation should happen

**Investigation Needed**:
- Check orchestrator CSV generation logic
- Verify data export agent functionality
- Test CSV generation in isolation
- Compare with working CSV generation in other parts of system

**Priority**: Medium - Core feature missing, affects data analysis workflow

### Bug: Frequent LLM Timeouts During Analysis

**Issue**: LLM timeouts occur consistently every 12-15 documents during analysis phase, requiring automatic fallback to more expensive Pro model.

**Symptoms**:
- **Pattern timing**: Timeouts occur at regular intervals (12-15 documents)
- **Consistent across experiments**: Observed in both 1a_caf_civic_character and 1b_chf_constitutional_health
- **Flash model affected**: vertex_ai/gemini-2.5-flash times out, not Pro model
- **Automatic fallback works**: System correctly falls back to vertex_ai/gemini-2.5-pro
- **No data loss**: Analysis completes successfully after fallback

**Confirmed Facts**:
- **1a_caf_civic_character**: 1 timeout at document 3 (8 total documents)
- **1b_chf_constitutional_health**: 3 timeouts at documents 15, 30, and 45 (54 total documents)
- **Timeout pattern**: Approximately every 12-15 documents
- **Fallback success**: All timeouts resolved by switching to Pro model
- **Performance impact**: Pro model is significantly slower and more expensive

**What We Know**:
- **Consistent pattern**: Not random, follows predictable timing
- **Model-specific**: Only affects Flash model, not Pro
- **System resilience**: Automatic fallback mechanism works correctly
- **No data corruption**: Analysis results are complete and accurate
- **Cost implications**: Fallback increases processing time and API costs

**What We Don't Know**:
- **Root cause**: Why Flash model times out at regular intervals
- **Rate limiting**: Whether it's API rate limiting or model capacity
- **Document complexity**: If timeout correlates with document length/complexity
- **Caching effects**: Whether shared cache state affects timeout timing
- **Optimal batch size**: What document count prevents timeouts

**Investigation Needed**:
- Check LLM API rate limiting and quotas
- Analyze document complexity correlation with timeouts
- Test different batch sizes and processing intervals
- Investigate Flash model capacity limits
- Consider implementing progressive timeout handling

**Priority**: Medium - Affects performance and costs, but system remains functional

### Bug: Derived Metrics Calculation Not Working

**Issue**: Derived metrics functions execute but return raw analysis data instead of calculated values.

**Symptoms**:
- **Functions generated**: Derived metrics functions are created successfully
- **Execution appears successful**: No errors during derived metrics phase
- **Wrong data stored**: `derived_metrics_data` artifacts contain raw analysis results instead of calculated values
- **Missing calculated metrics**: No `relational_climate`, `emotional_balance`, `success_climate`, etc. values
- **CSV export affected**: `derived_metrics.csv` shows "no_derived_metrics_calculated"

**Root Cause**: `_execute_derived_metrics_functions()` in `clean_analysis_orchestrator.py` (lines 1522-1576) stores raw analysis results instead of calculated derived metrics.

**Evidence**:
- `derived_metrics_data` artifacts contain raw analysis results with `analysis_id`, `result_hash`, `result_content`
- Expected structure: `[{"document_id": "...", "relational_climate": 0.5, "emotional_balance": 0.3, ...}]`
- Actual structure: `[{"analysis_id": "...", "result_hash": "...", "result_content": {...}}]`

**Impact**: 
- No derived metrics available for CSV export
- Missing calculated metrics for analysis
- Core functionality not working

**Priority**: High - Core functionality missing, affects data analysis workflow

**Investigation Needed**:
- Debug `_execute_derived_metrics_functions()` execution
- Check if `calculate_derived_metrics(df)` is being called correctly
- Verify DataFrame conversion and derived metrics calculation
- Test derived metrics functions in isolation

### Bugs Moved to Sprint 16

**Note**: The following critical bugs have been moved to Sprint 16 (Alpha Release Preparation) for immediate resolution:

- **[ALPHA-008] Derived Metrics Synthesis Regression** - CRITICAL priority
- **[ALPHA-009] Derived Metrics Syntax Error** - HIGH priority

**Total Bugs Moved**: 2 critical bugs moved to Sprint 16

### Task: Cleanup Deprecated Agents

**Issue**: Remove deprecated agent implementations and consolidate to current architecture.

**Scope**:
- Identify deprecated agents in `/discernus/agents/` directory
- Remove obsolete agent files and configurations
- Update references to deprecated agents in codebase
- Ensure no breaking changes to current functionality

**Priority**: Low - Cleanup task for code quality and maintainability