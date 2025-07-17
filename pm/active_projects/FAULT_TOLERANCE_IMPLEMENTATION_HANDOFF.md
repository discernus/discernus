# Fault Tolerance Implementation Handoff

**Date:** January 13, 2025  
**From:** Analysis Agent (Current)  
**To:** Implementation Agent (Next)  
**Priority:** Critical - Research Progress Blocked

## Executive Summary

**Context:** MVA Experiment 2 revealed critical workflow failures despite successful LLM analysis completion. 46 analyses worth $50+ in API costs were trapped in unusable format due to fault tolerance gaps.

**Mission:** Implement fault-tolerant provenance system and complete end-to-end workflow to prevent LLM data loss and enable researcher access to expensive analyses.

## Work Completed (Current Agent)

### ✅ Analysis & Documentation
1. **Research Provenance Guide v3.0** (`docs/RESEARCH_PROVENANCE_GUIDE_V3.md`)
   - MECE file organization specification
   - Immediate LLM persistence requirements
   - Progressive checkpointing strategy

2. **Provenance System Gap Analysis** (`pm/active_projects/PROVENANCE_SYSTEM_GAP_ANALYSIS.md`)
   - Detailed implementation roadmap with 3-phase approach
   - Specific technical requirements and success criteria
   - Risk assessment and mitigation strategies

3. **Updated Architectural Recovery Plan** (`pm/active_projects/ARCHITECTURAL_RECOVERY_AND_UNIFICATION_PLAN.md`)
   - Realistic status assessment (NOT "one bug away")
   - Prioritized next steps with 3-4 week timeline
   - MVA/experiment_2 as validation target

### ✅ Problem Analysis
- **Root Cause Identified:** DataExtractionAgent crashes with `'str' object has no attribute 'get'` parsing error
- **Impact Quantified:** $50+ in LLM costs lost per failed experiment
- **Success Metrics Defined:** 46 analyses successfully extracted and synthesized

## Technical Implementation Tasks

### Phase 1: Critical Fault Tolerance (Week 1) 🔴

#### 1.1 LLMArchiveManager Implementation
**File:** `discernus/core/llm_archive_manager.py`

```python
class LLMArchiveManager:
    def __init__(self, session_path):
        self.archive_path = session_path / "llm_archive"
        self.archive_path.mkdir(exist_ok=True)
    
    def save_call(self, call_id, prompt, response, metadata):
        """Save LLM call immediately upon response"""
        # Write prompt, response, and metadata to separate files
        # Format: call_001_prompt.txt, call_001_response.txt, call_001_metadata.json
        
    def load_call(self, call_id):
        """Load existing LLM call data"""
        
    def exists(self, call_id):
        """Check if call already exists (prevent duplicate API calls)"""
```

**Integration Points:**
- `discernus/gateway/llm_gateway.py`: Add immediate persistence after LLM response
- `discernus/agents/analysis_agent.py`: Use archive manager instead of memory storage

#### 1.2 CheckpointManager Implementation  
**File:** `discernus/core/checkpoint_manager.py`

```python
class CheckpointManager:
    def __init__(self, session_path):
        self.checkpoint_path = session_path / "system_state"
        
    def save_checkpoint(self, stage, workflow_state):
        """Save progressive state after each workflow stage"""
        # Format: stage_1_analysis_complete.json
        
    def load_checkpoint(self, stage):
        """Load state from specific checkpoint"""
        
    def get_latest_checkpoint(self):
        """Find most recent successful checkpoint"""
        
    def can_resume(self):
        """Check if session can be resumed from checkpoint"""
```

#### 1.3 DataExtractionAgent Bug Fix
**File:** `discernus/agents/data_extraction_agent.py`

**Current Error:** `'str' object has no attribute 'get'`

**Investigation Required:**
- Review MVA Experiment 2 failure logs: `projects/MVA/experiment_2/logs/session_20250717_155122/`
- Check JSON parsing logic in data extraction
- Add robust error handling for malformed LLM responses

**Expected Fix Pattern:**
```python
def extract_json_from_response(self, raw_response):
    try:
        # Current parsing logic (needs debugging)
        parsed = json.loads(raw_response)
        return parsed
    except (json.JSONDecodeError, AttributeError) as e:
        self.logger.error(f"JSON parsing failed: {e}")
        # Fallback to LLM-assisted extraction
        return self._llm_fix_json(raw_response)
```

### Phase 2: Complete Core Workflow (Week 2) 🟡

#### 2.1 CalculationAgent Implementation
**File:** `discernus/agents/calculation_agent.py`

**Purpose:** Execute mathematical calculations from framework `calculation_spec`

**Requirements:**
- Read framework YAML configuration
- Execute formulas on extracted anchor scores
- Output calculated indices (e.g., cohesion_index)
- Handle missing/invalid score data gracefully

#### 2.2 SynthesisAgent Implementation
**File:** `discernus/agents/synthesis_agent.py`

**Purpose:** Generate final human-readable deliverables

**Requirements:**
- Create `final_report.md` with qualitative analysis
- Generate `results.csv` with quantitative data
- Combine analysis summaries, scores, evidence, and calculations
- Format for academic publication standards

#### 2.3 WorkflowOrchestrator Hardening
**File:** `discernus/orchestration/workflow_orchestrator.py`

**Issues:**
- Workflow stops after Step 1 (AnalysisAgent)
- No graceful degradation on agent failures
- No session resumption capability

**Required Changes:**
- Continue execution despite individual agent failures
- Implement checkpoint-based resumption
- Add comprehensive error handling and logging

### Phase 3: Validation & Testing (Week 2-3) 🟢

#### 3.1 End-to-End Workflow Test
**Target:** `projects/MVA/experiment_2/`

**Success Criteria:**
- Resume from existing session with 46 trapped analyses
- Complete DataExtraction without losing existing data
- Execute Calculation and Synthesis agents
- Produce final deliverables: `final_report.md`, `results.csv`
- Verify hypothesis testing results match our manual analysis

#### 3.2 Cost Protection Validation
**Test Scenarios:**
- Crash after AnalysisAgent → Resume without duplicate LLM calls
- Crash after DataExtraction → Resume from checkpoint
- Crash after Calculation → Resume and complete Synthesis

**Success Metrics:**
- Zero duplicate LLM API calls during resumption
- Complete data recovery from any checkpoint
- Session resumption within 30 seconds

## Key Technical Constraints

### 1. Preserve Existing Data
- **DO NOT** re-run the 46 MVA analyses (expensive!)
- **DO** extract them from existing session files
- **DO** maintain backward compatibility with current session format

### 2. THIN Philosophy Compliance
- **LLMArchiveManager:** Pure utility, no intelligence
- **CheckpointManager:** Simple state persistence, no logic
- **Agent fixes:** Minimal changes, maximum reliability

### 3. Academic Integrity
- **All changes must be logged** in project chronolog
- **Maintain tamper-evident audit trail**
- **Preserve forensic model provenance**

## Files to Modify

### Core Implementation:
- `discernus/core/llm_archive_manager.py` (NEW)
- `discernus/core/checkpoint_manager.py` (NEW)
- `discernus/agents/data_extraction_agent.py` (FIX)
- `discernus/agents/calculation_agent.py` (NEW)
- `discernus/agents/synthesis_agent.py` (NEW)

### Integration Points:
- `discernus/gateway/llm_gateway.py` (MODIFY)
- `discernus/orchestration/workflow_orchestrator.py` (MODIFY)
- `discernus/agents/analysis_agent.py` (MODIFY)

### Test Target:
- `projects/MVA/experiment_2/` (VALIDATE)

## Success Definition

**Phase 1 Complete When:**
- ✅ MVA Experiment 2 session can be resumed without re-running LLM calls
- ✅ DataExtractionAgent processes 46 existing analyses without crashing
- ✅ Zero duplicate API calls during recovery

**Phase 2 Complete When:**
- ✅ Complete end-to-end workflow produces final deliverables
- ✅ `final_report.md` and `results.csv` generated from MVA data
- ✅ Hypothesis testing results match manual analysis

**Project Complete When:**
- ✅ `pdaf_retest` project executes successfully end-to-end
- ✅ Cost protection verified across all workflow stages
- ✅ Academic integrity compliance maintained

## Emergency Contacts

**If Stuck:**
- Review `docs/RESEARCH_PROVENANCE_GUIDE_V3.md` for architecture guidance
- Check `pm/active_projects/PROVENANCE_SYSTEM_GAP_ANALYSIS.md` for detailed specs
- Examine MVA Experiment 2 session logs for actual failure patterns

**Critical Success Factor:**
**DO NOT** lose the existing 46 LLM analyses - they represent significant research investment and must be preserved and made accessible.

---

**Ready for Implementation Agent Handoff** 