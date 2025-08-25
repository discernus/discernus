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

### Sprint 1: Critical Infrastructure & Quality Assurance (IMMEDIATE)

**Timeline:** 1-2 days
**Goal:** Fix critical system issues and establish testing foundation

#### [CRITICAL-001] Fix Graceful Degradation in Derived Metrics Phase

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
  - [ ] Derived metrics phase failures cause immediate experiment termination
  - [ ] Clear error messages indicate the specific failure point
  - [ ] No graceful degradation for critical pipeline components
  - [ ] Statistical analysis phase depends on derived metrics and should also fail if derived metrics fail
- **Effort**: 1-2 hours
- **Priority**: **CRITICAL** (data integrity issue)
- **Status**: **NEEDS VERIFICATION** - Implementation exists but fail-fast behavior needs testing

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
  - [ ] False failures are eliminated
  - [ ] Real issues (if any) are identified
- **Effort**: 1-2 hours
- **Priority**: **HIGHEST** - Blocking everything

#### [QUALITY-001] Fix Fact-Checker False Positive on Evidence Citations

- **Description**: Fact-checker incorrectly flags legitimate evidence attribution `(Source: filename.txt)` as "Citation Violation"
- **Impact**: 
  - False positives on correct evidence citations
  - Revision agent asked to "fix" legitimate provenance tracking
  - Undermines evidence attribution which is required for academic integrity
- **Root Cause**: Citation Violation rubric is too broad, catching internal evidence references
- **Solution**: Refine rubric to distinguish between external academic citations and internal evidence attribution
- **Acceptance Criteria**:
  - [ ] `(Source: filename.txt)` format is NOT flagged as citation violation
  - [ ] External academic citations like `(Author, Year)` are still flagged
  - [ ] Rubric clearly distinguishes evidence attribution from academic citations
  - [ ] False positive rate on evidence citations is zero
- **Effort**: 30 minutes
- **Priority**: **HIGH** - Affects report quality and revision agent effectiveness
- **Status**: **NEEDS VERIFICATION** - Implementation exists but behavior needs testing

#### [QUALITY-002] Review Revision Agent Prompt for Framework Dimension Issues

- **Description**: Revision agent failed to fix "Dimension Hallucination" where report incorrectly refers to "Identity", "Emotion", "Reality" as dimensions instead of axes
- **Impact**: 
  - Critical factual errors remain in final reports
  - Framework-specific accuracy issues not being corrected
  - Revision agent underperforming on framework structure corrections
- **Root Cause**: Revision agent prompt may not be clear about handling framework-specific factual issues
- **Solution**: Review and update revision agent prompt to better handle framework dimension vs. axis distinctions
- **Acceptance Criteria**:
  - [ ] Revision agent successfully corrects dimension hallucination errors
  - [ ] Prompt clearly defines what constitutes framework factual issues
  - [ ] Examples include framework structure corrections
  - [ ] Framework-agnostic approach maintained
- **Effort**: 1 hour
- **Priority**: **HIGH** - Affects report accuracy and revision agent effectiveness
- **Status**: **NEEDS VERIFICATION** - Implementation exists but behavior needs testing

#### [QUALITY-003] Review Synthesis Prompt for Framework Dimension Accuracy

- **Description**: Synthesis agent generated report with incorrect framework terminology (calling axes "dimensions")
- **Impact**: 
  - Reports contain framework-specific factual errors
  - Undermines framework accuracy and researcher trust
  - Creates downstream fact-checking issues
- **Root Cause**: Synthesis prompt may not be clear about framework structure and terminology
- **Solution**: Review synthesis prompt to ensure it generates accurate framework terminology
- **Acceptance Criteria**:
  - [ ] Synthesis agent uses correct framework terminology (axes vs. dimensions)
  - [ ] Reports accurately reflect framework structure
  - [ ] Framework-agnostic approach maintained
  - [ ] Reduced dimension hallucination in initial reports
- **Effort**: 1 hour
- **Priority**: **MEDIUM** - Prevention is better than correction
- **Status**: **NEEDS VERIFICATION** - Implementation exists but behavior needs testing

#### [OBSERVABILITY-001] MLflow Integration for txtai Observability

- **Description**: Integrate MLflow with txtai for advanced observability and trace logging of RAG operations
- **Dependencies**: [TEST-INFRA] completion
- **Root Cause**: Current txtai logging is basic; MLflow integration provides automatic tracing of pipelines and embeddings operations
- **Solution**: Install MLflow plugin for txtai, configure tracking URI, and set up txtai autologging
- **Impact**:
  - Automatic tracing of RAG index operations
  - Pipeline-level observability without core system modifications
  - System-level debugging and performance monitoring
  - Production-ready observability for fact-checker operations
- **Acceptance Criteria**:
  - [ ] MLflow plugin for txtai installed and configured
  - [ ] txtai autologging enabled for embeddings operations
  - [ ] RAG index building and querying automatically traced
  - [ ] Performance metrics and operation timing captured
  - [ ] Integration with existing logging infrastructure
- **Effort**: 3-4 hours
- **Priority**: **MEDIUM** - Future enhancement for production monitoring
- **Status**: **BACKLOGGED** - Simple Python logging implemented first

#### [CRITICAL-003] Fix Silent Statistical Analysis Failures

- **Description**: **CRITICAL BUG**: Statistical analysis phase reports success but produces no numerical results, allowing experiments to continue to synthesis with invalid data
- **Dependencies**: [CRITICAL-001], [CRITICAL-002]
- **Root Cause**: `_run_statistical_analysis_phase` method executes statistical functions but doesn't validate the output, blindly setting `"validation_passed": True"`
- **Evidence**: Final report shows "While the analysis pipeline reported successful completion, the final output contained only metadata about the analysis run. It did not include the expected descriptive statistics or correlation coefficients."
- **Impact**:
  - Experiments produce invalid reports without statistical data
  - Violates fail-fast principles for critical pipeline components
  - Makes debugging extremely difficult when statistical analysis fails
  - Results in qualitative-only reports when quantitative analysis was intended
- **Solution**: Add validation to `_run_statistical_analysis_phase` using existing `_validate_statistical_results` method
- **Acceptance Criteria**:
  - [ ] Statistical analysis phase validates output before proceeding
  - [ ] Experiments fail fast when statistical analysis produces no numerical results
  - [ ] Clear error messages indicate statistical analysis failure
  - [ ] No experiments proceed to synthesis without valid statistical data
- **Effort**: 30 minutes
- **Priority**: **CRITICAL** - Data integrity and fail-fast principles
- **Status**: **NEEDS VERIFICATION** - Implementation exists but fail-fast behavior needs testing

#### [CRITICAL-004] Fix Missing Derived Metrics Artifact Storage

- **Description**: **CRITICAL BUG**: Derived metrics artifacts are not being stored in the run results directory, unlike statistical results which are properly stored
- **Dependencies**: [CRITICAL-003]
- **Root Cause**: Derived metrics phase generates artifacts but doesn't save them to the results directory structure
- **Evidence**: 
  - Statistical results are stored as `statistical_results.json` in run results directory
  - Derived metrics artifacts are missing from the same location
  - This creates incomplete experiment records and violates data integrity principles
- **Impact**:
  - Incomplete experiment documentation and provenance
  - Missing critical analysis artifacts for research reproducibility
  - Violates the principle of complete experiment result preservation
  - Makes debugging and result validation difficult
- **Solution**: Ensure derived metrics artifacts are saved to the run results directory alongside statistical results
- **Acceptance Criteria**:
  - [ ] Derived metrics artifacts are stored in run results directory
  - [ ] Artifacts follow same naming and organization pattern as statistical results
  - [ ] All derived metrics outputs are preserved for experiment reproducibility
  - [ ] Integration with existing artifact storage system
- **Effort**: 2-3 hours
- **Priority**: **HIGH** - Data integrity and experiment completeness
- **Status**: **BACKLOGGED** - Requires investigation of derived metrics artifact handling

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

#### [CRITICAL-007] Fix Orchestrator Graceful Degradation Violations

- **Description**: **CRITICAL BUG**: Orchestrator continues experiments despite critical fact-checking failures, violating fail-fast principles
- **Dependencies**: None
- **Root Cause**: Fact-checking phase failures are caught and logged as warnings, but experiments continue to synthesis phase
- **Evidence**: 
  - `_run_fact_checking_phase` catches exceptions and logs them as warnings
  - `_create_basic_results_directory` provides fallback results when normal results creation fails
  - RAG index preparation failures are logged but don't stop experiment execution
- **Impact**:
  - Experiments produce results despite critical validation failures
  - Violates fail-fast principles for quality assurance
  - Creates false confidence in experiment results
  - Makes debugging extremely difficult when critical components fail
- **Solution**: Modify orchestrator to fail fast when critical components (fact-checking, RAG index preparation) fail
- **Acceptance Criteria**:
  - [ ] Fact-checking phase failures cause experiment to fail fast
  - [ ] RAG index preparation failures cause experiment to fail fast
  - [ ] Results creation failures cause experiment to fail fast
  - [ ] Clear error messages indicate which critical component failed
  - [ ] No experiments proceed to synthesis with critical component failures
- **Effort**: 2-3 hours
- **Priority**: **CRITICAL** - Quality assurance and fail-fast principles
- **Status**: **BACKLOGGED**



### Sprint 2: RAG Index Architecture & Performance (HIGH PRIORITY)

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

#### [ARCH-RAG-01] Centralize RAG Index Management for Scalability

- **Description**: Refactor RAG index creation and management out of the orchestrator and into a dedicated, reusable component to adhere to THIN principles, fix the broken synthesis RAG implementation, and create a scalable architecture.
- **Dependencies**: None, but blocks durable fixes for synthesis agent.
- **Root Cause**: 
  - RAG index logic is currently duplicated and tightly coupled within the `CleanAnalysisOrchestrator`.
  - The synthesis phase has an incomplete, non-functional RAG implementation, leading to a non-scalable workaround (injecting all evidence into the prompt).
  - The orchestrator is becoming "THICK," violating the Single Responsibility Principle.
  - The current RAG index caching relies on `.tar.gz` compression, which is an unnecessary, complex, and opaque layer that conflicts with the project's native directory-based approach.
- **Solution**: 
  - Create a new `discernus/core/rag_index_manager.py` component.
  - The `RAGIndexManager` will be responsible for building, caching, and managing all `txtai` indexes.
  - This will require modifying `LocalArtifactStorage` to be directory-aware, removing the need for `.tar.gz` compression and aligning with the project's native file-based architecture.
  - The manager will be flexible enough to handle both the comprehensive fact-checker index and the specialized evidence-only synthesis index.
  - The new architecture will treat RAG indexes as permanent, first-class provenance artifacts, persisting them to the final results directory instead of treating them as disposable, temporary tools.
- **Implementation Notes & Best Practices (from `txtai` research)**:
  - **Content Storage is Mandatory**: The `txtai` Embeddings object MUST be initialized with `{"content": True}` to ensure document text is stored alongside the embeddings. This is the root cause of previous content retrieval failures.
  - **Directory-Native Storage is Correct**: `txtai`'s native `.save()` method creates a directory. Our plan to make `LocalArtifactStorage` directory-aware is the correct, non-hacky solution.
  - **No External DB Needed**: The internal content storage mechanism removes any need for external databases like SQLite.
  - **Future-Proofing**: The `RAGIndexManager` should be designed with future enhancements in mind, such as the potential use of hybrid (sparse/dense) search for improved accuracy.
- **Acceptance Criteria**:
  - [x] `LocalArtifactStorage` is refactored to natively support storing and retrieving directories, eliminating the `.tar.gz` compression layer for RAG indexes.
  - [x] A new `RAGIndexManager` class is created in `discernus/core/rag_index_manager.py` that utilizes the directory-aware storage and correctly initializes `txtai` with `{"content": True}`.
  - [x] The `CleanAnalysisOrchestrator._build_fact_checker_rag_index` method is refactored to delegate index creation to the `RAGIndexManager`.
  - [x] The `CleanAnalysisOrchestrator.run_synthesis_phase` is refactored to use the `RAGIndexManager` to build a dedicated, evidence-only RAG index from `evidence_v6` artifacts.
  - [x] The newly created evidence-only RAG index is passed to the `UnifiedSynthesisAgent`.
  - [x] The `UnifiedSynthesisAgent` is refactored to accept and perform semantic queries against the provided RAG index, instead of relying on a static evidence database in its prompt.
  - [x] The final implementation is scalable and does not pass the entire evidence database into the LLM context window.
  - [x] Upon successful completion of a run, the final RAG indexes (fact-checker and synthesis) are saved as permanent artifacts in the run's `results/rag_indexes/` directory, ensuring full methodological provenance.
- **Effort**: 2-3 days
- **Priority**: **HIGH** - Critical for architectural integrity and scalability.
- **Status**: ✅ **COMPLETED**

#### [CACHE-001] RAG Index Caching Implementation (Temporary)

- **Description**: Implement caching for RAG indexes to eliminate redundant rebuilding and improve development velocity
- **Dependencies**: [THIN-OPT] ✅
- **Root Cause**: RAG index rebuilt from scratch every time, even when evidence artifacts are identical, causing 10-15 second delays
- **Critical Fix Applied**: Fixed txtai directory-based index handling - txtai saves indexes as directories, not files, requiring tar.gz compression for caching
- **Acceptance Criteria**:
  - [ ] RAG index built and cached immediately after analysis phase (Phase 4.5)
  - [ ] Cache key based on evidence artifact hashes for deterministic caching
  - [ ] Synthesis phase checks cache first, builds only if needed
  - [ ] txtai index save/load functionality integrated with LocalArtifactStorage
  - [ ] **CRITICAL**: Proper tar.gz handling for txtai directory-based indexes
  - [ ] Cache hit provides 10-15 second speed improvement over rebuild
  - [ ] Follows same caching pattern as derived metrics and statistical analysis
  - [ ] Unit tests cover tar.gz compression/decompression scenarios
- **Effort**: 4 hours
- **Priority**: **HIGH** - Significant development velocity improvement
- **Status**: **NEEDS VERIFICATION** - Implementation exists but caching behavior needs testing
- **Note**: This implementation will be superseded by [ARCH-RAG-01] refactor. After refactor completion, caching will need to be reimplemented for the new directory-native architecture without tar.gz compression.

#### [CACHE-002] Reimplement RAG Index Caching for New Architecture

- **Description**: Reimplement RAG index caching after [ARCH-RAG-01] refactor to leverage the new directory-native architecture
- **Dependencies**: [ARCH-RAG-01] ✅ (RAG index refactor complete), [CACHE-001]
- **Root Cause**: [CACHE-001] implementation used tar.gz compression workaround that will be eliminated by the refactor
- **Solution**: Implement caching for the new `RAGIndexManager` using native directory storage
- **Acceptance Criteria**:
  - [ ] Caching integrated with new `RAGIndexManager` class
  - [ ] Cache stores native txtai directories without compression overhead
  - [ ] Cache keys derive from `index_build_fingerprint` (SHA-256 over canonical JSON of evidence hashes + config + cache_version)
  - [ ] RAG index manifest includes `config`, `doc_count`, `evidence_input_hashes`, and `index_build_fingerprint`
  - [ ] Performance improvements exceed current 10-15 second speedup
  - [ ] Caching works for both fact-checker and synthesis RAG indexes
  - [ ] Cache invalidation properly handles RAG index configuration changes
  - [ ] Unit tests cover new directory-native caching scenarios
- **Effort**: 2-3 hours
- **Priority**: **HIGH** - Maintains development velocity improvements from [CACHE-001]
- **Status**: **BLOCKED** - Waiting for [ARCH-RAG-01] completion

#### [CACHE-003] Implement Cache Fingerprinting Standard

- **Description**: Implement comprehensive cache fingerprinting to prevent stale cache hits when prompts, templates, or configurations change
- **Dependencies**: [CACHE-002] (RAG index caching reimplemented)
- **Root Cause**: Current cache keys don't include all behavior-affecting inputs (prompts, templates, configs), leading to stale cache hits when these change
- **Evidence**: Statistical analysis cache hit despite prompt template changes; derived metrics cache lacks prompt fingerprinting entirely
- **Solution**: Implement standardized cache fingerprinting for all code-generation caches
- **Acceptance Criteria**:
  - [ ] **Statistical Analysis Cache**: Include `effective_prompt_fingerprint` (SHA-256 of assembled prompt) or `template_fingerprint` (SHA-256 of prompt.yaml)
  - [ ] **Derived Metrics Cache**: Add `_get_prompt_template_hash()` method and include in cache key
  - [ ] **Validation Cache**: Include coherence agent prompt/template hash in cache key
  - [ ] **Cache Key Construction**: Use canonical JSON (sorted keys) + SHA-256 instead of ad-hoc string concatenation
  - [ ] **Fail-Closed Behavior**: If prompt fingerprint cannot be computed, treat as cache miss (no stale reuse)
  - [ ] **Cache Versioning**: Include `cache_version` in all cache inputs and fingerprints
  - [ ] **Runtime Controls**: Add `--no-cache` CLI flag and `DISCERNUS_NO_CACHE=1` env var
  - [ ] **Unit Tests**: Changing only prompt text changes cache key; changing only model changes cache key
- **Effort**: 4-6 hours
- **Priority**: **HIGH** - Prevents critical stale cache issues and improves development reliability
- **Status**: **BACKLOGGED** - Waiting for [CACHE-002] completion

#### [LOGGING-001] Complete Dual-Track Logging Implementation

- **Description**: Fix the incomplete dual-track logging system to ensure all 6 log files are properly populated according to architecture specification
- **Dependencies**: [CLI-007] (CLI logging implementation)
- **Root Cause**: Dual-track logging system is partially implemented - missing orchestrator events, artifact logging, and performance tracking
- **Evidence from CAF Experiment Session**: 
  - `orchestrator.jsonl` missing entirely (should contain stage transitions and execution events)
  - `artifacts.jsonl` missing entirely (should contain artifact creation and relationships)
  - `performance.log` empty (perf_timer() not logging to this file)
  - `errors.log` empty (good - no errors, but should contain error context when they occur)
  - `llm_interactions.log` empty (LLM interactions logged to agents.jsonl instead)
- **Solution**: Complete the dual-track logging implementation with proper event emission from all components
- **Acceptance Criteria**:
  - [ ] **Orchestrator Events**: `CleanAnalysisOrchestrator` emits stage transition events to `orchestrator.jsonl`
  - [ ] **Artifact Logging**: `LocalArtifactStorage` logs artifact creation/modification events to `artifacts.jsonl`
  - [ ] **Performance Tracking**: `perf_timer()` context manager logs metrics to `performance.log`
  - [ ] **Error Logging**: Error handling captures context and logs to `errors.log`
  - [ ] **LLM Interactions**: Consistent logging either to `llm_interactions.log` or consolidated in `agents.jsonl`
  - [ ] **Dual-Track Compliance**: All 6 log files properly populated according to `DUAL_TRACK_LOGGING_ARCHITECTURE.md`
  - [ ] **Event Emission**: Stage boundaries, artifact operations, and system events properly logged
- **Effort**: 3-4 hours
- **Priority**: **HIGH** - Critical for complete dual-track logging implementation
- **Status**: **BACKLOGGED** - Waiting for [CLI-007] completion

### Sprint 3: Testing & Documentation (MEDIUM PRIORITY)

**Timeline:** 2-3 days
**Goal:** Establish comprehensive testing and documentation foundation

#### [TEST-002] Integration Test Strategy

- **Description**: Develop comprehensive integration test strategy
- **Dependencies**: [TEST-001] ✅
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

#### [UX-001] Synthesis Flow Logging Cleanup

- **Description**: Fix synthesis phase logging order to improve readability and logical flow
- **Dependencies**: [TEST-003] ✅
- **Root Cause**: `LocalArtifactStorage.get_artifact()` logs every evidence retrieval during synthesis and RAG index building, creating hundreds of verbose log lines
- **Solution**: Added `quiet=True` parameter to `get_artifact()` and updated all bulk evidence retrieval components
- **Acceptance Criteria**:
  - [x] Evidence retrieval logging suppressed during bulk synthesis operations
  - [x] `UnifiedSynthesisAgent._get_all_evidence()` uses quiet mode
  - [x] `SynthesisPromptAssembler` uses quiet mode for evidence counting
  - [ ] `CleanAnalysisOrchestrator._validate_synthesis_assets()` uses quiet mode for validation
  - [x] `TxtaiEvidenceCurator._get_all_evidence()` uses quiet mode for RAG index building
  - [x] Individual artifact retrievals still logged when appropriate
  - [x] Clean synthesis flow without hundreds of "📥 Retrieved artifact" messages
- **Effort**: 1.5 hours
- **Priority**: **LOW** - Minor UX improvement
- **Status**: **PARTIALLY IMPLEMENTED** - Missing critical method implementation, tests will fail

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
- **Dependencies**: [TEST-002] ✅
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

#### [INTEGRITY-002] Implement FactCheckerAgent for Synthesis Validation

- **Description**: Implement a `FactCheckerAgent` to validate the final synthesis report against source artifacts, preventing factual hallucinations.
- **Dependencies**: [DOCS-003] ✅
- **Architecture**:
  - A second, temporary RAG index will be created post-synthesis containing the final report, framework spec, statistical results, and evidence database.
  - The `FactCheckerAgent` will query this RAG index using a rubric-driven approach.
- **Acceptance Criteria**:
  - [ ] `FactCheckerAgent` is created.
  - [ ] Orchestrator builds a temporary "Fact-Checker RAG" after synthesis.
  - [ ] A `fact_checker_rubric.yaml` is created to define specific, verifiable checks.
  - [ ] The agent generates a `validation_report.md` detailing any findings.
  - [ ] If CRITICAL issues are found, a warning notice is prepended to the `final_report.md`.
  - [ ] Rubric checks for: dimension hallucinations, statistical mismatches, evidence quote validity, and grandiose claims.
- **Effort**: 2-3 days
- **Priority**: HIGH
- **Academic Value**: Provides a critical safeguard against LLM hallucination, ensuring the integrity and trustworthiness of the final research output.

#### [DOCS-001] Comprehensive Architecture Document Update

- **Description**: Update DISCERNUS_SYSTEM_ARCHITECTURE.md to reflect current system state and recent architectural changes
- **Dependencies**: [TEST-001] ✅ (testing foundation established)
- **Current Issues**: Document is outdated and doesn't reflect recent THIN compliance achievements, orchestrator deprecation, and current system architecture
- **Acceptance Criteria**:
  - [ ] Update "Current System Implementation" section to reflect CleanAnalysisOrchestrator as sole orchestrator
  - [ ] Document completed THIN compliance achievements (100% compliance across all 17 agents)
  - [ ] Update agent ecosystem overview to reflect current agent status and deprecation
  - [ ] Remove references to deprecated orchestrators (ExperimentOrchestrator, ThinOrchestrator, etc.)
  - [ ] Update technology stack to reflect current implementation (local storage, no Redis, etc.)
  - [ ] Document current 3-stage pipeline architecture (Analysis → Synthesis → Finalization)
  - [ ] Update agent classifications and compliance status
  - [ ] Reflect current caching and performance optimizations
  - [ ] Update risk assessment based on current system state
  - [ ] Ensure all architectural diagrams and examples are current
- **Effort**: 2-3 days
- **Priority**: **HIGH** - Critical for developer onboarding and architectural clarity
- **Academic Value**: Ensures documentation matches actual system capabilities and prevents architectural confusion
- **Impact**: This document is the primary architectural reference for developers and researchers

#### [DOCS-002] Update Dual-Track Logging Architecture Documentation

- **Description**: Update DUAL_TRACK_LOGGING_ARCHITECTURE.md to reflect current logging implementation and recent improvements
- **Dependencies**: [DOCS-001] (architecture document update)
- **Current Issues**: Document is outdated and doesn't reflect current logging system implementation, recent improvements, and actual system capabilities
- **Acceptance Criteria**:
  - [ ] Update logging architecture overview to reflect current implementation (Loguru-based system)
  - [ ] Document current logging configuration and capabilities in `discernus/core/logging_config.py`
  - [ ] Update performance logging section to reflect current `perf_timer()` implementation
  - [ ] Document current log file structure and rotation policies
  - [ ] Update terminal output section to reflect current Rich console implementation
  - [ ] Document current error handling and logging patterns
  - [ ] Reflect current audit logging and provenance capabilities
  - [ ] Update implementation examples to match current system behavior
  - [ ] Document current logging performance and overhead characteristics
  - [ ] Ensure all architectural diagrams reflect current system state
- **Effort**: 1-2 days
- **Priority**: **MEDIUM** - Important for operational understanding and debugging
- **Academic Value**: Ensures logging documentation matches actual system capabilities for debugging and audit trails
- **Impact**: This document is critical for understanding system operation and debugging issues

#### [DOCS-003] Comprehensive Architecture Documentation Audit & Update

- **Description**: Comprehensive audit and update of all architecture documentation to ensure consistency and accuracy
- **Dependencies**: [DOCS-001] ✅, [DOCS-002] ✅
- **Current Issues**: Multiple architecture documents may have inconsistencies, outdated information, or gaps in coverage
- **Acceptance Criteria**:
  - [ ] Audit all architecture documents for consistency and accuracy
  - [ ] Update PROVENANCE_SYSTEM.md if needed (appears current but verify)
  - [ ] Ensure all documents reflect current system state and capabilities
  - [ ] Verify architectural diagrams and examples are current
  - [ ] Check for any missing architecture documentation
  - [ ] Ensure cross-references between documents are accurate
  - [ ] Validate that all recent architectural changes are documented
  - [ ] Create architecture documentation index/overview if needed
  - [ ] Ensure all documents follow consistent formatting and structure
- **Effort**: 1-2 days
- **Priority**: **MEDIUM** - Ensures documentation quality and consistency
- **Academic Value**: Maintains high-quality architectural documentation for researchers and developers
- **Impact**: Prevents architectural confusion and ensures all stakeholders have accurate system understanding

### Sprint 4: Agent Behavior & Prompt Strategy (HIGH PRIORITY)

**Timeline:** 1-2 days
**Goal:** Refine agent prompts and logic to improve the quality and accuracy of the final research output.

#### [ARCH-SYNTH-01] Implement Architecturally Enforced Numerical Integrity

- **Description**: The `UnifiedSynthesisAgent` has proven unreliable at maintaining verbatim numerical accuracy, ignoring direct prompt instructions and introducing rounding/truncation errors. This architectural flaw results in `CRITICAL` data integrity failures. The solution is to remove the LLM from the responsibility chain for numerical data.
- **Dependencies**: `[ARCH-RAG-01]` (complete)
- **Solution**:
  - 1. **Create a `SynthesisFinisher` Utility**: A new, dedicated component (`discernus/core/synthesis_finisher.py`) will be created. Its sole responsibility is to take a draft text with placeholders and a dictionary of statistical results, and substitute the precise values.
  - 2. **Update Synthesis Prompt**: The `enhanced_synthesis_prompt.yaml` will be modified to instruct the LLM to insert machine-readable placeholders (e.g., `{{corr_hope_vs_fear}}`) instead of numerical values.
  - 3. **Integrate into Orchestrator**: The `CleanAnalysisOrchestrator.run_synthesis_phase` will be updated to first call the synthesis agent to get the draft, then call the `SynthesisFinisher` to produce the final, numerically accurate report before storing the artifact.
- **Acceptance Criteria**:
  - [ ] A new `SynthesisFinisher` utility is created with full unit test coverage.
  - [ ] The `UnifiedSynthesisAgent` prompt is updated to generate placeholders.
  - [ ] The `CleanAnalysisOrchestrator` uses the `SynthesisFinisher` to create the final report.
  - [ ] A full test run of `simple_test_cff` results in zero "Statistic Mismatch" `CRITICAL` errors in the `fact_check_results.json`.
- **Effort**: 3-4 hours
- **Priority**: **CRITICAL** - This is the final blocker to achieving a stable, end-to-end pipeline with full data integrity.
- **Status**: **IN_PROGRESS**


### Sprint 5: End-to-End Logging & Provenance Transformation (HIGH PRIORITY)

**Timeline:** 1-2 weeks
**Goal:** Transform Discernus into an academic-grade platform with comprehensive transparency
**Dependencies:** Alpha release pipeline complete, testing infrastructure stable

**Sprint Structure:**

#### Phase 0: Component Audit & Gap Analysis (Days 1-2)
- **Systematic Component Audit**
  - Audit each system component for current logging and provenance capabilities
  - Map current vs. desired state for academic-grade transparency
  - Identify specific gaps, integration requirements, and effort estimates
  - Create comprehensive implementation roadmap with prioritized components

- **Academic Standards Assessment**
  - Evaluate compliance with peer review transparency requirements
  - Assess fraud detection support capabilities
  - Review reproducibility and citation support standards
  - Define specific success criteria for each component

#### Phase 1: Foundation (Days 3-5)
- **Enhanced Logging Infrastructure**
  - Expand current Loguru system with structured logging
  - Implement log aggregation and search capabilities
  - Add performance monitoring and metrics collection

- **Basic Provenance Foundation**
  - Git integration with `--auto-commit` flag
  - Human-readable run organization
  - Basic audit trail generation

#### Phase 2: Academic Compliance (Days 6-9)
- **Complete Provenance Chains**
  - Full experiment lifecycle tracking
  - Methodology documentation generation
  - Reliability metrics and cross-run consistency

- **Enhanced Observability**
  - MLflow integration for RAG operations
  - Pipeline-level tracing and debugging
  - Performance analytics and bottleneck identification

#### Phase 3: Production Readiness (Days 10-12)
- **Fraud Detection & Validation**
  - Content integrity verification
  - Tamper-evident audit trails
  - Academic citation support

- **Documentation & Integration**
  - Update all architecture documents
  - Create provenance user guides
  - Integration testing and validation

**Strategic Value:**
- Transforms Discernus from basic logging to academic-grade provenance in one focused effort
- Addresses the core academic acceptance blocker (transparency and audit trails)
- Creates a cohesive, well-integrated provenance system rather than piecemeal improvements
- Positions Discernus as the gold standard for research transparency

### Sprint 5: Future Enhancements (LOW PRIORITY)

**Timeline:** Future sprints
**Goal:** Prepare for next phase of development

---

## Provenance System Implementation Strategy

**Current Reality**: System has basic audit logging and results structure, but lacks academic-grade provenance features described in documentation.

**3-Phase Implementation Plan**:

**Phase 1 (Sprint 3) - [PROVENANCE-001]**: **HIGH Priority**
- Basic Git integration and human-readable organization
- Transforms system from "basic logging" to "academic-grade provenance"
- **Effort**: 3-4 days
- **Impact**: Immediate transformation for peer review readiness

**Phase 2 (Next Sprint) - [PROVENANCE-002]**: **MEDIUM Priority**  
- Academic compliance and fraud detection support
- Meets basic peer review requirements
- **Effort**: 4-5 days
- **Impact**: Positions Discernus as meeting traditional academic standards

**Phase 3 (Future) - [PROVENANCE-003]**: **LOW Priority**
- Advanced features exceeding traditional research standards
- Competitive advantage in academic research market
- **Effort**: 3-4 days
- **Impact**: Market differentiation and competitive advantage

**Total Effort**: 10-13 days over 3 phases
**Strategic Value**: Transforms Discernus from basic research tool to academic-grade platform

#### [CLI-007] Implement CLI Logging & Provenance

- **Description**: Add comprehensive logging and provenance tracking to CLI
- **Dependencies**: [DX-001] ✅
- **Root Cause**: Current dual-track logging system is partially implemented - missing orchestrator events, artifact logging, and performance tracking
- **Evidence**: 
  - `orchestrator.jsonl` missing entirely (should contain stage transitions and execution events)
  - `artifacts.jsonl` missing entirely (should contain artifact creation and relationships)
  - `performance.log` empty (perf_timer() not logging to this file)
  - `errors.log` empty (good - no errors, but should contain error context when they occur)
  - `llm_interactions.log` empty (LLM interactions logged to agents.jsonl instead)
- **Solution**: Complete the dual-track logging implementation with proper event emission
- **Acceptance Criteria**:
  - [ ] **Orchestrator Events**: `orchestrator.jsonl` contains stage transitions, execution events, and workflow orchestration
  - [ ] **Artifact Logging**: `artifacts.jsonl` contains artifact creation, modification, and provenance chain events
  - [ ] **Performance Logging**: `performance.log` captures timing metrics from `perf_timer()` context manager
  - [ ] **Error Logging**: `errors.log` captures error context, failure details, and debugging information
  - [ ] **LLM Interactions**: Either populate `llm_interactions.log` or consolidate into `agents.jsonl` consistently
  - [ ] **Dual-Track Compliance**: All 6 log files properly populated according to architecture specification
  - [ ] **Event Emission**: Orchestrator and artifact storage emit proper events at stage boundaries
- **Effort**: 2-3 days
- **Priority**: **HIGH** - Critical for complete dual-track logging implementation

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
- **Dependencies**: [PROVENANCE-002] ✅ (Phase 2 academic compliance complete)
- **Current Status**: Not needed for Phase 1 foundation - can be implemented later if LLM hallucination becomes an issue
- **Acceptance Criteria**:
  - [ ] ProvenanceStamp system integrated into corpus loading
  - [ ] Content hashes generated for all corpus documents
  - [ ] LLM prompts enhanced with provenance stamps
  - [ ] LLM responses validated for correct provenance references
  - [ ] Provenance reports generated for audit trail
  - [ ] Integration detects content tampering and hallucination incidents
- **Effort**: 1-2 days
- **Priority**: **LOW** - Future enhancement if needed
- **Academic Value**: Prevents catastrophic failure where LLMs analyze fabricated content
- **Note**: Current system already has basic content integrity through audit logging and artifact hashing

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

### [PROVENANCE-001] Phase 1: Foundation - Basic Academic Provenance

- **Description**: Implement foundational academic provenance features to transform current system from basic logging to academic-grade provenance
- **Dependencies**: [ARCH-004] ✅ (orchestrator cleanup complete)
- **Current Status**: System has basic audit logging and results structure, needs Git integration and human-readable organization
- **Evidence from Current Implementation**: 
  - Dual-track logging partially implemented: `agents.jsonl` and `system.jsonl` working, but `orchestrator.jsonl` and `artifacts.jsonl` missing
  - Performance logging not capturing `perf_timer()` metrics
  - LLM interaction logging inconsistent (empty `llm_interactions.log`, events in `agents.jsonl`)
- **Acceptance Criteria**:
  - [ ] **Basic Git Integration**: Add `--auto-commit` flag to CLI with basic Git commit after successful runs
  - [ ] **Force Override**: Preserve research despite .gitignore patterns
  - [ ] **Human-Readable Structure**: Implement basic symlink architecture for academic-friendly organization
  - [ ] **README Generation**: Auto-generate README files for each run with basic audit guide
  - [ ] **Basic Validation**: Create `scripts/validate_run_integrity.py` with basic integrity checking
  - [ ] **Simple Validation Report**: Generate basic validation report for each run
  - [ ] **Logging Completeness**: All 6 dual-track log files properly populated and accessible
  - [ ] **Performance Tracking**: `perf_timer()` metrics captured in `performance.log`
- **Effort**: 3-4 days
- **Priority**: **HIGH** - Alpha blocker for academic acceptance
- **Academic Value**: Transforms system from "basic logging" to "academic-grade provenance" with minimal effort
- **Impact**: Immediate transformation of system capabilities for peer review readiness

### [PROVENANCE-002] Phase 2: Academic Compliance - Peer Review Standards

- **Description**: Enhance provenance system to meet basic peer review requirements and fraud detection support
- **Dependencies**: [PROVENANCE-001] ✅ (Phase 1 foundation complete)
- **Acceptance Criteria**:
  - [ ] **Enhanced Audit Trails**: Complete provenance chain documentation with citation-ready metadata
  - [ ] **Methodology Documentation**: Auto-generate methodology sections for academic papers
  - [ ] **Multi-Run Reliability**: Implement Cronbach's α calculation and cross-run consistency metrics
  - [ ] **Reliability Warnings**: Alert researchers when reliability thresholds aren't met
  - [ ] **Fraud Detection Support**: Complete chronological audit trails for all experiment runs
  - [ ] **Source Authentication**: Records for corpus provenance and text authenticity
  - [ ] **Citation Support**: Git commit hashes and metadata for academic citations
- **Effort**: 4-5 days
- **Priority**: **MEDIUM** - Critical for peer review acceptance
- **Academic Value**: Meets basic peer review requirements and enables fraud detection support
- **Impact**: Positions Discernus as meeting traditional academic standards

### [PROVENANCE-003] Phase 3: Advanced Features - Exceed Traditional Standards

- **Description**: Implement advanced provenance features that exceed traditional research standards
- **Dependencies**: [PROVENANCE-002] ✅ (Phase 2 academic compliance complete)
- **Acceptance Criteria**:
  - [ ] **Advanced Validation**: Statistical validation automation and cross-platform reproducibility testing
  - [ ] **Academic Integration**: Direct integration with academic review platforms and automated compliance checking
  - [ ] **Institutional Support**: Audit and reporting capabilities for institutional requirements
  - [ ] **Interactive Transparency**: Transparency browsers and decision audit trails with searchable metadata
  - [ ] **Framework Interpretation**: Workflow documentation for framework interpretation and application
  - [ ] **Advanced Security**: Enhanced security features for high-stakes research
- **Effort**: 3-4 days
- **Priority**: **LOW** - Future enhancement for competitive advantage
- **Academic Value**: Positions Discernus as exceeding traditional research standards
- **Impact**: Competitive advantage in academic research market

---

## Dependencies

### Current Dependencies
- **CLI-002**: [TEST-INFRA] (blocked by test infrastructure fix)
- **CACHE-002**: [ARCH-RAG-01] (blocked by RAG index refactor)
- **CACHE-003**: [CACHE-002] (blocked by RAG index caching reimplementation)
- **CLI-007**: [DX-001] (blocked by developer onboarding)
- **LOGGING-001**: [CLI-007] (blocked by CLI logging implementation)
- **CLI-008**: [CLI-007] (blocked by CLI logging implementation)
- **TECH-002**: [CLI-008] (blocked by CLI testing)

### Provenance System Dependencies
- **PROVENANCE-001**: [TEST-001] ✅ (blocked by testing foundation)
- **PROVENANCE-002**: [PROVENANCE-001] (blocked by Phase 1 foundation)
- **PROVENANCE-003**: [PROVENANCE-002] (blocked by Phase 2 academic compliance)
- **INTEGRITY-001**: [PROVENANCE-002] (blocked by Phase 2 academic compliance)

### RAG Index Refactor Dependencies
- **CACHE-002**: [ARCH-RAG-01] (blocked by RAG index refactor completion)
- **CACHE-003**: [CACHE-002] (blocked by RAG index caching reimplementation)

---

## Current Focus Areas

1. **Sprint 1: Critical Infrastructure & Quality Assurance** - Fix critical system issues and establish testing foundation (IMMEDIATE)
2. **Sprint 2: RAG Index Architecture & Performance** - Centralize RAG index management and optimize performance (HIGH PRIORITY)
3. **Sprint 3: Testing & Documentation** - Establish comprehensive testing and documentation foundation (MEDIUM PRIORITY)
4. **Sprint 4: End-to-End Logging & Provenance Transformation** - Transform system to academic-grade provenance (HIGH PRIORITY)
5. **Sprint 5: Future Enhancements** - Advanced features and optimizations (LOW PRIORITY)

---

## Success Metrics

- **Testing Infrastructure**: All tests pass without false failures
- **Provenance System**: Phase 1 foundation complete - system transformed to academic-grade provenance
- **THIN Architecture**: System maintains clean separation of concerns
- **Code Quality**: 80%+ unit test coverage achieved
- **User Experience**: Clear onboarding and documentation available

### Provenance System Success Metrics
- **Phase 1**: Basic Git integration and human-readable organization working
- **Phase 2**: Academic compliance and fraud detection support implemented
- **Phase 3**: Advanced features exceeding traditional research standards
- **Overall Goal**: Discernus positioned as gold standard for computational research transparency

---



### Sprint 2: RAG Index Content Completeness (NEXT)

**Timeline:** 2-3 days
**Goal:** Ensure comprehensive fact-checker RAG index contains all necessary validation data

#### [RAG-002] Complete Framework Specification in RAG Index ✅ **COMPLETED**

- **Description**: RAG index missing complete framework specification content - only 2 of 10 dimensions (Dignity, Tribalism) found during validation
- **Dependencies**: None (RAG-001 ✅ completed)
- **Root Cause**: `_build_fact_checker_rag_index()` method not properly including full framework specification content
- **Impact**: 
  - Dimension Hallucination checks fail for legitimate framework dimensions
  - Cannot validate framework structure and terminology
  - Incomplete fact-checking coverage
- **Acceptance Criteria**:
  - [x] All 10 CAF dimensions (Dignity, Tribalism, Truth, Manipulation, Justice, Resentment, Hope, Fear, Pragmatism, Fantasy) found in RAG index
  - [x] Complete framework specification text indexed and searchable
  - [x] Framework structure and axis definitions accessible for validation
- **Effort**: 3-4 hours ✅ **COMPLETED**
- **Priority**: **HIGH** (fact-checking completeness)
- **Status**: ✅ **COMPLETED** - Framework specification is properly included in comprehensive RAG index

#### [RAG-003] Include Comprehensive Statistical Results in RAG Index ✅ **COMPLETED**

- **Description**: RAG index missing comprehensive `statistical_results.json` equivalent for numerical validation
- **Dependencies**: None (RAG-001 ✅ completed)
- **Root Cause**: Statistical analysis results not being properly formatted and included in fact-checker RAG index
- **Impact**: 
  - Cannot validate numerical claims (means, correlations, standard deviations)
  - Statistic Mismatch checks fail due to missing reference data
  - No verification of calculated values against source data
- **Acceptance Criteria**:
  - [x] Complete statistical results (means, correlations, std deviations) indexed
  - [x] Speaker-level derived metrics accessible for validation
  - [x] Correlation matrix and descriptive statistics searchable
- **Effort**: 2-3 hours ✅ **COMPLETED**
- **Priority**: **HIGH** (numerical validation)
- **Status**: ✅ **COMPLETED** - Statistical results are properly included in comprehensive RAG index

#### [RAG-004] Include Full Corpus Documents in RAG Index ✅ **COMPLETED**

- **Description**: RAG index missing full text of corpus documents for quote verification
- **Dependencies**: None (RAG-001 ✅ completed)
- **Root Cause**: Evidence Quote Mismatch checks cannot access full corpus text for quote cross-referencing
- **Impact**: 
  - Cannot verify evidence quotes against source documents
  - Quote validation relies on incomplete evidence extracts
  - Reduced confidence in evidence attribution accuracy
- **Acceptance Criteria**:
  - [x] Full text of all corpus documents indexed and searchable
  - [x] Quote verification can cross-reference against complete source text
  - [x] Evidence attribution can be validated end-to-end
- **Effort**: 2-3 hours ✅ **COMPLETED**
- **Priority**: **MEDIUM** (evidence validation)
- **Status**: ✅ **COMPLETED** - Full corpus documents are properly included in comprehensive RAG index

#### [RAG-007] Fix txtai Document ID Mismatch in FactCheckerAgent

- **Description**: FactCheckerAgent cannot retrieve document content due to ID mismatch between txtai search results and stored documents
- **Dependencies**: [RAG-001] ✅, [RAG-005] ✅
- **Root Cause**: txtai search returns document IDs that don't match the sequential IDs (0, 1, 2...) assigned during RAGIndexManager.build_comprehensive_index()
- **Impact**: 
  - Fact-checker reports "Document ID X not found in Y stored documents" errors
  - Cannot access framework specifications, statistical results, or corpus content for validation
  - All fact-checking operations fail despite comprehensive RAG index construction
- **Current Status**: 
  - ✅ RAG index construction working correctly (134 documents indexed)
  - ✅ Document storage working correctly (documents preserved in rag_index.documents)
  - ❌ Document retrieval failing due to ID mismatch between txtai.search() and stored document IDs
- **Acceptance Criteria**:
  - [ ] txtai search results successfully map to stored documents
  - [ ] FactCheckerAgent can retrieve framework specifications for dimension validation
  - [ ] FactCheckerAgent can retrieve statistical results for numerical validation
  - [ ] FactCheckerAgent can retrieve corpus content for quote verification
- **Effort**: 2-3 hours
- **Priority**: **HIGH** (blocks all fact-checking functionality)





### Sprint 3: Advanced RAG Architecture (FUTURE)

**Timeline:** 1-2 weeks
**Goal:** Implement advanced txtai features for improved performance and accuracy

#### [RAG-007] Implement Sub-Indexes Architecture

- **Description**: Create specialized RAG indexes for different data types (framework, statistics, evidence, corpus) for improved query performance and accuracy
- **Dependencies**: [RAG-002], [RAG-003], [RAG-004], [RAG-005] ✅
- **Root Cause**: Single comprehensive index may not be optimal for different query types and data characteristics
- **Impact**: 
  - Improved query accuracy through specialized indexing strategies
  - Better performance for specific data type queries
  - Reduced cross-contamination between different content types
  - Enhanced filtering and retrieval precision
- **Acceptance Criteria**:
  - [ ] Framework-specific index for dimension and structure validation
  - [ ] Statistics-specific index for numerical validation
  - [ ] Evidence-specific index for quote verification
  - [ ] Corpus-specific index for full-text search
  - [ ] Unified query interface across all sub-indexes
- **Effort**: 1-2 weeks
- **Priority**: **MEDIUM** (performance optimization)

#### [RAG-008] Implement Hybrid Search Capabilities

- **Description**: Add sparse/dense hybrid search to txtai indexes for improved retrieval accuracy
- **Dependencies**: [RAG-007] ✅
- **Root Cause**: Pure dense vector search may miss exact matches that sparse search would find
- **Impact**: 
  - Improved retrieval accuracy for both semantic and exact matches
  - Better handling of technical terms and specific phrases
  - Enhanced fact-checking precision for numerical and textual validation
- **Acceptance Criteria**:
  - [ ] Hybrid search configuration in RAGIndexManager
  - [ ] Benchmarking against current dense-only approach
  - [ ] Configurable search strategy per index type
  - [ ] Maintained or improved query performance
- **Effort**: 1 week
- **Priority**: **LOW** (advanced optimization)

## Backlog Maintenance

- **Last Updated**: 2025-08-25
- **Next Review**: After critical infrastructure verification
- **Cleanup Status**: ✅ Groomed and streamlined with sprint restructuring
- **Completed Items Moved**: [CRITICAL-005], [CRITICAL-006], [ARCH-004], [RAG-001], [RAG-005], and [RAG-006] moved to DONE.md
- **Redundant Items**: Informal duplicate items consolidated into formal backlog structure
- **Sprint Restructuring**: Completed - fixed dependency conflicts and logical flow
- **Verification Required**: Multiple "completed" items unchecked due to missing implementation verification
- **New Insights**: 
  - Added [CACHE-003] for comprehensive cache fingerprinting standard based on stale cache analysis
  - Added [LOGGING-001] for dual-track logging completion based on CAF experiment session analysis
  - Enhanced [CLI-007] and [PROVENANCE-001] with specific logging implementation requirements
  - Added [RAG-002], [RAG-003], [RAG-004] for comprehensive fact-checker RAG index completeness
  - Unchecked [UX-001], [CRITICAL-001], [CRITICAL-002], [CRITICAL-003], [PERF-001], [CACHE-001], [QUALITY-001], [QUALITY-002], [QUALITY-003] due to missing verification

## Current Priorities

### High Priority
**Note**: The following informal items have been consolidated into formal backlog items:
- ~~Fix RAG index failures in fact-checking system~~ → **Addressed by [CRITICAL-006] ✅**
- ~~Fix silent validation failures in fact-checking system~~ → **Addressed by [CRITICAL-005] ✅**  
- ~~Fix problematic fallback patterns in core pipeline~~ → **Addressed by [CRITICAL-007]**

**Remaining High Priority Items:**
- [CRITICAL-007] Fix Orchestrator Graceful Degradation Violations (Sprint 1)
- [CRITICAL-004] Fix Missing Derived Metrics Artifact Storage (Sprint 1)
- [TEST-INFRA] Fix Integration Test Infrastructure (Sprint 1)

**Note**: [CRITICAL-005] and [CRITICAL-006] have been completed and moved to DONE.md

- [x] ~~Fix derived metrics and statistical analysis validation gap~~ **ATTEMPTED & REVERTED**
  - **Issue**: Current validation passes metadata-only results that contain no actual statistical outputs
  - **Attempted Solution**: Hash-based validation in code generation prompts
    - Add validation_hash field to generated functions
    - Calculate hash from actual results (e.g., hash(str(sorted(results.keys())))
    - Simple validation: just check for presence of validation_hash
    - More elegant than complex nested data structure analysis
    - Aligns with THIN principles
  - **Result**: Architecturally sound but practically unusable
    - LLM (Gemini 2.5 Pro) consistently failed to follow prompt instructions
    - Despite multiple prompt refinements, functions returned simple values instead of required dictionaries with validation hashes
    - Hash-based validation correctly rejected non-compliant functions, proving the architecture works
    - **Root Cause**: Prompt compliance issue, not system architecture problem
  - **Status**: Reverted (commit 6ad02c19) - system returned to operational state
  - **Lesson Learned**: Even flagship models may not reliably follow complex prompt requirements
  - **Alternative Approaches**: Try different models (Claude, GPT-4), post-processing, or accept current validation approach

- [ ] Replace brittle placeholder system with THIN revision agent approach
  - **Problem**: Current `SynthesisFinisher` with `{corr(var1, var2)}` placeholders is architecturally fragile
    - Single character changes in LLM output break entire numerical integrity system
    - Brittle regex parsing violates THIN principles
    - Over-engineered solution to hypothetical problem (no actual numerical failures observed)
    - ~200 lines of complex code for undemonstrated need
  - **THIN Solution**: Focused revision agent with clear boundaries
    - Synthesis agent writes naturally (no placeholder constraints)
    - Fact-checker validates comprehensively as it does now
    - New RevisionAgent makes targeted corrections based on fact-checker feedback
    - Error threshold: fail-fast if too many issues for safe revision
  - **Revision Agent Scope**:
    - ✅ Allowed: Numerical corrections, tone moderation (grandiose claims), factual fixes, evidence attribution
    - ❌ Forbidden: Structural rewrites, new analysis, narrative flow changes, major section changes
    - Constraint: Output should be 95%+ identical to input, preserving author voice
  - **Error Thresholds**: MAX_NUMERICAL_ERRORS=10, MAX_GRANDIOSE_CLAIMS=5, MAX_TOTAL_ISSUES=15
  - **Architecture**: Synthesis → Fact-Check → Revision (or error) → Final Validation
  - **Benefits**: Robust, maintainable, uses LLM strengths, solves real vs hypothetical problems
  - **Implementation**: Remove SynthesisFinisher, create RevisionAgent with constrained editing prompt
  - **Status**: Ready for implementation - replaces current brittle system
  - **Priority**: High (architectural improvement, reduces technical debt)

- [ ] Audit production pipeline for THICK parsing anti-patterns
  - **Problem**: Integration testing revealed brittle parsing patterns that violate THIN architecture principles
    - CAF experiment failed due to hardcoded filename parsing (`[:-2]` index slicing)
    - Speaker extraction logic assumed fixed filename structure, broke on multi-word names
    - Parsing failures produce silent degradation rather than fail-fast behavior
    - Violates project's THIN principles of avoiding parsing in favor of binary data flow
  - **Scope**: Audit components that parse filenames, paths, or assume fixed data structures
    - Data ingestion and metadata extraction components (HIGH priority)
    - Analysis functions that derive grouping variables (MEDIUM priority)
    - Output formatting and reporting functions (LOW priority)
  - **Acceptance Criteria**:
    - [ ] Identify all instances of brittle parsing (hardcoded indices, fixed structure assumptions)
    - [ ] Document parsing failures discovered during integration testing
    - [ ] Prioritize fixes based on actual failure impact vs theoretical concerns
    - [ ] Replace brittle parsing with robust, semantic-based extraction where needed
    - [ ] Maintain THIN architecture principles throughout
  - **Dependencies**: Complete integration test gauntlet to surface all parsing issues
  - **Status**: Backlogged - waiting for integration test completion
  - **Priority**: Medium (architectural improvement, prevents future failures)
