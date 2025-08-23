# Implement Intended THIN Architecture

## Overview
This document outlines the step-by-step plan to refactor the current entangled synthesis approach into the intended THIN architecture where the orchestrator uses the `SynthesisAssembler` to prepare context-rich prompts, then hands them to agents for execution.

## Current State Analysis
- **Problem**: `UnifiedSynthesisAgent` is doing orchestration work (assembling prompts internally)
- **Violation**: Mixing concerns - agent is both building prompts and executing LLM calls
- **Architecture**: Current approach is not THIN - agent has hidden orchestration logic

## Target Architecture
```
Orchestrator → Reads Raw Content → SynthesisAssembler → Raw Content Assembly → UnifiedSynthesisAgent → LLM Call
     ↓              ↓                    ↓                    ↓                    ↓              ↓
  Gathers      Reads files         Assembles raw        Single prompt      Executes      Returns
  Context      as-is               content into         with all data      prompt        Report
              (no parsing)         comprehensive        (no parsing)       (no parsing)
```

**THIN Principle**: Each component does one thing well
- **Orchestrator**: Reads files and passes raw content
- **Assembler**: Concatenates and formats (no parsing logic)  
- **Agent**: Gets complete context and does all interpretation

## Phase 1: Test-Driven Analysis (TDD Foundation)

### Step 1.1: Create Failing Integration Test ✅
**File**: `discernus/tests/test_intended_architecture_integration.py`
**Purpose**: Verify the complete flow works end-to-end
**Test Cases**:
- Orchestrator calls assembler to build prompt
- Assembler produces rich, context-filled prompt
- Agent receives complete prompt and executes
- Final report contains evidence and proper context

**Status**: ✅ **COMPLETE** - Test created and failing as expected
**Result**: Test confirms orchestrator does NOT use assembler (calls agent directly with file paths)
**Next**: Move to Step 1.2 (unit tests for orchestrator)

### Step 1.2: Create Failing Unit Tests for Orchestrator ✅
**File**: `discernus/tests/test_clean_analysis_orchestrator_synthesis_flow.py`
**Purpose**: Test orchestrator's synthesis orchestration logic
**Test Cases**:
- `_run_synthesis` calls `SynthesisPromptAssembler.assemble()`
- Orchestrator passes correct context to assembler
- Orchestrator receives prompt from assembler
- Orchestrator passes complete prompt to agent

**Status**: ✅ **COMPLETE** - 8 comprehensive unit tests created and failing as expected
**Result**: Tests confirm orchestrator does NOT import or use `SynthesisPromptAssembler`
**Next**: Move to Step 1.3 (unit tests for assembler functionality)

### Step 1.3: Create Failing Unit Tests for Assembler ✅
**File**: `discernus/tests/test_synthesis_prompt_assembler.py`
**Purpose**: Test prompt assembly logic in isolation
**Test Cases**:
- `assemble()` method accepts correct parameters
- Method reads and parses framework content
- Method reads and parses experiment content
- Method reads and parses research data artifacts
- Method produces properly formatted prompt
- Method handles missing or malformed data gracefully

**Status**: ✅ **COMPLETE** - 13 comprehensive tests created, 12 passing, 1 failing
**Result**: `SynthesisPromptAssembler` exists and works! **Architectural insight**: Should pass raw content, not parse
**Next**: Move to Step 1.4 (unit tests for agent intended flow)

### Step 1.4: Create Failing Unit Tests for Agent ✅
**File**: `discernus/tests/test_unified_synthesis_agent_intended_flow.py`
**Purpose**: Test agent receives and executes complete prompts
**Test Cases**:
- Agent accepts complete prompt string (not file paths)
- Agent executes prompt without additional assembly
- Agent returns report without modification
- Agent handles prompt execution errors gracefully

**Status**: ✅ **COMPLETE** - 13 comprehensive tests created and failing as expected
**Result**: Agent doesn't accept `complete_prompt` parameter - still uses old interface with file paths
**Next**: **Phase 1 COMPLETE** - Move to Phase 2 (implementation)

## 🎯 Phase 1: Test-Driven Analysis (TDD Foundation) ✅ COMPLETE

**Summary**: Successfully created comprehensive failing tests that identify all architectural gaps
**Results**:
- ✅ **Step 1.1**: Integration test confirms orchestrator doesn't use assembler
- ✅ **Step 1.2**: Orchestrator unit tests confirm missing assembler integration  
- ✅ **Step 1.3**: Assembler unit tests confirm assembler exists but parses content (should pass raw)
- ✅ **Step 1.4**: Agent unit tests confirm agent doesn't accept complete prompts

**Key Insights**:
1. **Orchestrator gap**: Not using `SynthesisPromptAssembler` at all
2. **Assembler gap**: Parsing content instead of passing raw content
3. **Agent gap**: Still using old interface with file paths and artifact hashes

**Next**: **Phase 2** - Implement the intended THIN architecture

## Phase 2: Implement Orchestrator Changes (THIN Principles)

### Step 2.1: Refactor `_run_synthesis` Method
**File**: `discernus/core/clean_analysis_orchestrator.py`
**Changes**:
- Remove direct file path passing to agent
- Add call to `SynthesisPromptAssembler.assemble()`
- Pass assembled prompt to agent
- Ensure proper error handling

**THIN Principle**: Orchestrator orchestrates, doesn't do agent work

### Step 2.2: Update Orchestrator Dependencies
**File**: `discernus/core/clean_analysis_orchestrator.py`
**Changes**:
- Import `SynthesisPromptAssembler`
- Initialize assembler in `__init__` or `_load_specs`
- Ensure assembler has access to artifact storage

**THIN Principle**: Clear dependency injection

### Step 2.3: Implement Context Gathering in Orchestrator
**File**: `discernus/core/clean_analysis_orchestrator.py`
**Changes**:
- Gather framework content (not just path)
- Gather experiment content (not just path)
- Gather research data artifacts
- Pass complete context to assembler

**THIN Principle**: Orchestrator manages data flow

## Phase 3: Implement Assembler Functionality

### Step 3.1: Create/Update `SynthesisPromptAssembler`
**File**: `discernus/core/prompt_assemblers/synthesis_prompt_assembler.py`
**Purpose**: Build rich, context-filled prompts
**Methods**:
- `assemble(framework_content, experiment_content, research_data, evidence_hashes)`
- `_format_framework_context(framework_content)`
- `_format_experiment_context(experiment_content)`
- `_format_research_data(research_data)`
- `_format_evidence_context(evidence_hashes)`

**THIN Principle**: Single responsibility - prompt assembly only

### Step 3.2: Implement Prompt Template Loading
**File**: `discernus/core/prompt_assemblers/synthesis_prompt_assembler.py`
**Changes**:
- Load base prompt from YAML template
- Handle template variable substitution
- Ensure proper error handling for missing templates

**THIN Principle**: Externalized prompts, not hardcoded

### Step 3.3: Implement Context Formatting
**File**: `discernus/core/prompt_assemblers/synthesis_prompt_assembler.py`
**Changes**:
- Parse framework content for key sections
- Extract experiment objectives and hypotheses
- Format statistical results and derived metrics
- Include evidence availability information

**THIN Principle**: Structured, predictable output

## Phase 4: Refactor Agent for THIN Execution

### Step 4.1: Update Agent Method Signature
**File**: `discernus/core/reuse_candidates/unified_synthesis_agent.py`
**Changes**:
- Change `generate_final_report` to accept `complete_prompt: str`
- Remove file path parameters
- Remove internal assembler usage
- Simplify method to pure execution

**THIN Principle**: Agent executes, doesn't orchestrate

### Step 4.2: Remove Internal Prompt Assembly
**File**: `discernus/core/reuse_candidates/unified_synthesis_agent.py`
**Changes**:
- Remove `SynthesisPromptAssembler` import
- Remove `_build_prompt` method
- Remove file reading logic
- Remove context assembly logic

**THIN Principle**: Single responsibility - LLM execution only

### Step 4.3: Implement Pure Execution Logic
**File**: `discernus/core/reuse_candidates/unified_synthesis_agent.py`
**Changes**:
- Accept complete prompt string
- Execute LLM call with prompt
- Return result without modification
- Handle execution errors gracefully

**THIN Principle**: Simple, focused execution

## Phase 5: Integration and Validation

### Step 5.1: Update Integration Tests
**File**: `discernus/tests/test_intended_architecture_integration.py`
**Changes**:
- Mock orchestrator's assembler call
- Verify prompt assembly happens in orchestrator
- Verify agent receives complete prompt
- Verify end-to-end flow works

**TDD Principle**: Tests drive implementation

### Step 5.2: Update Unit Tests
**File**: Multiple test files
**Changes**:
- Update orchestrator tests to verify assembler usage
- Update assembler tests to verify prompt building
- Update agent tests to verify pure execution

**TDD Principle**: Comprehensive test coverage

### Step 5.3: End-to-End Validation
**Command**: `python3 -m discernus.cli run projects/1a_caf_civic_character --skip-validation`
**Purpose**: Verify complete pipeline works with new architecture
**Success Criteria**:
- No errors in synthesis phase
- Rich, evidence-filled report generated
- Proper separation of concerns maintained

## Phase 6: Cleanup and Documentation

### Step 6.1: Remove Dead Code
**Files**: Multiple
**Changes**:
- Remove unused imports
- Remove deprecated methods
- Clean up temporary workarounds

**THIN Principle**: Minimal, focused codebase

### Step 6.2: Update Documentation
**Files**: Multiple
**Changes**:
- Update architecture documentation
- Update agent documentation
- Update orchestrator documentation
- Document new data flow

**THIN Principle**: Clear, maintainable documentation

### Step 6.3: Performance Validation
**Purpose**: Ensure refactoring doesn't degrade performance
**Tests**:
- Measure synthesis time
- Compare report quality
- Verify memory usage

**THIN Principle**: Efficient, not just simple

## Success Criteria

### Functional Requirements
- [ ] Orchestrator uses `SynthesisPromptAssembler` to build prompts
- [ ] Agent receives complete prompts and executes without assembly
- [ ] End-to-end pipeline produces evidence-rich reports
- [ ] No regression in report quality or completeness

### Architectural Requirements
- [ ] Clear separation of concerns maintained
- [ ] Orchestrator orchestrates, assembler assembles, agent executes
- [ ] Externalized prompts in YAML files
- [ ] Proper dependency injection and error handling

### Quality Requirements
- [ ] All tests pass (TDD compliance)
- [ ] No code duplication
- [ ] Clear, maintainable code structure
- [ ] Proper error handling and logging

## Risk Mitigation

### Technical Risks
- **Risk**: Breaking existing functionality during refactoring
- **Mitigation**: Comprehensive test coverage, incremental changes
- **Risk**: Performance degradation from additional method calls
- **Mitigation**: Performance testing, optimization if needed

### Timeline Risks
- **Risk**: Underestimating complexity of prompt assembly
- **Mitigation**: Start with simple cases, iterate
- **Risk**: Integration issues between components
- **Mitigation**: Thorough testing at each phase

## Next Steps

1. **Immediate**: Begin Phase 1 (Test-Driven Analysis)
2. **Week 1**: Complete Phases 1-2 (Foundation and Orchestrator)
3. **Week 2**: Complete Phases 3-4 (Assembler and Agent)
4. **Week 3**: Complete Phases 5-6 (Integration and Cleanup)

## Notes

- **TDD First**: Every feature starts with a failing test
- **THIN Throughout**: Maintain separation of concerns at every step
- **Incremental**: Small, testable changes rather than big-bang refactoring
- **Validation**: End-to-end testing at each major milestone
