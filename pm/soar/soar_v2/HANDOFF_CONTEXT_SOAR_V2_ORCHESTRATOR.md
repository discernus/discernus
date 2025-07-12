# SOAR v2.0 Orchestrator Implementation Handoff

**Date**: January 12, 2025  
**Status**: Framework Context Propagation Issue  
**Priority**: Critical - Core functionality 90% complete  
**Handoff**: For fresh agent to complete final orchestration step

---

## Current State Summary

### ✅ What's Working (Don't Rewrite)

**SOAR 1.0 Infrastructure (Complete)**:
- **ThinOrchestrator** (996 lines): Multi-agent conversation orchestration works perfectly
- **CLI** (22 lines): Path-passing works, loads projects correctly
- **ValidationAgent** (24 lines): Framework-agnostic validation with LLM intelligence
- **Conversation System**: Complete audit trail, session management, Redis pub-sub events
- **Framework Loading**: Successfully loads CFF v3.1 (12K chars) and experiment (16K chars)

**Evidence of Working System**:
```bash
# This command works and creates conversation logs:
soar execute examples/soar_cff_sample_project --dev-mode

# Creates: conversation_20250711_230804_c90a61be.jsonl
# Redis events: soar.validation.started, soar.framework.validated, soar.instructions.generated
```

### ❌ The ONE Critical Issue

**Research Question Extraction Failure**:
- CLI shows: `"research_question": "Research question not found"`
- Should show: `"How do political speeches from different ideological orientations..."`
- This causes moderator_llm to spawn wrong agents and produce generic conversation

**Framework Context Isolation**:
- Framework specification (12K chars) loads successfully in validation
- But framework context never reaches analysis agents
- Agents produce generic analysis instead of CFF-guided analysis

---

## Specific Problem Diagnosis

### 1. Research Question Extraction Bug

**Location**: `soar_cli.py:314-322`

**Current Broken Code**:
```python
# Simple extraction - look for research question
lines = experiment_content.split('\n')
for line in lines:
    if 'research question' in line.lower() and ':' in line:
        research_question = line.split(':', 1)[1].strip()
        break
```

**Problem**: The experiment.md uses section headers `## Research Question` not inline format

**Exact Fix Needed**:
```python
def _extract_research_question(experiment_content: str) -> str:
    """Extract research question from experiment.md markdown"""
    lines = experiment_content.split('\n')
    in_research_section = False
    
    for line in lines:
        line = line.strip()
        
        # Check for research question section header
        if line.lower().startswith('## research question'):
            in_research_section = True
            continue
            
        # If we're in the research section and find a non-empty line
        if in_research_section and line and not line.startswith('#'):
            # Look for primary question
            if line.startswith('**Primary Question**:'):
                return line.split(':', 1)[1].strip()
            # Or just return first substantial line
            return line
            
        # Stop if we hit another section
        if in_research_section and line.startswith('##'):
            break
    
    return "Research question not found"
```

### 2. Framework Context Propagation Issue

**Location**: `discernus/orchestration/orchestrator.py:85-90`

**Current ResearchConfig**:
```python
@dataclass
class ResearchConfig:
    """Minimal research session configuration"""
    research_question: str
    source_texts: str
    enable_code_execution: bool = True
    dev_mode: bool = False
    simulated_researcher_profile: str = "experienced_computational_social_scientist"
```

**Missing Framework Context**:
```python
@dataclass
class ResearchConfig:
    """Research session configuration with framework support"""
    research_question: str
    source_texts: str
    framework_specification: Optional[str] = None  # ADD THIS
    framework_name: Optional[str] = None  # ADD THIS
    enable_code_execution: bool = True
    dev_mode: bool = False
    simulated_researcher_profile: str = "experienced_computational_social_scientist"
```

### 3. ThinOrchestrator Framework Integration

**Location**: `discernus/orchestration/orchestrator.py` (around line 200-300)

**Current Problem**: The ThinOrchestrator spawns agents without framework context

**Solution Strategy**: Enhance agent spawning to include framework context in prompts

**Key Method to Modify**: `_spawn_agent_with_role()` or similar agent creation method

---

## Implementation Tasks (In Order)

### Task 1: Fix Research Question Extraction (15 minutes)
- **File**: `soar_cli.py`
- **Method**: `_extract_research_question()`
- **Test**: Should return "How do political speeches from different ideological orientations..."

### Task 2: Add Framework Context to ResearchConfig (10 minutes)
- **File**: `discernus/orchestration/orchestrator.py`
- **Class**: `ResearchConfig`
- **Test**: Framework specification should be available in config

### Task 3: Enhance CLI to Pass Framework Context (20 minutes)
- **File**: `soar_cli.py`
- **Method**: `_load_project_components()` and execution logic
- **Action**: Load framework specification and pass to ResearchConfig

### Task 4: Modify ThinOrchestrator Agent Spawning (30 minutes)
- **File**: `discernus/orchestration/orchestrator.py`
- **Method**: Agent creation/spawning logic
- **Action**: Include framework context in agent prompts
- **Test**: Analysis agents should receive framework specification

---

## Key Files and Components

### Working Components (Don't Touch):
- `discernus/agents/validation_agent.py` (24 lines) - Works perfectly
- `soar_cli.py` (CLI interface) - Just needs research question fix
- `discernus/core/framework_loader.py` - Framework loading works
- `discernus/orchestration/orchestrator.py` - Orchestration works, just needs framework context

### Test Case:
- `examples/soar_cff_sample_project/` - Complete test case
- Expected: CFF-guided analysis with dimension scores
- Current: Generic conversation about "Citation File Format"

### Redis Events Working:
- `soar.validation.started` ✅
- `soar.framework.validated` ✅  
- `soar.instructions.generated` ✅ (but instructions are null)

---

## Success Criteria

### Immediate Success (Fix Research Question):
```bash
soar execute examples/soar_cff_sample_project --dev-mode
# Should show: "Research Question: How do political speeches from different ideological orientations..."
```

### Complete Success (Framework-Guided Analysis):
- Analysis agents receive CFF v3.1 framework specification
- Results show CFF dimension scores (-1.0 to +1.0 range)
- Evidence citations from political speeches
- No generic conversation about "Citation File Format"

### Validation Test:
- Run: `soar execute examples/soar_cff_sample_project --dev-mode`
- Check conversation log for framework-specific analysis
- Verify agents discuss "social cohesion" and "CFF dimensions"

---

## Minor Issues to Address

### Redis Module Missing:
```bash
pip install redis
```

### Chronolog Capture:
- File `chronolog_capture.py` exists but needs redis module
- Redis events are publishing successfully
- Just need to capture them properly

---

## Architecture Context

### THIN Principles Established:
- CLI just passes paths (22 lines) ✅
- Validation agent uses LLM intelligence (24 lines) ✅
- Framework-agnostic design works with any framework ✅

### Infrastructure Ready:
- Redis pub-sub events working ✅
- Conversation logging working ✅
- Framework loading and validation working ✅
- Multi-agent orchestration working ✅

**The Missing Link**: Framework context needs to reach analysis agents through the existing ThinOrchestrator system.

---

## Next Agent Instructions

1. **Start with Research Question Fix** - Simple 15-minute fix that will show immediate progress
2. **Add Framework Context to ResearchConfig** - 10-minute dataclass enhancement
3. **Enhance CLI Framework Loading** - 20-minute integration
4. **Modify ThinOrchestrator Agent Spawning** - 30-minute core fix

**Total Estimated Time**: 75 minutes to complete framework-guided analysis

**Test Early**: After each fix, run the test case to see progress

**Don't Rewrite**: The orchestration system works. Just add framework context to existing agent spawning.

**Success Indicator**: When `soar execute examples/soar_cff_sample_project` produces CFF dimension scores instead of generic conversation, you've succeeded.

---

## Critical Memory

The user correctly identified that I was trying to rewrite existing working infrastructure. The **ThinOrchestrator system already works** - it creates conversation logs, manages agents, and orchestrates analysis. The issue is **framework context propagation**, not orchestration architecture.

**Focus on the gap, not the system.** 