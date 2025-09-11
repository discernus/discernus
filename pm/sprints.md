# Discernus v10 Sprints

**Purpose**: Organized backlog with sprint planning, dependencies, and detailed item specifications.

**Usage**:

- "groom our sprints" → organize inbox items into proper sprint structure
- Items moved here from inbox.md during grooming sessions

---

## Current Status

**Latest Updates**:

- ✅ **Sprint 12.1 COMPLETED**: Directory structure remediation with standard mode CSV export, dual directory consolidation, and complete specification compliance
- ✅ **Sprint 14 COMPLETED**: Open source strategy and licensing with multiple repository creation, GPL v3 license implementation, and public release branch preparation

**Current Focus**: System is stable with comprehensive validation, logging integrity, robust fallback handling, complete research transparency capabilities, full statistical preparation workflow with provenance integration, clean architecture with deprecated code removed, complete directory structure compliance, and open source strategy implemented with multiple repositories ready for public release

---

## Current Sprint Planning

**Next Priority**: Sprint 17 (Critical Bug Fixes) - URGENT PRIORITY
**Status**: Ready for execution
**Dependencies**: None - can begin immediately

**Previous Priority**: Sprint 16 (Alpha Release Preparation) - BLOCKED by critical bugs
**Status**: On hold until bugs are fixed
**Dependencies**: Sprint 17 completion required

---

## New Sprint Structure

---

### Sprint 17: Critical Bug Fixes (URGENT PRIORITY)

**Description**: Fix critical bugs discovered during gauntlet testing that block alpha release
**Purpose**: Resolve system reliability issues before proceeding with expensive experiments and alpha release
**Priority**: URGENT - System stability blockers
**Timeline**: 1-2 weeks - must complete before resuming gauntlet testing
**Dependencies**: None - can begin immediately

#### [BUG-001] Fix Intermittent Final Report Generation Failure

- **Description**: Fix intermittent bug where draft synthesis reports are created but not moved to outputs/final_report.md
- **Purpose**: Ensure consistent final report generation for all experiments
- **Priority**: HIGH - Core output missing
- **Acceptance Criteria**:
  - Final report consistently generated in outputs/ directory
  - No manual intervention required
  - assets.json file properly created with report_hash
  - All experiments produce final_report.md
- **Technical Details**:
  - Investigate orchestrator final report saving logic
  - Check for race conditions in synthesis completion
  - Verify assets.json generation and report_hash storage
  - Test with different framework complexities
- **Estimated Effort**: 2-3 days

#### [BUG-002] Fix CSV Export Generation

- **Description**: Implement missing CSV export functionality for scores.csv, evidence.csv, and metadata.csv
- **Purpose**: Enable data analysis workflow with structured data exports
- **Priority**: HIGH - Core feature missing
- **Acceptance Criteria**:
  - scores.csv with analysis scores and derived metrics
  - evidence.csv with supporting quotes and evidence
  - metadata.csv with document and run metadata
  - Statistical package with import scripts
  - All CSV files in data/ directory
- **Technical Details**:
  - Check orchestrator CSV generation logic
  - Verify data export agent functionality
  - Test CSV generation in isolation
  - Compare with working CSV generation in other parts of system
- **Estimated Effort**: 2-3 days

#### [BUG-003] Fix Standalone Validation Command

- **Description**: Fix `discernus validate` command parsing errors that prevent experiment validation
- **Purpose**: Enable users to validate experiments before running them
- **Priority**: MEDIUM - User workflow improvement
- **Acceptance Criteria**:
  - `discernus validate [experiment]` works correctly
  - No parsing errors on valid experiments
  - Consistent with orchestrator validation results
  - Clear error messages for invalid experiments
- **Technical Details**:
  - Check validation agent LLM response parsing logic
  - Compare standalone vs orchestrator validation code paths
  - Test with different experiment types
- **Estimated Effort**: 1-2 days

#### [BUG-004] Optimize LLM Timeout Handling

- **Description**: Investigate and optimize frequent LLM timeouts every 12-15 documents
- **Purpose**: Improve performance and reduce costs by minimizing Pro model fallbacks
- **Priority**: MEDIUM - Performance optimization
- **Acceptance Criteria**:
  - Reduced timeout frequency
  - Better timeout handling strategy
  - Maintained analysis quality
  - Lower processing costs
- **Technical Details**:
  - Check LLM API rate limiting and quotas
  - Analyze document complexity correlation with timeouts
  - Test different batch sizes and processing intervals
  - Investigate Flash model capacity limits
- **Estimated Effort**: 2-3 days

**Sprint 17 Success Criteria**:
- All 4 bugs resolved and tested
- Gauntlet testing can resume with confidence
- System stability improved for alpha release
- No regression in existing functionality

---

### Sprint 16: Alpha Release Preparation (BLOCKED - ON HOLD)

**Description**: Essential items required for alpha release readiness
**Purpose**: Ensure system is ready for alpha release with essential testing, basic documentation, and core performance validation
**Priority**: CRITICAL - Alpha release blockers (BLOCKED by Sprint 17)
**Timeline**: 2-3 weeks - must complete before alpha release
**Dependencies**: Sprint 17 completion required

#### [ALPHA-001] Essential Test Gauntlet Run

- **Description**: Run essential test suite to validate Alpha Release readiness using specific, appropriate experiments
- **Purpose**: Ensure core systems work correctly before release with concrete, measurable tests
- **Priority**: HIGH - Release validation
- **Acceptance Criteria**:
  - **Tier 1 Tests (Must Pass)**: nano_test_experiment and micro_test_experiment complete successfully
  - **Tier 2 Tests (Should Pass)**: At least 2 of 3 small experiments pass (business_ethics, entman_framing, lakoff_framing)
  - **Tier 3 Test (Nice to Pass)**: 1a_caf_civic_character completes successfully
  - **Tier 4 Tests (Culmination)**: 1b_chf_constitutional_health (54 docs, 30+ min) and vanderveen_presidential_pdaf (56 docs, 20+ min) complete successfully with clean runs (no shared cache)
- **Clean Slate Validation**: Each test starts with only essential files (corpus folder, experiment.md, framework, corpus manifest)
- **Full Pipeline Test**: `discernus run [relative path]` produces complete final_report.md with no "could not do" mentions or errors
- **Archive Validation**: Archive step places all assets in correct locations
- **Sequential CLI Test**: Step-by-step CLI execution (analysis only → check → continue → final) produces identical results
  - **Core Functionality**: CLI commands work, analysis completes, synthesis generates reports
  - **Framework Validation**: v10 frameworks parse and execute correctly
  - **Evidence Architecture**: Evidence retrieval and integration works
  - **No Critical Regressions**: All previously working functionality still works
  - **Results Documented**: Test results logged with pass/fail status and timing
- **Dependencies**: None
- **Effort**: 1 week

#### [ALPHA-002] Core Performance & Scalability Validation

- **Description**: Validate core performance characteristics and document basic scalability limits using specific experiments
- **Purpose**: Provide essential performance information for alpha users with concrete benchmarks
- **Priority**: HIGH - Release readiness
- **Acceptance Criteria**:
  - **Performance Benchmarks**: Document timing for nano (30s), micro (2min), small (5min), medium (10min), large (20-30min) experiments
  - **Resource Requirements**: Memory usage, disk space, API costs for each experiment tier
  - **Scalability Limits**: Maximum corpus size tested (56 documents for alpha), known breaking points
  - **Performance Targets**: nano < 1min, micro < 3min, small < 8min, medium < 15min, large < 45min
  - **Clean Run Validation**: Tier 4 tests complete successfully without shared cache (full system validation)
  - **Known Limitations**: Document what doesn't work and basic workarounds
  - **Cost Estimates**: API cost per document for different experiment sizes
  - **Release Readiness**: Clear go/no-go decision based on performance data
- **Dependencies**: [ALPHA-001]
- **Effort**: 1 week

#### [ALPHA-003] Essential Unit Testing Implementation

- **Description**: Implement focused unit testing for critical functions that can break silently
- **Purpose**: Prevent silent failures that could break research
- **Priority**: HIGH - Quality assurance
- **Acceptance Criteria**:
  - Framework validation tests (schema parsing, required field checking)
  - Statistical calculation tests (basic ANOVA, correlations, effect sizes)
  - Data validation tests (score range validation, JSON schema compliance)
  - All tests run in < 30 seconds with no flaky tests
  - Test coverage ≥ 60% for critical modules
- **Dependencies**: None
- **Effort**: 1 week

#### [ALPHA-004] Basic Automated Testing Infrastructure

- **Description**: Establish basic automated testing infrastructure for regression prevention
- **Purpose**: Catch regressions and maintain code quality during alpha development
- **Priority**: HIGH - Quality assurance
- **Acceptance Criteria**:
  - All existing tests pass without import errors
  - Automated test suite runs in < 30 seconds
  - Basic GitHub Actions workflow for core tests
  - Test coverage ≥ 60% for core modules
  - Critical functions have unit tests
  - No flaky or non-deterministic tests
- **Dependencies**: [ALPHA-003]
- **Effort**: 1 week

#### [ALPHA-005] Essential Alpha Documentation

- **Description**: Complete documentation consolidation and create missing components for Alpha Release
- **Purpose**: Provide comprehensive, well-organized documentation for alpha users and developers
- **Priority**: HIGH - Essential for alpha users
- **Status**: ✅ COMPLETE - Full documentation consolidation and architecture reorganization implemented
- **Acceptance Criteria**:
  - **✅ Installation Guide**: COMPLETE - Moved to `docs/user/INSTALLATION_GUIDE.md`
  - **✅ CLI Reference**: COMPLETE - Consolidated in `docs/user/CLI_REFERENCE.md`
  - **✅ Troubleshooting**: COMPLETE - Moved to `docs/user/TROUBLESHOOTING_GUIDE.md`
  - **✅ Experiment Guide**: COMPLETE - Integrated into user documentation
  - **✅ Quick Start Guide**: COMPLETE - Created `docs/user/QUICK_START_GUIDE.md` with 5-minute tutorial
  - **✅ Performance Guide**: COMPLETE - Created `docs/user/PERFORMANCE_GUIDE.md` with benchmarks
  - **✅ Release Notes**: COMPLETE - Created `docs/user/RELEASE_NOTES.md` with alpha features
  - **✅ Documentation Cleanup**: COMPLETE - Full consolidation with user/developer separation
- **Consolidation Results**:
  - **New Structure**: `docs/user/` for users, `docs/developer/` for developers
  - **Navigation**: Clear entry points for each user type
  - **Content**: Consolidated duplicate documentation
  - **Archives**: Moved outdated docs to `docs/archive/`
  - **Cross-References**: Updated all links and navigation
- **Files Created**:
  - `docs/user/README.md` - Main user entry point
  - `docs/user/QUICK_START_GUIDE.md` - 5-minute tutorial
  - `docs/user/PERFORMANCE_GUIDE.md` - Performance benchmarks
  - `docs/user/RELEASE_NOTES.md` - Alpha release notes
  - `docs/user/PROVENANCE_GUIDE.md` - User-friendly research tracking guide
  - `docs/README.md` - Main documentation index
  - `docs/archive/README.md` - Archive documentation
- **Files Moved**:
  - `docs/INSTALLATION_GUIDE.md` → `docs/user/`
  - `docs/CLI_REFERENCE.md` → `docs/user/`
  - `docs/SYSTEM_STATUS.md` → `docs/user/`
  - `docs/developer/troubleshooting/TROUBLESHOOTING_GUIDE.md` → `docs/user/`
  - `docs/PROVENANCE_SYSTEM.md` → `docs/architecture/`
  - `docs/synthesis_agent_architecture_v2.md` → `docs/archive/`
  - `docs/ARCHIVE.md` → `docs/archive/`
  - `docs/architecture/DISCERNUS_SYSTEM_ARCHITECTURE.md` → `docs/developer/architecture/`
  - `docs/architecture/DUAL_TRACK_LOGGING_ARCHITECTURE.md` → `docs/developer/architecture/`
  - `docs/architecture/typesense_bm25_pipeline_documentation.md` → `docs/developer/architecture/`
  - `docs/architecture/INTEGRATED_PROVENANCE_VALIDATION_SPEC.md` → `docs/archive/`
- **Dependencies**: [ALPHA-001], [ALPHA-002] - Performance data from gauntlet testing
- **Effort**: 1 week (7-11 hours total) - COMPLETED

#### [ALPHA-006] CLI Help Text Cleanup

- **Description**: Streamline and simplify CLI help text to reduce verbosity and improve usability
- **Purpose**: Make CLI more user-friendly by providing concise, focused help information
- **Priority**: MEDIUM - User experience improvement
- **Acceptance Criteria**:
  - **Concise Help**: Main help shows only essential commands with brief descriptions
  - **Hierarchical Help**: Detailed help available via --help flag for specific commands
  - **Clear Examples**: Each command shows 1-2 practical examples
  - **Remove Redundancy**: Eliminate repetitive or overly verbose explanations
  - **Focus on Core**: Prioritize run, validate, list commands in main help
  - **Consistent Format**: Standardized help text format across all commands
  - **Quick Reference**: Help text fits in standard terminal without scrolling
- **Dependencies**: None
- **Effort**: 2-3 days

#### [ALPHA-007] Promote Function and Workbench Concept Review

- **Description**: Examine and evaluate the promote function and workbench concept in the CLI for alpha release readiness
- **Purpose**: Ensure promote functionality and workbench concept are properly implemented and documented for alpha users
- **Priority**: MEDIUM - Feature completeness
- **Acceptance Criteria**:
  - **Promote Function Analysis**: Review current promote command implementation and functionality
  - **Workbench Concept Review**: Examine workbench directory structure and usage patterns
  - **Integration Assessment**: Evaluate how promote and workbench integrate with core CLI workflow
  - **Documentation Gap Analysis**: Identify missing documentation for promote and workbench features
  - **User Experience Review**: Assess usability and discoverability of promote/workbench features
  - **Alpha Readiness**: Determine if promote/workbench features are ready for alpha release
  - **Recommendations**: Provide specific recommendations for improvement or removal
  - **Implementation Plan**: If needed, create plan for completing or fixing promote/workbench functionality
- **Dependencies**: None
- **Effort**: 3-4 days

---

## Current Sprint Planning

**Next Priority**: Sprint 16 (Alpha Release Preparation) - CRITICAL PRIORITY
**Status**: Ready for execution
**Dependencies**: None - can begin immediately
