# Discernus v10 Sprints

**Purpose**: Organized backlog with sprint planning, dependencies, and detailed item specifications.

**Usage**:

- "groom our sprints" → organize inbox items into proper sprint structure
- Items moved here from inbox.md during grooming sessions

---

## Current Status

**Date**: 2025-01-27
**Status**: Sprints 5 & 6 Completed - Ready for Sprint 7
**Next Priority**: Sprint 7 (Research Validation & Experimental Studies)

**Infrastructure Status**:

- ✅ **Sprints 1-6**: All completed successfully (moved to done.md)
- ✅ **Critical Issues**: All CRITICAL-001 through CRITICAL-005 resolved
- ✅ **Core Features**: CLI v10, Statistical Pipeline, Framework Validation operational
- ✅ **Quality Enhancements**: Caching, logging, data quality, evidence retrieval optimized
- ✅ **Architecture**: THIN architecture principles established and maintained
- ✅ **CLI UX**: Command structure optimized, help text improved, path handling standardized
- ✅ **Ready for Sprint 7**: Research validation and experimental studies

---

## Current Sprint Planning

---

---

### Sprint 9: Bug Fixes & Stability (HIGH PRIORITY)

**Timeline**: 1-2 weeks
**Goal**: Address critical bugs and stability issues affecting core functionality

#### [BUG-001] CLI Flag Compliance Gap - Synthesis Model Selection

- **Description**: Synthesis stage agents default to Flash instead of Flash Lite despite explicit CLI specification
- **Problem**: CLI allows specifying Flash Lite for synthesis, but agents ignore this and use Flash
- **Impact**: Unexpected cost increases and performance issues
- **Root Cause**: Agent-level model selection logic not respecting CLI flags
- **Solution**:
  - Audit all synthesis agents for model selection logic
  - Ensure CLI flags are properly passed through to agent execution
  - Add validation to verify model selection matches CLI specification
  - Update agent base classes to handle model selection consistently
- **Testing**: Verify CLI flag compliance across all synthesis operations
- **Effort**: 4-6 hours
- **Priority**: HIGH - Affects cost and performance predictability
- **Status**: PENDING

#### [BUG-002] Cost Tracking Reporting Zero Costs

- **Description**: CLI shows $0.0000 and 0 tokens even when cost log contains actual usage data (~$0.003, 23K tokens)
- **Problem**: Cost tracking display is broken, showing zeros despite successful LLM calls
- **Impact**: Users cannot monitor actual costs, affecting budget management
- **Investigation**:
  - Check cost tracking integration with LLM gateway
  - Verify cost data collection and storage
  - Identify disconnect between actual costs and display logic
  - Ensure cost tracking works across all model types
- **Solution**: Fix cost data retrieval and display in CLI output
- **Testing**: Verify cost reporting accuracy across different scenarios
- **Effort**: 2-3 hours
- **Priority**: HIGH - Affects financial visibility
- **Status**: PENDING

#### [BUG-003] CLI Dry Run Strict Validation Broken

- **Description**: Dry run only performs basic check, Helen coherence validation not engaged
- **Problem**: Dry run mode doesn't execute full validation suite, missing critical coherence checks
- **Impact**: False confidence in experiment validity before actual execution
- **Root Cause**: Dry run bypasses Helen validation system
- **Solution**:
  - Integrate Helen coherence validation into dry run mode
  - Ensure all validation checks run in dry run (without expensive operations)
  - Provide clear feedback on what validations were performed
  - Maintain performance benefits of dry run while ensuring completeness
- **Testing**: Verify dry run catches same issues as full validation
- **Effort**: 3-4 hours
- **Priority**: HIGH - Affects experiment reliability
- **Status**: PENDING

#### [CLI-UX-012] CLI Model Validation Missing

- **Task**: Add CLI validation that specified models exist in `models.yaml` before running experiments
- **Problem**: CLI does not validate that specified models exist in `models.yaml` before running experiments, leading to runtime failures after hours of execution
- **Current Behavior**:
  - CLI accepts any model string without validation
  - Experiment runs until it hits the model at execution time
  - Poor user experience: fails late with confusing errors
- **What Should Happen**:
  - CLI validates models against `models.yaml` before proceeding
  - Fast failure with clear error messages
  - Prevents wasted time and resources
- **Impact**: User confusion, wasted experiment time, poor error handling
- **Priority**: HIGH - Affects user experience and resource efficiency
- **Files to Modify**: `discernus/cli.py` - add model validation layer
- **Effort**: 2-3 hours
- **Status**: **PENDING**

---
