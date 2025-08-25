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

#### [CRITICAL-003] Fix Silent Statistical Analysis Failures ✅ **COMPLETED**

- **Description**: **CRITICAL BUG**: Statistical analysis phase reports success but produces no numerical results, allowing experiments to continue to synthesis with invalid data
- **Dependencies**: [CRITICAL-001] ✅, [CRITICAL-002] ✅
- **Root Cause**: `_run_statistical_analysis_phase` method executes statistical functions but doesn't validate the output, blindly setting `"validation_passed": True"`
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

#### [CRITICAL-004] Fix Missing Derived Metrics Artifact Storage

- **Description**: **CRITICAL BUG**: Derived metrics artifacts are not being stored in the run results directory, unlike statistical results which are properly stored
- **Dependencies**: [CRITICAL-003] ✅
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

#### [CACHE-001] RAG Index Caching Implementation ✅ **COMPLETED** (Temporary)

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
- **Note**: This implementation will be superseded by [ARCH-RAG-01] refactor. After refactor completion, caching will need to be reimplemented for the new directory-native architecture without tar.gz compression.

#### [CACHE-002] Reimplement RAG Index Caching for New Architecture

- **Description**: Reimplement RAG index caching after [ARCH-RAG-01] refactor to leverage the new directory-native architecture
- **Dependencies**: [ARCH-RAG-01] ✅ (RAG index refactor complete)
- **Root Cause**: [CACHE-001] implementation used tar.gz compression workaround that will be eliminated by the refactor
- **Solution**: Implement caching for the new `RAGIndexManager` using native directory storage
- **Acceptance Criteria**:
  - [ ] Caching integrated with new `RAGIndexManager` class
  - [ ] Cache stores native txtai directories without compression overhead
  - [ ] Cache keys include RAG index configuration parameters (e.g., `{"content": True}` settings)
  - [ ] Performance improvements exceed current 10-15 second speedup
  - [ ] Caching works for both fact-checker and synthesis RAG indexes
  - [ ] Cache invalidation properly handles RAG index configuration changes
  - [ ] Unit tests cover new directory-native caching scenarios
- **Effort**: 2-3 hours
- **Priority**: **HIGH** - Maintains development velocity improvements from [CACHE-001]
- **Status**: **BLOCKED** - Waiting for [ARCH-RAG-01] completion

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
- **Acceptance Criteria**:
  - [ ] **Basic Git Integration**: Add `--auto-commit` flag to CLI with basic Git commit after successful runs
  - [ ] **Force Override**: Preserve research despite .gitignore patterns
  - [ ] **Human-Readable Structure**: Implement basic symlink architecture for academic-friendly organization
  - [ ] **README Generation**: Auto-generate README files for each run with basic audit guide
  - [ ] **Basic Validation**: Create `scripts/validate_run_integrity.py` with basic integrity checking
  - [ ] **Simple Validation Report**: Generate basic validation report for each run
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
- **CLI-007**: [DX-001] (blocked by developer onboarding)
- **CLI-008**: [CLI-007] (blocked by CLI logging implementation)
- **TECH-002**: [CLI-008] (blocked by CLI testing)

### Provenance System Dependencies
- **PROVENANCE-001**: [TEST-001] ✅ (blocked by testing foundation)
- **PROVENANCE-002**: [PROVENANCE-001] (blocked by Phase 1 foundation)
- **PROVENANCE-003**: [PROVENANCE-002] (blocked by Phase 2 academic compliance)
- **INTEGRITY-001**: [PROVENANCE-002] (blocked by Phase 2 academic compliance)

### RAG Index Refactor Dependencies
- **CACHE-002**: [ARCH-RAG-01] (blocked by RAG index refactor completion)

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

## Backlog Maintenance

- **Last Updated**: 2025-01-23
- **Next Review**: After testing infrastructure fix
- **Cleanup Status**: ✅ Groomed and streamlined with sprint restructuring
- **Completed Items Moved**: [CRITICAL-005], [CRITICAL-006], and [ARCH-004] moved to DONE.md
- **Redundant Items**: Informal duplicate items consolidated into formal backlog structure
- **Sprint Restructuring**: Completed - fixed dependency conflicts and logical flow

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

- [ ] Fix derived metrics and statistical analysis validation gap
  - **Issue**: Current validation passes metadata-only results that contain no actual statistical outputs
  - **Current Approach**: Complex data structure validation that's getting THICK
  - **Proposed Solution**: Hash-based validation in code generation prompts
    - Add validation_hash field to generated functions
    - Calculate hash from actual results (e.g., hash(str(sorted(results.keys())))
    - Simple validation: just check for presence of validation_hash
    - More elegant than complex nested data structure analysis
    - Aligns with THIN principles
  - **Status**: Backlogged for future implementation
  - **Priority**: Medium
