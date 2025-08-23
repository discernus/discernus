# Discernus v10 Backlog

**Date:** 2025-08-23
**Status:** Testing Infrastructure Fix Required - CLI v10 Compliance Complete
**Next Priority:** Fix integration test infrastructure to unblock validation

---

## Current Status

**CLI v10 Compliance:** ✅ **COMPLETE**
**Statistical Analysis Pipeline:** ✅ **COMPLETE**
**Framework Validation:** ✅ **COMPLETE**
**Current Blocker:** Integration tests failing due to incorrect mocking

---

## Current Sprint Planning

### Sprint 1: Critical Fixes (IMMEDIATE PRIORITY)

**Timeline:** 2-3 hours
**Goal:** Fix critical data integrity issues and unblock validation

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
- **Status**: ✅ **FIXED** - Experiment now fails fast with exit code 1 and clear error message
- **Follow-up Issue**: Cache invalidation issue discovered - cached functions reference non-existent files

#### [CRITICAL-002] Fix Derived Metrics Cache Stale File References ✅ **COMPLETED**

- **Description**: **CRITICAL BUG**: Cached derived metrics functions reference temporary file paths that get cleaned up, causing "functions file not found" errors on cache hits
- **Dependencies**: [CRITICAL-001] ✅
- **Root Cause**: Cache stores function metadata pointing to temporary workspace files, but temporary directories are cleaned up after each run (lines 769-772)
- **Evidence**: Cache hit shows "💾 Using cached derived metrics functions" but then fails with "Derived metrics functions file not found"
- **Solution**: Store actual function code content in cache, recreate function files from cached content when cache hit occurs
- **Impact**:
  - Cache hits cause experiment failures instead of performance improvements
  - Violates caching reliability principles
  - Makes development velocity worse instead of better
- **Acceptance Criteria**:
  - [x] Cache stores actual function code content, not just metadata
  - [x] Cache hits recreate function files from stored content
  - [x] Both derived metrics and statistical analysis caches fixed
  - [x] Workspace cleanup doesn't break cached functions
- **Effort**: 1 hour ✅ **COMPLETED**
- **Priority**: **CRITICAL** - Blocking caching benefits
- **Status**: ✅ **FIXED** - Cache now stores and recreates function code content

#### [PERF-001] Implement Validation Caching ✅ **COMPLETED**

- **Description**: Implement caching for experiment coherence validation to eliminate redundant validation when input assets haven't changed
- **Dependencies**: [CRITICAL-002] ✅
- **Root Cause**: Validation runs every time even when framework, experiment, and corpus haven't changed, causing unnecessary LLM calls and delays
- **Solution**: Cache validation results based on content hashes of framework, experiment, corpus, and model
- **Impact**:
  - Eliminates 20-30 second validation delays on repeated runs
  - Reduces LLM API costs for development iterations
  - Maintains same validation quality and error detection
- **Acceptance Criteria**:
  - [x] ValidationCacheManager created with deterministic cache keys
  - [x] Cache key based on framework + experiment + corpus + model content
  - [x] Validation results cached with success/failure status and issues
  - [x] Cache hits skip validation and use stored results
  - [x] Failed validations properly cached and re-raise errors
  - [x] Unit tests cover all caching scenarios
  - [x] Integration with CleanAnalysisOrchestrator performance metrics
- **Effort**: 2 hours ✅ **COMPLETED**
- **Priority**: **HIGH** - Significant development velocity improvement
- **Status**: ✅ **IMPLEMENTED** - Validation now cached with 20-30 second speedup on cache hits

#### [TEST-INFRA] Fix Integration Test Infrastructure

- **Description**: Integration tests incorrectly mock critical setup, causing false failures
- **Impact**: False test failures prevent validation of all features
- **Root Cause**: Tests mock `_initialize_infrastructure` which bypasses `artifact_storage` setup
- **Acceptance Criteria**:
  - [ ] Integration tests run without infrastructure errors
  - [ ] Tests accurately reflect actual system status
  - [ ] False failures are eliminated
  - [ ] Real issues (if any) are identified
- **Effort**: 1-2 hours
- **Priority**: **HIGHEST** - Blocking everything

#### [CRITICAL-003] Fix Silent Statistical Analysis Failures ✅ **COMPLETED**

- **Description**: **CRITICAL BUG**: Statistical analysis phase reports success but produces no numerical results, allowing experiments to continue to synthesis with invalid data
- **Dependencies**: [CRITICAL-001] ✅, [CRITICAL-002] ✅
- **Root Cause**: `_run_statistical_analysis_phase` method executes statistical functions but doesn't validate the output, blindly setting `"validation_passed": True`
- **Evidence**: Final report shows "While the analysis pipeline reported successful completion, the final output contained only metadata about the analysis run. It did not include the expected descriptive statistics or correlation coefficients."
- **Impact**:
  - Experiments produce invalid reports without statistical data
  - Violates fail-fast principles for critical pipeline components
  - Makes debugging extremely difficult when statistical analysis fails
  - Results in qualitative-only reports when quantitative analysis was intended
- **Solution**: Add validation to `_run_statistical_analysis_phase` using existing `_validate_statistical_results` method
- **Acceptance Criteria**:
  - [x] Statistical analysis phase validates output before proceeding
  - [x] Experiments fail fast when statistical analysis produces no numerical results
  - [x] Clear error messages indicate statistical analysis failure
  - [x] No experiments proceed to synthesis without valid statistical data
- **Effort**: 30 minutes ✅ **COMPLETED**
- **Priority**: **CRITICAL** - Data integrity and fail-fast principles
- **Status**: ✅ **FIXED** - Statistical analysis now validates output and fails fast on invalid results

#### [CLI-002] Fix Non-Compliant Test Experiments

- **Description**: Update test experiments to comply with v10 specifications
- **Dependencies**: [TEST-INFRA] ✅
- **Acceptance Criteria**:
  - [ ] All test experiments pass v10 validation
  - [ ] Test data matches current corpus specifications
  - [ ] Framework references are current
- **Effort**: 2-3 hours

#### [TEST-001] Unit Test Coverage Targets

- **Description**: Establish and achieve unit test coverage targets
- **Dependencies**: [TEST-INFRA] ✅
- **Acceptance Criteria**:
  - [ ] Core components have 80%+ coverage
  - [ ] Critical paths have 90%+ coverage
  - [ ] Test suite runs in under 30 seconds
- **Effort**: 4-6 hours

### Sprint 2: THIN Architecture Optimization (HIGH PRIORITY)

**Timeline:** 1-2 days
**Goal:** Optimize core system architecture

#### [THIN-OPT] Statistical Calculation Process Optimization

- **Description**: Streamline statistical calculation process for better performance
- **Dependencies**: [TEST-001] ✅
- **Acceptance Criteria**:
  - [ ] Statistical calculations complete in under 60 seconds
  - [ ] Memory usage optimized for large datasets
  - [ ] Process maintains THIN architecture principles
- **Effort**: 1 day

#### [CACHE-001] RAG Index Caching Implementation ✅ **COMPLETED**

- **Description**: Implement caching for RAG indexes to eliminate redundant rebuilding and improve development velocity
- **Dependencies**: [THIN-OPT] ✅
- **Root Cause**: RAG index rebuilt from scratch every time, even when evidence artifacts are identical, causing 10-15 second delays
- **Critical Fix Applied**: Fixed txtai directory-based index handling - txtai saves indexes as directories, not files, requiring tar.gz compression for caching
- **Acceptance Criteria**:
  - [x] RAG index built and cached immediately after analysis phase (Phase 4.5)
  - [x] Cache key based on evidence artifact hashes for deterministic caching
  - [x] Synthesis phase checks cache first, builds only if needed
  - [x] txtai index save/load functionality integrated with LocalArtifactStorage
  - [x] **CRITICAL**: Proper tar.gz handling for txtai directory-based indexes
  - [x] Cache hit provides 10-15 second speed improvement over rebuild
  - [x] Follows same caching pattern as derived metrics and statistical analysis
  - [x] Unit tests cover tar.gz compression/decompression scenarios
- **Effort**: 4 hours ✅ **COMPLETED**
- **Priority**: **HIGH** - Significant development velocity improvement
- **Status**: ✅ **IMPLEMENTED** - RAG index caching working with proper txtai directory handling

#### [ARCH-004] Complete Orchestrator Deprecation & Cleanup

- **Description**: Complete the deprecation and cleanup of all legacy orchestrators to establish CleanAnalysisOrchestrator as the sole production orchestrator
- **Dependencies**: [CACHE-001] ✅
- **Acceptance Criteria**:
  - [ ] All deprecated orchestrators moved to deprecated/ folder
  - [ ] CLI help and documentation updated to remove deprecated options
  - [ ] No code references to deprecated orchestrators in active codebase
  - [ ] Clear documentation of single orchestrator architecture
  - [ ] Deprecation warnings removed from active code
- **Effort**: 4-6 hours

### Sprint 3: Quality & Documentation (MEDIUM PRIORITY)

**Timeline:** 2-3 days
**Goal:** Improve system quality and user experience

#### [TEST-002] Integration Test Strategy

- **Description**: Develop comprehensive integration test strategy
- **Dependencies**: [ARCH-004] ✅
- **Acceptance Criteria**:
  - [ ] Integration test plan documented
  - [ ] Test scenarios cover critical user workflows
  - [ ] Mock data strategy established
- **Effort**: 1 day

#### [TEST-003] Test Data Management

- **Description**: Implement proper test data management and cleanup
- **Dependencies**: [TEST-002] ✅
- **Acceptance Criteria**:
  - [ ] Test data is isolated and cleanable
  - [ ] No test artifacts pollute production data
  - [ ] Test cleanup is automated
- **Effort**: 6-8 hours

#### [DX-001] Onboarding Documentation

- **Description**: Create clear onboarding documentation for new contributors
- **Dependencies**: [TEST-003] ✅
- **Acceptance Criteria**:
  - [ ] Quick start guide for new developers
  - [ ] Environment setup instructions
  - [ ] Common troubleshooting guide
- **Effort**: 1 day

#### [UX-001] Synthesis Flow Logging Cleanup ✅ **COMPLETED**

- **Description**: Fix synthesis phase logging order to improve readability and logical flow
- **Dependencies**: [TEST-003] ✅
- **Root Cause**: `LocalArtifactStorage.get_artifact()` logs every evidence retrieval during synthesis and RAG index building, creating hundreds of verbose log lines
- **Solution**: Added `quiet=True` parameter to `get_artifact()` and updated all bulk evidence retrieval components
- **Acceptance Criteria**:
  - [x] Evidence retrieval logging suppressed during bulk synthesis operations
  - [x] `UnifiedSynthesisAgent._get_all_evidence()` uses quiet mode
  - [x] `SynthesisPromptAssembler` uses quiet mode for evidence counting
  - [x] `CleanAnalysisOrchestrator._validate_synthesis_assets()` uses quiet mode for validation
  - [x] `TxtaiEvidenceCurator._get_all_evidence()` uses quiet mode for RAG index building
  - [x] Individual artifact retrievals still logged when appropriate
  - [x] Clean synthesis flow without hundreds of "📥 Retrieved artifact" messages
- **Effort**: 1.5 hours ✅ **COMPLETED**
- **Priority**: **LOW** - Minor UX improvement
- **Status**: ✅ **FULLY IMPLEMENTED** - All synthesis and RAG index logging now clean and readable

#### [UX-002] Optimize Synthesis Asset Validation

- **Description**: Streamline synthesis asset validation to reduce verbosity and eliminate redundant checks when RAG index exists
- **Dependencies**: [CACHE-001] ✅
- **Root Cause**: `_validate_synthesis_assets()` performs redundant evidence validation after RAG index is built, creating verbose terminal output
- **Current Issues**:
  - Evidence artifacts validated twice (during RAG build + synthesis validation)
  - Verbose logging for each evidence artifact retrieval
  - Redundant corpus document validation
  - Terminal output cluttered with unnecessary validation messages
- **Acceptance Criteria**:
  - [ ] Skip evidence artifact validation if RAG index exists and is populated
  - [ ] Reduce logging verbosity for evidence checks (single summary line)
  - [ ] Keep essential validations (framework, experiment, statistical results)
  - [ ] Maintain corpus file validation but with less verbose logging
  - [ ] Add logic: "if RAG index exists, evidence already validated"
- **Effort**: 2-3 hours
- **Priority**: **MEDIUM** - Improves development experience and reduces terminal noise

#### [UX-003] Integrate CSV Export Agent

- **Description**: Integrate CSV Export Agent into CleanAnalysisOrchestrator for professional CSV generation
- **Dependencies**: [ARCH-004] ✅
- **Acceptance Criteria**:
  - [ ] CSV Export Agent integrated into orchestration flow
  - [ ] Raw scores exported to CSV with proper formatting
  - [ ] Statistical analysis results exported to CSV with test details
  - [ ] Derived metrics exported to CSV with dynamic column discovery
  - [ ] Evidence linking maintained in CSV exports
  - [ ] Data structure adapter maps current format to CSV agent expectations
- **Effort**: 4-6 hours
- **Priority**: **MEDIUM** - Enhances research output quality and usability

#### [UX-004] Integrate Automated Visualization Agent

- **Description**: Integrate AutomatedVisualizationAgent into synthesis process for publication-ready charts and graphs
- **Dependencies**: [UX-003] ✅
- **Acceptance Criteria**:
  - [ ] AutomatedVisualizationAgent integrated into synthesis phase
  - [ ] Framework-specific visualization functions generated automatically
  - [ ] Publication-ready charts for dimension scores, correlations, and trends
  - [ ] Visualizations saved alongside final reports in results directory
  - [ ] Academic-quality output with proper styling and error handling
  - [ ] Framework-agnostic approach maintained
- **Effort**: 6-8 hours
- **Priority**: **MEDIUM** - Significantly enhances research output quality and publication readiness

### Sprint 4: Future Enhancements (LOW PRIORITY)

**Timeline:** Future sprints
**Goal:** Prepare for next phase of development

#### [CLI-007] Implement CLI Logging & Provenance

- **Description**: Add comprehensive logging and provenance tracking to CLI
- **Dependencies**: [DX-001] ✅
- **Acceptance Criteria**:
  - [ ] All CLI actions are logged
  - [ ] Provenance chain is maintained
  - [ ] Debug information is accessible
- **Effort**: 2-3 days

#### [CLI-008] Comprehensive CLI Testing

- **Description**: Implement end-to-end CLI testing suite
- **Dependencies**: [CLI-007] ✅
- **Acceptance Criteria**:
  - [ ] CLI test suite covers all commands
  - [ ] Error scenarios are tested
  - [ ] Performance benchmarks established
- **Effort**: 3-4 days

#### [TECH-002] Model Selection Optimization

- **Description**: Optimize model selection for cost and performance
- **Dependencies**: [CLI-008] ✅
- **Acceptance Criteria**:
  - [ ] Model selection is automated
  - [ ] Cost optimization is implemented
  - [ ] Performance benchmarks are established
- **Effort**: 2-3 days

---

## Backlog (Future Consideration)

### [ARCH-001] Multi-Agent Progressive Synthesis Architecture (Phase 2)

- **Description**: Implement progressive synthesis with multiple agents
- **Priority**: Low - Future enhancement
- **Effort**: 1-2 weeks

### [TECH-003] Error Handling & Resilience

- **Description**: Implement comprehensive error handling and retry logic
- **Priority**: Low - Quality improvement
- **Effort**: 3-5 days

### [RAG-ENHANCE] Evidence Integration Enhancement

- **Description**: Enhance RAG system for better evidence integration
- **Priority**: Low - Feature enhancement
- **Effort**: 1 week

### [INTEGRITY-001] Integrate Provenance Stamp System

- **Description**: Integrate tamper-evident content tracking to prevent LLM hallucination and ensure content integrity
- **Dependencies**: None (strategic infrastructure)
- **Acceptance Criteria**:
  - [ ] ProvenanceStamp system integrated into corpus loading
  - [ ] Content hashes generated for all corpus documents
  - [ ] LLM prompts enhanced with provenance stamps
  - [ ] LLM responses validated for correct provenance references
  - [ ] Provenance reports generated for audit trail
  - [ ] Integration detects content tampering and hallucination incidents
- **Effort**: 1-2 days
- **Priority**: Medium - Critical for research integrity and academic compliance
- **Academic Value**: Prevents catastrophic failure where LLMs analyze fabricated content

### [EXTEND-001] Integrate Capability Registry System

- **Description**: Integrate THIN extensibility system to allow academics to add domain-specific tools and libraries
- **Dependencies**: None (strategic infrastructure)
- **Acceptance Criteria**:
  - [ ] CapabilityRegistry integrated into SecureCodeExecutor
  - [ ] Core capabilities loaded from presets
  - [ ] Extension system supports academic domain-specific libraries
  - [ ] YAML-based extension templates for researchers
  - [ ] Security boundaries enforced for allowed libraries and builtins
  - [ ] Documentation for creating academic extensions
- **Effort**: 2-3 days
- **Priority**: Medium - Enables academic adoption and domain-specific research
- **Academic Value**: Allows researchers to extend platform without forking codebase

### [PROVENANCE-001] Enhance Academic Artifact Organization

- **Description**: Leverage provenance_organizer.py patterns to enhance academic-grade artifact organization and auditing
- **Dependencies**: [INTEGRITY-001] (provenance stamp system)
- **Code Reuse**: `discernus/core/provenance_organizer.py` contains valuable patterns for:
  - Transforming hash-based storage into human-readable academic structure
  - Academic-standard directory organization with symlink performance
  - Artifact type mapping and provenance transparency
  - Complete audit trail generation for external review
- **Acceptance Criteria**:
  - [ ] Analyze provenance_organizer.py patterns for reusable components
  - [ ] Integrate academic-friendly artifact organization into CleanAnalysisOrchestrator
  - [ ] Maintain performance via symlinks to shared cache
  - [ ] Provide human-readable artifact names and directory structure
  - [ ] Generate comprehensive provenance reports for academic compliance
  - [ ] Support external audit and review workflows
- **Effort**: 3-4 days
- **Priority**: Low - Future enhancement for academic adoption
- **Academic Value**: Transforms technical artifacts into researcher-friendly organization

---

## Dependencies

- **CLI-002**: [TEST-INFRA] ✅
- **CACHE-001**: [THIN-OPT] ✅
- **ARCH-004**: [CACHE-001] ✅
- **CLI-007**: [DX-001] ✅
- **CLI-008**: [CLI-007] ✅
- **TECH-002**: [CLI-008] ✅

---

## Current Focus Areas

1. **Testing Infrastructure Fix** - Unblock all validation
2. **THIN Architecture Optimization** - Improve core system performance
3. **Quality & Documentation** - Enhance user experience and maintainability

---

## Success Metrics

- **Testing Infrastructure**: All tests pass without false failures
- **THIN Architecture**: System maintains clean separation of concerns
- **Code Quality**: 80%+ unit test coverage achieved
- **User Experience**: Clear onboarding and documentation available

---

## Backlog Maintenance

- **Last Updated**: 2025-01-23
- **Next Review**: After Sprint 1 completion
- **Cleanup Status**: ✅ Groomed and streamlined
