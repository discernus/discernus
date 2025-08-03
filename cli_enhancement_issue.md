# CLI Enhancement: Command Chaining and User Experience Improvements

## Summary

Improve Discernus CLI user experience with command chaining capabilities and streamlined workflows for common research patterns.

## Current State ✅

**Direct CLI Command - SOLVED**
- ✅ Package properly installed with `pip install -e .`
- ✅ Direct `discernus` command now works (was `python3 -m discernus.cli`)
- ✅ All individual commands function correctly
- ✅ Enhanced `promote` command with cleanup functionality
- ✅ Framework size limit increased from 15KB → 30KB

**Available Commands:**
```bash
discernus run projects/experiment
discernus promote projects/experiment --cleanup --force  
discernus validate projects/experiment
discernus list
discernus status
```

## Desired State 🎯

**Command Chaining Workflows**
Enable common research workflow patterns:
```bash
# Promote from workbench then run experiment
discernus promote run projects/experiment --cleanup

# Validate then run with confidence  
discernus validate run projects/experiment

# Full workflow: promote, validate, run
discernus promote validate run projects/experiment --cleanup
```

**Enhanced User Experience**
- Streamlined workflows for common patterns
- Fewer commands needed for typical research cycles
- Better error handling with early exit on failures
- Consistent option passing between chained commands

## Technical Issues 🔧

**Current Implementation Problems:**
1. **Click Argument Parsing**: `workflow` command has issues with variable arguments
   - Error: `Got unexpected extra arguments (validate run projects/experiment)`
   - Click struggling with `nargs=-1` before final experiment path argument

2. **Command Context Isolation**: Need proper context passing between chained commands
   - Options like `--cleanup`, `--force` should apply to relevant commands in chain
   - Error propagation and early exit on failures

## Implementation Strategy 💡

**Option 1: Fix Current Workflow Command**
- Debug Click argument parsing for variable operation lists
- Improve command context and option inheritance
- Add proper error handling and rollback

**Option 2: Dedicated Workflow Commands**  
- Create specific commands for common patterns:
  - `discernus deploy` (promote + validate + run)
  - `discernus iterate` (promote + run)
  - `discernus check` (validate + run)

**Option 3: Pipeline Syntax**
- Use pipe-like syntax: `discernus promote | run projects/experiment`
- More Unix-like approach to command composition

## Research Impact 📊

**Current Pain Points:**
- Researchers must remember multiple command sequences
- Manual coordination of promote → validate → run cycles  
- Verbose command syntax slows iteration

**Expected Benefits:**
- Faster research iteration cycles
- Reduced cognitive load for common workflows
- More natural command patterns matching research thinking
- Better error handling prevents partial workflow completion

## Acceptance Criteria ✅

- [ ] Command chaining works: `discernus promote run projects/experiment`
- [ ] Options properly inherit: `--cleanup` applies to promote, `--analysis-model` to run
- [ ] Early exit on failures with clear error messages
- [ ] Dry-run support shows complete workflow plan
- [ ] Backward compatibility maintained for individual commands
- [ ] Documentation updated with workflow examples

## Priority: Medium

This enhances user experience but doesn't block core functionality. Individual commands work well as workaround.

## Context

This issue emerged from Session 2025-08-02 where we:
- ✅ Successfully implemented direct `discernus` CLI command
- ✅ Enhanced promote command with automatic cleanup
- ✅ Increased framework size limits from 15KB to 30KB
- ⚠️ Attempted but couldn't complete command chaining due to Click parsing issues

The core CLI improvements are complete and functional. Command chaining is a nice-to-have enhancement for future development.