# 📋 **Complete Post-Partum Recovery Plan: MVA System Architecture Overhaul**

**Date**: 2025-01-17  
**Status**: Ready for Implementation  
**Priority**: Critical Path to Production Readiness  

## 🎯 **Executive Summary**

Transform the MVA system from "infantile but alive" to production-ready by addressing all architectural gaps identified in the post-partum analysis. This plan addresses both immediate needs (completing MVA Experiment 3) and long-term architectural improvements for fault tolerance, performance, and academic reproducibility.

---

## ✅ **COMPLETED ITEMS (For Posterity)**

### **Fault Tolerance Foundation**
- **LiteLLM Cost Tracking**: Response cost capture from `response._hidden_params["response_cost"]`
  - File: `discernus/gateway/llm_gateway.py` (lines 200-220)
  - Status: ✅ IMPLEMENTED - costs tracked and stored in archive metadata
- **DataExtractionAgent Schema Transformation**: LLM-to-LLM schema flattening with fallback logic
  - File: `discernus/agents/data_extraction_agent.py` (lines 248-424)  
  - Status: ✅ IMPLEMENTED - handles both hierarchical and flat JSON formats
- **CalculationAgent Bug Fix**: API standardization to `success`/`json_output`/`error` format
  - File: `discernus/agents/calculation_agent.py`
  - Status: ✅ IMPLEMENTED - consistent API across all agents
- **SynthesisAgent Enhancement**: Fixed via upstream data improvements
  - Status: ✅ IMPLEMENTED - receives clean data from DataExtractionAgent
- **Zero Data Loss Protection**: LLM Archive Manager provides tamper-evident storage
  - Files: `discernus/core/llm_archive_manager.py`
  - Status: ✅ IMPLEMENTED - all LLM interactions safely archived

### **Documentation & Guidelines**
- **Framework Development Guide**: Critical schema requirements documented
  - File: `docs/guides/FRAMEWORK_DEVELOPMENT_GUIDE.md` (section 2.4)
  - Status: ✅ IMPLEMENTED - emphasizes output_contract.schema importance
- **Test Coverage Gap Analysis**: Root cause analysis of missed schema issues
  - File: `pm/active_projects/TEST_COVERAGE_GAP_ANALYSIS.md`
  - Status: ✅ IMPLEMENTED - comprehensive analysis of test-reality mismatch

---

## 🚨 **PHASE 1: IMMEDIATE RESUMPTION (Complete Experiment 3)**

**Priority**: **CRITICAL** - Complete the experiment  
**Timeline**: 2-3 hours  
**Owner**: Next agent  
**Dependencies**: None (uses existing fixed agents)

### **Critical Insight: Fault Tolerance Sweet Spot**
The DataExtractionAgent failed while processing exactly this data:
- **Source**: `projects/MVA/experiments/experiment_3/results/2025-07-17_21-59-15/state_after_step_1_AnalysisAgent.json`
- **Content**: 94 markdown-formatted CFF analyses in `analysis_results` object
- **Format**: Rich markdown with embedded scores like `* **Tribal Dominance: 0.1 / 1.0**`

### **Implementation Tasks**

#### **1.1 Create State-Based Resumption Script**
```python
# File: resume_experiment_3.py
import json
from pathlib import Path
from discernus.agents.data_extraction_agent import DataExtractionAgent
from discernus.agents.calculation_agent import CalculationAgent
from discernus.agents.synthesis_agent import SynthesisAgent
from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import get_model_registry

def resume_experiment_3():
    # Load exact state where failure occurred
    state_file = "projects/MVA/experiments/experiment_3/results/2025-07-17_21-59-15/state_after_step_1_AnalysisAgent.json"
    with open(state_file, 'r') as f:
        state = json.load(f)
    
    # Resume from step 2 with our fixed agents
    model_registry = get_model_registry()
    gateway = LLMGateway(model_registry)
    
    # Step 2: Data Extraction
    data_extraction_agent = DataExtractionAgent(gateway)
    extraction_result = data_extraction_agent.execute(state, {})
    
    # Step 3: Calculation
    calculation_agent = CalculationAgent(gateway)
    calculation_result = calculation_agent.execute(extraction_result, {})
    
    # Step 4: Synthesis
    synthesis_agent = SynthesisAgent(gateway)
    final_result = synthesis_agent.execute(calculation_result, {})
    
    return final_result
```

#### **1.2 Validation & Testing**
- **Test Schema Transformation**: Verify LLM-to-LLM transformation works on markdown content
- **Test Field Name Generation**: Confirm CFF-compatible field names (`tribal_dominance_score`, etc.)
- **Test Calculation Logic**: Verify cohesion indices calculate correctly using framework's `calculation_spec`
- **Test Complete Workflow**: Steps 2-4 complete successfully with meaningful results

#### **1.3 Success Criteria**
- ✅ MVA Experiment 3 produces complete CSV with correct CFF field names
- ✅ Cohesion indices calculate correctly (descriptive_cohesion_index, etc.)
- ✅ Academic-quality final report generated
- ✅ All 94 analysis results properly processed

---

## 🏗️ **PHASE 2: INCREMENTAL STATE PERSISTENCE (Critical Architectural Fix)**

**Priority**: **HIGH** - Fix fault tolerance gap  
**Timeline**: 1-2 days  
**Owner**: Next agent  
**Dependencies**: Phase 1 completion

### **Critical Problem Identified**
> "State_after_step json file did not arrive until Step 1 was completed. That makes it risky to rely on generally, IMHO... if these step_after json files are critical path, we need to make them fault tolerant."

### **The Fault Tolerance Paradox**
- **✅ Individual LLM Calls**: Written to disk immediately (fault tolerant)
- **❌ Workflow State**: Only written at step completion (NOT fault tolerant)

**Current Risk:**
```
Step 1: 47 LLM calls over 30 minutes
├── Call 1-46: ✅ Safely on disk  
├── **CRASH at Call 47** 💥
└── Result: ❌ 29 minutes of work LOST (no state file exists)
```

### **Incremental State Architecture**

#### **2.1 Enhance WorkflowOrchestrator**
**File**: `discernus/orchestration/workflow_orchestrator.py`

```python
def _update_incremental_state(self, workflow_state, step_num, call_num):
    """Update state file after each successful LLM call"""
    state_file = self.session_path / f"state_step_{step_num}_partial.json"
    
    # Atomic write (write to .tmp, then rename)
    temp_file = state_file.with_suffix('.tmp')
    with open(temp_file, 'w') as f:
        json.dump(workflow_state, f, indent=2)
    temp_file.rename(state_file)
    
    # Update call counter
    workflow_state['_incremental_state'] = {
        'step_num': step_num,
        'last_completed_call': call_num,
        'timestamp': datetime.utcnow().isoformat()
    }
```

#### **2.2 State File Management Pattern**
- **During Step**: `state_step_N_partial.json` (updated after each LLM call)
- **Step Complete**: `state_after_step_N.json` (final state)
- **Crash Recovery**: Load from latest `state_step_N_partial.json`

#### **2.3 Resumption Logic**
```python
def resume_from_partial_state(partial_state_file):
    """Resume workflow from incremental state file"""
    state = load_json(partial_state_file)
    last_completed_call = state['_incremental_state']['last_completed_call']
    
    # Resume from next call
    return resume_from_call(last_completed_call + 1)
```

#### **2.4 CLI Integration**
```bash
# Resume from partial state
discernus_cli.py resume --from-partial-state "state_step_1_partial.json"

# Resume from specific call number
discernus_cli.py resume --from-call 47 --state-file "state_step_1_partial.json"
```

### **Success Criteria**
- ✅ System never loses more than 1 LLM call's worth of work
- ✅ Resume from exact failure point
- ✅ State files written incrementally during execution
- ✅ Atomic write operations prevent corruption

---

## 📊 **PHASE 3: TEST COVERAGE GAP REMEDIATION**

**Priority**: **HIGH** - Prevent future failures  
**Timeline**: 2-3 days  
**Owner**: Next agent  
**Dependencies**: Phase 2 completion

### **Root Cause Analysis**
**Source**: `pm/active_projects/TEST_COVERAGE_GAP_ANALYSIS.md`

**The Critical Discovery**: Our test suite completely missed the schema transformation issues that caused MVA Experiment 3 to catastrophically fail.

### **Test-Reality Mismatch Problem**

#### **What Tests Were Testing (IDEALIZED)**
```json
// Test prompt constrains LLM to produce flat JSON:
"Return JSON: {\"worldview\": \"Progressive\", \"scores\": {\"identity\": 0.5}}"
```

#### **What Production Actually Produces (REALISTIC)**
```json
// Real LLM produces complex hierarchical structures:
{
  "Political Worldview Classification": {
    "Worldview": "Progressive"
  },
  "Cohesive Flourishing Framework v4.1 Analysis": {
    "Identity Axis": {
      "Tribal Dominance": {"Score": 0.1, "Confidence": 0.8}
    }
  }
}
```

### **Implementation Tasks**

#### **3.1 Realistic Test Data Generation**
**File**: `discernus/tests/realistic_test_data_generator.py`

```python
def generate_realistic_llm_responses():
    """Generate test responses that match actual LLM behavior"""
    # Use actual LLM calls with constrained prompts
    # Capture real hierarchical structures
    # Save as test fixtures for consistent testing
```

#### **3.2 Schema Transformation Test Suite**
**File**: `discernus/tests/schema_transformation_tests.py`

```python
def test_hierarchical_json_transformation():
    """Test transformation with real hierarchical JSON structures"""
    # Test CFF v4.1 hierarchical patterns
    # Test Claude/GPT/Mistral different nesting patterns
    # Test framework-agnostic transformation
```

#### **3.3 End-to-End Integration Tests**
**File**: `discernus/tests/end_to_end_workflow_tests.py`

```python
def test_complete_workflow_with_realistic_data():
    """Test full workflow with realistic LLM responses"""
    # Use real LLM responses from test fixtures
    # Test complete 4-step workflow
    # Verify CSV output matches framework expectations
```

### **Success Criteria**
- ✅ Tests use realistic LLM response patterns
- ✅ Schema transformation tested with actual hierarchical structures
- ✅ End-to-end workflow validated with real data
- ✅ Framework-agnostic testing (CFF, PDAF, custom frameworks)

---

## ⚡ **PHASE 4: PERFORMANCE & INFRASTRUCTURE UPGRADES**

**Priority**: **MEDIUM** - Optimize for production use  
**Timeline**: 3-4 days  
**Owner**: Next agent  
**Dependencies**: Phase 3 completion

### **4.1 LiteLLM Proxy Integration**
**Problem**: Currently pounding Vertex AI with basic retry logic
**Solution**: Free, open-source LiteLLM proxy with sophisticated traffic management

#### **Current Architecture (RISKY)**
```python
# Direct SDK calls - no rate limiting
response = litellm.completion(model="vertex_ai/gemini-2.5-pro", ...)
```

#### **Target Architecture (ROBUST)**
```python
# Proxy-based calls with automatic rate limiting
response = litellm.completion(
    model="vertex_ai/gemini-2.5-pro", 
    api_base="http://localhost:4000",  # LiteLLM proxy
    ...
)
```

#### **Implementation Tasks**
- **Setup LiteLLM Proxy**: Docker container with rate limiting configuration
- **Update LLMGateway**: Route all calls through proxy instead of direct SDK
- **Configuration**: RPM/TPM limits, cost budgets, fallback models
- **Files**: `discernus/gateway/llm_gateway.py`, `docker-compose.yml`

### **4.2 Parallel Processing Architecture**
**Problem**: Sequential processing - no parallelization
**Files**: `discernus/orchestration/workflow_orchestrator.py`

#### **Current Issues**
- No parallel LLM calls within agents
- No parallel data extraction while analysis runs
- No progressive CSV writing
- Memory accumulation during long runs

#### **Target Architecture**
```python
# Parallel LLM calls within agents
async def process_corpus_parallel(self, corpus_files):
    tasks = [self.analyze_text(file) for file in corpus_files]
    results = await asyncio.gather(*tasks)
    return results

# Progressive CSV writing
def append_result_to_csv(self, result, csv_file):
    # Append each result as it completes
    # No memory accumulation
```

### **4.3 Real-Time Logging & Monitoring**
**Problem**: Multiple logging issues identified

#### **4.3.1 Session Run Log Buffering**
**File**: `discernus/core/session_logger.py`
**Problem**: Logs accumulate in memory, written only at end
**Solution**: Immediate append-only logging (<500ms persistence)

#### **4.3.2 Human-Readable Log Truncation**
**File**: `projects/MVA/experiments/experiment_3/logs/session_20250717_215915/session_20250717_215915_human.md`
**Problem**: Shows analysis start but cuts off scores ("72b9..." truncation)
**Solution**: Full CFF anchor scores, confidence values, evidence quotes

#### **4.3.3 Conversation Log Mislabeling**
**File**: `projects/MVA/experiments/experiment_3/conversations/conversation_20250717_215915_2efa762b.jsonl`
**Problem**: Just workflow step tracking, NOT actual conversation content
**Solution**: Capture actual LLM prompts, responses, and analysis content

### **Success Criteria**
- ✅ 10x performance improvement via parallelization
- ✅ Automatic rate limiting and cost management
- ✅ Real-time logging with <500ms persistence
- ✅ Human-readable logs show actual analysis scores

---

## 📁 **PHASE 5: PROVENANCE & ACADEMIC COMPLIANCE**

**Priority**: **MEDIUM** - Academic reproducibility  
**Timeline**: 2-3 days  
**Owner**: Next agent  
**Dependencies**: Phase 4 completion

### **5.1 Directory Structure Standardization**
**Problem**: "project/experiments/experiment/ and then everything is chaotic after that"
**Current**: Multiple dated folders for single runs

#### **Current Structure (CHAOTIC)**
```
projects/MVA/experiments/experiment_3/results/
├── 2025-07-17_21-59-14/     # Why two folders?
├── 2025-07-17_21-59-15/     # For single run?
└── [scattered files]
```

#### **Target Structure (ORGANIZED)**
```
projects/MVA/experiments/experiment_3/sessions/
└── session_20250717_215915/
    ├── state_files/
    ├── llm_archive/
    ├── results/
    ├── logs/
    └── conversations/
```

### **5.2 LLM Version Tracking**
**Problem**: Only records `vertex_ai/gemini-2.5-pro` - no version numbers or dates
**Files**: LLM archive metadata, provenance records

#### **Current (INADEQUATE)**
```json
{"model": "vertex_ai/gemini-2.5-pro"}
```

#### **Target (REPRODUCIBLE)**
```json
{
  "model": "vertex_ai/gemini-2.5-pro",
  "version_hash": "gemini-2.5-pro-20250115",
  "training_cutoff": "2024-10-15",
  "api_version": "v1beta",
  "safety_settings": {...},
  "generation_config": {...}
}
```

### **5.3 Statistical Plan Clarification**
**Problem**: Experiment has `# DEPRECATED: statistical_plan` but calculations still needed
**Files**: `projects/MVA/experiments/experiment_3/experiment_snapshot.md`

#### **Resolution Strategy**
- **Framework-driven calculations**: Use `calculation_spec` from framework
- **Clear deprecation guidance**: Document what replaces statistical_plan
- **Calculation transparency**: Show formula source in results

### **Success Criteria**
- ✅ Clean project/experiment/session directory structure
- ✅ Complete LLM version tracking for reproducibility
- ✅ Clear statistical calculation methodology
- ✅ Academic-grade provenance documentation

---

## 🔧 **PHASE 6: SCHEMA TRANSFORMATION REFORM (THIN-ify)**

**Priority**: **LOW** - Architectural purity  
**Timeline**: 1-2 days  
**Owner**: Next agent  
**Dependencies**: Phase 5 completion

### **Critical Issue: Current Approach is THICK**
**Problem**: Hardcoded CFF knowledge violates THIN principles
**File**: `discernus/agents/data_extraction_agent.py`

#### **Current THICK Pattern**
```python
# This is hardcoded knowledge about CFF structure - THICK!
["Cohesive Flourishing Framework v4.1 Analysis", "Identity Axis", "Tribal Dominance"]
```

#### **What Happens with Claude/GPT/Mistral?**
- Different nesting patterns
- Different field names
- Different hierarchical structures
- → **Parsing errors as predicted**

### **THIN Alternative Implementation**

#### **6.1 Pure LLM-to-LLM Transformation**
```python
def _llm_flatten_json(self, hierarchical_json, framework_schema):
    """Use LLM to flatten JSON in framework-agnostic way"""
    prompt = f"""
    Transform this hierarchical JSON to flat format.
    Target schema: {framework_schema}
    Input: {hierarchical_json}
    Output flat JSON with exact field names from schema.
    """
    return llm_gateway.call_model("vertex_ai/gemini-2.5-flash", prompt)
```

#### **6.2 Framework-Driven Schema Specification**
```python
def _get_target_schema(self, framework_spec):
    """Extract target field names from framework output_contract"""
    return framework_spec.get('output_contract', {}).get('schema', {})
```

### **Success Criteria**
- ✅ Zero hardcoded framework knowledge
- ✅ Pure LLM-to-LLM transformation
- ✅ Claude/GPT/Mistral compatibility
- ✅ Framework-agnostic architecture

---

## 🎯 **IMPLEMENTATION PRIORITY MATRIX**

| Phase | Priority | Timeline | Blocking | Impact |
|-------|----------|----------|----------|---------|
| **Phase 1** | CRITICAL | 2-3 hours | None | Complete Experiment 3 |
| **Phase 2** | HIGH | 1-2 days | Phase 1 | Fix fault tolerance gap |
| **Phase 3** | HIGH | 2-3 days | Phase 2 | Prevent future failures |
| **Phase 4** | MEDIUM | 3-4 days | Phase 3 | Production performance |
| **Phase 5** | MEDIUM | 2-3 days | Phase 4 | Academic compliance |
| **Phase 6** | LOW | 1-2 days | Phase 5 | Architectural purity |

## 📋 **HANDOFF CHECKLIST**

### **For Next Agent - Phase 1 Implementation**
- [ ] Review state file: `projects/MVA/experiments/experiment_3/results/2025-07-17_21-59-15/state_after_step_1_AnalysisAgent.json`
- [ ] Test DataExtractionAgent with markdown content
- [ ] Verify schema transformation produces CFF-compatible field names
- [ ] Create `resume_experiment_3.py` script
- [ ] Execute steps 2-4 of workflow
- [ ] Validate final CSV and cohesion calculations

### **Key Files to Understand**
- `discernus/agents/data_extraction_agent.py` - Fixed schema transformation
- `discernus/agents/calculation_agent.py` - Cohesion index calculations
- `discernus/orchestration/workflow_orchestrator.py` - Workflow execution
- `projects/MVA/experiments/experiment_3/framework_snapshot.md` - CFF framework spec

### **Success Metrics**
- **Immediate**: MVA Experiment 3 completes with valid results
- **Medium-term**: System fault tolerance prevents data loss
- **Long-term**: Production-ready academic research platform

---

**Ready for immediate implementation. All architectural analysis complete.** 