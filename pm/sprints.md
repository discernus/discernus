# Discernus v10 Sprints

**Purpose**: Organized backlog with sprint planning, dependencies, and detailed item specifications.

**Usage**:

- "groom our sprints" → organize inbox items into proper sprint structure
- Items moved here from inbox.md during grooming sessions

---

## Current Status

**Date**: 2025-01-27
**Status**: All Major Infrastructure Issues Resolved - Ready for Sprint 5
**Next Priority**: Sprint 6 (CLI UX Improvements)

**Infrastructure Status**:
- ✅ **Sprints 1-4**: All completed successfully (moved to done.md)
- ✅ **Critical Issues**: All CRITICAL-001 through CRITICAL-005 resolved
- ✅ **Core Features**: CLI v10, Statistical Pipeline, Framework Validation operational
- ✅ **Quality Enhancements**: Caching, logging, data quality, evidence retrieval optimized
- ✅ **Ready for Sprint 5**: Architecture refactoring and advanced features

---

## Current Sprint Planning

### Sprint 5: Architecture Refactoring & Code Quality (MEDIUM PRIORITY)

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

#### [PERF-002] Enhanced Derived Metrics Caching - Calculation Results

- **Description**: Extend derived metrics caching to include calculation results, not just function generation
- **Impact**: Eliminate redundant calculations when analysis data hasn't changed, improving development velocity
- **Current State**: Only function generation is cached (LLM prompts and function code)
- **Solution**: Cache computed derived metrics results using analysis data + framework content as cache key
- **Benefits**:
  - Eliminate redundant score calculations
  - Faster iteration during analysis refinement
  - Reduced computational overhead
- **Effort**: 1-2 days
- **Priority**: **MEDIUM** - Performance optimization for iterative development
- **Status**: **PENDING**

#### [PERF-003] Enhanced Statistical Analysis Caching - Statistical Results

- **Description**: Extend statistical analysis caching to include statistical results, not just function generation
- **Impact**: Eliminate redundant statistical computations when data hasn't changed
- **Current State**: Only function generation is cached (LLM prompts and function code)
- **Solution**: Cache computed statistical results using analysis + derived metrics + framework content as cache key
- **Benefits**:
  - Eliminate redundant ANOVA, correlation, and statistical calculations
  - Faster statistical analysis iteration
  - Reduced computational overhead for repeated runs
- **Effort**: 1-2 days
- **Priority**: **MEDIUM** - Performance optimization for statistical workflows
- **Status**: **PENDING**

#### [ARCH-004] Simplify LLM Configuration Architecture

- **Description**: Reduce complexity in LLM model selection and configuration management
- **Current State**: Over-engineered with 4-tier configuration hierarchy, 20+ model options, agent-specific assignments, complex fallback chains, and dynamic model selection
- **Problem**: Premature optimization creating development friction and maintenance overhead
- **Solution**: Simplify to 2-tier hierarchy (CLI + config file), 2 core models (Flash for analysis, Pro for synthesis), remove agent-specific complexity
- **Benefits**:
  - Easier to understand and maintain
  - Faster development with less configuration debugging
  - More predictable behavior across runs
  - Reduced testing surface and edge cases
  - Clearer user experience
- **What to Remove**:
  - Environment variable complexity
  - Validation model (use synthesis model)
  - Agent-specific model assignments
  - Dynamic model selection and tiered processing
  - Complex fallback chains
  - Scale-based model switching
- **Target Architecture**: 2 models, single config file, CLI overrides, no runtime complexity
- **Effort**: 1-2 days
- **Priority**: **MEDIUM** - Development velocity improvement
- **Timeline**: Future sprint - not blocking current work
- **Status**: **PENDING**

---

### Sprint 6: CLI UX Improvements (HIGH PRIORITY)

**Timeline**: 2-3 weeks
**Goal**: Major improvements to command-line interface user experience and discoverability

#### [CLI-UX-001] Fix Critical Documentation Inconsistencies in CLI Help Text

- **Task**: Fix incorrect command syntax in help text examples and documentation
- **Problem**: Help text shows `python3 -m discernus.cli` but actual usage requires `python3 -m discernus`
- **Impact**: New users are immediately confused by broken examples
- **Scope**: Update all help text examples, documentation, and README files
- **Priority**: HIGH - Affects all new users
- **Effort**: 1-2 hours
- **Status**: **PENDING**

#### [CLI-UX-002] Simplify Overloaded Command Structure

- **Task**: Reduce 17+ commands to a more manageable set with logical grouping
- **Problem**: Too many commands overwhelm users, no clear hierarchy between core vs utility commands
- **Proposed Structure**:
  - **Core (4 commands)**: run, validate, debug, list
  - **Utility (4 commands)**: cache, config, artifacts, workflow
  - **Advanced (remaining)**: Move complex commands to subcommands or hide by default
- **Priority**: HIGH - Major UX improvement for discoverability
- **Effort**: 4-6 hours
- **Status**: **PENDING**

#### [CLI-UX-003] Standardize Command Path Handling Patterns

- **Task**: Make all commands consistently default to current directory
- **Problem**: Some commands require explicit paths, others default to current directory
- **Scope**: Update cache, artifacts, and other commands to match run/validate pattern
- **Priority**: MEDIUM - Consistency improvement
- **Effort**: 2-3 hours
- **Status**: **PENDING**

#### [CLI-UX-004] Remove or Improve Deprecated Command Messaging

- **Task**: Either remove deprecated commands or provide clear upgrade paths
- **Problem**: `start` and `stop` commands show confusing "removed" messages
- **Options**: Remove entirely, provide clear migration messages, or implement stubs that guide users
- **Priority**: MEDIUM - Cleans up confusing user experience
- **Effort**: 1-2 hours
- **Status**: **PENDING**

#### [CLI-UX-005] Implement Missing Continue Command or Remove References

- **Task**: Either implement the `continue` command mentioned in help text or remove all references
- **Problem**: Help text mentions `discernus continue` but command doesn't exist
- **Analysis**: Should implement intelligent experiment resumption based on cached artifacts
- **Priority**: MEDIUM - Help text accuracy
- **Effort**: 3-4 hours (if implementing) or 30 min (if removing)
- **Status**: **PENDING**

#### [CLI-UX-006] Improve Help Text Quality and Clarity

- **Task**: Rewrite unclear help text, especially for complex commands
- **Specific Issues**:
  - `workflow` command ARGS explanation is unclear
  - Cache management options need better descriptions
  - Command examples should be more comprehensive
- **Priority**: MEDIUM - User guidance improvement
- **Effort**: 2-3 hours
- **Status**: **PENDING**

#### [CLI-UX-007] Add Command Categories to Help Display

- **Task**: Organize help output with clear command categories
- **Proposed Structure**:
  ```
  CORE COMMANDS:
    run           Execute complete experiment
    validate      Check experiment structure

  UTILITY COMMANDS:
    cache         Manage validation cache
    config        Configuration management

  ADVANCED COMMANDS:
    telemetry     Infrastructure monitoring
  ```
- **Priority**: MEDIUM - Improved discoverability
- **Effort**: 2-3 hours
- **Status**: **PENDING**

#### [CLI-UX-008] Standardize Option Patterns Across Commands

- **Task**: Ensure consistent option naming and patterns
- **Issues Found**:
  - `--cleanup-failed` should be `--clean-failed`
  - Not all destructive commands have `--dry-run`
  - Inconsistent flag patterns for similar operations
- **Priority**: LOW - Consistency polish
- **Effort**: 1-2 hours
- **Status**: **PENDING**

#### [CLI-UX-009] Improve Error Messages with Actionable Guidance

- **Task**: Replace generic error messages with helpful suggestions
- **Examples**:
  - Path not found: suggest checking path or using `discernus list`
  - Invalid experiment: suggest running validation
  - Missing dependencies: suggest installation commands
- **Priority**: MEDIUM - User experience improvement
- **Effort**: 2-3 hours
- **Status**: **PENDING**

#### [CLI-UX-010] Add Interactive Command Discovery

- **Task**: Implement `--help` improvements and command suggestions
- **Features**:
  - Show related commands when command not found
  - Suggest corrections for typos
  - Provide "did you mean?" suggestions
- **Priority**: LOW - Nice-to-have improvement
- **Effort**: 3-4 hours
- **Status**: **PENDING**

---

### Sprint 7: Research Validation & Experimental Studies (HIGH PRIORITY)

**Timeline**: 3-4 weeks
**Goal**: Execute key research validation experiments and complete major study designs

#### [EXPERIMENT-001] Repeat Constitutional Health Experiment 1 with 3-Run Internal Median Aggregation

- **Task**: Repeat experiment 1 constitutional health with the new 3-run internal median aggregation analysis approach
- **Timing**: After refining report structure and shaking out a few more bugs
- **Purpose**: Validate the new variance reduction approach with a known experiment
- **Dependencies**: Report structure refinement, bug fixes, variance reduction implementation
- **Priority**: MEDIUM - Validation experiment, not urgent
- **Effort**: 2-3 days
- **Status**: **PENDING**

#### [EXPERIMENT-002] BYU Team Populism Studies Replication Series

- **Task**: Structure two or three new experiments that replicate BYU team populism studies
- **Studies to Replicate**:
  - Vanderveen study
  - Bolsonaro study
  - One other (TBD)
- **Purpose**: Essential research for alpha release outreach
- **Priority**: HIGH - Critical for alpha release credibility
- **Dependencies**: Framework validation, corpus preparation
- **Timeline**: Before alpha release outreach
- **Effort**: 1-2 weeks
- **Status**: **PENDING**

#### [EXPERIMENT-003] Complete 2-D Trump Populism Study Design and Corpus

- **Task**: Complete the corpus and experiment design for the 2-D Trump populism study currently in draft
- **Context**: Very large study requiring meticulous attention to detail - will be a landmark research piece
- **Scope**:
  - Complete corpus design and preparation
  - Finalize experiment specification
  - Ensure all methodological details are properly documented
  - Validate framework and corpus coherence
- **Purpose**: Landmark populism research study demonstrating Discernus capabilities
- **Priority**: HIGH - Major research undertaking with significant impact potential
- **Dependencies**: Framework validation, corpus preparation tools, experiment design refinement
- **Timeline**: Before alpha release outreach
- **Effort**: Large - requires careful attention to every detail
- **Status**: **PENDING**
