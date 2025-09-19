# Discernus V2 Sprints - Integrated Ecosystem Rewrite

**Purpose**: Organized backlog for the V2 Integrated Ecosystem Rewrite, replacing the previous "Show Your Work" migration plan.

**Usage**:

- This plan supersedes the previous incremental refactoring sprints.
- Each sprint epic corresponds directly to a phase in the `v2_integrated_ecosystem_rewrite_plan.md`.

---

## Current Status

**Latest Updates**:

- ✅ **ARCHITECTURE PIVOT**: We have formally adopted the V2 Integrated Ecosystem Rewrite plan.
- ✅ **ANALYSIS COMPLETE**: The V1 orchestrator (`CleanAnalysisOrchestrator`) has been analyzed and confirmed to be a monolithic source of technical debt. The aborted `ShowYourWorkOrchestrator` has been deleted.
- 📋 **PLANNING COMPLETE**: This document now reflects the full V2 rewrite plan.

**Current Focus**: **Phase 1: Agent Standardization & Foundational Tooling**. The immediate priority is to establish the core interfaces and data contracts that all V2 agents will use.

---

## V2 Rewrite Sprint Plan

### Sprint V2-1: Agent Standardization & Foundational Tooling ✅ TRULY COMPLETE
**Corresponds to**: V2 Plan - Phase 1 (Weeks 1-2)
**Goal**: Create the canonical agent interface, base classes, and data handoff contracts. This is the foundation for the entire V2 ecosystem.

**Detailed Tasks**:

#### [V2-1.1] Define `StandardAgent` Interface ✅
- **Implementation**: Created `discernus/core/standard_agent.py` with the exact interface from V2 plan
- **Constructor**: `__init__(security: ExperimentSecurityBoundary, storage: LocalArtifactStorage, audit: AuditLogger, config: Optional[AgentConfig] = None)`
- **Methods**: `execute(**kwargs) -> AgentResult` and `get_capabilities() -> List[str]`
- **Files Created**: `discernus/core/standard_agent.py`, `discernus/core/agent_result.py`

#### [V2-1.2] Build Agent Base Classes ✅
- **ToolCallingAgent**: For agents needing structured output via tool calls
- **ValidationAgent**: For verification and coherence checking with `validate()` method
- **SynthesisAgent**: For report generation with `synthesize()` method  
- **VerificationAgent**: For adversarial attestation with `verify()` method
- **Files Created**: `discernus/core/agent_base_classes.py`

#### [V2-1.3] Implement `RunContext` ✅
- **Purpose**: Typed data class for all inter-agent handoffs to eliminate hidden state
- **Fields**: `analysis_results`, `derived_metrics`, `evidence`, `statistical_results`, `metadata` (artifact hashes, versions, cache keys)
- **Implementation**: Dataclass with type hints and validation
- **Files Created**: `discernus/core/run_context.py`

#### [V2-1.4] Create Agent Configuration System ✅
- **AgentConfig**: Dataclass with `model`, `parameters`, `retry_config`, `verification_config`
- **RetryConfig**: Dataclass for retry policies
- **VerificationConfig**: Optional verification settings
- **Files Created**: `discernus/core/agent_config.py`

#### [V2-1.5] Centralize Gateway/Model Policy ✅
- **Policy**: All LLM calls routed through project gateway
- **Defaults**: Vertex AI unless overridden by config
- **Safety**: Centralize safety/retry settings in gateway
- **Enforcement**: Agents cannot instantiate model clients directly
- **Files Updated**: Gateway classes to enforce this policy

**Definition of Done**:
- ✅ `StandardAgent` interface implemented with exact signature from V2 plan
- ✅ All 4 base classes (`ToolCallingAgent`, `ValidationAgent`, `SynthesisAgent`, `VerificationAgent`) implemented
- ✅ `RunContext` dataclass created with all required fields and type hints
- ✅ `AgentConfig` system implemented with retry and verification configs
- ✅ Gateway policy enforced - decorators prevent direct model client instantiation
- ✅ Unit tests for all new interfaces and classes (14 tests passing)
- ✅ Documentation for agent development patterns

**Completion Date**: 2024-12-19
**Commits**: 
- de83a0da7 - "Complete V2-1: Agent foundation & interfaces"
- 9a28a44f2 - "Migrate legacy EvidenceRetrieverAgent to V2 and add gateway policy enforcement"
**Status**: Truly complete - all requirements met

### Sprint V2-2: EvidenceRetrieverAgent Migration & RAG Consolidation ⚠️ FOUNDATION COMPLETE
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
- ✅ `EvidenceRetrieverAgent` implements `StandardAgent` interface
- ✅ Constructor uses proper dependency injection (no `Dict[str, Any]` config)
- ✅ Agent has clear method separation for evidence workflow
- ✅ Tool calling integrated with `record_evidence_finding` and `verify_evidence_relevance`
- ✅ `RAGIndexManager` created and handles all RAG lifecycle operations
- ✅ Agent reads framework and statistical results directly from artifacts
- ✅ Agent discovers evidence artifacts from analysis hashes without orchestrator help
- ❌ All orchestrator RAG methods deleted (80+ lines removed) - **PENDING INTEGRATION**
- ❌ Orchestrator evidence phase reduced to ~10 lines (simple agent call) - **PENDING INTEGRATION**
- ✅ No regression in evidence quality (validated with existing experiments)
- ✅ Unit tests for `RAGIndexManager` and refactored agent
- ✅ Integration tests showing end-to-end evidence retrieval works

**Foundation Completion Date**: 2024-12-19
**Commit**: a8631afff - "Complete V2-2: RAG consolidation and removal plan"
**Status**: Foundation complete - V2 agent ready, orchestrator integration pending

### Sprint V2-3: UnifiedSynthesisAgent Migration ⚠️ FOUNDATION COMPLETE
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
- ✅ `UnifiedSynthesisAgent` implements `StandardAgent` interface
- ✅ Agent constructor uses proper dependency injection
- ✅ Agent reads all inputs from `RunContext` object (no filesystem scanning)
- ✅ Agent consumes V2 artifact formats (`analysis_scores.json`, `evidence_quotes.json`, `computational_work.json`)
- ✅ CSV parsing logic removed and replaced with structured data consumption
- ✅ Computational work and verification results integrated into synthesis
- ✅ Statistical results presented with consistent significant digits and disclosure
- ✅ Tool calling implemented for structured report metadata output
- ✅ No regression in synthesis quality (validated with existing experiments)
- ✅ Unit tests for refactored agent (15 tests passing)
- ✅ Integration tests showing end-to-end synthesis works with V2 artifacts
- ❌ Orchestrator updated to use V2UnifiedSynthesisAgent - **PENDING INTEGRATION**

**Foundation Completion Date**: 2024-12-19
**Commit**: fbf4750ae - "Complete V2-3: UnifiedSynthesisAgent migration to V2 standard"
**Status**: Foundation complete - V2 agent ready, orchestrator integration pending

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

### Sprint V2-5: V2 Orchestrator Implementation 🎯 CURRENT FOCUS
**Corresponds to**: V2 Plan - Phase 3
**Goal**: Build the new, simple, agent-native orchestrator.
**Priority**: HIGH - Core V2 system implementation

**Detailed Tasks**:

#### [V2-5.1] Build `V2Orchestrator` Core
- **Core Architecture**: 
  ```python
  class V2Orchestrator:
      def __init__(self, agents: Dict[str, StandardAgent]):
          self.agents = agents
      def execute_strategy(self, strategy: ExecutionStrategy) -> ExperimentResult:
          return strategy.execute(self.agents)
  ```
- **Agent Registry**: Dynamic agent discovery and capability declaration
- **Configuration Management**: Clean separation of experiment vs. runtime config
- **Files to Create**: `discernus/core/v2_orchestrator.py`

#### [V2-5.2] Implement Strategy Pattern
- **FullExperimentStrategy**: Complete pipeline execution with verification
- **AnalysisOnlyStrategy**: Analysis phase only
- **StatisticalPrepStrategy**: Analysis + statistical phases
- **ResumeFromStatsStrategy**: Resume from statistical results
- **Strategy Interface**: 
  ```python
  class ExecutionStrategy:
      def execute(self, agents: Dict[str, StandardAgent]) -> ExperimentResult:
          # Simple linear execution with verification
  ```
- **Files to Create**: `discernus/core/execution_strategies.py`

#### [V2-5.3] Implement Resume Capability
- **Resume Manifest**: Write `resume_manifest.json` after each phase with artifact hashes and minimal metadata
- **Resume Logic**: `ResumeFromStats` reads manifest instead of directory scans
- **Cache Integration**: Leverage agent-level caching automatically
- **Files as Canonical**: Persist all artifacts to disk as source of truth; no DB in this stage

#### [V2-5.4] Create `ExperimentRunConfig`
- **Replace Boolean Flags**: Single typed config object instead of multiple boolean flags
- **Configuration**: Model selection, verification settings, resume options
- **Files to Create**: `discernus/core/experiment_run_config.py`

#### [V2-5.5] Integrate with CLI
- **CLI Flag**: Add `--orchestrator-version=v2` for backward-compatible rollout
- **Default V1**: Keep V1 as default until parity validation complete
- **Configuration**: Ensure all existing CLI options work with V2 orchestrator
- **Files to Update**: `discernus/cli.py`

**Definition of Done**:
- ✅ `V2Orchestrator` implemented with agent registry and strategy execution
- ✅ All execution strategies implemented (`FullExperimentStrategy`, `AnalysisOnlyStrategy`, etc.)
- ✅ Strategy pattern allows different execution modes as separate classes
- ✅ Resume capability uses `resume_manifest.json` (no directory scanning)
- ✅ `ExperimentRunConfig` replaces boolean flags with typed configuration
- ✅ CLI integration with `--orchestrator-version=v2` flag
- ✅ Agent-level caching works automatically with V2 orchestrator
- ✅ Verification integration optional at each step
- ✅ Files remain canonical source of truth (no DB footprint)
- ✅ Unit tests for orchestrator and all strategies
- ✅ Integration tests showing V2 orchestrator works end-to-end
- ✅ Performance comparison with V1 orchestrator

### Sprint V2-6: V2 Validation & Migration 🎯 FINAL FOCUS
**Corresponds to**: V2 Plan - Phase 4 (Validation & Rollout)
**Goal**: Validate V2 system against V1 and manage migration.
**Priority**: HIGH - Ensure V2 system is production-ready

**Detailed Tasks**:

#### [V2-6.1] Validation Testing
- **Parity Testing**: Run same experiments through both V1 and V2 orchestrators
- **Output Comparison**: Byte-identical results where applicable across experiment matrix
- **Performance Testing**: Measure speed, cost, reliability improvements
- **Error Handling**: Comprehensive failure scenarios and recovery testing
- **Acceptance Criteria**: V2 must match or exceed V1 performance and reliability

#### [V2-6.2] Make V2 Default
- **CLI Default**: Switch default orchestrator to V2
- **Deprecation Warnings**: Add warnings for V1 usage
- **Rollback Capability**: Maintain `--orchestrator-version=v1` for emergency rollback
- **Files to Update**: `discernus/cli.py`

#### [V2-6.3] Documentation & Migration Guide
- **API Documentation**: Complete documentation for new agent ecosystem
- **Migration Guide**: Guide for extending the system with new agents
- **Architecture Documentation**: Update project architecture docs
- **Agent Development Guide**: Patterns and best practices for V2 agents
- **Files to Create**: `docs/v2_architecture.md`, `docs/agent_development_guide.md`

#### [V2-6.4] Legacy Code Cleanup
- **Remove V1 Orchestrator**: Delete `CleanAnalysisOrchestrator` and associated code
- **Clean Up Imports**: Remove references to deprecated classes
- **Update Tests**: Migrate tests to use V2 patterns
- **Files to Remove**: `discernus/core/clean_analysis_orchestrator.py` and related files

#### [V2-6.5] Production Monitoring
- **Logging**: Ensure comprehensive logging for V2 orchestrator
- **Metrics**: Performance and reliability metrics collection
- **Alerting**: Set up monitoring and alerting for production use
- **Cost Tracking**: Enhanced cost tracking for V2 agent ecosystem

**Definition of Done**:
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
