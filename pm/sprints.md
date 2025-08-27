# Discernus v10 Sprints

**Purpose**: Organized backlog with sprint planning, dependencies, and detailed item specifications.

**Usage**: 
- "groom our sprints" → organize inbox items into proper sprint structure
- Items moved here from inbox.md during grooming sessions

---

## Current Status

**Date**: 2025-01-27
**Status**: Testing Infrastructure Fix Required - CLI v10 Compliance Complete
**Next Priority**: Fix integration test infrastructure to unblock validation

**CLI v10 Compliance**: ✅ **COMPLETE**
**Statistical Analysis Pipeline**: ✅ **COMPLETE**
**Framework Validation**: ✅ **COMPLETE**
**Current Blocker**: Integration tests failing due to incorrect mocking

---

## Current Sprint Planning

### Sprint 1: Critical Infrastructure & Quality Assurance (IMMEDIATE)

**Timeline**: 1-2 days
**Goal**: Fix critical system issues and establish testing foundation

#### [CRITICAL-001] Fix Graceful Degradation in Derived Metrics Phase ✅ **COMPLETED**

- **Description**: **CRITICAL BUG**: Derived metrics phase failures are being silently caught and the experiment continues with degraded results instead of failing fast
- **Dependencies**: None (blocking everything)
- **Root Cause**: Lines 197-201 in CleanAnalysisOrchestrator catch derived metrics failures and continue with `{"error": str(e), "status": "failed"}` instead of propagating the error
- **Evidence**: Terminal shows "Derived metrics phase failed, attempting to continue: Derived metrics functions file not found" but experiment completes successfully
- **Impact**: 
  - Masks critical LLM generation failures
  - Produces unreliable experiment results
  - Violates THIN architecture fail-fast principles
  - Makes debugging extremely difficult
- **Acceptance Criteria**:
  - [x] Derived metrics phase failures cause immediate experiment termination
  - [x] Clear error messages indicate the specific failure point
  - [x] No graceful degradation for critical pipeline components
  - [x] Statistical analysis phase depends on derived metrics and should also fail if derived metrics fail
- **Effort**: 1-2 hours ✅ **COMPLETED**
- **Priority**: **CRITICAL** (data integrity issue)
- **Status**: ✅ **VERIFIED COMPLETE** - All acceptance criteria met, fail-fast behavior properly implemented

#### [CRITICAL-002] Fix Derived Metrics Cache Stale File References

- **Description**: **CRITICAL BUG**: Cached derived metrics functions reference temporary file paths that get cleaned up, causing "functions file not found" errors on cache hits
- **Dependencies**: [CRITICAL-001]
- **Root Cause**: Cache stores function metadata pointing to temporary workspace files, but temporary directories are cleaned up after each run (lines 769-772)
- **Evidence**: Cache hit shows "💾 Using cached derived metrics functions" but then fails with "Derived metrics functions file not found"
- **Solution**: Store actual function code content in cache, recreate function files from cached content when cache hit occurs
- **Impact**:
  - Cache hits cause experiment failures instead of performance improvements
  - Violates caching reliability principles
  - Makes development velocity worse instead of better
- **Acceptance Criteria**:
  - [ ] Cache stores actual function code content, not just metadata
  - [ ] Cache hits recreate function files from stored content
  - [ ] Both derived metrics and statistical analysis caches fixed
  - [ ] Workspace cleanup doesn't break cached functions
- **Effort**: 1 hour
- **Priority**: **CRITICAL** - Blocking caching benefits
- **Status**: **NEEDS VERIFICATION** - Implementation exists but cache content storage needs testing

#### [PERF-001] Implement Validation Caching

- **Description**: Implement caching for experiment coherence validation to eliminate redundant validation when input assets haven't changed
- **Dependencies**: [CRITICAL-002]
- **Root Cause**: Validation runs every time even when framework, experiment, and corpus haven't changed, causing unnecessary LLM calls and delays
- **Solution**: Cache validation results based on content hashes of framework, experiment, corpus, and model
- **Impact**:
  - Eliminates 20-30 second validation delays on repeated runs
  - Reduces LLM API costs for development iterations
  - Maintains same validation quality and error detection
- **Acceptance Criteria**:
  - [ ] ValidationCacheManager created with deterministic cache keys
  - [ ] Cache key based on framework + experiment + corpus + model content
  - [ ] Validation results cached with success/failure status and issues
  - [ ] Cache hits skip validation and use stored results
  - [ ] Failed validations properly cached and re-raise errors
  - [ ] Unit tests cover all caching scenarios
  - [ ] Integration with CleanAnalysisOrchestrator performance metrics
- **Effort**: 2 hours
- **Priority**: **HIGH** - Significant development velocity improvement
- **Status**: **NEEDS VERIFICATION** - Implementation exists but caching behavior needs testing

#### [TEST-INFRA] Fix Integration Test Infrastructure

- **Description**: Integration tests incorrectly mock critical setup, causing false failures
- **Impact**: False test failures prevent validation of all features
- **Root Cause**: Tests mock `_initialize_infrastructure` which bypasses `artifact_storage` setup
- **Acceptance Criteria**:
  - [ ] Integration tests run without infrastructure errors
  - [ ] Tests accurately reflect actual system status
  - [ ] Mocking doesn't bypass critical system components
  - [ ] Test failures indicate real problems, not setup issues
- **Effort**: 2-3 hours
- **Priority**: **HIGH** - Blocking validation of all features
- **Status**: **NEEDS IMPLEMENTATION**

#### [CRITICAL-003] Fix Evidence Planning and Integration Failures

- **Description**: **CRITICAL BUG**: Evidence planning and integration failures are breaking the synthesis pipeline, causing reports to lack proper textual evidence support for statistical claims
- **Dependencies**: [TEST-INFRA]
- **Root Cause**: 
  - LLM responses not properly formatted as JSON blocks
  - Regex pattern too strict, causing "No JSON block found in LLM response"
  - Evidence retrieval prompt too verbose and complex
  - Fallback evidence retrieval provides empty results instead of useful evidence
- **Impact**:
  - Research integrity compromised - framework designed to link evidence to conclusions is broken
  - Report quality degraded - synthesis reports lack textual support for statistical claims
  - Pipeline reliability - evidence integration phase consistently fails, affecting all experiments
- **Evidence from Terminal**:
  - `"No JSON block found in LLM response. Could not parse plan."`
  - `"Invalid or empty evidence plan provided. Using fallback."`
  - `"No curated evidence artifact provided. Synthesis will proceed without curated evidence."`
  - Evidence database contains 66 evidence pieces but synthesis can't access them
- **Acceptance Criteria**:
  - [ ] JSON parsing regex made more robust to handle various LLM response formats
  - [ ] Evidence retrieval prompt simplified with explicit JSON formatting examples
  - [ ] Fallback evidence retrieval provides useful evidence even when planning fails
  - [ ] Response format validation added before parsing attempts
  - [ ] Evidence integration phase works reliably across all experiments
- **Effort**: 2-3 days
- **Priority**: **CRITICAL** - Research integrity issue
- **Status**: **NEEDS IMPLEMENTATION**

#### [CRITICAL-004] Fix Orchestrator Data Structure Mismatch

- **Description**: **CRITICAL BUG**: The orchestrator creates individual analysis files but the `AutomatedDerivedMetricsAgent` expects a consolidated `analysis_data.json` file, causing pipeline failures
- **Dependencies**: [CRITICAL-003]
- **Root Cause**: 
  - Data flow inconsistency between orchestrator and agent expectations
  - Missing standardized data format contract
  - Agent's fallback mechanism insufficient for LLM generation
  - Tight coupling between orchestrator file creation and agent expectations
- **Impact**:
  - Experiments fail during derived metrics phase
  - `AutomatedDerivedMetricsAgent` cannot generate required functions
  - Pipeline breaks with "No such file or directory" errors
  - Temporary workspace management becomes brittle
- **Evidence from Terminal**:
  - `[Errno 2] No such file or directory: '.../temp_derived_metrics/automatedderivedmetricsagent_functions.py'`
  - Agent looking for `analysis_data.json` but finding individual files
  - Fallback to generic data structure insufficient for LLM generation
- **Acceptance Criteria**:
  - [ ] Data structure contracts between orchestrator and agents documented
  - [ ] Expected file formats and naming conventions standardized
  - [ ] All components with file structure dependencies identified
  - [ ] Standardized data flow specifications created
  - [ ] Pipeline works reliably with consistent data structures
- **Effort**: 2-3 days
- **Priority**: **CRITICAL** - Pipeline failure issue
- **Status**: **NEEDS IMPLEMENTATION**

#### [CRITICAL-005] Fix Import Chain Dependency Failures

- **Description**: **CRITICAL BUG**: Multiple import failures indicate broken dependency resolution and circular import issues in the orchestration layer
- **Dependencies**: [CRITICAL-004]
- **Root Cause**: 
  - Broken dependency resolution - import paths don't match actual module structure
  - Circular import potential - components importing from each other creating dependency cycles
  - Module structure changes - code references modules that have been moved or restructured
  - Missing `__init__.py` files in agent directories
- **Impact**:
  - CLI fails to start with import errors
  - Blocking all experiments until imports are fixed
  - Indicates deeper architectural dependency issues
  - Suggests module organization needs review
- **Evidence from Terminal**:
  - `cannot import name 'ValidationCache' from 'discernus.core.validation_cache'`
  - `cannot import name 'FactCheckerAgent' from 'discernus.agents.fact_checker_agent'`
  - Multiple import failures during orchestrator initialization
- **Acceptance Criteria**:
  - [ ] All import chains in orchestration layer mapped and documented
  - [ ] Circular import dependencies identified and eliminated
  - [ ] Module dependency graph documented
  - [ ] Module organization and structure reviewed and standardized
  - [ ] CLI starts without import errors
- **Effort**: 1-2 days
- **Priority**: **CRITICAL** - System startup failure
- **Status**: **NEEDS IMPLEMENTATION**

### Sprint 2: Logging Architecture & Code Quality (HIGH PRIORITY)

**Timeline**: 3-5 days
**Goal**: Fix logging configuration complexity and establish clean architecture

#### [LOGGING-001] Logging Configuration Complexity Crisis

- **Description**: **CRITICAL ARCHITECTURAL FLAW**: Discovered a convoluted, multi-layered logging configuration system causing verbose debug output and making experiments unreadable
- **Dependencies**: [CRITICAL-005]
- **Root Cause**: 
  - Multiple logging systems coexisting (Standard Python logging, loguru, custom configurations)
  - Orchestrator hardcoded `txtai_logger.setLevel(logging.DEBUG)` in 3 separate locations
  - Inconsistent levels - console set to WARNING but components override with DEBUG
  - No centralized logging policy enforcement
- **Impact**:
  - Experiments produce overwhelming debug output
  - Terminal becomes unreadable during execution
  - Researchers can't see actual progress or errors
  - Violates "human-centric UX" principle
- **Evidence from Terminal**:
  - txtai embeddings debug output flooding console
  - Multiple logging systems competing for output
  - Console handlers being overridden by component-level settings
- **Acceptance Criteria**:
  - [ ] All logging configurations across codebase mapped and documented
  - [ ] All components that override logging levels identified
  - [ ] Logging hierarchy and override points documented
  - [ ] Centralized logging policy and enforcement created
  - [ ] Duplicate and conflicting logging systems eliminated
  - [ ] Clear separation between debug (file) and user (console) output
- **Effort**: 3-5 days
- **Priority**: **HIGH** - Researcher experience issue
- **Status**: **NEEDS IMPLEMENTATION**

#### [LOGGING-002] Rich CLI Usage Investigation

- **Description**: Investigate current use of Rich CLI library in Discernus platform to ensure optimal researcher experience
- **Dependencies**: [LOGGING-001]
- **Current State**:
  - Rich CLI wrapper implemented in `discernus/cli_console.py`
  - Extensive usage throughout main CLI for tables, panels, formatting
  - Professional terminal interface with consistent styling
- **Investigation Areas**:
  - Review Rich library best practices and latest features
  - Assess current implementation against Rich library capabilities
  - Identify opportunities for improved user experience (progress bars, live updates, better error handling)
  - Evaluate performance impact of current Rich usage
- **Deliverables**:
  - Analysis report of current Rich CLI implementation
  - Recommendations for optimization and enhancement
  - Implementation plan for any identified improvements
  - Performance benchmarks if changes are proposed
- **Effort**: 2-3 days
- **Priority**: **MEDIUM** - Enhancement opportunity
- **Status**: **NEEDS INVESTIGATION**

#### [LOGGING-003] Loguru Implementation Investigation

- **Description**: Investigate current use of loguru logging library in Discernus platform to ensure optimal logging implementation
- **Dependencies**: [LOGGING-001]
- **Current State**:
  - Comprehensive logging configuration in `discernus/core/logging_config.py`
  - Multiple log handlers: console, file, error, performance, LLM interactions
  - Mixed usage patterns across codebase (some loguru, some standard logging)
- **Investigation Areas**:
  - Review loguru best practices and latest features
  - Assess current implementation against loguru capabilities
  - Identify opportunities for improved logging structure and performance
  - Evaluate consistency of logging usage across codebase
- **Deliverables**:
  - Analysis report of current loguru implementation
  - Recommendations for optimization and standardization
  - Implementation plan for any identified improvements
  - Performance analysis of current logging overhead
- **Effort**: 2-3 days
- **Priority**: **MEDIUM** - Enhancement opportunity
- **Status**: **NEEDS INVESTIGATION**

### Sprint 3: Architecture Refactoring & Code Quality (MEDIUM PRIORITY)

**Timeline**: 5-7 days
**Goal**: Fix architectural issues and establish clean interfaces

#### [ARCH-001] Method Signature Contract Violations

- **Description**: Method signature mismatches between orchestrator and agents indicate broken contracts and tight coupling
- **Dependencies**: [LOGGING-001]
- **Root Cause**: 
  - Missing method implementations - code references methods that were never implemented
  - Contract drift - method signatures changed without updating all callers
  - Interface mismatch - components expect different method signatures
  - Tight coupling - orchestrator depends on specific storage method implementations
- **Impact**:
  - Runtime errors during artifact storage operations
  - Pipeline breaks when expected methods are missing
  - Indicates incomplete implementation or refactoring
  - Suggests interface contracts need formalization
- **Evidence from Terminal**:
  - `'LocalArtifactStorage' object has no attribute 'get_hash_by_type'`
  - `SynthesisPromptAssembler.assemble_prompt() got an unexpected keyword argument 'evidence_artifacts'`
- **Acceptance Criteria**:
  - [ ] All method signatures between orchestrator and components mapped and documented
  - [ ] Expected interfaces and contracts documented
  - [ ] All broken method references identified and fixed
  - [ ] Interface specification documents created
  - [ ] Formal interface contracts established
- **Effort**: 1-2 days
- **Priority**: **MEDIUM** - Code quality issue
- **Status**: **NEEDS IMPLEMENTATION**

#### [ARCH-002] Temporary Workspace Management Complexity

- **Description**: Complex temporary workspace creation, management, and cleanup indicates orchestrator doing too much file management work
- **Dependencies**: [ARCH-001]
- **Root Cause**: 
  - Orchestrator doing too much - file management should be agent responsibility
  - Complex state management - temporary workspace lifecycle is complex and error-prone
  - Tight coupling - agents depend on orchestrator's file creation patterns
  - No clear ownership - unclear who owns temporary file management
- **Impact**:
  - Complex error handling for file operations
  - Agents fail when expected files don't exist
  - Temporary workspace management becomes brittle
  - Violates single responsibility principle
- **Acceptance Criteria**:
  - [ ] All temporary workspace management operations mapped and documented
  - [ ] File lifecycle and ownership clearly defined
  - [ ] All file dependencies between components identified
  - [ ] File management responsibility matrix created
  - [ ] Agents manage their own temporary files
  - [ ] Orchestrator doesn't handle file creation details
- **Effort**: 2-3 days
- **Priority**: **MEDIUM** - Architecture improvement
- **Status**: **NEEDS IMPLEMENTATION**
