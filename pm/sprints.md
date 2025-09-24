# Discernus V2 Sprints - Agent Refactoring & Integration Testing

**Purpose**: Organized backlog for fixing critical agent architecture issues and achieving robust end-to-end functionality.

**Usage**:

- Each sprint has clear definition of done criteria
- Focus on atomic processing and proper agent separation
- Comprehensive integration testing across experiment sizes

---

## Current Status

**Latest Updates**:

- ✅ **CRITICAL BUGS IDENTIFIED**: AnalysisAgent processes documents incorrectly (batch vs atomic)
- ✅ **TOKEN LIMIT ISSUES RESOLVED**: Synthesis agent no longer receives massive composite analysis data
- ✅ **CSV GENERATION DISABLED**: Eliminated timeout issues for alpha release
- ✅ **V2 AGENT ECOSYSTEM COMPLETE**: All core agents migrated to V2 standard
- 🔄 **CURRENT FOCUS**: Documentation cleanup and alpha release preparation

**Current Focus**: **Sprint DOC-CLEANUP-1: Documentation Cleanup for Alpha Release**. Remove deprecated documentation and prepare clean user experience.

---

## Documentation & Alpha Release Sprint Plan

### Sprint DOC-CLEANUP-1: Documentation Cleanup for Alpha Release 📋 **CURRENT FOCUS**

**Timeline**: 1 week
**Goal**: Remove deprecated documentation and prepare clean user experience for alpha release
**Definition of Done**: Documentation is clean, focused, and ready for alpha users

**Detailed Tasks**:

#### [DOC-CLEANUP-1.1] Remove Deprecated Specifications

- **Objective**: Delete entire `docs/specifications/deprecated/` directory
- **Files to Remove**: 13 deprecated specification files (v3, v4, v5, v6, v7, v7.1, v7.2, v7.3, v8)
- **Rationale**: Historical artifacts that will confuse alpha users
- **Definition of Done**: Deprecated specifications directory completely removed

#### [DOC-CLEANUP-1.2] Remove Duplicate Architecture Documentation

- **Objective**: Remove duplicate architecture documentation
- **Files to Remove**: `docs/architecture/DISCERNUS_SYSTEM_ARCHITECTURE.md`
- **Keep**: `docs/developer/architecture/DISCERNUS_SYSTEM_ARCHITECTURE.md` (more comprehensive)
- **Definition of Done**: No duplicate architecture documentation exists

#### [DOC-CLEANUP-1.3] Clean Up Archive Directory

- **Objective**: Remove outdated archive content
- **Files to Remove**: 
  - `docs/archive/INTEGRATED_PROVENANCE_VALIDATION_SPEC.md` (draft, not implemented)
  - `docs/archive/synthesis_agent_architecture_v2.md` (superseded)
  - `docs/archive/ARCHIVE.md` (internal process document)
- **Keep**: `docs/archive/README.md` (archive policy for maintainers)
- **Definition of Done**: Archive directory contains only essential maintainer documentation

#### [DOC-CLEANUP-1.4] Review Internal Process Documentation

- **Objective**: Identify internal documentation that should be moved to attic branch
- **Files to Review**:
  - `docs/developer/BATCH_PROCESSING_REGRESSION_REMEDIATION_PLAN.md`
  - `docs/developer/TDD_CRITICAL_REGRESSION_PROTOCOL.md`
  - `docs/developer/CURSOR_AGENT_DISCIPLINE_GUIDE.md`
  - `docs/developer/CURSOR_AGENT_TDD_LEARNINGS.md`
  - `docs/developer/THIN_COMPLIANCE_FIX_SUMMARY.md`
- **Definition of Done**: Internal process docs moved to attic branch or removed

#### [DOC-CLEANUP-1.5] Consolidate Redundant Technical Documentation

- **Objective**: Merge redundant technical documentation
- **Files to Consolidate**:
  - Merge `docs/developer/LLM_MODEL_SELECTION_GUIDE.md` content into `CLI_BEST_PRACTICES.md`
  - Consider archiving `docs/developer/DSQ_ARCHITECTURE_GUIDE.md`
- **Definition of Done**: No redundant technical documentation exists

**Definition of Done**:
- ✅ Deprecated specifications directory completely removed
- ✅ No duplicate architecture documentation exists
- ✅ Archive directory contains only essential maintainer documentation
- ✅ Internal process docs moved to attic branch or removed
- ✅ No redundant technical documentation exists
- ✅ Documentation structure is clean and focused for alpha users

---

### Sprint DOC-ENHANCE-1: Essential Documentation for Alpha Release 📋 **PENDING**

**Timeline**: 2 weeks
**Goal**: Add missing essential documentation for alpha release
**Definition of Done**: Alpha users have complete documentation for successful platform adoption

**Detailed Tasks**:

#### [DOC-ENHANCE-1.1] Create Framework Examples Guide

- **Objective**: Provide working examples of different framework types
- **Content**: 3-5 working framework examples with different analytical approaches
- **Include**: Sentiment analysis, discourse analysis, ethics frameworks
- **Show**: Common patterns, best practices, and anti-patterns
- **File**: `docs/user/FRAMEWORK_EXAMPLES.md`
- **Definition of Done**: Users can create frameworks using provided examples

#### [DOC-ENHANCE-1.2] Create Corpus Preparation Guide

- **Objective**: Guide users on how to format and organize text collections
- **Content**: Text formatting requirements, metadata standards, quality control
- **Include**: Step-by-step corpus preparation, validation checklist
- **File**: `docs/user/CORPUS_PREPARATION.md`
- **Definition of Done**: Users can prepare corpora that pass validation

#### [DOC-ENHANCE-1.3] Create Results Interpretation Guide

- **Objective**: Help users understand and interpret analysis outputs
- **Content**: How to read analysis outputs, understand statistical results, evidence tracking
- **Include**: Statistical significance interpretation, evidence validation process
- **File**: `docs/user/RESULTS_INTERPRETATION.md`
- **Definition of Done**: Users can interpret and validate their results

#### [DOC-ENHANCE-1.4] Create Contributing Guide

- **Objective**: Enable community contributions to the project
- **Content**: Development setup, code contribution process, framework contribution guidelines
- **Include**: Code style, pull request process, testing requirements
- **File**: `docs/developer/CONTRIBUTING.md`
- **Definition of Done**: Contributors can successfully contribute to the project

#### [DOC-ENHANCE-1.5] Create Migration Guide

- **Objective**: Help users upgrade from previous versions
- **Content**: Breaking changes, configuration migration, workarounds
- **Include**: Step-by-step migration process, common issues
- **File**: `docs/user/MIGRATION_GUIDE.md`
- **Definition of Done**: Users can successfully migrate from previous versions

**Definition of Done**:
- ✅ Framework Examples Guide with 3-5 working examples
- ✅ Corpus Preparation Guide with validation checklist
- ✅ Results Interpretation Guide with statistical guidance
- ✅ Contributing Guide with development setup
- ✅ Migration Guide with breaking changes and workarounds
- ✅ All guides tested with real examples and scenarios

---

### Sprint DOC-COMMUNITY-1: Community Documentation for Alpha Release 📋 **PENDING**

**Timeline**: 1 week
**Goal**: Create community and support documentation for alpha release
**Definition of Done**: Alpha users have clear community guidelines and support channels

**Detailed Tasks**:

#### [DOC-COMMUNITY-1.1] Create Community Guidelines

- **Objective**: Establish community standards and participation guidelines
- **Content**: Alpha testing participation, issue reporting process, community standards
- **Include**: Code of conduct, contribution guidelines, feedback process
- **File**: `docs/COMMUNITY_GUIDELINES.md`
- **Definition of Done**: Clear community standards established

#### [DOC-COMMUNITY-1.2] Create Security and Privacy Guide

- **Objective**: Document data handling and privacy considerations
- **Content**: Data privacy, API key management, best practices for sensitive data
- **Include**: Security considerations, data handling guidelines
- **File**: `docs/user/SECURITY_GUIDE.md`
- **Definition of Done**: Users understand security and privacy implications

#### [DOC-COMMUNITY-1.3] Enhance Troubleshooting Guide

- **Objective**: Expand troubleshooting coverage for alpha-specific issues
- **Content**: Alpha-specific limitations, common issues, debugging approaches
- **Include**: Performance issues, cost management, error recovery
- **File**: Update `docs/user/TROUBLESHOOTING_GUIDE.md`
- **Definition of Done**: Comprehensive troubleshooting coverage for alpha users

#### [DOC-COMMUNITY-1.4] Create Alpha Testing Guide

- **Objective**: Guide users through alpha testing process
- **Content**: Alpha limitations, testing scenarios, feedback collection
- **Include**: What to test, how to report issues, expected behaviors
- **File**: `docs/user/ALPHA_TESTING_GUIDE.md`
- **Definition of Done**: Clear alpha testing process established

**Definition of Done**:
- ✅ Community Guidelines with participation standards
- ✅ Security and Privacy Guide with data handling guidelines
- ✅ Enhanced Troubleshooting Guide with alpha-specific issues
- ✅ Alpha Testing Guide with testing scenarios and feedback process
- ✅ All community documentation tested and validated

---

## Sprint Priority and Timeline

### **IMMEDIATE PRIORITY (Alpha Release Blockers)**

1. **Sprint DOC-CLEANUP-1** - Documentation Cleanup for Alpha Release (1 week)
   - Remove deprecated specifications and duplicate docs
   - Clean up archive directory and internal process docs
   - **Status**: 📋 **CURRENT FOCUS**

2. **Sprint DOC-ENHANCE-1** - Essential Documentation for Alpha Release (2 weeks)
   - Framework Examples Guide, Corpus Preparation Guide
   - Results Interpretation Guide, Contributing Guide, Migration Guide
   - **Status**: 📋 **PENDING**

### **HIGH PRIORITY (Alpha Release Enhancers)**

3. **Sprint DOC-COMMUNITY-1** - Community Documentation for Alpha Release (1 week)
   - Community Guidelines, Security Guide, Alpha Testing Guide
   - **Status**: 📋 **PENDING**

4. **Sprint V2-INTEGRATION-1** - Small Experiment Testing (1 week)
   - Test nano, micro, and MLKMX experiments
   - **Status**: 📋 **PENDING**

### **MEDIUM PRIORITY (Post-Alpha)**

5. **Sprint V2-INTEGRATION-2** - Medium Experiment Testing (1 week)
   - Test business ethics, framing, and political experiments
   - **Status**: 📋 **PENDING**

6. **Sprint V2-INTEGRATION-3** - Large Experiment Testing (1 week)
   - Test kirk, trump populism, and constitutional health experiments
   - **Status**: 📋 **PENDING**

### **LOW PRIORITY (Future)**

7. **Sprint V2-INTEGRATION-4** - Performance & Reliability Testing (1 week)
   - Stress testing, error recovery, performance optimization
   - **Status**: 📋 **PENDING**

8. **Sprint V2-8** - Convert Legacy Agents to V2 Native (Future)
   - Technical debt reduction and performance optimization
   - **Status**: ⏳ **PENDING**

9. **Sprint V2-10** - Restore Advanced CLI Functionality (Future)
   - Model selection flags, dry-run, validation, auto-commit
   - **Status**: ⏳ **PENDING**

---

## V2 Agent Refactoring Sprint Plan




### Sprint V2-INTEGRATION-1: Small Experiment Testing 📋 **PENDING**

**Timeline**: 1 week
**Goal**: Comprehensive testing with small experiments to verify atomic processing
**Definition of Done**: All small experiments run successfully end-to-end

**Detailed Tasks**:

#### [V2-INTEGRATION-1.1] Test Nano Experiment

- **Test**: Run nano_test_experiment with atomic processing
- **Definition of Done**: Complete success, all artifacts created correctly

#### [V2-INTEGRATION-1.2] Test Micro Experiment

- **Test**: Run micro_test_experiment with atomic processing
- **Definition of Done**: Complete success, all artifacts created correctly

#### [V2-INTEGRATION-1.3] Test MLKMX Experiment

- **Test**: Run mlkmx experiment with atomic processing
- **Definition of Done**: Complete success, all artifacts created correctly

### Sprint V2-INTEGRATION-2: Medium Experiment Testing 📋 **PENDING**

**Timeline**: 1 week
**Goal**: Test with medium-sized experiments to verify scalability
**Definition of Done**: Medium experiments run successfully without token limit issues

**Detailed Tasks**:

#### [V2-INTEGRATION-2.1] Test Business Ethics Experiment

- **Test**: Run business_ethics_experiment
- **Definition of Done**: Complete success, proper atomic processing

#### [V2-INTEGRATION-2.2] Test Framing Experiments

- **Test**: Run entman_framing_experiment and lakoff_framing_experiment
- **Definition of Done**: Complete success, proper atomic processing

#### [V2-INTEGRATION-2.3] Test Political Experiments

- **Test**: Run 2a_populist_rhetoric_study
- **Definition of Done**: Complete success, proper atomic processing

### Sprint V2-INTEGRATION-3: Large Experiment Testing 📋 **PENDING**

**Timeline**: 1 week
**Goal**: Test with large experiments to verify system robustness
**Definition of Done**: Large experiments run successfully with proper error handling

**Detailed Tasks**:

#### [V2-INTEGRATION-3.1] Test Kirk Experiment

- **Test**: Run kirk experiment with atomic processing
- **Definition of Done**: Complete success, no token limit issues, proper evidence curation

#### [V2-INTEGRATION-3.2] Test Trump Populism Experiment

- **Test**: Run 2d_trump_populism experiment
- **Definition of Done**: Complete success, proper atomic processing

#### [V2-INTEGRATION-3.3] Test Constitutional Health Experiment

- **Test**: Run 1b_chf_constitutional_health experiment
- **Definition of Done**: Complete success, proper atomic processing

### Sprint V2-INTEGRATION-4: Performance & Reliability Testing 📋 **PENDING**

**Timeline**: 1 week
**Goal**: Comprehensive performance and reliability testing
**Definition of Done**: System is robust, reliable, and ready for production use

**Detailed Tasks**:

#### [V2-INTEGRATION-4.1] Stress Testing

- **Test**: Run multiple experiments in parallel
- **Definition of Done**: System handles concurrent experiments without issues

#### [V2-INTEGRATION-4.2] Error Recovery Testing

- **Test**: Test system recovery from various failure modes
- **Definition of Done**: System recovers gracefully from failures

#### [V2-INTEGRATION-4.3] Performance Optimization

- **Test**: Optimize system performance based on testing results
- **Definition of Done**: System meets performance requirements

---


### Sprint V2-2: EvidenceRetrieverAgent Migration & RAG Consolidation 🔴 IN PROGRESS

**Corresponds to**: V2 Plan - Phase 1 (Weeks 3-4) & Phase 1.5
**Goal**: Migrate the most complex legacy agent to the V2 standard and centralize all RAG logic within it, removing it from the orchestrator.

**Detailed Tasks**:

#### [V2-2.1] Refactor `EvidenceRetrieverAgent` Constructor

- **Current Issue**: Uses `config: Dict[str, Any]` anti-pattern
- **Solution**: Replace with proper dependency injection following `AnalysisAgent` pattern
- **New Constructor**: `__init__(security: ExperimentSecurityBoundary, storage: LocalArtifactStorage, audit: AuditLogger, config: Optional[AgentConfig] = None)`
- **Files to Update**: `discernus/agents/evidence_retriever_agent/evidence_retriever_agent.py`

#### [V2-2.2] Implement Responsibility Separation

- **Method Structure**:
  - `_discover_evidence_artifacts(analysis_hashes: List[str]) -> List[str]`
  - `_generate_evidence_queries(statistical_results: Dict) -> List[str]`
  - `_retrieve_evidence(queries: List[str]) -> List[Dict]`
  - `_structure_evidence_output(evidence: List[Dict]) -> Dict`
- **Purpose**: Clear separation of concerns within the agent

#### [V2-2.3] Add Tool Calling Integration

- **Tools to Add**:
  - `record_evidence_finding` for structured output
  - `verify_evidence_relevance` for verification step
- **Implementation**: Follow existing tool calling patterns from `AnalysisAgent`

#### [V2-2.4] Implement "Own RAG" Pattern

- **RAGIndexManager**: Create dedicated class for RAG lifecycle management
- **Index Scope Selection**: Choose sources based on `RunContext` and statistical cues
- **Index Build**: Delegate to `RAGIndexManager` for txtai index with metadata
- **Caching & Invalidation**: Cache keys from experiment/framework IDs, upstream artifact hashes
- **Retrieval**: Generate queries via tool call, run top-k lookups with structured quotes
- **Provenance**: Record cache key, source hashes, retrieval parameters in metadata
- **Files to Create**: `discernus/core/rag_index_manager.py`

#### [V2-2.5] Ensure Agent Self-Sufficiency

- **Framework Reading**: Agent reads framework directly from path (not pre-created artifact)
- **Artifact Discovery**: Agent discovers evidence artifacts from analysis hashes
- **Statistical Results**: Agent reads statistical results from artifact hash
- **No Orchestrator Dependencies**: Agent handles all infrastructure setup internally

#### [V2-2.6] Delete Orchestrator RAG Logic (Phase 1.5)

- **Remove Methods**: All `_build_fact_checker_rag_index` and `_build_*rag_index*` functions
- **Normalize Artifacts**: Evidence artifact typing/versioning for agent discovery
- **Cache Management**: Move to dedicated RAG cache manager
- **Files to Update**: `discernus/core/clean_analysis_orchestrator.py`

**Definition of Done**:

- ❌ `EvidenceRetrieverAgent` implements `StandardAgent` interface
- ❌ Constructor uses proper dependency injection (no `Dict[str, Any]` config)
- ❌ Agent has clear method separation for evidence workflow
- ❌ Tool calling integrated with `record_evidence_finding` and `verify_evidence_relevance`
- ❌ `RAGIndexManager` created and handles all RAG lifecycle operations
- ❌ Agent reads framework and statistical results directly from artifacts
- ❌ Agent discovers evidence artifacts from analysis hashes without orchestrator help
- ❌ All orchestrator RAG methods deleted (80+ lines removed)
- ❌ Orchestrator evidence phase reduced to ~10 lines (simple agent call)
- ❌ No regression in evidence quality (validated with existing experiments)
- ❌ Unit tests for `RAGIndexManager` and refactored agent
- ❌ Integration tests showing end-to-end evidence retrieval works

**Foundation Completion Date**: TBD
**Commit**: TBD
**Status**: In Progress - Agent requires full implementation.

### Sprint V2-3: UnifiedSynthesisAgent Migration 🔴 IN PROGRESS

**Corresponds to**: V2 Plan - Phase 2 (Weeks 5-6)
**Goal**: Migrate the synthesis agent to the new standard, focusing on consuming V2-native artifacts.

**Detailed Tasks**:

#### [V2-3.1] Refactor `UnifiedSynthesisAgent` Interface

- **Implement `StandardAgent`**: Update constructor and methods to match standard interface
- **Constructor**: `__init__(security: ExperimentSecurityBoundary, storage: LocalArtifactStorage, audit: AuditLogger, config: Optional[AgentConfig] = None)`
- **Execute Method**: `execute(run_context: RunContext) -> AgentResult`
- **Files to Update**: `discernus/agents/unified_synthesis_agent/agent.py`

#### [V2-3.2] Artifact Format Migration

- **Read V2 Artifacts**: Consume `analysis_scores.json`, `evidence_quotes.json`, `computational_work.json` directly
- **Remove CSV Parsing**: Eliminate all CSV parsing and old artifact format assumptions
- **Compatibility Layer**: Temporary adapter for transition period if needed
- **Raw Object Policy**: Operate on in-memory objects for handoffs; serialize only for final artifacts

#### [V2-3.3] Consume `RunContext` for All Inputs

- **Analysis Results**: Read from `run_context.analysis_results` instead of filesystem discovery
- **Evidence Data**: Read from `run_context.evidence` instead of scanning for evidence files
- **Statistical Results**: Read from `run_context.statistical_results` instead of CSV parsing
- **Metadata**: Use `run_context.metadata` for artifact hashes and cache keys
- **No Filesystem Scanning**: Remove all logic that discovers artifacts from disk

#### [V2-3.4] Enhanced Synthesis Features

- **Computational Work Integration**: Incorporate computational work from V2 artifacts
- **Verification Result Integration**: Include verification results in synthesis
- **Statistical Presentation**: Consistent 2-3 significant digits with disclosure
- **Tool Calling**: Add structured output via tool calling for report metadata

**Definition of Done**:

- ❌ `UnifiedSynthesisAgent` implements `StandardAgent` interface
- ❌ Agent constructor uses proper dependency injection
- ❌ Agent reads all inputs from `RunContext` object (no filesystem scanning)
- ❌ Agent consumes V2 artifact formats (`analysis_scores.json`, `evidence_quotes.json`, `computational_work.json`)
- ❌ CSV parsing logic removed and replaced with structured data consumption
- ❌ Computational work and verification results integrated into synthesis
- ❌ Statistical results presented with consistent significant digits and disclosure
- ❌ Tool calling implemented for structured report metadata output
- ❌ No regression in synthesis quality (validated with existing experiments)
- ❌ Unit tests for refactored agent (15 tests passing)
- ❌ Integration tests showing end-to-end synthesis works with V2 artifacts
- ❌ Orchestrator updated to use V2UnifiedSynthesisAgent

**Foundation Completion Date**: TBD
**Commit**: TBD
**Status**: In Progress - Agent requires full implementation.

### Sprint V2-3.5: ~~Orchestrator Integration & Legacy Cleanup~~ ❌ CANCELLED

**Strategic Decision**: Skip legacy orchestrator integration in favor of building new V2 orchestrator from scratch.

**Rationale**:

- Legacy orchestrator (4,394 lines) is monolithic and architecturally incompatible with V2 patterns
- Integration effort would be massive and temporary (thrown away when V2 orchestrator is built)
- Risk of introducing bugs in working V1 system
- Better to build clean V2 orchestrator with V2 patterns from the start

**Alternative Path**: Complete agent foundation + build new V2 orchestrator (Sprints V2-4, V2-5, V2-6)

### Sprint V2-4: ~~Verification Agent Ecosystem~~ ❌ CANCELLED

**Strategic Decision**: Skip separate verification agents - current embedded verification is already adversarial and working well.

**Rationale**:

- Current embedded verification uses independent LLM calls with separate prompts
- Verification steps are already adversarial (agent verifies its own work with fresh LLM context)
- Embedded approach is simpler, proven, and follows same architectural principles
- Focus should be on V2 orchestrator which provides the real architectural value

**Current Verification Status**: ✅ **ALREADY WORKING**

- Analysis Agent: `_step5_verification()` with independent LLM call
- Statistical Agent: `_step2_verification()` with independent LLM call
- Both use separate prompts and tool calling for structured verification results

**Detailed Tasks**:

#### [V2-4.1] Implement `VerificationAgent` Base Class

- **Base Class**: Create abstract base class extending `StandardAgent`
- **Verify Method**: `verify(primary_results: Dict[str, Any], computational_work: Dict[str, Any]) -> VerificationResult`
- **VerificationResult**: Dataclass with `verified: bool`, `discrepancies: List[str]`, `attestation_data: Dict`
- **Files to Create**: `discernus/core/verification_agent.py`, `discernus/core/verification_result.py`

#### [V2-4.2] Build Specific Verification Agents

- **AnalysisVerificationAgent**: Re-executes computational work from `AnalysisAgent`
  - Reads `analysis_scores.json` and `computational_work.json`
  - Re-runs analysis code and compares results
  - Files: `discernus/agents/analysis_verification_agent/`
- **StatisticalVerificationAgent**: Validates statistical calculations
  - Reads `statistics.json` and `statistical_work.json`
  - Re-executes statistical code and validates results
  - Files: `discernus/agents/statistical_verification_agent/`
- **EvidenceVerificationAgent**: Checks evidence relevance and accuracy
  - Reads `evidence_quotes.json` and validates against source
  - Verifies evidence retrieval accuracy
  - Files: `discernus/agents/evidence_verification_agent/`
- **SynthesisVerificationAgent**: Fact-checks synthesis claims
  - Reads synthesis report and validates claims against evidence
  - Cross-references statistical assertions
  - Files: `discernus/agents/synthesis_verification_agent/`

#### [V2-4.3] Create `CacheIntegrityVerifier`

- **Purpose**: Verifies cache keys and artifact hashes across phases
- **Detection**: Identifies stale/mismatched caches
- **Validation**: Ensures cache coherence throughout pipeline
- **Files to Create**: `discernus/agents/cache_integrity_verifier/`

#### [V2-4.4] Create `SynthesisFactCheckLite`

- **Purpose**: Advisory, read-only cross-check of sampled claims against evidence artifacts
- **No Orchestrator RAG**: Uses only evidence artifacts, no orchestrator RAG dependency
- **Sampling**: Checks subset of synthesis claims for efficiency
- **Files to Create**: `discernus/agents/synthesis_fact_check_lite/`

**Definition of Done**:

- ✅ `VerificationAgent` base class implemented with standard `verify` method
- ✅ `VerificationResult` dataclass created with verification status and discrepancy tracking
- ✅ `AnalysisVerificationAgent` re-executes and validates analysis computational work
- ✅ `StatisticalVerificationAgent` validates statistical calculations independently
- ✅ `EvidenceVerificationAgent` checks evidence relevance and accuracy
- ✅ `SynthesisVerificationAgent` fact-checks synthesis claims against evidence
- ✅ `CacheIntegrityVerifier` detects stale/mismatched caches across phases
- ✅ `SynthesisFactCheckLite` provides advisory fact-checking without orchestrator RAG
- ✅ All verification agents follow `StandardAgent` interface
- ✅ Verification agents produce `attestation_<hash>.json` artifacts
- ✅ Unit tests for all verification agents
- ✅ Integration tests showing verification catches actual discrepancies
- ✅ Performance testing ensures verification doesn't significantly slow pipeline


### Sprint V2-6: Legacy Agent Migration to V2 ⚠️ IN PROGRESS, THIN VIOLATION CORRECTED

**Corresponds to**: V2 Plan - Phase 4 (Agent Completion)
**Goal**: Migrate AnalysisAgent and StatisticalAgent to V2 StandardAgent interface.
**Priority**: HIGH - Complete V2 agent ecosystem for production readiness

**Detailed Tasks**:

#### [V2-6.1] Create V2AnalysisAgent ✅

- **Base Class**: Inherit from `StandardAgent` and `ToolCallingAgent`
- **Constructor**: `__init__(security: ExperimentSecurityBoundary, storage: LocalArtifactStorage, audit: AuditLogger, config: Optional[AgentConfig] = None)`
- **Execute Method**: `execute(run_context: RunContext = None, **kwargs) -> AgentResult`
- **Capabilities Method**: `get_capabilities() -> List[str]`
- **Wrapper Logic**: Wrap existing `analyze_documents()` logic in `execute()` method
- **Return Conversion**: Convert dict returns to `AgentResult` objects
- **Files Created**: `discernus/agents/analysis_agent/v2_analysis_agent.py`
- **THIN Compliance**: **Corrected.** Initial implementation violated THIN principles by performing file I/O. This was fixed, but the data handoff from orchestrator remains brittle (passes manifest as single document).

#### [V2-6.2] Create V2StatisticalAgent ✅

- **Base Class**: Inherit from `StandardAgent` and `ToolCallingAgent`
- **Constructor**: `__init__(security: ExperimentSecurityBoundary, storage: LocalArtifactStorage, audit: AuditLogger, config: Optional[AgentConfig] = None)`
- **Execute Method**: `execute(run_context: RunContext = None, **kwargs) -> AgentResult`
- **Capabilities Method**: `get_capabilities() -> List[str]`
- **Wrapper Logic**: Wrap existing `analyze_batch()` logic in `execute()` method
- **Return Conversion**: Convert dict returns to `AgentResult` objects
- **Files Created**: `discernus/agents/statistical_agent/v2_statistical_agent.py`
- **Artifact Integration**: Properly stores analysis artifacts for statistical processing

#### [V2-6.3] Test V2 Orchestrator with Real Agents ⚠️ INCOMPLETE

- **Integration Test**: Run `nano_test_experiment` with real V2 agents
- **LLM Integration**: Test actual LLM calls and error handling
- **Data Flow**: Test real file I/O, artifact storage, and RAG operations
- **Performance**: Measure execution time and resource usage
- **Files Created**: `test_v2_orchestrator_real_agents.py`
- **Results**: 🔴 **FAILURE** - Test relies on mock agents for Evidence and Synthesis, proving the pipeline is not end-to-end functional.

#### [V2-6.4] CLI Integration ⚠️ PENDING

- **CLI Flag**: Add `--orchestrator-version=v2` for backward-compatible rollout
- **Default V1**: Keep V1 as default until V2 validation complete
- **Configuration**: Ensure all existing CLI options work with V2 orchestrator
- **Files to Update**: `discernus/cli.py`
- **Status**: Not yet implemented - V2 orchestrator works via direct instantiation

**Definition of Done**:

- ✅ `V2AnalysisAgent` implements `StandardAgent` interface with real LLM integration
- ✅ `V2StatisticalAgent` implements `StandardAgent` interface with real LLM integration
- ✅ Both agents wrap existing `analyze_documents()` logic in `execute()` method
- ✅ Both agents return `AgentResult` objects instead of dicts
- ✅ Both agents have proper `get_capabilities()` methods
- ❌ V2 orchestrator successfully runs `nano_test_experiment` with **all real** V2 agents.
- ⚠️ CLI integration with `--orchestrator-version=v2` flag working (PENDING)
- ✅ Unit tests for both V2 agents (15+ tests each)
- ❌ Integration tests showing end-to-end pipeline with real agents **(no mocks)**.
- ✅ Performance testing shows V2 agents meet or exceed V1 performance
- ✅ Error handling tested with real LLM failures and edge cases

**Completion Date**: TBD
**Status**: ⚠️ **IN PROGRESS** - Wrappers are created, but integration is incomplete and brittle.

### Sprint V2-7: V2 Validation & Migration 🎯 CURRENT FOCUS

**Corresponds to**: V2 Plan - Phase 5 (Validation & Rollout)
**Goal**: Validate V2 system against V1 and manage migration.
**Priority**: CRITICAL - Ensure V2 system is production-ready.

**Detailed Tasks**:

#### [V2-7.1] Fix Orchestrator Data Flow

- **Problem**: Orchestrator passes the entire corpus manifest file as a single document, which is incorrect.
- **Solution**: Modify `ExecutionStrategy` to read the corpus manifest, load each referenced document's content, and pass a list of document contents to the `V2AnalysisAgent`.
- **Files to Update**: `discernus/core/execution_strategies.py`

#### [V2-7.2] Complete Agent Implementations

- **V2EvidenceRetrieverAgent**: Complete the full implementation based on the V2 standard.
- **V2UnifiedSynthesisAgent**: Complete the full implementation based on the V2 standard.
- **Files to Update**: `discernus/agents/evidence_retriever_agent/v2_evidence_retriever_agent.py`, `discernus/agents/unified_synthesis_agent/v2_unified_synthesis_agent.py`

#### [V2-7.3] Solidify Integration Testing

- **Remove Mocks**: Update `test_v2_orchestrator_real_agents.py` to use the real `V2EvidenceRetrieverAgent` and `V2UnifiedSynthesisAgent`.
- **Add Micro Test**: Create `test_v2_orchestrator_micro_experiment.py` to validate the pipeline against a different framework and corpus.
- **Add Cache Clearing**: Ensure tests clear caches before execution to guarantee a clean run.
- **Files to Update**: `test_v2_orchestrator_real_agents.py`

#### [V2-7.4] Make V2 Default

- **CLI Default**: Switch default orchestrator to V2
- **Deprecation Warnings**: Add warnings for V1 usage
- **Rollback Capability**: Maintain `--orchestrator-version=v1` for emergency rollback
- **Files to Update**: `discernus/cli.py`

#### [V2-7.5] Documentation & Migration Guide

- **API Documentation**: Complete documentation for new agent ecosystem
- **Migration Guide**: Guide for extending the system with new agents
- **Architecture Documentation**: Update project architecture docs
- **Agent Development Guide**: Patterns and best practices for V2 agents
- **Files to Create**: `docs/v2_architecture.md`, `docs/agent_development_guide.md`

#### [V2-7.6] Legacy Code Cleanup

- **Remove V1 Orchestrator**: Delete `CleanAnalysisOrchestrator` and associated code
- **Clean Up Imports**: Remove references to deprecated classes
- **Update Tests**: Migrate tests to use V2 patterns
- **Files to Remove**: `discernus/core/clean_analysis_orchestrator.py` and related files

#### [V2-7.7] Production Monitoring

- **Logging**: Ensure comprehensive logging for V2 orchestrator
- **Metrics**: Performance and reliability metrics collection
- **Alerting**: Set up monitoring and alerting for production use
- **Cost Tracking**: Enhanced cost tracking for V2 agent ecosystem

**Definition of Done**:

- ✅ **Primary Goal**: Successfully run both `nano_test_experiment` and `micro_test_experiment` back-to-back using the full, real V2 agent pipeline with caches cleared between runs.
- ✅ Orchestrator correctly loads individual documents from the corpus manifest and passes them to the analysis agent.
- ✅ `test_v2_orchestrator_real_agents.py` passes using **zero** mock agents.
- ✅ `test_v2_orchestrator_micro_experiment.py` passes using **zero** mock agents.
- ✅ Parity testing complete - V2 matches V1 output across experiment matrix
- ✅ Performance testing shows V2 meets or exceeds V1 benchmarks
- ✅ V2 orchestrator is CLI default with deprecation warnings for V1
- ✅ Complete API documentation for V2 agent ecosystem
- ✅ Migration guide and agent development documentation created
- ✅ V1 `CleanAnalysisOrchestrator` and legacy code removed
- ✅ All tests migrated to V2 patterns
- ✅ Production monitoring and alerting configured
- ✅ Cost tracking enhanced for V2 ecosystem
- ✅ Emergency rollback to V1 capability maintained
- ✅ Architecture documentation updated to reflect V2 design

### Sprint V2-8: Convert Legacy Agents to V2 Native ⏳ PENDING

**Corresponds to**: V2 Plan - Technical Debt Reduction
**Goal**: Convert legacy agent wrappers to true V2 native implementations for better performance and maintainability.
**Priority**: MEDIUM - Technical debt reduction and performance optimization.

**Detailed Tasks**:

#### [V2-8.1] Convert StatisticalAgent to V2 Native

- **Current State**: V2StatisticalAgent is a thin wrapper around legacy StatisticalAgent
- **Target**: Direct V2 StandardAgent implementation with no legacy dependency
- **Interface**: Replace `analyze_batch()` with native `execute(run_context: RunContext) -> AgentResult`
- **Data Access**: Use RunContext and artifact storage directly instead of parameter passing
- **Benefits**: Eliminate wrapper overhead, cleaner architecture, better maintainability
- **Files to Create**: `discernus/agents/statistical_agent/native_v2_statistical_agent.py`
- **Files to Update**: Orchestrator registration to use native agent

#### [V2-8.2] Convert AnalysisAgent to V2 Native

- **Current State**: V2AnalysisAgent is a thin wrapper around legacy AnalysisAgent
- **Target**: Direct V2 StandardAgent implementation with no legacy dependency
- **Interface**: Replace `analyze_documents()` with native `execute(run_context: RunContext) -> AgentResult`
- **Data Access**: Use RunContext and artifact storage directly instead of parameter passing
- **Benefits**: Eliminate wrapper overhead, cleaner architecture, better maintainability
- **Files to Create**: `discernus/agents/analysis_agent/native_v2_analysis_agent.py`
- **Files to Update**: Orchestrator registration to use native agent

#### [V2-8.3] Performance and Architecture Validation

- **Benchmark Testing**: Compare wrapper vs native performance across experiment matrix
- **Memory Profiling**: Measure memory footprint reduction from eliminating double instantiation
- **Code Quality**: Validate cleaner error handling and logging patterns
- **Maintainability**: Confirm single implementation is easier to debug and extend

#### [V2-8.4] Migration and Cleanup

- **Gradual Rollout**: Deploy native agents with fallback to wrapper versions
- **Legacy Removal**: Remove legacy agent implementations once native versions are proven
- **Test Migration**: Update all tests to use native agents
- **Documentation**: Update agent development guide with native patterns

**Definition of Done**:

- ⏳ StatisticalAgent has native V2 implementation with no legacy dependency
- ⏳ AnalysisAgent has native V2 implementation with no legacy dependency
- ⏳ Both native agents implement StandardAgent interface directly
- ⏳ Performance testing shows measurable improvements (speed, memory)
- ⏳ All existing functionality preserved with no regressions
- ⏳ Legacy agent code removed after successful migration
- ⏳ Unit and integration tests updated for native implementations
- ⏳ Documentation updated with native agent development patterns

### Sprint V2-10: Restore Advanced CLI Functionality ⏳ PENDING

**Corresponds to**: V2 Plan - Phase 5 (CLI Parity)
**Goal**: Restore remaining V1 CLI options to the V2 `run` command.
**Priority**: MEDIUM - After resume functionality is fixed.

**Detailed Tasks**:

#### [V2-10.1] Implement Model Selection Flags

- **Task**: Plumb model selection flags (`--analysis-model`, `--synthesis-model`, etc.) from the CLI down to the individual V2 agents.
- **Details**: Requires modifying agent constructors and the orchestrator to pass model names to the `LLMGateway`.

#### [V2-10.2] Implement `--dry-run` and `--verbose-trace`

- **Task**: Add logic to V2 execution strategies to simulate a run without executing expensive operations. Plumb the verbose trace flag to the `AuditLogger`.
- **Details**: `--dry-run` should print the agents that would be called and the artifacts that would be created.

#### [V2-10.3] Implement Experiment Validation (`--skip-validation`)

- **Task**: Create a `V2ExperimentCoherenceAgent` and integrate it as the first step in the execution strategy. The `--skip-validation` flag will bypass it.
- **Details**: Reintroduces the robust validation step from the V1 CLI.

#### [V2-10.4] Implement Automatic Git Commits (`--no-auto-commit`)

- **Task**: Add logic to the `V2Orchestrator` to automatically commit results to Git upon successful completion of a run.
- **Details**: Restores critical provenance tracking. The `--no-auto-commit` flag will disable this behavior.

**Definition of Done**:

- ⏳ The `discernus run` command supports all model selection flags.
- ⏳ The `discernus run` command supports `--dry-run` and `--verbose-trace`.
- ⏳ The `discernus run` command runs a validation step by default, which can be disabled with `--skip-validation`.
- ⏳ Successful runs are automatically committed to Git, which can be disabled with `--no-auto-commit`.
- ⏳ All restored options are covered by integration tests.

---

## Archived Sprints (Pre-V2 Plan)

The following sprints were part of the previous incremental refactoring approach ("Show Your Work Migration") and have been superseded by the V2 Integrated Ecosystem Rewrite. The goals of these sprints are addressed more holistically by the new plan, which favors a foundational rewrite over piecemeal changes to the V1 orchestrator. This section is preserved for historical context.

### Archived Sprint: Critical Bug Fix Sprints

- **Goal**: Fix data structure errors in the V1 orchestrator.
- **Status**: Superseded. The V2 orchestrator will not have these issues.

### Archived Sprint: Statistical Agent Development Sprints

- **Goal**: Build a THIN statistical agent.
- **Status**: Superseded. This will be implemented as part of the V2 agent ecosystem with standardized interfaces.

### Archived Sprint: Evidence Management THIN Refactoring Sprint

- **Goal**: Move evidence preparation from the V1 orchestrator to the `EvidenceRetrieverAgent`.
- **Status**: Superseded. This is a core part of Sprint V2-2.

### Archived Sprint: Enhanced Analysis Agent Integration Sprints

- **Goal**: Integrate a new analysis agent into the V1 orchestrator.
- **Status**: Superseded. The V2 plan includes migrating all agents, including the analysis agent, to the new standard.

### Archived Sprint: Show Your Work Migration Sprints

- **Goal**: Incrementally refactor the V1 orchestrator to meet "Show Your Work" contracts.
- **Status**: Superseded by the full V2 rewrite.

---

## Migration Progress Tracking

### Phase 1: Agent Standardization ⚠️ **IN PROGRESS**

- Sprint V2-1: Define interfaces and base classes
- Sprint V2-2: Migrate EvidenceRetrieverAgent and consolidate RAG

### Phase 2: Complete Agent Ecosystem 📋 **PLANNED**

- Sprint V2-3: Migrate UnifiedSynthesisAgent
- Sprint V2-4: Build verification agent ecosystem

### Phase 3: V2 Orchestrator Implementation 📋 **PLANNED**

- Sprint V2-5: Build agent-native orchestrator

### Phase 4: Migration and Cleanup 📋 **FUTURE**

- Sprint V2-6: Rollout and legacy cleanup

---

## Success Criteria

- Zero orchestrator RAG code remains; all RAG owned by EvidenceRetriever via `RAGIndexManager`
- No hidden state between phases; all handoffs via `RunContext`
- Resume-from-stats uses manifest-only; no directory globbing
- Output parity (byte-identical where applicable) across a matrix of experiments
- All LLM calls routed through gateway; files remain canonical; no DB footprint prior to DB stage
