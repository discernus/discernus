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

**Alpha Model Strategy**: Vertex AI only for alpha release to ensure complete end-to-end testing and reliability. Future releases will consider additional LLM support based on user feedback and testing requirements.

---

## Current Sprint Planning

**Next Priority**: Sprint 16 (Alpha Release Preparation) - READY TO BEGIN
**Status**: Ready for execution - Sprint 17 blockers resolved
**Dependencies**: Sprint 17 completion ✅ **COMPLETED**

**Previous Priority**: Sprint 17 (Critical Bug Fixes) - ✅ **COMPLETED**
**Status**: All 4 critical bugs resolved and tested
**Dependencies**: None - completed successfully

---

## New Sprint Structure

---

### Sprint 17: Critical Bug Fixes ✅ **COMPLETED**

**Description**: Fix critical bugs discovered during gauntlet testing that block alpha release
**Purpose**: Resolve system reliability issues before proceeding with expensive experiments and alpha release
**Priority**: URGENT - System stability blockers
**Timeline**: 1-2 weeks - must complete before resuming gauntlet testing
**Dependencies**: None - can begin immediately
**Status**: ✅ **COMPLETED** - All 4 critical bugs resolved and tested

#### [BUG-001] Fix Intermittent Final Report Generation Failure ✅ **COMPLETED**

- **Description**: Fix intermittent bug where draft synthesis reports are created but not moved to outputs/final_report.md
- **Purpose**: Ensure consistent final report generation for all experiments
- **Priority**: HIGH - Core output missing
- **Acceptance Criteria**:
  - Final report consistently generated in outputs/ directory ✅
  - No manual intervention required ✅
  - assets.json file properly created with report_hash ✅
  - All experiments produce final_report.md ✅
- **Solution**: Fixed JSON serialization error with NumPy types in _create_clean_outputs_directory
- **Technical Details**:
  - Root cause: TypeError when serializing np.bool_, np.integer, np.floating to JSON
  - Added convert_to_serializable() helper function to handle NumPy types
  - Prevents silent fallback to basic_outputs_created status
  - Final report and assets.json now generate consistently
- **Estimated Effort**: 2-3 days

#### [BUG-002] Fix CSV Export Generation ✅ **COMPLETED**

- **Description**: Implement missing CSV export functionality for scores.csv, evidence.csv, and metadata.csv
- **Purpose**: Enable data analysis workflow with structured data exports
- **Priority**: HIGH - Core feature missing
- **Acceptance Criteria**:
  - scores.csv with analysis scores and derived metrics ✅
  - evidence.csv with supporting quotes and evidence ✅
  - metadata.csv with document and run metadata ✅
  - Statistical package with import scripts ✅
  - All CSV files in data/ directory ✅
- **Solution**: Implemented direct CSV generation in Phase 8.5 using in-memory data
- **Technical Details**:
  - Replaced complex artifact loading with direct data conversion
  - Generate CSV files when all data is available in memory
  - Fixed data structure parsing for dimensional scores and evidence quotes
  - All three CSV files now working properly with real data
- **Estimated Effort**: 2-3 days

#### [BUG-003] Fix Standalone Validation Command ✅ **COMPLETED**

- **Description**: Fix `discernus validate` command parsing errors that prevent experiment validation
- **Purpose**: Enable users to validate experiments before running them
- **Priority**: MEDIUM - User workflow improvement
- **Acceptance Criteria**:
  - ✅ `discernus validate [experiment]` works correctly
  - ✅ No parsing errors on valid experiments
  - ✅ Consistent with orchestrator validation results
  - ✅ Clear error messages for invalid experiments
- **Solution**: Enhanced JSON parsing in ExperimentCoherenceAgent to handle markdown code blocks
- **Technical Details**:
  - Added robust JSON extraction from LLM responses with markdown code block support
  - Handles both ```json and ``` code block formats
  - Maintains THIN principles with graceful fallbacks
  - Tested with nano_test_experiment and micro_test_experiment
- **Estimated Effort**: 1-2 days

#### [BUG-004] Optimize LLM Timeout Handling ✅ **COMPLETED**

- **Description**: Investigate and optimize frequent LLM timeouts every 12-15 documents
- **Purpose**: Improve performance and reduce costs by minimizing Pro model fallbacks
- **Priority**: MEDIUM - Performance optimization
- **Acceptance Criteria**:
  - ✅ Reduced timeout frequency
  - ✅ Better timeout handling strategy
  - ✅ Maintained analysis quality
  - ✅ Lower processing costs
- **Solution**: Increased Gemini 2.5 Flash model timeout from 300s to 600s for better batch processing
- **Technical Details**:
  - Root cause: Flash model 300s timeout too short for processing 12-15 documents
  - Increased timeout to 600s (10 minutes) to handle larger batches
  - Maintained immediate fallback to Pro model on timeout
  - Updated model configuration and documentation
  - Pro model timeout remains 500s for synthesis tasks
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

#### [ALPHA-006] Alpha Model Strategy Documentation

- **Description**: Document Vertex AI-only approach for alpha release with future LLM expansion roadmap
- **Purpose**: Set clear expectations for alpha users and prevent untested model combinations
- **Priority**: HIGH - User expectation management
- **Acceptance Criteria**:
  - Clear documentation that alpha release is Vertex AI only
  - Explanation of why this approach ensures reliability
  - Roadmap for future LLM support in post-alpha releases
  - Warning against using non-Vertex models in alpha
  - Model selection guidance for alpha users
- **Dependencies**: None
- **Effort**: 1 day
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

### Sprint 18: Agent Parsing Consistency (HIGH PRIORITY)

**Description**: Update all agents to use consistent "raw Python objects, no JSON parsing" pattern
**Purpose**: Eliminate parsing errors and align all agents with the system's current architecture
**Priority**: HIGH - System consistency and reliability
**Timeline**: 1-2 weeks
**Dependencies**: Sprint 17 completion (critical bugs must be fixed first)

#### [CONSISTENCY-001] Update DerivedMetricsAgent to Raw Python Pattern

- **Description**: Fix DerivedMetricsAgent parsing error by adopting the same pattern as UnifiedSynthesisAgent
- **Purpose**: Eliminate `'\n        "metric_name_1"'` parsing error and make agent consistent with system architecture
- **Priority**: HIGH - Currently blocking statistical prep feature
- **Status**: Ready for execution
- **Root Cause**: Agent still uses old JSON/delimiter parsing while system has moved to raw Python objects
- **Current Error**: `'\n        "metric_name_1"'` - string processing failure in function generation
- **Solution Pattern**: Follow UnifiedSynthesisAgent approach:
  - Skip all LLM response parsing
  - Save raw LLM response directly as Python code
  - Use `eval()` or `exec()` to load functions
  - Avoid JSON serialization entirely
- **Acceptance Criteria**:
  - ✅ Statistical prep feature works without parsing errors
  - ✅ DerivedMetricsAgent generates functions successfully
  - ✅ No more `'\n        "metric_name_1"'` errors
  - ✅ Agent follows same pattern as UnifiedSynthesisAgent
  - ✅ All derived metrics calculations work correctly
- **Files to Update**:
  - `discernus/agents/automated_derived_metrics/agent.py`
  - `discernus/agents/automated_derived_metrics/prompt.yaml`
- **Dependencies**: None
- **Effort**: 2-3 days

#### [CONSISTENCY-002] Update StatisticalAnalysisAgent to Raw Python Pattern

- **Description**: Update StatisticalAnalysisAgent to use raw Python objects instead of delimiter parsing
- **Purpose**: Make all agents consistent with the system's current architecture
- **Priority**: MEDIUM - Not currently blocking, but inconsistent with system design
- **Status**: Ready for execution
- **Current Issue**: Still uses old delimiter parsing (`<<<DISCERNUS_FUNCTION_START>>>`) despite docstring claiming "no parsing"
- **Solution Pattern**: Follow same approach as DerivedMetricsAgent fix
- **Acceptance Criteria**:
  - ✅ Agent uses raw Python objects instead of delimiter parsing
  - ✅ No more `extract_code_blocks()` calls
  - ✅ Consistent with UnifiedSynthesisAgent pattern
  - ✅ All statistical analysis functions work correctly
- **Files to Update**:
  - `discernus/agents/automated_statistical_analysis/agent.py`
  - `discernus/agents/automated_statistical_analysis/prompt.yaml`
- **Dependencies**: [CONSISTENCY-001] - Learn from DerivedMetricsAgent implementation
- **Effort**: 1-2 days

#### [CONSISTENCY-003] Remove Temporary Statistical Prep Fix

- **Description**: Remove the temporary bypass in CleanAnalysisOrchestrator once agents are fixed
- **Purpose**: Clean up temporary workaround and restore proper agent-based derived metrics
- **Priority**: LOW - Cleanup task
- **Status**: Blocked by [CONSISTENCY-001]
- **Current State**: Statistical prep uses hardcoded template instead of DerivedMetricsAgent
- **Acceptance Criteria**:
  - ✅ Remove temporary template file copying
  - ✅ Restore DerivedMetricsAgent calls in orchestrator
  - ✅ Statistical prep uses proper agent-generated functions
  - ✅ No regression in functionality
- **Files to Update**:
  - `discernus/core/clean_analysis_orchestrator.py`
- **Dependencies**: [CONSISTENCY-001] completion
- **Effort**: 0.5 days

---

### Sprint 19: Structured Output Migration (Post-Alpha)

**Description**: Migrate utility agents to structured output while preserving model choice for artistic agents
**Purpose**: Improve reliability and eliminate parsing errors for utility agents while maintaining research flexibility
**Priority**: MEDIUM - Post-alpha architectural improvement
**Timeline**: 1-2 weeks
**Dependencies**: Alpha release completion

**Architectural Principle**: 
- **Utility Agents** (validation, derived metrics, statistical analysis, evidence retrieval): Standardize on Vertex AI structured output for consistency
- **Artistic Agents** (raw scoring, final synthesis): Preserve model choice flexibility for research quality and researcher preferences

#### [STRUCTURED-001] Migrate Utility Agents to Structured Output

- **Description**: Convert utility agents to use Vertex AI structured output instead of JSON parsing
- **Purpose**: Eliminate parsing errors and improve reliability for non-research-critical agents
- **Priority**: MEDIUM - Post-alpha improvement
- **Acceptance Criteria**:
  - ExperimentCoherenceAgent uses structured output
  - DerivedMetricsAgent uses structured output
  - StatisticalAnalysisAgent uses structured output
  - EvidenceRetrievalAgent uses structured output
  - No more delimiter parsing or JSON extraction
  - Maintained functionality with improved reliability
- **Dependencies**: Alpha release completion
- **Effort**: 1-2 weeks

#### [STRUCTURED-002] Preserve Artistic Agent Model Choice

- **Description**: Ensure raw scoring and synthesis agents maintain model choice flexibility
- **Purpose**: Preserve research quality and researcher preferences for critical research outputs
- **Priority**: MEDIUM - Research quality preservation
- **Acceptance Criteria**:
  - Raw scoring agents support all available models
  - Synthesis agents support all available models
  - No forced Vertex AI usage for artistic agents
  - Clear documentation of agent type distinctions
- **Dependencies**: [STRUCTURED-001]
- **Effort**: 1 week

---

## Current Sprint Planning

**Next Priority**: Sprint 17 (Critical Bug Fixes) - URGENT PRIORITY
**Status**: Ready for execution
**Dependencies**: None - can begin immediately

**Following Priority**: Sprint 18 (Agent Parsing Consistency) - HIGH PRIORITY
**Status**: Ready for execution after Sprint 17
**Dependencies**: Sprint 17 completion required
