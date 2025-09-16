# Discernus v10 Sprints - Show Your Work Migration

**Purpose**: Organized backlog focused on migrating from existing pipeline to Show Your Work architecture.

**Usage**:

- "groom our sprints" → organize inbox items into proper sprint structure
- Items moved here from inbox.md during grooming sessions

---

## Current Status

**Latest Updates**:

- 🎯 **NEW ENHANCED ANALYSIS AGENT**: Successfully developed 6-step THIN approach with inline markup
- ✅ **PROTOTYPE VALIDATED**: Testing shows excellent alignment between markup density and scoring
- 🔄 **ARCHITECTURE PIVOT**: Migrating to Show Your Work architecture with tool calling and adversarial attestation
- ✅ **Phase 0.5 COMPLETED**: Analysis agent converted to tool calling (partial migration)
- ✅ **STATISTICAL ANALYSIS FIXED**: Removed THICK antipatterns, statistical analysis now works correctly
- ✅ **CACHE SYSTEM IMPROVED**: Fixed input-based caching for better cache hit rates
- ✅ **TEMP WORKSPACE CLEANUP**: Eliminated THICK temp directory creation antipattern
- 📋 **MIGRATION PLAN CREATED**: Comprehensive 4-phase migration plan documented

**Current Focus**: **Critical Data Structure Error** - The experiment execution is failing with `'list' object has no attribute 'get'` error during initialization. This is blocking all experiments and needs immediate resolution.

**Next Priority**: **Evidence Retrieval Phase** - After fixing the data structure error, the next blocking issue is the "RAG index not available" error in the evidence retrieval phase.

**Migration Strategy**: Continue systematic refactoring of CleanAnalysisOrchestrator to use Show Your Work patterns while preserving mature functionality. Focus on evidence retrieval phase next.

---

## Current Sprint Planning

**Next Priority**: Critical Data Structure Error Fix - **URGENT PRIORITY**
**Status**: Blocking all experiments - Fix `'list' object has no attribute 'get'` error during initialization
**Dependencies**: None - can begin immediately

**Following Priority**: Evidence Retrieval Phase Fix - **URGENT PRIORITY**
**Status**: Ready for execution - Fix "RAG index not available" error blocking experiments
**Dependencies**: Data structure error fix completion

**Future Priority**: Sprint EAA-1 (Enhanced Analysis Agent Integration) - **HIGH PRIORITY**
**Status**: Ready for execution - Replace existing analysis agent with superior THIN approach
**Dependencies**: Evidence retrieval fix completion

**Future Priority**: Sprint SYW-2 (Add Verification Layer) - **MEDIUM PRIORITY**
**Status**: Planned - depends on evidence retrieval fix and EAA-1
**Dependencies**: Evidence retrieval must work, enhanced analysis agent must be integrated

---

## Critical Bug Fix Sprints

### Sprint BUG-1: Fix Data Structure Error ⚠️ **URGENT PRIORITY**

**Description**: Fix `'list' object has no attribute 'get'` error that blocks all experiment execution
**Purpose**: Restore basic experiment functionality to enable further development
**Priority**: URGENT - Blocking all experiments
**Timeline**: 1-2 days - critical path blocker
**Success Criteria**: Experiments can run successfully in statistical preparation mode
**Dependencies**: None - can start immediately

#### [BUG1-001] Debug Data Structure Mismatch

- **Description**: Identify exact location where list is being treated as dictionary with `.get()` calls
- **Purpose**: Pinpoint root cause of the data structure error
- **Priority**: CRITICAL - Must identify root cause before fixing
- **Current Status**: Error occurs during `_initialize_infrastructure` phase, before detailed logging
- **Investigation Areas**:
  - `_verify_caching_performance` method in orchestrator
  - Artifact storage registry structure
  - Data structure assumptions in initialization code
  - YAML parsing results being treated as dictionaries
- **Solution Strategy**:
  - Add comprehensive debug logging to trace exact error location
  - Check data structure types at each step of initialization
  - Validate artifact storage registry structure
  - Test with minimal reproducible case
- **Acceptance Criteria**:
  - ✅ Exact error location identified and documented
  - ✅ Root cause of data structure mismatch understood
  - ✅ Debug logging shows data structure types at each step
  - ✅ Minimal reproducible case created
- **Files to Investigate**:
  - `discernus/core/clean_analysis_orchestrator.py` (_initialize_infrastructure, _verify_caching_performance)
  - `discernus/core/local_artifact_storage.py` (registry structure)
  - YAML parsing and data structure handling
- **Dependencies**: None
- **Effort**: 1 day

#### [BUG1-002] Fix Data Structure Handling

- **Description**: Correct the data structure handling to prevent list/dictionary mismatch
- **Purpose**: Restore experiment execution functionality
- **Priority**: CRITICAL - Must fix to enable experiments
- **Solution Strategy**:
  - Fix data structure assumptions in identified locations
  - Ensure proper type checking before `.get()` calls
  - Validate artifact storage registry structure
  - Add defensive programming for data structure handling
- **Acceptance Criteria**:
  - ✅ No more `'list' object has no attribute 'get'` errors
  - ✅ Experiments can run successfully in statistical preparation mode
  - ✅ All data structure handling is type-safe
  - ✅ No regression in existing functionality
- **Files to Update**:
  - `discernus/core/clean_analysis_orchestrator.py` (identified error locations)
  - `discernus/core/local_artifact_storage.py` (if registry structure issues)
- **Dependencies**: [BUG1-001] - Root cause must be identified first
- **Effort**: 1 day

#### [BUG1-003] Add Provenance Integration for Marked-Up Documents

- **Description**: Copy marked-up documents to experiment run folder and create README for interpretation
- **Purpose**: Complete provenance integration by including marked-up documents in experiment runs
- **Priority**: HIGH - Required for provenance completeness
- **Current Issue**: Marked-up documents are generated but not copied to experiment run folder
- **Solution Strategy**:
  - Copy marked-up documents from shared cache to experiment run folder
  - Create README explaining how to interpret marked-up documents
  - Update provenance specification to include marked-up document handling
  - Ensure marked-up documents are discoverable in experiment runs
- **Acceptance Criteria**:
  - ✅ Marked-up documents copied to experiment run folder
  - ✅ README created explaining document interpretation
  - ✅ Provenance specification updated
  - ✅ Marked-up documents discoverable in experiment runs
- **Files to Update**:
  - `discernus/core/clean_analysis_orchestrator.py` (provenance integration)
  - `pm/active_projects/STATISTICAL_PREPARATION_PROVENANCE_INTEGRATION.md` (specification update)
- **Dependencies**: [BUG1-002] - Experiments must run first
- **Effort**: 1 day

**Sprint BUG-1 Success Criteria**:
- ✅ No more data structure errors during experiment execution
- ✅ Experiments run successfully in statistical preparation mode
- ✅ Marked-up documents included in experiment run provenance
- ✅ Provenance integration specification updated
- ✅ All existing functionality preserved

---

## Statistical Agent Development Sprints

### Sprint SA-1: Build THIN Statistical Agent ⚠️ **HIGH PRIORITY**

**Description**: Build a THIN statistical agent that performs statistical analysis using LLM internal execution with minimal tool calling
**Purpose**: Enable comprehensive statistical analysis of analysis results with full Show Your Work transparency
**Priority**: HIGH - Critical for research validation and statistical rigor
**Timeline**: 2 weeks - after EAA-1 completion
**Success Criteria**: Statistical agent processes analysis artifacts and produces verified statistical results with CSV outputs
**Dependencies**: Sprint EAA-1 (Enhanced Analysis Agent Integration) must complete first

#### [SA1-001] Create Statistical Agent Structure

- **Description**: Build the basic statistical agent with THIN architecture
- **Purpose**: Create the foundation for statistical analysis capabilities
- **Priority**: CRITICAL - Foundation for all statistical work
- **Requirements**:
  - **Name**: `statistical_agent` (not statistical_planning_execution_agent)
  - **Location**: `discernus/agents/statistical_agent/`
  - **THIN approach**: LLM does statistical planning, execution, and verification internally
  - **Minimal tool calling**: Only for deterministic verification (thumbs up/down)
  - **No parsing**: Raw content in, structured output via tool calls
- **Solution Strategy**:
  - Create single agent with two internal steps
  - Step 1: Statistical planning + execution (no tool calls)
  - Step 2: Internal verification (tool call for thumbs up/down)
  - Use existing agent base class and patterns
- **Acceptance Criteria**:
  - ✅ Agent inherits from proper base class
  - ✅ Two-step internal process (planning+execution, verification)
  - ✅ No parsing of input files
  - ✅ Raw content passed to LLM
  - ✅ Tool calling only for verification step
- **Files to Create**:
  - `discernus/agents/statistical_agent/__init__.py`
  - `discernus/agents/statistical_agent/main.py`
  - `discernus/agents/statistical_agent/prompt.yaml`
- **Dependencies**: Sprint EAA-1 completion
- **Effort**: 2-3 days

#### [SA1-002] Implement Statistical Analysis Logic

- **Description**: Implement the core statistical analysis functionality
- **Purpose**: Enable LLM to perform comprehensive statistical analysis
- **Priority**: HIGH - Core functionality
- **Requirements**:
  - **Input handling**: Framework content, analysis artifacts, experiment content, corpus content
  - **Statistical planning**: LLM determines appropriate statistical tests
  - **Data aggregation**: LLM aggregates data from multiple analysis artifacts
  - **Code execution**: LLM generates and executes statistical code internally
  - **CSV generation**: LLM produces CSV files for human researchers
- **Solution Strategy**:
  - Use LLM internal execution for all statistical work
  - Provide raw file content, let LLM figure out structure
  - LLM generates Python code using numpy, pandas, scipy.stats, pingouin
  - LLM executes code internally and saves results
  - No parsing or data extraction in software
- **Acceptance Criteria**:
  - ✅ Handles any framework and experiment combination
  - ✅ Aggregates data from multiple analysis artifacts
  - ✅ Generates appropriate statistical tests
  - ✅ Executes statistical code internally
  - ✅ Produces CSV outputs for researchers
  - ✅ No framework-specific assumptions
- **Files to Update**:
  - `discernus/agents/statistical_agent/main.py` (core logic)
  - `discernus/agents/statistical_agent/prompt.yaml` (statistical prompts)
- **Dependencies**: [SA1-001] - Agent structure must exist
- **Effort**: 3-4 days

#### [SA1-003] Add Verification and Tool Calling

- **Description**: Implement internal verification with minimal tool calling
- **Purpose**: Ensure statistical analysis accuracy and provide deterministic verification
- **Priority**: HIGH - Required for Show Your Work principles
- **Requirements**:
  - **Internal verification**: LLM verifies its own statistical work
  - **Tool calling**: Single tool call for thumbs up/down verification
  - **Deterministic output**: Clear verification status
  - **Error handling**: Graceful handling of verification failures
- **Solution Strategy**:
  - LLM reviews its own statistical work
  - Calls `verify_statistical_analysis` tool with boolean result
  - Tool schema: `{"verified": true/false}`
  - No complex verification logic in software
- **Acceptance Criteria**:
  - ✅ LLM verifies its own work internally
  - ✅ Single tool call for verification result
  - ✅ Deterministic boolean output
  - ✅ Error handling for tool call failures
  - ✅ Clear verification status reporting
- **Files to Update**:
  - `discernus/agents/statistical_agent/main.py` (verification logic)
  - `discernus/agents/statistical_agent/prompt.yaml` (verification prompts)
- **Dependencies**: [SA1-002] - Core logic must exist
- **Effort**: 1-2 days

#### [SA1-004] Integrate with Orchestrator

- **Description**: Ensure statistical agent works with existing orchestrator
- **Purpose**: Enable statistical analysis in production pipeline
- **Priority**: HIGH - Required for end-to-end functionality
- **Requirements**:
  - **Orchestrator compatibility**: Works with existing orchestrator
  - **CLI integration**: Works with all existing CLI flags
  - **Experiment agnosticism**: Handles any framework/experiment combination
  - **Batch processing**: Efficiently processes multiple analysis artifacts
- **Solution Strategy**:
  - Update orchestrator to use new statistical agent
  - Ensure CLI flags work correctly
  - Test with various frameworks and experiments
  - Optimize for batch processing
- **Acceptance Criteria**:
  - ✅ Works with existing orchestrator
  - ✅ All CLI flags work correctly
  - ✅ Processes any framework without modification
  - ✅ Handles multiple analysis artifacts efficiently
  - ✅ No regression in existing functionality
- **Files to Update**:
  - `discernus/core/clean_analysis_orchestrator.py`
  - `discernus/cli.py` (if needed for new flags)
  - `discernus/agents/__init__.py` (agent registration)
- **Dependencies**: [SA1-001], [SA1-002], [SA1-003] - All agent components must be ready
- **Effort**: 2-3 days

#### [SA1-005] Add Logging and Cost Tracking

- **Description**: Integrate with project's logging and cost tracking systems
- **Purpose**: Full observability and cost management for statistical analysis
- **Priority**: MEDIUM - Required for production monitoring
- **Requirements**:
  - **Audit logging**: All statistical agent events logged
  - **Cost tracking**: Token usage and costs tracked
  - **Performance metrics**: Processing time, success rates
  - **Resume capability**: Caching for interrupted operations
- **Solution Strategy**:
  - Use existing `AuditLogger` for all events
  - Track costs per LLM call
  - Implement caching for resume capability
  - Add performance timing
- **Acceptance Criteria**:
  - ✅ All agent actions logged with timestamps
  - ✅ Token usage and costs tracked
  - ✅ Processing times logged
  - ✅ Caching enables resume from any step
  - ✅ Cost reports generated per experiment
- **Files to Update**:
  - `discernus/agents/statistical_agent/main.py` (logging integration)
  - `discernus/core/audit_logger.py` (if needed for new event types)
- **Dependencies**: [SA1-001] - Agent must exist first
- **Effort**: 1-2 days

#### [SA1-006] Comprehensive Testing and Validation

- **Description**: Thorough testing of statistical agent
- **Purpose**: Ensure production readiness and reliability
- **Priority**: HIGH - Required before deployment
- **Testing Requirements**:
  - **Unit tests**: All agent methods tested
  - **Integration tests**: Full orchestrator integration
  - **Performance tests**: Multiple analysis artifacts processing
  - **Framework tests**: Multiple framework compatibility
  - **Verification tests**: Tool calling reliability
- **Solution Strategy**:
  - Create comprehensive test suite
  - Test with various frameworks and experiments
  - Performance testing with multiple analysis artifacts
  - Test verification scenarios and error handling
  - Validate cost tracking and logging
- **Acceptance Criteria**:
  - ✅ All unit tests pass
  - ✅ Integration tests pass
  - ✅ Multiple analysis artifacts processing successful
  - ✅ Multiple frameworks work correctly
  - ✅ Verification scenarios work reliably
  - ✅ Cost tracking accurate
  - ✅ No memory leaks or performance issues
- **Files to Create**:
  - `discernus/tests/test_statistical_agent_integration.py`
  - `discernus/tests/test_statistical_agent_performance.py`
  - `discernus/tests/test_statistical_agent_verification.py`
- **Dependencies**: [SA1-001] through [SA1-005] - All components must be complete
- **Effort**: 2-3 days

---

## Enhanced Analysis Agent Integration Sprints

### Sprint EAA-1: Integrate Enhanced Analysis Agent as Default ⚠️ **URGENT**

**Description**: Replace existing analysis agent with the new 6-step THIN approach featuring inline markup, comprehensive logging, and full orchestrator compatibility
**Purpose**: Deploy superior analysis agent that provides better transparency, reliability, and human-readable output
**Priority**: URGENT - Critical improvement to core analysis functionality
**Timeline**: 2 weeks - comprehensive integration with full testing
**Success Criteria**: Enhanced analysis agent becomes default with full orchestrator compatibility, experiment agnosticism, and production readiness
**Dependencies**: None - can start immediately

#### [EAA1-001] Create Production Analysis Agent

- **Description**: Build production-ready analysis agent based on enhanced prototype
- **Purpose**: Create the new default analysis agent with all production requirements
- **Priority**: CRITICAL - Foundation for all other tasks
- **Requirements**:
  - **Name**: `analysis_agent` (not enhanced_analysis_agent)
  - **Location**: `discernus/agents/analysis_agent/`
  - **Externalized prompt**: YAML file in `discernus/agents/analysis_agent/prompt.yaml`
  - **Complete experiment agnosticism**: No framework-specific assumptions
  - **6-step THIN approach**: Composite analysis → Evidence extraction → Score extraction → Derived metrics → Verification → Markup extraction
- **Solution Strategy**:
  - Adapt `test_thin_approach/enhanced_analysis_agent.py` for production
  - Remove all framework-specific code (PDAF references, etc.)
  - Implement proper agent base class inheritance
  - Add comprehensive error handling and retry logic
  - Ensure 1000+ document processing capability
- **Acceptance Criteria**:
  - ✅ Agent inherits from proper base class
  - ✅ Completely framework agnostic (no hardcoded dimensions)
  - ✅ Externalized YAML prompt template
  - ✅ Handles any framework via prompt parameters
  - ✅ Robust error handling for long document sequences
  - ✅ Memory efficient for 1000+ document processing
- **Files to Create**:
  - `discernus/agents/analysis_agent/__init__.py`
  - `discernus/agents/analysis_agent/main.py`
  - `discernus/agents/analysis_agent/prompt.yaml`
- **Dependencies**: None
- **Effort**: 3-4 days

#### [EAA1-002] Implement Content-Addressable Asset Naming

- **Description**: Ensure all artifacts use human-readable, content-addressable naming per project standards
- **Purpose**: Maintain artifact discoverability and caching compatibility
- **Priority**: HIGH - Required for orchestrator integration
- **Current Issue**: Prototype uses generic names like `enhanced_analysis_results.json`
- **Solution Strategy**:
  - Use `LocalArtifactStorage` for all artifact storage
  - Generate descriptive names with content hashes
  - Follow existing naming conventions: `analysis_result_<hash>.json`, `evidence_<hash>.json`, etc.
  - Ensure markup artifacts are properly named: `marked_up_document_<hash>.md`
- **Acceptance Criteria**:
  - ✅ All artifacts use content-addressable storage
  - ✅ Human-readable names with descriptive prefixes
  - ✅ Consistent with existing artifact naming patterns
  - ✅ Markup documents saved as `.md` files
  - ✅ Artifacts accessible via standard storage interface
- **Files to Update**:
  - `discernus/agents/analysis_agent/main.py` (artifact storage methods)
- **Dependencies**: [EAA1-001] - Agent must exist first
- **Effort**: 1-2 days

#### [EAA1-003] Add Comprehensive Logging and Cost Tracking

- **Description**: Integrate with project's logging and cost tracking systems
- **Purpose**: Full observability and cost management for production use
- **Priority**: HIGH - Required for production monitoring
- **Requirements**:
  - **Audit logging**: All agent events logged via `AuditLogger`
  - **Cost tracking**: Token usage and costs tracked per step
  - **Performance metrics**: Processing time, success rates, error rates
  - **Resume capability**: Caching for interrupted operations
- **Solution Strategy**:
  - Use existing `AuditLogger` for all agent events
  - Track costs per LLM call (Flash vs Flash Lite)
  - Implement caching at each step for resume capability
  - Add performance timing for each analysis step
  - Log all errors with context for debugging
- **Acceptance Criteria**:
  - ✅ All agent actions logged with timestamps
  - ✅ Token usage and costs tracked per model
  - ✅ Processing times logged for each step
  - ✅ Caching enables resume from any step
  - ✅ Error logging includes full context
  - ✅ Cost reports generated per experiment
- **Files to Update**:
  - `discernus/agents/analysis_agent/main.py` (logging integration)
  - `discernus/core/audit_logger.py` (if needed for new event types)
- **Dependencies**: [EAA1-001] - Agent must exist first
- **Effort**: 2-3 days

#### [EAA1-004] Integrate with Orchestrator

- **Description**: Ensure new analysis agent works seamlessly with existing orchestrator
- **Purpose**: Maintain orchestrator compatibility while upgrading analysis capability
- **Priority**: HIGH - Required for end-to-end functionality
- **Requirements**:
  - **Orchestrator compatibility**: Drop-in replacement for existing analysis agent
  - **CLI integration**: Works with all existing CLI flags
  - **Experiment agnosticism**: Handles any framework/experiment combination
  - **Batch processing**: Efficiently processes large document sets
- **Solution Strategy**:
  - Update orchestrator to use new analysis agent
  - Ensure CLI flags work correctly (model selection, etc.)
  - Test with various frameworks and experiments
  - Optimize for batch processing efficiency
  - Maintain backward compatibility with existing experiments
- **Acceptance Criteria**:
  - ✅ Drop-in replacement for existing analysis agent
  - ✅ All CLI flags work correctly
  - ✅ Processes any framework without modification
  - ✅ Handles 1000+ documents without failures
  - ✅ Maintains existing orchestrator interface
  - ✅ No regression in existing functionality
- **Files to Update**:
  - `discernus/core/clean_analysis_orchestrator.py`
  - `discernus/cli.py` (if needed for new flags)
  - `discernus/agents/__init__.py` (agent registration)
- **Dependencies**: [EAA1-001], [EAA1-002], [EAA1-003] - All agent components must be ready
- **Effort**: 2-3 days

#### [EAA1-005] Add Caching and Resume Capability

- **Description**: Implement comprehensive caching system for resume operations
- **Purpose**: Enable interrupted experiments to resume from cached data
- **Priority**: HIGH - Required for production reliability
- **Requirements**:
  - **Step-level caching**: Cache results after each of the 6 steps
  - **Resume capability**: Resume from any cached step
  - **Cache invalidation**: Smart cache invalidation based on input changes
  - **Storage efficiency**: Efficient storage of large markup documents
- **Solution Strategy**:
  - Implement caching after each analysis step
  - Add resume logic to skip completed steps
  - Use content hashing for cache invalidation
  - Optimize storage for large markup files
  - Add cache management utilities
- **Acceptance Criteria**:
  - ✅ Each step cached independently
  - ✅ Resume from any step works correctly
  - ✅ Cache invalidation on input changes
  - ✅ Efficient storage of large documents
  - ✅ Cache management commands available
  - ✅ No data loss on interruption
- **Files to Update**:
  - `discernus/agents/analysis_agent/main.py` (caching logic)
  - `discernus/core/local_artifact_storage.py` (if needed for optimizations)
- **Dependencies**: [EAA1-001], [EAA1-002] - Agent and storage must exist
- **Effort**: 2-3 days

#### [EAA1-006] Comprehensive Testing and Validation

- **Description**: Thorough testing of integrated analysis agent
- **Purpose**: Ensure production readiness and reliability
- **Priority**: HIGH - Required before deployment
- **Testing Requirements**:
  - **Unit tests**: All agent methods tested
  - **Integration tests**: Full orchestrator integration
  - **Performance tests**: 1000+ document processing
  - **Framework tests**: Multiple framework compatibility
  - **Resume tests**: Interruption and resume scenarios
- **Solution Strategy**:
  - Create comprehensive test suite
  - Test with various frameworks and experiments
  - Performance testing with large document sets
  - Test resume scenarios and error handling
  - Validate cost tracking and logging
- **Acceptance Criteria**:
  - ✅ All unit tests pass
  - ✅ Integration tests pass
  - ✅ 1000+ document processing successful
  - ✅ Multiple frameworks work correctly
  - ✅ Resume scenarios work reliably
  - ✅ Cost tracking accurate
  - ✅ No memory leaks or performance issues
- **Files to Create**:
  - `discernus/tests/test_analysis_agent_integration.py`
  - `discernus/tests/test_analysis_agent_performance.py`
  - `discernus/tests/test_analysis_agent_resume.py`
- **Dependencies**: [EAA1-001] through [EAA1-005] - All components must be complete
- **Effort**: 3-4 days

---

## Show Your Work Migration Sprints

### Migration Philosophy

**Contract-Driven Development**: The UnifiedSynthesisAgent is the final consumer of all pipeline artifacts. We define its exact data contracts first, then build each upstream component to meet those contracts. This ensures:
- No synthesis compatibility issues
- Clear success criteria for each component  
- Systematic progression through the pipeline
- End-to-end validation at each step

**Evidence Pipeline Already Compatible**: Analysis of the evidence curation process reveals it's already 80% Show Your Work compliant - it reads tool-calling artifacts (evidence_v6) and produces synthesis-compatible output. This accelerates our migration timeline.

**Systematic Refactoring Over Replacement**: Rather than building a new orchestrator, we systematically refactor the existing CleanAnalysisOrchestrator to use Show Your Work patterns while preserving mature functionality.

**Reference**: See `pm/active_projects/synthesis_data_contracts.md` for detailed synthesis requirements.

---

### Sprint SYW-1: Meet Research Data Contract ⚠️ **URGENT**

**Description**: Ensure statistical analysis produces artifacts that meet synthesis agent's research data contract
**Purpose**: Fix statistical analysis failure and establish foundation for synthesis compatibility  
**Priority**: URGENT - Required for synthesis to work
**Timeline**: 1 week - critical path for migration
**Contract Goal**: Produce research data artifact containing analysis scores, statistical results, and computational work in synthesis-compatible format
**Dependencies**: None - can start immediately

#### [SYW1-001.6] Fix Evidence Retrieval Phase ⚠️ **URGENT**

- **Description**: Fix "RAG index not available" error blocking experiments after statistical analysis
- **Purpose**: Enable experiments to proceed through evidence retrieval phase
- **Priority**: URGENT - Blocking all experiments after statistical analysis completion
- **Current Error**: "RAG index not available - cannot proceed to evidence retrieval"
- **Investigation Areas**:
  - EvidenceRetrieverAgent initialization and configuration
  - RAG index creation and population logic
  - Integration between statistical analysis and evidence retrieval phases
  - Missing dependencies or configuration for evidence retrieval
- **Solution Strategy**:
  - Debug evidence retrieval phase initialization
  - Check EvidenceRetrieverAgent dependencies and configuration
  - Validate RAG index creation process
  - Ensure proper handoff from statistical analysis to evidence retrieval
- **Acceptance Criteria**:
  - ✅ Evidence retrieval phase initializes correctly
  - ✅ RAG index created and populated successfully
  - ✅ Evidence retrieval completes without errors
  - ✅ Experiments can proceed through all phases
- **Files to Investigate**:
  - `discernus/core/clean_analysis_orchestrator.py` (evidence retrieval phase)
  - `discernus/agents/evidence_retriever_agent/` (agent implementation)
  - RAG index creation and management logic
- **Dependencies**: [SYW1-001] - Statistical analysis must work first
- **Effort**: 1-2 days

#### [SYW1-002] Add Missing Computational Work Artifacts

- **Description**: Save computational work data as separate JSON artifacts per Show Your Work architecture
- **Purpose**: Create proper `computational_work_<hash>.json` files for verification and provenance
- **Priority**: HIGH - Required for Show Your Work compliance
- **Current Issue**: Computational work data embedded in analysis results, not saved as separate artifacts
- **Solution Strategy**:
  - Modify `_process_tool_calls()` in EnhancedAnalysisAgent
  - Save computational work tool call data as separate artifacts
  - Use predictable filenames for Show Your Work compatibility
  - Maintain backward compatibility with existing format
- **Acceptance Criteria**:
  - ✅ `computational_work_<hash>.json` files created for each document
  - ✅ Files contain executed code, output, and derived metrics
  - ✅ Artifacts accessible via content-addressable storage
  - ✅ No regression in existing functionality
- **Files to Update**:
  - `discernus/agents/EnhancedAnalysisAgent/main.py` (_process_tool_calls)
- **Dependencies**: None
- **Effort**: 1-2 days

#### [SYW1-003] Debug Statistical Function Execution

- **Description**: Investigate and fix why statistical functions are generated but not executed
- **Purpose**: Restore statistical analysis execution to working state
- **Priority**: HIGH - Required for complete pipeline
- **Current Issue**: Functions generated successfully but execution fails silently
- **Investigation Areas**:
  - Function loading and module namespace issues
  - Data format compatibility between DataFrame and functions
  - Error handling that may be masking failures
  - Integration between statistical agent and orchestrator
- **Solution Strategy**:
  - Add comprehensive debugging to statistical execution pipeline
  - Validate function signatures and data format compatibility
  - Improve error reporting and logging
  - Test with minimal reproducible case
- **Acceptance Criteria**:
  - ✅ Root cause of execution failure identified and documented
  - ✅ Statistical functions execute successfully
  - ✅ Numerical results produced (ANOVA, descriptive stats, etc.)
  - ✅ Clear error messages for any failures
- **Files to Update**:
  - `discernus/core/clean_analysis_orchestrator.py` (_execute_statistical_functions)
  - Statistical function loading and execution logic
- **Dependencies**: [SYW1-001] - Data format must be fixed first
- **Effort**: 2-3 days

#### [SYW1-004] Add Synthesis Compatibility Layer

- **Description**: Ensure synthesis can work with new tool-calling artifacts via compatibility layer
- **Purpose**: Enable end-to-end pipeline while synthesis migration is pending
- **Priority**: HIGH - Required for complete pipeline
- **Current Issue**: Synthesis expects old artifact format, but analysis now produces Show Your Work artifacts
- **Solution Strategy**:
  - Create compatibility layer that translates Show Your Work artifacts to expected format
  - Ensure synthesis can read evidence from `evidence_quotes.json` files
  - Maintain existing synthesis functionality without full migration
  - Document what needs full migration in SYW-4
- **Acceptance Criteria**:
  - ✅ Synthesis can read new artifact format via compatibility layer
  - ✅ RAG index populated correctly from new evidence format
  - ✅ Final report generated with statistical results
  - ✅ Report quality matches existing standards
  - ✅ No regression in synthesis functionality
- **Files to Update**:
  - `discernus/agents/unified_synthesis_agent.py` (compatibility layer)
  - Evidence reading and RAG population logic
- **Dependencies**: [SYW1-001], [SYW1-002], [SYW1-003]
- **Effort**: 2-3 days

#### [SYW1-005] Validate Evidence Curation Works

- **Description**: Confirm evidence retrieval phase works with tool-calling analysis artifacts
- **Purpose**: Validate evidence curation can read evidence_v6 artifacts from tool-calling analysis
- **Priority**: HIGH - Evidence contract validation
- **Current Status**: Evidence curation should work since it reads evidence_v6 artifacts (which analysis still produces)
- **Solution Strategy**:
  - Run micro_test_experiment through evidence retrieval phase
  - Validate EvidenceRetrieverAgent can build index from evidence_v6 artifacts
  - Confirm curated evidence artifact created successfully
  - Test evidence search and retrieval functionality
- **Acceptance Criteria**:
  - ✅ Evidence retrieval phase completes successfully
  - ✅ RAG index built from tool-calling evidence artifacts
  - ✅ Curated evidence artifact created with proper format
  - ✅ Evidence search returns relevant quotes for statistical findings
  - ✅ Evidence ready for synthesis consumption
- **Dependencies**: [SYW1-001], [SYW1-002], [SYW1-003] - Statistical analysis must work first
- **Effort**: 1 day

#### [SYW1-006] Validate End-to-End Pipeline

- **Description**: Ensure complete micro_test_experiment runs successfully from start to finish
- **Purpose**: Validate that all migration changes work together correctly
- **Priority**: MEDIUM - Integration validation
- **Solution Strategy**:
  - Run micro_test_experiment with clean cache
  - Validate all phases complete successfully including synthesis
  - Compare results with mature architecture (1b_chf_constitutional_health)
  - Document any remaining gaps or issues
- **Acceptance Criteria**:
  - ✅ micro_test_experiment completes without errors
  - ✅ Final report generated with statistical results
  - ✅ All expected artifacts present in shared cache
  - ✅ CSV exports contain correct data
  - ✅ Performance within acceptable bounds
- **Dependencies**: [SYW1-005] - Evidence curation must work
- **Effort**: 1 day

**Sprint SYW-1 Success Criteria**:
- ✅ Research data contract met: Statistical analysis produces synthesis-compatible artifacts
- ✅ micro_test_experiment runs successfully through evidence retrieval phase
- ✅ Statistical analysis produces valid numerical results
- ✅ All Show Your Work artifacts properly created and stored (analysis_scores.json, computational_work.json)
- ✅ Evidence curation works with tool-calling artifacts (evidence_v6 format)
- ✅ Research data artifact aggregated and available for synthesis
- ✅ No regression in existing functionality
- ✅ **BONUS**: Evidence contract partially met (evidence curation already compatible)

---

### Sprint SYW-2: Complete Evidence Contract 🔍 **MEDIUM PRIORITY**

**Description**: Add verification agent to complete evidence contract (evidence curation already works)
**Purpose**: Add attestation layer to evidence pipeline for full Show Your Work compliance
**Priority**: MEDIUM - Evidence curation already functional, verification adds robustness
**Timeline**: 1-2 weeks
**Contract Status**: **PARTIALLY MET** - Evidence curation works with tool-calling artifacts, just needs verification layer
**Contract Goal**: Add attestation artifacts to complete evidence contract for synthesis
**Dependencies**: Sprint SYW-1 completion required

#### [SYW2-001] Create VerificationAgent

- **Description**: Implement VerificationAgent that re-executes and validates computational work
- **Purpose**: Add adversarial attestation layer to Show Your Work architecture
- **Priority**: HIGH - Core architectural requirement
- **Solution Strategy**:
  - Create new VerificationAgent class with tool calling support
  - Read `analysis_scores.json`, `evidence_quotes.json`, `computational_work.json`
  - Re-execute code internally and compare results
  - Use tool calling to generate `attestation.json` files
- **Acceptance Criteria**:
  - ✅ VerificationAgent successfully re-executes computational work
  - ✅ Generates `attestation_<hash>.json` files with verification results
  - ✅ Detects and reports calculation discrepancies
  - ✅ Integrates cleanly with existing orchestrator
- **Files to Create**:
  - `discernus/agents/VerificationAgent/agent.py`
  - `discernus/agents/VerificationAgent/prompt.txt`
- **Dependencies**: [SYW1-002] - Computational work artifacts must exist
- **Effort**: 1 week

#### [SYW2-002] Integrate Verification into Orchestrator

- **Description**: Add verification step to CleanAnalysisOrchestrator after each document analysis
- **Purpose**: Make verification part of standard pipeline
- **Priority**: MEDIUM - Integration requirement
- **Solution Strategy**:
  - Add verification call after each document analysis
  - Implement fail-fast on verification failure
  - Add verification metrics to performance tracking
  - Maintain backward compatibility with verification disabled
- **Acceptance Criteria**:
  - ✅ Verification runs automatically after each analysis
  - ✅ Pipeline fails fast on verification errors
  - ✅ Verification success rates tracked and reported
  - ✅ Option to disable verification for testing
- **Dependencies**: [SYW2-001]
- **Effort**: 2-3 days

**Sprint SYW-2 Success Criteria**:
- ✅ All document analyses include verification step
- ✅ Verification successfully validates computational work  
- ✅ Pipeline fails appropriately on verification errors
- ✅ Verification artifacts properly stored and tracked
- ✅ **ACCELERATED**: Evidence pipeline already 80% Show Your Work compliant
- ✅ Evidence contract fully met with verification layer added

---

### Sprint SYW-3: Migrate Statistical Analysis 📊 **MEDIUM PRIORITY**

**Description**: Replace existing statistical analysis with Show Your Work tool-calling approach
**Purpose**: Complete migration of statistical pipeline to Show Your Work architecture
**Priority**: MEDIUM - Architectural consistency
**Timeline**: 2-3 weeks
**Dependencies**: Sprint SYW-2 completion required

#### [SYW3-001] Create Statistical Planning + Execution Agent

- **Description**: New agent that reads `analysis_scores.json` files and uses tool calling for results
- **Purpose**: Replace existing statistical analysis with Show Your Work approach
- **Priority**: MEDIUM - Architectural migration
- **Solution Strategy**:
  - Create agent that reads all `analysis_scores.json` files directly
  - Use tool calling for `record_statistical_results`
  - Generate `statistics.json` and `statistical_work.json`
  - Create CSVs from structured data, not parsing
- **Acceptance Criteria**:
  - ✅ Reads analysis artifacts directly (not CSV)
  - ✅ Uses tool calling for all statistical results
  - ✅ Generates proper Show Your Work artifacts
  - ✅ Maintains same statistical analysis quality
- **Dependencies**: Sprint SYW-2 completion
- **Effort**: 1-2 weeks

#### [SYW3-002] Create Statistical Verification Agent

- **Description**: Verify statistical calculations using adversarial attestation
- **Purpose**: Add verification layer to statistical analysis
- **Priority**: MEDIUM - Show Your Work compliance
- **Solution Strategy**:
  - Re-execute statistical code independently
  - Compare results with original calculations
  - Generate `statistical_attestation.json`
- **Acceptance Criteria**:
  - ✅ Successfully verifies statistical calculations
  - ✅ Detects and reports statistical errors
  - ✅ Generates proper attestation artifacts
- **Dependencies**: [SYW3-001]
- **Effort**: 1 week

**Sprint SYW-3 Success Criteria**:
- Statistical analysis uses tool calling throughout
- All statistical calculations verified independently
- CSV generation moved to statistical agent
- Maintains existing statistical analysis quality

---

### Sprint SYW-4: Complete Show Your Work Pipeline 🎯 **FUTURE**

**Description**: Implement complete Show Your Work architecture with new orchestrator
**Purpose**: Full migration to Show Your Work architecture
**Priority**: FUTURE - Complete architectural transition
**Timeline**: 3-4 weeks
**Dependencies**: Sprint SYW-3 completion required

#### [SYW4-001] Complete CleanAnalysisOrchestrator Refactoring

- **Description**: Finish refactoring CleanAnalysisOrchestrator to fully support Show Your Work architecture
- **Purpose**: Complete the systematic refactoring to Show Your Work while preserving all existing functionality
- **Priority**: FUTURE - Architectural completion
- **Solution Strategy**:
  - Refactor remaining components to use Show Your Work artifacts natively
  - Clean up any remaining hybrid patterns
  - Optimize artifact management for Show Your Work schema
  - Preserve all existing CLI, logging, caching, and security functionality
- **Acceptance Criteria**:
  - ✅ Orchestrator natively uses Show Your Work artifacts throughout
  - ✅ All existing functionality preserved (CLI, caching, logging, security)
  - ✅ Performance maintained or improved
  - ✅ Clean, consistent Show Your Work patterns throughout
- **Dependencies**: Sprint SYW-3 completion
- **Effort**: 1-2 weeks (refactoring vs 2-3 weeks replacement)

#### [SYW4-002] Migrate Synthesis Agent to Show Your Work Artifacts

- **Description**: Update UnifiedSynthesisAgent to read Show Your Work artifacts instead of parsed responses
- **Purpose**: Enable synthesis to work with new artifact format while maintaining report quality
- **Priority**: HIGH - Critical for end-to-end pipeline
- **Current Challenge**: Synthesis agent expects old format artifacts and CSV files
- **Solution Strategy**:
  - Update artifact reading to consume `analysis_scores.json`, `evidence_quotes.json`, `computational_work.json`
  - Modify RAG population to read from `evidence_quotes.json` files directly
  - Update statistical integration to read from `statistics.json` instead of CSV parsing
  - Preserve all existing synthesis logic and report generation quality
  - Maintain academic report format and sophistication
- **Acceptance Criteria**:
  - ✅ Synthesis reads Show Your Work artifacts natively
  - ✅ RAG index populated correctly from new evidence format
  - ✅ Statistical results integrated from `statistics.json`
  - ✅ Computational work incorporated from artifact files
  - ✅ Final report quality matches existing standards
  - ✅ All synthesis features preserved (fact-checking, evidence retrieval, etc.)
- **Files to Update**:
  - `discernus/agents/unified_synthesis_agent.py`
  - Evidence retrieval and RAG population logic
  - Statistical integration components
- **Dependencies**: [SYW4-001] - Orchestrator must provide correct artifact paths
- **Effort**: 2-3 weeks (complex integration work)

#### [SYW4-003] Migrate Evidence CSV Generation

- **Description**: Create deterministic Evidence CSV Export Module  
- **Purpose**: Complete Show Your Work evidence handling
- **Priority**: MEDIUM - CSV export functionality
- **Solution Strategy**:
  - Read `evidence_quotes.json` files directly
  - Generate CSV without LLM involvement
  - Remove evidence processing from orchestrator
- **Acceptance Criteria**:
  - ✅ Evidence CSV generated deterministically
  - ✅ No LLM calls for CSV generation
  - ✅ Maintains existing CSV format
- **Dependencies**: [SYW4-002] - Synthesis migration must be complete first
- **Effort**: 1 week

**Sprint SYW-4 Success Criteria**:
- CleanAnalysisOrchestrator fully refactored to Show Your Work architecture
- All artifacts follow Show Your Work schema natively
- All existing functionality preserved and enhanced
- Clean, maintainable codebase ready for production

---

## Legacy Sprint Archive

The following sprints were part of the old architecture and are no longer relevant due to the Show Your Work migration:

### Archived Sprints (Pre-Migration)
- Sprint 16: Alpha Release Preparation (SUPERSEDED by migration)
- Sprint 17: Critical Bug Fixes (COMPLETED - incorporated into SYW-1)
- Sprint 18: Critical Regression Fixes (SUPERSEDED by SYW-1)
- Sprint 19: Agent Parsing Consistency (SUPERSEDED by tool calling migration)
- Sprint 19: Structured Output Migration (SUPERSEDED by Show Your Work architecture)

**Note**: These sprints addressed issues that are resolved by the Show Your Work migration or are no longer relevant to the new architecture.

---

## Migration Progress Tracking

### Phase 0.5: Partial Tool Calling ✅ **COMPLETED**
- Analysis agent converted to tool calling
- Backward compatibility maintained
- CSV export working

### Phase 1: Fix Current Hybrid ⚠️ **PARTIALLY COMPLETED**
- Sprint SYW-1: Statistical analysis fixed, cache system improved
- **REMAINING**: Evidence retrieval phase ("RAG index not available" error)
- Target: Restore end-to-end pipeline functionality

### Phase 2: Add Verification Layer 📋 **PLANNED**
- Sprint SYW-2 implements adversarial attestation
- Target: Core Show Your Work verification

### Phase 3: Migrate Statistical Analysis 📋 **PLANNED**
- Sprint SYW-3 completes statistical migration
- Target: Full tool calling statistical pipeline

### Phase 4: Complete Architecture 📋 **FUTURE**
- Sprint SYW-4 implements clean Show Your Work orchestrator
- Target: Production-ready Show Your Work system
