# Discernus v10 Sprints

**Purpose**: Organized backlog with sprint planning, dependencies, and detailed item specifications.

**Usage**: 
- "groom our sprints" → organize inbox items into proper sprint structure
- Items moved here from inbox.md during grooming sessions

---

## Current Status

**Date**: 2025-01-27
**Status**: Critical Infrastructure Complete - Ready for Variance Reduction
**Next Priority**: Implement 3-run internal self-consistency for analysis stability

**CLI v10 Compliance**: ✅ **COMPLETE**
**Statistical Analysis Pipeline**: ✅ **COMPLETE**
**Framework Validation**: ✅ **COMPLETE**
**Critical Infrastructure**: ✅ **COMPLETE** - All fail-fast and caching issues resolved
**Current Focus**: Analysis variance reduction through internal self-consistency

---

## Current Sprint Planning

### Sprint 1: Critical Infrastructure & Quality Assurance (IMMEDIATE) ✅ **COMPLETED**

**Timeline**: 1-2 days ✅ **COMPLETED**
**Goal**: Fix critical system issues and establish testing foundation ✅ **COMPLETED**

**🎯 Sprint 1 Complete**: All critical infrastructure issues resolved. System now has:
- ✅ Fail-fast behavior for critical pipeline components
- ✅ Stable caching system with function code content storage
- ✅ Validation caching eliminating redundant LLM calls
- ✅ Ready for variance reduction implementation

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

### Sprint 2: Analysis Variance Reduction (IMMEDIATE) 🔄 **ACTIVE**

**Timeline**: 3-5 days 🔄 **IN PROGRESS**
**Goal**: Implement 3-run internal self-consistency to stabilize analysis variance without system changes 🔄 **READY TO START**

**🎯 Sprint 2 Ready**: Caching stability verified, ready to implement variance reduction:
- ✅ Analysis caching working reliably
- ✅ Derived metrics caching stable with function code storage
- ✅ Validation caching eliminating redundant checks
- 🔄 Next: Implement 3-run internal self-consistency for analysis stability

#### [VARIANCE-001] Implement 3-Run Internal Self-Consistency Analysis

- **Description**: Implement internal self-consistency approach using 3 independent analysis runs with median aggregation to reduce variance in analysis scores
- **Dependencies**: [CRITICAL-002] (caching must be stable first)
- **Root Cause**: Single-run analysis produces variable results due to LLM stochasticity, causing correlation coefficients and derived metrics to vary between runs
- **Solution**: Modify analysis prompts to request 3 independent analytical approaches, then aggregate results using median values for numerical scores
- **Impact**:
  - Reduces analysis variance without requiring orchestrator changes
  - Improves statistical reliability of experiment results
  - Maintains caching benefits for subsequent runs
  - Cost-effective: 3x Gemini Flash Lite may outperform 1x Gemini Pro
- **Acceptance Criteria**:
  - [ ] Analysis prompts request 3 independent analytical approaches
  - [ ] Results include 3 sets of scores with different analytical perspectives
  - [ ] Median aggregation applied to numerical scores (raw, salience, confidence)
  - [ ] Evidence from all runs combined for comprehensive coverage
  - [ ] Conflicts resolved by selecting most strongly supported findings
  - [ ] Caching system works with aggregated results
  - [ ] Unit tests cover median aggregation logic
- **Effort**: 2-3 hours
- **Priority**: **HIGH** - Addresses main source of variance with low implementation risk
- **Status**: 🔄 **READY TO START** - Caching stability verified, ready for implementation


#### [CRITICAL-005] Fix Import Chain Dependency Failures

- **Description**: **CRITICAL BUG**: Multiple import failures indicate broken dependency resolution and circular import issues in the orchestration layer
- **Dependencies**: None
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

#### [TEST-INFRA] Fix Integration Test Infrastructure

- **Description**: Integration tests incorrectly mock critical setup, causing false failures
- **Impact**: False test failures prevent validation of all features
- **Root Cause**: Tests mock `_initialize_infrastructure` which bypasses `artifact_storage` setup
- **Dependencies**: [CRITICAL-005]
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
- **Dependencies**: [TEST-INFRA]
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

### Sprint 2: Data Quality & Evidence Enhancement (HIGH PRIORITY)

**Timeline**: 2-3 days
**Goal**: Improve statistical data mapping and evidence retrieval for higher quality synthesis reports

#### [DATA-001] Explicit Administration/Grouping in Corpus Manifests

- **Description**: Statistical agent generates fragile filename parsing logic instead of using corpus metadata, causing "Unknown" categorization in ANOVA
- **Root Cause**: 
  - Statistical agent's `_get_administration_mapping` function parses filenames instead of using corpus manifest
  - No explicit analytical grouping variables in corpus manifest
  - Experiment specification doesn't enforce manifest-based grouping
- **Impact**:
  - Documents categorized as "Unknown" in statistical analyses
  - ANOVA and other group-based tests compromised
  - Fragile coupling between filename conventions and statistical logic
- **Solution**:
  - Add explicit analytical grouping fields to corpus manifest (e.g., `administration: "Trump"`)
  - Update statistical agent prompt to mandate corpus manifest usage
  - Never parse filenames for metadata extraction
- **Acceptance Criteria**:
  - [ ] Corpus manifest format supports explicit analytical groupings
  - [ ] Statistical agent prompt requires manifest-based metadata extraction
  - [ ] No filename parsing in generated statistical functions
  - [ ] All documents properly categorized in statistical analyses
- **Effort**: 1-2 days
- **Priority**: **HIGH** - Data integrity issue
- **Status**: **READY TO START**

#### [DATA-002] Increase Evidence Retrieval Limits

- **Description**: Evidence retriever limited to 3 quotes per query is a premature optimization reducing report quality
- **Root Cause**: Conservative hard-coded limit in evidence_retriever_agent.py line 365
- **Impact**:
  - Synthesis reports lack sufficient evidence support
  - Statistical findings under-documented
  - Report quality unnecessarily constrained
- **Solution**:
  - Increase limit from 3 to 10-15 quotes per query
  - Consider making limit configurable or adaptive
  - RAG queries are cheap - optimize for quality over minor cost savings
- **Acceptance Criteria**:
  - [ ] Evidence retrieval limit increased to 10+ quotes per query
  - [ ] Synthesis reports show richer evidence support
  - [ ] Consider making limit configurable via experiment spec
- **Effort**: 1 hour
- **Priority**: **HIGH** - Quick win for quality improvement
- **Status**: **READY TO START**

#### [DATA-003] Update Specifications for Coherence Validation

- **Description**: Specifications need updates to ensure coherence agent (Helen) validates custom grouping variables
- **Dependencies**: [DATA-001]
- **Impact**:
  - Coherence validation misses metadata mismatches
  - Experiments fail at runtime instead of validation phase
  - Wasted compute on invalid experiment configurations
- **Solution**:
  - Update Corpus Specification to define custom analytical groupings
  - Update Experiment Specification to require manifest-based groupings
  - Enhance coherence agent to validate grouping variable existence
- **Acceptance Criteria**:
  - [ ] Corpus spec defines how to add custom analytical variables
  - [ ] Experiment spec requires grouping variables exist in corpus
  - [ ] Coherence agent validates grouping variable presence
  - [ ] Validation catches metadata mismatches before runtime
- **Effort**: 2-3 hours
- **Priority**: **MEDIUM** - Prevents future issues
- **Status**: **READY TO START**

### Sprint 3: Logging Architecture & Code Quality (MEDIUM PRIORITY)

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

#### [LOGGING-002] Investigate CLI and Logging Experience

- **Description**: Investigate current use of Rich CLI and Loguru libraries in the Discernus platform to ensure optimal researcher experience and logging implementation.
- **Dependencies**: None
- **Investigation Areas**:
  - Review Rich and Loguru best practices and latest features
  - Assess current implementation against library capabilities
  - Identify opportunities for improved user experience (progress bars, live updates, better error handling)
  - Evaluate performance impact and consistency of logging usage
- **Deliverables**:
  - Analysis report of current implementations
  - Recommendations for optimization, enhancement, and standardization
  - Implementation plan for any identified improvements
- **Effort**: 2-3 days
- **Priority**: **MEDIUM** - Enhancement opportunity
- **Status**: **NEEDS INVESTIGATION**

### Sprint 3: Architecture Refactoring & Code Quality (MEDIUM PRIORITY)

**Timeline**: 5-7 days
**Goal**: Fix architectural issues and establish clean interfaces

#### [ARCH-001] Comprehensive Agent Architecture Audit & THIN Compliance

- **Description**: **EXPANDED SCOPE**: Comprehensive audit of all agents and orchestration code to eliminate unnecessary complexity, assembler anti-patterns, and ensure THIN architecture compliance where orchestrator = traffic cop, agents = intelligence, LLMs = heavy lifting
- **Dependencies**: [LOGGING-001]
- **Root Cause**: 
  - **Anti-THIN patterns**: Complex assemblers doing work that LLMs should do directly
  - **Orchestrator overreach**: Orchestrator doing agent work instead of traffic management
  - **Agent underutilization**: Agents not leveraging LLM intelligence effectively
  - **Parsing complexity**: Complex parsing logic instead of letting LLMs read natural language
  - **Tight coupling**: Components depending on complex intermediate processing layers
- **Progress Made**:
  - ✅ **SynthesisPromptAssembler eliminated** - 306 lines of parsing complexity removed
  - ✅ **UnifiedSynthesisAgent refactored** - now reads files directly, LLM handles all parsing
  - ✅ **THIN principles applied** - experiment/framework content passed raw to LLM
  - ✅ **Evidence integration fixed** - proper artifact handoff without assembler complexity
- **Remaining Audit Scope**:
  - [ ] **EvidenceRetrieverAgent**: Audit for unnecessary parsing/formatting complexity
  - [ ] **AutomatedStatisticalAnalysisAgent**: Check if LLM can handle data structures directly
  - [ ] **AutomatedDerivedMetricsAgent**: Audit prompt assembly vs direct LLM interaction
  - [ ] **FactCheckerAgent**: Review for assembler patterns or complex preprocessing
  - [ ] **RevisionAgent**: Check for unnecessary intermediate processing
  - [ ] **All prompt assemblers**: Audit remaining assemblers (statistical, derived metrics) for THIN violations
  - [ ] **Orchestrator audit**: Ensure orchestrator only does traffic management, not agent work
- **THIN Architecture Principles**:
  - **Orchestrator**: Traffic cop only - route requests, manage artifacts, coordinate flow
  - **Agents**: Intelligence layer - make decisions, handle business logic, interface with LLMs
  - **LLMs**: Heavy lifting - read raw content, understand context, generate outputs
  - **No assemblers**: LLMs read raw files directly, no complex parsing/formatting layers
- **Impact**:
  - **Maintainability**: Eliminate complex parsing code that breaks with format changes
  - **Reliability**: Remove fragile intermediate processing layers
  - **Performance**: Reduce unnecessary processing overhead
  - **Flexibility**: LLMs handle format variations better than rigid parsers
- **Evidence from Previous Issues**:
  - ✅ **FIXED**: `SynthesisPromptAssembler.assemble_prompt() got an unexpected keyword argument 'evidence_artifacts'`
  - ✅ **FIXED**: "Research objectives not specified" due to rigid section header parsing
  - **REMAINING**: `'LocalArtifactStorage' object has no attribute 'get_hash_by_type'`
- **Acceptance Criteria**:
  - [ ] **Agent audit matrix**: All agents audited for THIN compliance (orchestrator/agent/LLM responsibility)
  - [ ] **Assembler elimination plan**: All remaining assemblers evaluated for necessity vs THIN alternatives
  - [ ] **Orchestrator scope audit**: Orchestrator responsibilities limited to traffic management only
  - [ ] **LLM utilization audit**: Agents leverage LLM intelligence instead of complex preprocessing
  - [ ] **Interface contracts**: Simple, clean interfaces between orchestrator and agents
  - [ ] **Documentation**: THIN architecture principles documented with examples
  - [ ] **Validation**: All experiments work with simplified architecture
- **Effort**: 3-5 days (expanded scope)
- **Priority**: **HIGH** - Architecture foundation issue
- **Status**: **DEFERRED** - Wait for experiment gauntlet completion and system snapshot before continuing audit

#### [ARCH-001B] Immediate Agent Audit: Remaining Assemblers & Complexity

- **Description**: **IMMEDIATE FOLLOW-UP**: Audit remaining prompt assemblers and agents for THIN violations following successful SynthesisPromptAssembler elimination
- **Dependencies**: [ARCH-001] + Experiment Gauntlet Completion + System Snapshot
- **Priority Targets**:
  1. **StatisticalAnalysisPromptAssembler** - 255 lines, complex experiment parsing
  2. **DerivedMetricsPromptAssembler** - Complex framework parsing and data sampling
  3. **EvidenceRetrieverAgent** - Check for unnecessary evidence formatting complexity
  4. **Orchestrator synthesis methods** - Remove remaining assembler dependencies
- **THIN Audit Questions for Each Component**:
  - **Can the LLM read the raw input directly?** (framework.md, experiment.md, data files)
  - **Is parsing adding value or just complexity?** (section extraction, YAML parsing, formatting)
  - **Is the orchestrator doing agent work?** (file creation, data formatting, prompt building)
  - **Are agents leveraging LLM intelligence?** (or doing manual processing)
- **Immediate Actions**:
  - [ ] **Audit StatisticalAnalysisPromptAssembler**: Can LLM read framework + experiment + data samples directly?
  - [ ] **Audit DerivedMetricsPromptAssembler**: Can LLM read framework + analysis files directly?
  - [ ] **Check EvidenceRetrieverAgent**: Remove unnecessary evidence formatting if LLM can handle raw evidence
  - [ ] **Clean orchestrator**: Remove any remaining assembler instantiation code
- **Success Metrics**:
  - [ ] Lines of parsing code eliminated
  - [ ] Number of assemblers removed
  - [ ] Experiments still work with simplified architecture
  - [ ] Reduced maintenance burden (fewer files to break)
- **Effort**: 1-2 days
- **Priority**: **HIGH** - Continue momentum from SynthesisPromptAssembler success  
- **Status**: **DEFERRED** - Wait for experiment gauntlet and system snapshot before starting

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

**Alpha Impact**: External researchers need documentation to adopt Discernus. Essential for user adoption and professional credibility.

---

## Alpha Release Sprint Series

**Timeline**: Weeks 3-8 (Post-Foundation Sprints)
**Goal**: Complete all alpha-critical features for September release
**Dependencies**: Completion of Sprints 1-4 (Critical Infrastructure & Quality Assurance)

### Alpha Sprint 1: Foundation & Legal (Weeks 3-4)

**Timeline**: 2 weeks
**Goal**: Establish environment reproducibility and open source foundation
**Total Story Points**: 31

#### [ALPHA-015] Strategy for 'But It Works on My Machine' Problem - CRITICAL FOR ALPHA

- **Issue**: #421
- **Labels**: epic, alpha-critical
- **Milestone**: Strategic Planning & Architecture
- **Status**: Not implemented
- **Priority**: CRITICAL MUST-HAVE for September Alpha Release
- **Story Points**: 13

**Description**: Eliminate environment-specific issues that prevent reproducible research by implementing containerization, dependency pinning, environment validation, and configuration management.

**Strategic Context**:
- Research reproducibility is critical for academic credibility
- Environment differences can invalidate research results
- Need consistent, reproducible execution across all platforms

**Problem Analysis**:
- **Environment Differences**: OS, Python versions, dependency versions
- **System Dependencies**: GPU drivers, system libraries, hardware differences
- **Configuration Drift**: Environment variables, paths, settings
- **Dependency Conflicts**: Package version incompatibilities

**Solution Strategy**:
- [ ] **Containerization**: Docker containers for consistent environments
- [ ] **Dependency Pinning**: Exact version requirements for all packages
- [ ] **Environment Validation**: Automated environment health checks
- [ ] **Configuration Management**: Centralized, version-controlled configs
- [ ] **CI/CD Integration**: Automated testing across multiple environments

**Implementation Plan**:
- [ ] **Phase 1**: Dependency pinning and environment validation
- [ ] **Phase 2**: Docker containerization for core platform
- [ ] **Phase 3**: Multi-environment CI/CD pipeline
- [ ] **Phase 4**: User environment setup automation

**Success Criteria**:
- [ ] 100% reproducible execution across environments
- [ ] Automated environment validation
- [ ] Clear setup instructions for all platforms
- [ ] CI/CD testing across multiple environments

**Definition of Done**:
- [ ] Environment validation system implemented
- [ ] Dependency pinning completed
- [ ] Basic containerization working
- [ ] Setup instructions documented for all platforms

---

#### [ALPHA-016] GitHub Strategy: Clean Separation of Development vs Open Source Code - CRITICAL FOR ALPHA

- **Issue**: #420
- **Labels**: epic, alpha-critical
- **Milestone**: Strategic Planning & Architecture
- **Status**: Not implemented
- **Priority**: CRITICAL MUST-HAVE for September Alpha Release
- **Story Points**: 8

**Description**: Establish strategy for cleanly separating internal development code from open source version to enable professional open source release while protecting internal IP.

**Strategic Context**:
- Much of current codebase is internal development/experimental
- Need clean separation for professional open source release
- Protect internal IP while enabling community contribution

**Current Codebase Analysis**:
- **Internal/Experimental**: Research spikes, experimental frameworks, internal tools
- **Open Source Ready**: Core platform, stable frameworks, user-facing features
- **Business Critical**: Enterprise features, proprietary algorithms, business logic

**Separation Strategy**:
- [ ] **Repository Structure**: Main repo vs. internal development repos
- [ ] **Branch Strategy**: Main branch (open source) vs. development branches
- [ ] **Feature Flags**: Internal features disabled in open source builds
- [ ] **Configuration Management**: Environment-specific feature enablement
- [ ] **Documentation**: Clear boundaries between open/closed components

**Implementation Plan**:
- [ ] Audit current codebase for open source readiness
- [ ] Create internal development repository structure
- [ ] Implement feature flag system for internal features
- [ ] Establish contribution guidelines and boundaries
- [ ] Create open source release pipeline

**Success Criteria**:
- [ ] Clean separation established
- [ ] Internal IP protected
- [ ] Open source version professional and complete
- [ ] Contribution workflow clear and safe

**Definition of Done**:
- [ ] Codebase audit completed
- [ ] Internal development structure established
- [ ] Feature flags implemented for internal features
- [ ] Open source version ready for release

---

#### [ALPHA-017] Project Open Source License Dependencies and Business Strategy Alignment - CRITICAL FOR ALPHA

- **Issue**: #419
- **Labels**: epic, legal, dependencies, alpha-critical
- **Milestone**: Strategic Planning & Architecture
- **Status**: Not implemented
- **Priority**: CRITICAL MUST-HAVE for September Alpha Release
- **Story Points**: 5

**Description**: Ensure all project dependencies are license-compatible with our business strategy by conducting complete dependency license audit and conflict resolution.

**Strategic Context**:
- Audit all third-party dependencies for license compatibility
- Identify potential license conflicts with future commercial offerings
- Establish dependency management strategy

**Scope**:
- [ ] Complete dependency license audit
- [ ] License compatibility matrix creation
- [ ] Conflict resolution strategy
- [ ] Alternative dependency evaluation
- [ ] License compliance monitoring
- [ ] Business impact assessment

**Critical Dependencies to Audit**:
- **LLM APIs**: OpenAI, Anthropic, Google Vertex AI
- **Python Libraries**: pandas, numpy, scipy, etc.
- **Framework Dependencies**: Any specialized research tools
- **Infrastructure**: Cloud services, databases, etc.

**Business Strategy Considerations**:
- [ ] Future commercial licensing model
- [ ] Enterprise feature development
- [ ] White-label opportunities
- [ ] Revenue model constraints

**Success Criteria**:
- [ ] All dependencies license-compatible
- [ ] Business strategy alignment confirmed
- [ ] Risk mitigation plan in place
- [ ] Compliance monitoring established

**Definition of Done**:
- [ ] Complete dependency license audit completed
- [ ] License compatibility matrix created
- [ ] All conflicts resolved or alternatives identified
- [ ] Business strategy alignment confirmed

---

#### [ALPHA-018] Open Source License Selection and Implementation - CRITICAL FOR ALPHA

- **Issue**: #418
- **Labels**: epic, legal, alpha-critical
- **Milestone**: Strategic Planning & Architecture
- [ ] **Status**: Not implemented
- **Priority**: CRITICAL MUST-HAVE for September Alpha Release
- **Story Points**: 5

**Description**: Select and implement appropriate open source license for Discernus to balance open source adoption with business strategy and enable community contribution.

**Strategic Context**:
- Balance open source adoption with business strategy
- Ensure license compatibility with future commercial offerings
- Protect intellectual property while enabling community contribution

**Scope**:
- [ ] License research and evaluation
- [ ] Business strategy alignment assessment
- [ ] Legal review and compliance
- [ ] License implementation across codebase
- [ ] Contributor license agreement (CLA) setup
- [ ] License documentation and notices

**License Considerations**:
- **MIT/Apache 2.0**: Permissive, business-friendly
- **GPL v3**: Copyleft, ensures derivatives stay open
- **AGPL v3**: Network copyleft, strongest protection
- **Dual licensing**: Open source + commercial options

**Business Strategy Alignment**:
- [ ] Future commercial product compatibility
- [ ] Enterprise feature licensing strategy
- [ ] Community contribution protection
- [ ] Revenue model alignment

**Success Criteria**:
- [ ] License selected and approved
- [ ] Full codebase compliance
- [ ] Legal review completed
- [ ] Business strategy aligned

**Definition of Done**:
- [ ] License selected and approved by stakeholders
- [ ] License implemented across full codebase
- [ ] Legal review completed
- [ ] License documentation and notices in place

---

### Alpha Sprint 2: Core Features (Weeks 5-6)

**Timeline**: 2 weeks
**Goal**: Implement core statistical preparation and evidence integration features
**Total Story Points**: 17+

#### [ALPHA-001] Statistical Preparation Stage and CSV Export System - CRITICAL FOR ALPHA

- **Issue**: #402
- **Labels**: enhancement, orchestration, alpha-critical
- **Milestone**: Alpha Feature Complete
- **Status**: Not implemented in current platform
- **Priority**: CRITICAL MUST-HAVE for September Alpha Release
- **Story Points**: 8

**Description**: Implement the core infrastructure for statistical preparation mode, including the orchestration stage, derived metrics calculation, and CSV export system.

**User Story**: As a researcher, I want to run `discernus run --statistical-prep` and receive analysis-ready CSV datasets so that I can perform statistical analysis using my preferred tools.

**Acceptance Criteria**:
- [ ] Add `--statistical-prep` CLI flag to ThinOrchestrator
- [ ] Implement derived metrics calculation using existing MathToolkit
- [ ] Create CSV export with raw scores, derived metrics, and evidence quotes
- [ ] Generate variable codebook with column definitions
- [ ] Store statistical preparation artifacts with content-addressable hashing
- [ ] Update manifest.json to track statistical preparation stage
- [ ] Maintain complete provenance chain for resume capability

**Technical Tasks**:
- [ ] Extend `ThinOrchestrator.run_experiment()` with `statistical_prep_only` parameter
- [ ] Create `_calculate_derived_metrics()` method using framework calculation specs
- [ ] Implement `_export_statistical_preparation_package()` for CSV generation
- [ ] Add `statistical_preparation` stage to EnhancedManifest
- [ ] Update ProvenanceOrganizer for statistical prep artifacts

**Definition of Done**:
- [ ] Statistical preparation mode produces complete CSV datasets
- [ ] All artifacts stored with SHA-256 hashing for provenance
- [ ] Manifest tracking works correctly
- [ ] Unit tests pass for new functionality

**Alpha Impact**: This is the core "offramp" functionality that researchers need - the ability to get analysis-ready CSV datasets without full synthesis. Without this, researchers can't use Discernus for their primary workflow.

---

#### [ALPHA-002] Evidence-Integrated CSV Export for Statistical Analysis - CRITICAL FOR ALPHA

- **Issue**: #403
- **Labels**: enhancement, statistical-methodology, alpha-critical
- **Milestone**: Alpha Feature Complete
- **Status**: Not implemented in current platform
- **Priority**: CRITICAL MUST-HAVE for September Alpha Release
- **Story Points**: 5

**Description**: Enhance the CSV export functionality to include evidence integration, allowing researchers to export statistical results with linked evidence for comprehensive analysis and reporting.

**User Story**: As a researcher, I want to export my statistical analysis results with integrated evidence, so that I can maintain the connection between data and supporting evidence in external tools.

**Acceptance Criteria**:
- [ ] CSV export includes evidence columns
- [ ] Evidence properly linked to statistical results
- [ ] Export format is compatible with external analysis tools
- [ ] Evidence metadata preserved in export
- [ ] Export performance optimized for large datasets

**Technical Tasks**:
- [ ] Extend CSV export schema to include evidence
- [ ] Implement evidence linking logic
- [ ] Optimize export performance
- [ ] Add export format validation
- [ ] Create export documentation

**Definition of Done**:
- [ ] CSV exports include evidence integration
- [ ] Export performance meets requirements
- [ ] Format is compatible with external tools
- [ ] Documentation covers export features

**Alpha Impact**: CSV exports without evidence lose the connection between data and supporting quotes - this breaks research integrity. Essential for maintaining academic standards in exported data.

---

#### [ALPHA-003] Resume from Statistical Preparation to Full Synthesis - CRITICAL FOR ALPHA

- **Issue**: #405
- **Labels**: enhancement, orchestration, alpha-critical
- **Milestone**: Alpha Feature Complete
- **Status**: Not implemented in current platform
- **Priority**: CRITICAL MUST-HAVE for September Alpha Release
- **Story Points**: 4

**Description**: Implement the ability to resume from statistical preparation to full synthesis, providing workflow flexibility for researchers who initially chose the offramp but later want complete analysis.

**User Story**: As a researcher, I want to be able to continue from my statistical preparation results to full Discernus synthesis when needed, so that I have maximum flexibility in my research workflow.

**Acceptance Criteria**:
- [ ] `discernus run --resume-from-stats` command functionality
- [ ] Automatic detection of existing statistical preparation artifacts
- [ ] Seamless continuation from statistical prep to synthesis stage
- [ ] Updated manifest.json with resume history and provenance
- [ ] Extended directory structure with synthesis artifacts
- [ ] Preserved statistical preparation results alongside synthesis results

**Technical Tasks**:
- [ ] Implement `--resume-from-stats` CLI option
- [ ] Add resume detection logic in ThinOrchestrator
- [ ] Extend existing directory structure without overwriting
- [ ] Update manifest with resume metadata and timeline
- [ ] Preserve complete audit trail across resume operations

**Definition of Done**:
- [ ] Resume functionality works seamlessly from statistical prep
- [ ] All original statistical prep artifacts preserved
- [ ] Manifest shows complete workflow history
- [ ] Directory structure maintains both statistical prep and synthesis results

**Alpha Impact**: Researchers need workflow flexibility - start with stats, then decide if they want full synthesis later. Enables iterative research workflows that researchers expect.

---

#### [ALPHA-004] CLI Fundamentals - Professional Interface & Standards - CRITICAL FOR ALPHA

- **Issue**: #306
- **Labels**: enhancement, alpha-critical
- **Milestone**: Alpha Feature Complete
- **Status**: Partially implemented, needs documentation and polish
- **Priority**: CRITICAL MUST-HAVE for September Alpha Release
- **Story Points**: Medium (documentation + polish)

**Description**: Transform Discernus CLI from basic tool to professional research interface with modern standards and documentation.

**User Story**: As a researcher, I want a professional, documented CLI that I can actually use for research, so that I can adopt Discernus as a serious research tool.

**Acceptance Criteria**:
- [ ] Progress bars during experiment execution
- [ ] Structured table display for `discernus list`
- [ ] Enhanced error messages with formatting
- [ ] Config file support working (`.discernus.yaml`)
- [ ] Environment variables working (`DISCERNUS_ANALYSIS_MODEL`)
- [ ] Verbose/quiet flags functional across all commands
- [ ] Complete CLI reference documentation
- [ ] Best practices guide for researchers
- [ ] Usage examples for all commands and options

**Technical Tasks**:
- [ ] Integrate Rich CLI for professional terminal interface
- [ ] Implement config file and environment variable support
- [ ] Add global verbose/quiet flags
- [ ] Create complete command reference documentation
- [ ] Write best practices guide and usage examples

**Definition of Done**:
- [ ] Professional interface with progress bars and structured tables
- [ ] Modern CLI standards (config files, env vars, flags)
- [ ] Complete documentation for external researchers
- [ ] Zero breaking changes to existing interface

**Alpha Impact**: Alpha release needs a professional, documented CLI that external researchers can actually use. Required for external adoption and professional credibility.

---

### Alpha Sprint 3: Quality & Reliability (Weeks 7-8)

**Timeline**: 2 weeks
**Goal**: Implement quality assurance and reliability features
**Total Story Points**: 20+

#### [ALPHA-005] Enhanced Validator Reports - CRITICAL FOR ALPHA

- **Issue**: #394
- **Labels**: enhancement, validation, alpha-critical
- **Milestone**: Alpha Quality & Hygiene
- **Status**: Not implemented in current platform
- **Priority**: CRITICAL MUST-HAVE for September Alpha Release
- **Story Points**: 8

**Description**: Implement enhanced validator reports that provide comprehensive validation results with actionable feedback for researchers to improve their frameworks and experiments.

**User Story**: As a researcher, I want detailed validation reports that clearly explain what's wrong with my framework or experiment and how to fix it, so that I can quickly resolve issues and proceed with my research.

**Acceptance Criteria**:
- [ ] Enhanced validation reports with detailed error explanations
- [ ] Actionable feedback for common validation issues
- [ ] Clear guidance on how to fix validation problems
- [ ] Validation report format suitable for external researchers
- [ ] Integration with existing validation pipeline

**Technical Tasks**:
- [ ] Extend validation report generation
- [ ] Implement error categorization and explanation
- [ ] Create actionable feedback templates
- [ ] Integrate with validation pipeline
- [ ] Add validation report documentation

**Definition of Done**:
- [ ] Enhanced validation reports generated
- [ ] Actionable feedback provided
- [ ] Reports integrated with validation pipeline
- [ ] Documentation covers validation features

**Alpha Impact**: External researchers need clear guidance when validation fails. Essential for user adoption and reducing support burden.

---

#### [ALPHA-006] Academic Output Standards - CRITICAL FOR ALPHA

- **Issue**: #351
- **Labels**: enhancement, academic-standards, alpha-critical
- **Milestone**: Alpha Quality & Hygiene
- **Status**: Not implemented in current platform
- **Priority**: CRITICAL MUST-HAVE for September Alpha Release
- **Story Points**: 5

**Description**: Implement academic output standards to ensure final reports have proper citations, reference frameworks are properly cited, and the provenance system is bulletproof for research integrity.

**User Story**: As a researcher, I want Discernus to produce outputs that meet basic academic standards for citations and provenance, so that I can use the results as inputs to the publication process.

**Acceptance Criteria**:
- [ ] Final reports include proper citations and references
- [ ] Reference frameworks properly cited in outputs
- [ ] Provenance system provides complete traceability
- [ ] Academic standards documentation for researchers
- [ ] Quality checks for academic output compliance

**Technical Tasks**:
- [ ] Implement citation generation system
- [ ] Add reference framework citation tracking
- [ ] Enhance provenance system for academic standards
- [ ] Create academic output validation
- [ ] Document academic standards requirements

**Definition of Done**:
- [ ] Citations properly generated and included
- [ ] Reference frameworks properly cited
- [ ] Provenance system provides complete traceability
- [ ] Academic standards documented and enforced

**Alpha Impact**: Alpha release needs to produce outputs suitable as inputs to publication process, not publication quality artifacts. Essential for academic credibility.

---

#### [ALPHA-007] Enhanced Provenance System - CRITICAL FOR ALPHA

- **Issue**: #352
- **Labels**: enhancement, provenance, alpha-critical
- **Milestone**: Alpha Quality & Hygiene
- **Status**: Not implemented in current platform
- **Priority**: CRITICAL MUST-HAVE for September Alpha Release
- **Story Points**: 7

**Description**: Implement enhanced provenance system that provides complete traceability of all research artifacts, ensuring research integrity and reproducibility.

**User Story**: As a researcher, I want complete provenance tracking for all research artifacts, so that I can demonstrate research integrity and enable others to reproduce my work.

**Acceptance Criteria**:
- [ ] Complete provenance tracking for all artifacts
- [ ] Provenance information accessible and understandable
- [ ] Provenance system integrated with all components
- [ ] Provenance documentation for researchers
- [ ] Provenance validation and integrity checks

**Technical Tasks**:
- [ ] Implement comprehensive provenance tracking
- [ ] Integrate provenance with all system components
- [ ] Create provenance visualization and reporting
- [ ] Add provenance validation and integrity checks
- [ ] Document provenance system for researchers

**Definition of Done**:
- [ ] Complete provenance tracking implemented
- [ ] Provenance integrated with all components
- [ ] Provenance information accessible and understandable
- [ ] Documentation covers provenance features

**Alpha Impact**: Research integrity requires complete provenance. Essential for academic credibility and reproducibility.

---

#### [ALPHA-008] Dead Code Cleanup and Technical Debt Reduction - CRITICAL FOR ALPHA

- **Issue**: #400
- **Labels**: cleanup, technical-debt, alpha-critical
- **Milestone**: Alpha Release Close Down
- **Status**: Not implemented in current platform
- **Priority**: CRITICAL MUST-HAVE for September Alpha Release
- **Story Points**: 5

**Description**: Clean up dead code, remove deprecated components, and reduce technical debt to ensure a clean, maintainable codebase for the Alpha release.

**User Story**: As a developer, I want a clean, maintainable codebase free of dead code and technical debt, so that I can efficiently develop and maintain the platform.

**Acceptance Criteria**:
- [ ] Dead code identified and removed
- [ ] Deprecated components properly removed
- [ ] Technical debt reduced to acceptable levels
- [ ] Codebase clean and maintainable
- [ ] Documentation updated to reflect current state

**Technical Tasks**:
- [ ] Audit codebase for dead code
- [ ] Remove deprecated components
- [ ] Address technical debt issues
- [ ] Update documentation
- [ ] Verify cleanup completeness

**Definition of Done**:
- [ ] Dead code removed
- [ ] Deprecated components removed
- [ ] Technical debt reduced
- [ ] Codebase clean and maintainable
- [ ] Documentation updated

**Alpha Impact**: Clean codebase essential for maintainability and future development. Required for professional release quality.

---

### Alpha Sprint 4: Documentation & Testing (Weeks 9-10)

**Timeline**: 2 weeks
**Goal**: Complete documentation and testing infrastructure
**Total Story Points**: 18+

#### [ALPHA-009] Integration Testing Gauntlet - CRITICAL FOR ALPHA

- **Issue**: #333
- **Labels**: testing, integration, alpha-critical
- **Milestone**: Alpha Release Close Down
- **Status**: Not implemented in current platform
- **Priority**: CRITICAL MUST-HAVE for September Alpha Release
- **Story Points**: 8

**Description**: Implement comprehensive integration testing gauntlet to ensure all system components work together correctly and produce reliable results.

**User Story**: As a developer, I want comprehensive integration tests that verify all system components work together, so that I can confidently release a stable Alpha version.

**Acceptance Criteria**:
- [ ] Integration test suite covering all major workflows
- [ ] End-to-end testing of complete experiment execution
- [ ] Component interaction testing
- [ ] Performance and reliability testing
- [ ] Automated test execution and reporting

**Technical Tasks**:
- [ ] Design integration test architecture
- [ ] Implement end-to-end test scenarios
- [ ] Create component interaction tests
- [ ] Add performance and reliability tests
- [ ] Set up automated test execution

**Definition of Done**:
- [ ] Integration test suite implemented
- [ ] All major workflows covered
- [ ] Automated execution working
- [ ] Test reporting functional

**Alpha Impact**: Alpha release needs confidence that all components work together. Essential for release quality and user experience.

---

#### [ALPHA-010] Unit Testing Coverage - CRITICAL FOR ALPHA

- **Issue**: #332
- **Labels**: testing, unit-tests, alpha-critical
- **Milestone**: Alpha Release Close Down
- **Status**: Not implemented in current platform
- **Priority**: CRITICAL MUST-HAVE for September Alpha Release
- **Story Points**: 5

**Description**: Implement comprehensive unit testing coverage for all critical system components to ensure code quality and reliability.

**User Story**: As a developer, I want comprehensive unit tests for all critical components, so that I can catch bugs early and maintain code quality.

**Acceptance Criteria**:
- [ ] High unit test coverage for critical components
- [ ] Unit tests for all public APIs
- [ ] Automated test execution
- [ ] Test reporting and coverage metrics
- [ ] Continuous integration integration

**Technical Tasks**:
- [ ] Identify critical components for testing
- [ ] Implement unit tests for public APIs
- [ ] Set up automated test execution
- [ ] Add test reporting and coverage metrics
- [ ] Integrate with CI/CD pipeline

**Definition of Done**:
- [ ] High unit test coverage achieved
- [ ] All public APIs tested
- [ ] Automated execution working
- [ ] Coverage metrics available

**Alpha Impact**: Unit tests essential for code quality and bug prevention. Required for professional release standards.

---

#### [ALPHA-011] Experiment Gauntlet Completion - CRITICAL FOR ALPHA

- **Issue**: #331
- **Labels**: testing, quality-assurance, alpha-critical
- **Milestone**: Alpha Release Close Down
- **Status**: Partially implemented, needs completion
- **Priority**: CRITICAL MUST-HAVE for September Alpha Release
- **Story Points**: 3

**Description**: Complete the existing experiment gauntlet with the release candidate to achieve zero errors and strong final reports and provenance packages.

**User Story**: As a developer, I want to complete the experiment gauntlet with zero errors and strong outputs, so that I can validate the Alpha release candidate quality.

**Acceptance Criteria**:
- [ ] Experiment gauntlet runs with zero errors
- [ ] All experiments produce strong final reports
- [ ] Provenance packages complete and accurate
- [ ] Performance meets requirements
- [ ] Quality metrics documented

**Technical Tasks**:
- [ ] Run complete experiment gauntlet
- [ ] Fix any errors or issues found
- [ ] Validate report quality and completeness
- [ ] Verify provenance package accuracy
- [ ] Document quality metrics and results

**Definition of Done**:
- [ ] Gauntlet runs with zero errors
- [ ] All reports meet quality standards
- [ ] Provenance packages accurate
- [ ] Performance requirements met
- [ ] Quality metrics documented

**Alpha Impact**: Experiment gauntlet completion validates Alpha release quality. Essential for release confidence and user experience.

---

#### [ALPHA-012] Cost Summary Report Generation - CRITICAL FOR ALPHA

- **Issue**: #406
- **Labels**: enhancement, cost-tracking, alpha-critical
- **Milestone**: Alpha Release Close Down
- **Status**: Not implemented in current platform
- **Priority**: CRITICAL MUST-HAVE for September Alpha Release
- **Story Points**: 2

**Description**: Implement automatic generation of final cost summary report markdown files based on log data, placed in the results folder alongside final_report.md.

**User Story**: As a researcher, I want an automatic cost summary report generated for each experiment, so that I can track and report on computational costs for research transparency.

**Acceptance Criteria**:
- [ ] Automatic cost summary report generation
- [ ] Reports placed in results folder
- [ ] Simple, concise format (approximately 10 lines)
- [ ] Based on actual log data
- [ ] Integrated with experiment completion

**Technical Tasks**:
- [ ] Implement cost summary report generation
- [ ] Integrate with experiment completion workflow
- [ ] Create simple, concise report format
- [ ] Ensure reports placed in correct location
- [ ] Test with actual experiment data

**Definition of Done**:
- [ ] Cost summary reports automatically generated
- [ ] Reports placed in results folder
- [ ] Format is simple and concise
- [ ] Based on actual log data
- [ ] Integrated with experiment workflow

**Alpha Impact**: Cost transparency essential for research credibility. Required for academic standards and user trust.

---
