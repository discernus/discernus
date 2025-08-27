# Inbox - Raw Backlog Items

**Purpose**: Raw capture of backlog items without organization or sprint planning. Items here will be groomed into organized sprints later.

**Usage**: 
- "inbox this" → append new items here with minimal formatting
- "groom our sprints" → move all items from here to sprints.md with proper organization

---

## Inbox Items

### Rich CLI Usage Investigation
**Date**: 2024-12-19  
**Priority**: Medium  
**Effort**: 2-3 days  
**Description**: Investigate current use of Rich CLI library in Discernus platform to ensure optimal researcher experience. Current implementation shows extensive usage in CLI interface but may have opportunities for enhancement.

**Current State**:
- Rich CLI wrapper implemented in `discernus/cli_console.py`
- Extensive usage throughout main CLI (`discernus/cli.py`) for tables, panels, formatting
- Professional terminal interface with consistent styling
- Used for experiment summaries, cost reporting, status displays, configuration management

**Investigation Areas**:
- Review Rich library best practices and latest features
- Assess current implementation against Rich library capabilities
- Identify opportunities for improved user experience (progress bars, live updates, better error handling)
- Evaluate performance impact of current Rich usage
- Consider alternative Rich components that could enhance researcher workflow
- Review accessibility and cross-platform compatibility

**Deliverables**:
- Analysis report of current Rich CLI implementation
- Recommendations for optimization and enhancement
- Implementation plan for any identified improvements
- Performance benchmarks if changes are proposed

**Stakeholders**: Research team, CLI users, platform developers

### Loguru Implementation Investigation
**Date**: 2024-12-19  
**Priority**: Medium  
**Effort**: 2-3 days  
**Description**: Investigate current use of loguru logging library in Discernus platform to ensure optimal logging implementation and researcher experience.

**Current State**:
- Comprehensive logging configuration in `discernus/core/logging_config.py`
- Multiple log handlers: console, file, error, performance, LLM interactions
- Performance timing context manager with memory tracking
- Audit logging integration for research provenance
- Mixed usage patterns across codebase (some loguru, some standard logging)

**Investigation Areas**:
- Review loguru best practices and latest features
- Assess current implementation against loguru capabilities
- Identify opportunities for improved logging structure and performance
- Evaluate consistency of logging usage across codebase
- Consider advanced loguru features (structured logging, async logging, log aggregation)
- Review logging performance impact and optimization opportunities
- Assess integration with existing audit logging system

**Deliverables**:
- Analysis report of current loguru implementation
- Recommendations for optimization and standardization
- Implementation plan for any identified improvements
- Performance analysis of current logging overhead
- Standardization plan for consistent logging across codebase

**Stakeholders**: Research team, developers, system administrators



### Logging Configuration Complexity Crisis
**Date**: 2025-01-27  
**Priority**: HIGH  
**Effort**: 3-5 days  
**Description**: Discovered a convoluted, multi-layered logging configuration system that's causing verbose debug output and making experiments unreadable. This represents a critical architectural flaw that needs immediate forensic analysis.

**Current State**:
- **Multiple logging systems**: Standard Python logging, loguru, and custom logging configurations all coexisting
- **Orchestrator override**: `CleanAnalysisOrchestrator` explicitly sets txtai loggers to DEBUG level in 3 separate locations
- **Inconsistent levels**: Console set to WARNING but multiple components override with DEBUG
- **Environment variables**: `LITELLM_LOG_LEVEL=WARNING` set but overridden by code
- **File vs console**: File logging captures everything (DEBUG) while console should be clean (WARNING)

**Root Cause Analysis**:
- Orchestrator has hardcoded `txtai_logger.setLevel(logging.DEBUG)` in 3 methods:
  - `_build_fact_checker_rag_index()` (line ~1957)
  - `_build_evidence_rag_index()` (line ~2676) 
  - `_build_comprehensive_rag_index()` (line ~3394)
- These overrides happen AFTER the main logging configuration is set
- Multiple logging libraries (logging, loguru) creating conflicts
- No centralized logging policy enforcement

**Impact**:
- Experiments produce overwhelming debug output
- Terminal becomes unreadable during execution
- Researchers can't see actual progress or errors
- Debug information floods console instead of being captured to files
- Violates the "human-centric UX" principle from project rules

**Evidence from Terminal**:
- txtai embeddings debug output flooding console
- LiteLLM verbose logging despite environment variable
- Multiple logging systems competing for output
- Console handlers being overridden by component-level settings

**Immediate Actions Taken**:
- Changed all 3 txtai logger overrides from DEBUG to WARNING
- Updated logging messages to reflect the change
- Maintained file logging at DEBUG level for debugging

**Forensic Audit Requirements**:
- Map all logging configurations across the codebase
- Identify all components that override logging levels
- Document the logging hierarchy and override points
- Create centralized logging policy and enforcement
- Eliminate duplicate and conflicting logging systems

**Refactoring Implications**:
- This complexity validates the need for orchestrator refactoring
- Logging should be centralized, not scattered across components
- Agents should not be managing their own logging levels
- Need clear separation between debug (file) and user (console) output

**Stakeholders**: Research team, developers, system administrators, CLI users

### Orchestrator Data Structure Mismatch
**Date**: 2025-01-27  
**Priority**: HIGH  
**Effort**: 2-3 days  
**Description**: The orchestrator creates individual analysis files but the `AutomatedDerivedMetricsAgent` expects a consolidated `analysis_data.json` file, causing pipeline failures.

**Current State**:
- Orchestrator creates individual files: `analysis_0.json`, `analysis_1.json`, etc.
- `AutomatedDerivedMetricsAgent._load_data_structure()` expects `analysis_data.json`
- Agent falls back to generic defaults when file not found
- LLM generation fails due to insufficient data context

**Root Cause Analysis**:
- **Data flow inconsistency**: Orchestrator and agent have different data structure expectations
- **Missing contract**: No standardized data format between orchestrator and agents
- **Fallback failure**: Agent's fallback mechanism doesn't provide enough context for LLM generation
- **Tight coupling**: Agent depends on specific orchestrator file creation patterns

**Impact**:
- Experiments fail during derived metrics phase
- `AutomatedDerivedMetricsAgent` cannot generate required functions
- Pipeline breaks with "No such file or directory" errors
- Temporary workspace management becomes brittle

**Evidence from Terminal**:
- `[Errno 2] No such file or directory: '.../temp_derived_metrics/automatedderivedmetricsagent_functions.py'`
- Agent looking for `analysis_data.json` but finding individual files
- Fallback to generic data structure insufficient for LLM generation

**Immediate Actions Taken**:
- Added creation of `analysis_data.json` alongside individual files
- Maintained backward compatibility for prompt assembler

**Forensic Audit Requirements**:
- Map all data structure contracts between orchestrator and agents
- Document expected file formats and naming conventions
- Identify all components with file structure dependencies
- Create standardized data flow specifications

**Refactoring Implications**:
- Data contracts should be explicit, not implicit
- Agents should be more self-sufficient in data handling
- Orchestrator should not manage file creation details
- Need clear separation between data flow and file management

**Stakeholders**: Research team, developers, pipeline maintainers

### Import Chain Dependency Failures
**Date**: 2025-01-27  
**Priority**: HIGH  
**Effort**: 1-2 days  
**Description**: Multiple import failures indicate broken dependency resolution and circular import issues in the orchestration layer.

**Current State**:
- `ValidationCache` import errors from `discernus.core.validation_cache`
- `FactCheckerAgent` import path issues requiring `from ..agents.fact_checker_agent.agent import FactCheckerAgent`
- Import statements referencing non-existent or incorrectly structured modules

**Root Cause Analysis**:
- **Broken dependency resolution**: Import paths don't match actual module structure
- **Circular import potential**: Components importing from each other creating dependency cycles
- **Module structure changes**: Code references modules that have been moved or restructured
- **Missing __init__.py files**: Empty `__init__.py` files in agent directories

**Impact**:
- CLI fails to start with import errors
- Blocking all experiments until imports are fixed
- Indicates deeper architectural dependency issues
- Suggests module organization needs review

**Evidence from Terminal**:
- `cannot import name 'ValidationCache' from 'discernus.core.validation_cache'`
- `cannot import name 'FactCheckerAgent' from 'discernus.agents.fact_checker_agent'`
- Multiple import failures during orchestrator initialization

**Immediate Actions Taken**:
- Fixed `ValidationCache` import to `ValidationCacheManager`
- Updated `FactCheckerAgent` import path to include `.agent` module
- Corrected import statements to match actual module structure

**Forensic Audit Requirements**:
- Map all import chains in the orchestration layer
- Identify circular import dependencies
- Document module dependency graph
- Review module organization and structure

**Refactoring Implications**:
- Need clear module dependency boundaries
- Eliminate circular imports
- Standardize import patterns
- Consider dependency injection for complex dependencies

**Stakeholders**: Developers, system architects, module maintainers

### Method Signature Contract Violations
**Date**: 2025-01-27  
**Priority**: MEDIUM  
**Effort**: 1-2 days  
**Description**: Method signature mismatches between orchestrator and agents indicate broken contracts and tight coupling.

**Current State**:
- `get_hash_by_type` method doesn't exist on `LocalArtifactStorage`
- `evidence_artifacts` parameter conflicts between different method signatures
- Orchestrator calling non-existent methods on storage components

**Root Cause Analysis**:
- **Missing method implementations**: Code references methods that were never implemented
- **Contract drift**: Method signatures changed without updating all callers
- **Interface mismatch**: Components expect different method signatures
- **Tight coupling**: Orchestrator depends on specific storage method implementations

**Impact**:
- Runtime errors during artifact storage operations
- Pipeline breaks when expected methods are missing
- Indicates incomplete implementation or refactoring
- Suggests interface contracts need formalization

**Evidence from Terminal**:
- `'LocalArtifactStorage' object has no attribute 'get_hash_by_type'`
- `SynthesisPromptAssembler.assemble_prompt() got an unexpected keyword argument 'evidence_artifacts'`
- Method signature mismatches during synthesis phase

**Immediate Actions Taken**:
- Replaced `get_hash_by_type` calls with direct registry lookups
- Updated method signatures to match expected parameters
- Fixed parameter conflicts in synthesis assembler

**Forensic Audit Requirements**:
- Map all method signatures between orchestrator and components
- Document expected interfaces and contracts
- Identify all broken method references
- Create interface specification documents

**Refactoring Implications**:
- Need formal interface contracts
- Eliminate tight coupling between components
- Standardize method signatures
- Consider interface abstraction layers

**Stakeholders**: Developers, interface designers, system architects

### Temporary Workspace Management Complexity
**Date**: 2025-01-27  
**Priority**: MEDIUM  
**Effort**: 2-3 days  
**Description**: Complex temporary workspace creation, management, and cleanup indicates orchestrator doing too much file management work.

**Current State**:
- Orchestrator creates `temp_derived_metrics` directories
- Manages file creation, deletion, and cleanup
- Complex temporary file lifecycle management
- Agents dependent on orchestrator's file management decisions

**Root Cause Analysis**:
- **Orchestrator doing too much**: File management should be agent responsibility
- **Complex state management**: Temporary workspace lifecycle is complex and error-prone
- **Tight coupling**: Agents depend on orchestrator's file creation patterns
- **No clear ownership**: Unclear who owns temporary file management

**Impact**:
- Complex error handling for file operations
- Agents fail when expected files don't exist
- Temporary workspace management becomes brittle
- Violates single responsibility principle

**Evidence from Terminal**:
- Complex temporary directory creation and cleanup
- File existence checks throughout the pipeline
- Agents looking for files in orchestrator-managed locations

**Forensic Audit Requirements**:
- Map all temporary workspace management operations
- Document file lifecycle and ownership
- Identify all file dependencies between components
- Create file management responsibility matrix

**Refactoring Implications**:
- Agents should manage their own temporary files
- Orchestrator should not handle file creation details
- Need clear file ownership boundaries
- Consider file management abstraction layer

**Stakeholders**: Developers, system architects, file system maintainers

### Evidence Planning and Integration Failures
**Date**: 2025-01-27  
**Priority**: HIGH  
**Effort**: 2-3 days  
**Description**: Critical failures in evidence planning and integration are breaking the synthesis pipeline, causing reports to lack proper textual evidence support for statistical claims.

**Current State**:
- **Evidence planning failure**: LLM responses not properly formatted as JSON blocks
- **Evidence plan parsing failure**: Regex pattern too strict, causing "No JSON block found in LLM response"
- **Fallback evidence retrieval**: When planning fails, synthesis proceeds without curated evidence
- **Report quality degradation**: Final reports lack proper evidence integration despite having evidence database

**Root Cause Analysis**:
- **LLM response format mismatch**: Evidence retrieval prompt asks for ```json ... ``` format but Gemini 2.5 Flash doesn't consistently return this
- **Overly strict parsing**: Current regex `r'```json\s*([\s\S]*?)\s*```` is too rigid for real LLM responses
- **Prompt complexity**: Evidence retrieval prompt is too verbose and doesn't clearly specify required JSON format
- **Fallback inadequacy**: When evidence planning fails, the fallback provides empty results instead of useful evidence

**Impact**:
- **Research integrity compromised**: Framework designed to link evidence to conclusions - this link is broken
- **Report quality degraded**: Synthesis reports lack textual support for statistical claims
- **User confidence reduced**: Users see warnings about missing evidence, reducing trust in results
- **Pipeline reliability**: Evidence integration phase consistently fails, affecting all experiments

**Evidence from Terminal**:
- `"No JSON block found in LLM response. Could not parse plan."`
- `"Invalid or empty evidence plan provided. Using fallback."`
- `"No curated evidence artifact provided. Synthesis will proceed without curated evidence."`
- Evidence database contains 66 evidence pieces but synthesis can't access them

**Immediate Actions Required**:
1. **Fix JSON parsing regex**: Make pattern more robust to handle various LLM response formats
2. **Simplify evidence retrieval prompt**: Reduce verbosity and add explicit JSON formatting examples
3. **Enhance fallback evidence retrieval**: Provide useful evidence even when planning fails
4. **Add response format validation**: Verify LLM responses before attempting parsing

**Forensic Audit Requirements**:
- Map all evidence planning and integration points in the pipeline
- Document expected LLM response formats and parsing requirements
- Identify all components with evidence integration dependencies
- Create robust evidence retrieval fallback strategies

**Refactoring Implications**:
- Evidence planning should be more resilient to LLM response variations
- Need clear separation between evidence planning and evidence integration
- Fallback mechanisms should provide value, not just error handling
- Consider structured prompting approaches for more reliable LLM responses

**Stakeholders**: Research team, developers, pipeline maintainers, report consumers
