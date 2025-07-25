# Implementation Plan V4: Radical Simplification - Technical Specification

**Date**: July 24, 2025  
**Status**: Active Implementation Plan - Architect Reviewed  
**Context**: Complete technical specification with all contracts defined

---

## 1. STRATEGIC CONTEXT

### Problem Statement
- Phase 3 orchestration debugging revealed coordination complexity crisis
- Monolithic OrchestratorAgent violates THIN principles (~524 lines)
- Production logic embedded in test runners creates hidden dependencies
- Fragmented logging systems provide poor development visibility

### Solution Approach
**Radical Simplification**: Constrain coordination to single, bulletproof 5-stage pipeline
- **Core Thesis**: Reliability > Flexibility for early-stage products
- **Strategy**: Eliminate coordination complexity through workflow standardization
- **Architecture**: THIN-compliant components with strict input contracts

### Success Criteria
- Working end-to-end pipeline (PreTest → BatchAnalysis → Synthesis → Review → Moderation)
- THIN-compliant architecture (components <150 lines)
- Production-ready input validation
- System handles arbitrary valid experiments

---

## 2. CURRENT STATUS ASSESSMENT

### Infrastructure Completed ✅
- **Redis Coordination**: Architect-specified keys/lists pattern implemented
- **Router Upgrade**: ThreadPoolExecutor replaces subprocess.Popen
- **Pipeline Structure**: Hardcoded STAGES array prevents coordination variations
- **Model Standardization**: Gemini 2.5 Pro standardized (Flash hung on CHF on 2025-07-24)

### Pipeline Status
- **Stage 1 (PreTest)**: ✅ Functional and validated - produces statistical variance analysis
- **Stage 2 (BatchAnalysis)**: ✅ Functional and validated - produces structured academic analysis
- **Stage 3 (CorpusSynthesis)**: ❌ Placeholder implementation only
- **Stage 4 (Review)**: ❌ Returns `["placeholder-review-task"]`
- **Stage 5 (Moderation)**: ❌ Returns `"placeholder-moderation-task"`

---

## 3. TECHNICAL SPECIFICATIONS

### 3.1 Model Configuration
- **Primary Model**: `vertex_ai/gemini-2.5-pro` (Flash reliability failure on CHF complexity test, 2025-07-24)
- **All References Updated**: No gemini-2.5-flash references remain in system
- **Rationale**: Reliability > cost optimization for academic research integrity

### 3.2 Agent Registry
**Location**: `agents/<AgentName>/config.json`

**Schema**:
```json
{
  "agent_name": "AnalyseBatchAgent",
  "task_types": ["analyse_batch"],
  "concurrency": 2,
  "version": "1.0.0"
}
```

**Discovery**: Router loads all `agents/*/config.json` files at startup for task routing

### 3.3 PreTest Agent Contract
**Output Schema**:
```json
{
  "recommended_runs_per_batch": 3,
  "token_estimate_per_doc": 2450,
  "variance_index": 0.17
}
```

**BatchPlanner Rules**:
- `recommended_runs_per_batch`: Clamped to min=1, max=10
- Used by Orchestrator to generate identical statistical runs
- Changes invalidate existing batch cache artifacts

### 3.4 Cache Semantics
**Cache Key Definition**:
```
cache_key = sha256(sorted(doc_hashes) + sorted(framework_hashes) + prompt_hash + run_index)
```

**Invalidation Rules**:
- PreTest changes to `recommended_runs_per_batch` → invalidate all dependent batch artifacts
- Framework hash changes → invalidate all dependent artifacts
- Corpus changes → invalidate all dependent artifacts

**Storage**: Redis with 24-hour expiration (`EX 86400`)

### 3.5 Failure/Timeout Policy
**BRPOP Timeout Behavior** (300 seconds):
- On timeout → set `run_status = ERROR_TIMEOUT`
- Export partial manifest with completed stages
- No automatic retries
- User can resume from last completed stage

**ThreadPoolExecutor Configuration**:
- `max_workers = min(available_models_concurrency, 4)`
- Per-future timeout: 15 minutes
- Prevents thread starvation on LLM call blocks

### 3.6 Output Specifications

#### Review/Moderation Dual Output
**HTML Transcript**: `debate/<RUN>.html` (human-readable conversation)

**Machine-Readable JSON**: `debate/<RUN>.json`
```json
{
  "claims": [
    {
      "id": "C1",
      "text": "Constitutional health shows degradation in populist rhetoric",
      "supporting_batches": ["B01", "B03"]
    }
  ],
  "final_synthesis": "Comprehensive analysis reveals...",
  "criticisms": [
    {
      "reviewer_type": "ideological",
      "critique": "Analysis may underweight progressive constitutional interpretations"
    }
  ]
}
```

### 3.7 Metrics Definitions
| Field | Definition | Source |
|-------|------------|--------|
| `mean_stage_latency` | `sum(stage_durations_ms) / stage_count` | Orchestrator logs |
| `cost_usd` | `Σ(input_tokens × input_price + output_tokens × output_price)` | LiteLLM logs |
| `cache_hit_ratio` | `skipped_batches / total_batches` on rerun | Cache status checks |
| `run_success` | Boolean completion status | Pipeline execution |

### 3.8 Experiment Specification v3
**Framework Identification** (hash-enforced):
```yaml
name: "phase3_chf_constitutional_debate"
description: "A standard constitutional health analysis."
research_question: "How do speakers approach constitutional issues?"
frameworks:
  - id: CAF_v4.3.md
    sha256: a1b2c3d4e5f6...
  - id: CHF_v1.1.md
    sha256: f6e5d4c3b2a1...
corpus_path: "projects/experiment/corpus/"
statistical_runs: 3  # optional override
```

**Validation**: Bouncer rejects missing or invalid sha256 hashes

### 3.9 Security Controls

#### Enabled Now
- **Hash Pinning**: All framework/corpus artifacts validated by SHA-256
- **Secrets Scanning**: CLI rejects files matching `/.env($|[._-])/` patterns
- **Path Validation**: Corpus paths restricted to project boundaries

#### Deferred (Post-Production)
- **Sandboxing**: Agent containers with `--network none`
- **Sentinel Agent**: Advanced prompt injection detection
- **Audit Logging**: Comprehensive security event logging

---

## 4. IMPLEMENTATION SEQUENCE

### Phase A: Complete Functional Pipeline (IMMEDIATE - 3-5 days)

#### **A1: Update Technical Contracts (Day 1)**
1. **Replace Flash References**: Update all model registry entries to `gemini-2.5-pro`
2. **Agent Discovery (Staged)**: Keep hardcoded `AGENT_SCRIPTS` mapping for reliability during pipeline completion (migrate to config.json discovery in Phase B)
3. **Define PreTest Schema**: Implement structured output validation
4. **Implement Cache Key Logic**: SHA-256 based cache key generation
5. **Add Timeout Handling**: ERROR_TIMEOUT status with partial manifest export

#### **A2: Implement Stage 3 - CorpusSynthesisAgent (Day 2)**
- Statistical aggregation of batch results using pandas/numpy
- Deterministic calculations with audit trail
- JSON output with comprehensive statistical summaries

#### **A3: Implement Stage 4 - ReviewerAgent (Day 3)**
- Adversarial critique from ideological/statistical perspectives
- Dual output: HTML transcript + structured JSON
- Implement claims extraction and batch reference tracking

#### **A4: Implement Stage 5 - ModeratorAgent (Day 4)**
- Conversation orchestration between reviewers
- Final synthesis with supporting evidence
- Dual output: `debate/<RUN>.html` + `debate/<RUN>.json`

#### **A5: End-to-End Validation (Day 5)**
- Complete pipeline test with CHF framework
- Validate all output artifacts conform to specifications
- Confirm metrics collection accuracy

**Success Criteria**: Complete experiment runs with all specified artifacts generated

---

### Phase B: Architectural Refactoring (1 week)

**Goal**: THIN-compliant, maintainable architecture

#### **B1: Extract Production Logic (Days 1-2)**
Create `discernus/core/experiment_manager.py` (~150 lines):
```python
class ExperimentManager:
    def create_framework_artifact(self, framework_content: str) -> str
    def create_corpus_artifacts(self, corpus_dir: Path) -> List[str]
    def format_orchestration_request(self, experiment: Dict) -> Dict
    def validate_experiment_structure(self, experiment: Dict) -> bool
```

#### **B2: Decompose OrchestratorAgent (Days 3-4)**
Split monolithic agent into focused components:
- `discernus/agents/orchestrator_agent.py` (~100 lines): Basic coordination only
- `discernus/core/batch_planner.py` (~100 lines): Statistical run calculation
- `discernus/core/task_factory.py` (~100 lines): Task data construction
- **Migrate Agent Discovery**: Replace hardcoded `AGENT_SCRIPTS` with `agents/*/config.json` scanning (~50 lines)

#### **B3: Implement Development Logging (Day 5)**
Create `scripts/dev_monitor.py` (~50 lines):
- Real-time task queue status
- Agent execution progress
- Error alerts with context
- Cost tracking per experiment

#### **B4: Regression Testing (Days 6-7)**
- Validate all existing functionality preserved
- Test with multiple framework types
- Confirm THIN compliance (all components <150 lines)

**Success Criteria**: Same functionality with clean, maintainable architecture

---

### Phase C: Input Specification Hardening (3-5 days)

**Goal**: Production-ready input validation with strict contracts

#### **C1: Create v3/v5 Specifications (Days 1-2)**
- Remove all flexible/ambiguous fields
- Add explicit constraints and complexity limits
- Enforce hash-based framework identification
- Implement manifest-based corpus specification

#### **C2: Implement "Bouncer and Concierge" Validation (Days 2-3)**
1. **Bouncer**: Pydantic-based deterministic validation
2. **Concierge**: LLM-powered error explanation
3. **Legacy Handling**: `ERR_LEGACY_SPEC` with upgrade suggestions

#### **C3: Remove Flexible Fields (Day 4)**
- Eliminate `custom_workflow`, `parallel_processing` options
- Add explicit constraints (`max_documents`, `max_frameworks_per_run`)
- Standardize on declarative format only

#### **C4: Validation Testing (Day 5)**
- Test specification compliance enforcement
- Validate helpful error messages
- Confirm graceful rejection of invalid inputs

**Success Criteria**: System accepts only specification-compliant inputs with helpful feedback

---

### Phase D: Production Validation (2-3 days)

**Goal**: Real-world readiness with arbitrary valid inputs

#### **D1: New Framework Testing (Day 1)**
- Test with frameworks not in test runners
- Validate framework-agnostic behavior
- Confirm output contract enforcement

#### **D2: Arbitrary Experiment Testing (Day 2)**
- Test with user-created experiments
- Validate corpus handling with various formats
- Confirm end-to-end reliability

#### **D3: Performance & Cost Validation (Day 3)**
- Measure and document performance metrics
- Validate cost calculations accuracy
- Confirm cache hit ratios on re-runs

**Success Criteria**: System reliably handles any specification-compliant input

---

## 5. DEPRECATED COMPONENTS

### Legacy PoC Architecture (Archived)
- **AnalyseChunkAgent**: Replaced by AnalyseBatchAgent for statistical batching
- **Dynamic Orchestration**: Replaced by hardcoded 5-stage pipeline
- **Consumer Group Pattern**: Replaced by keys/lists coordination

**Note**: Legacy components remain in git history but are not part of active system

---

## 6. ARCHITECTURAL REQUIREMENTS

### 6.1 Environment Portability (CRITICAL)

**Requirement**: All Python execution must be environment-agnostic

**Implementation Pattern**:
```python
import sys
PYTHON_EXECUTABLE = sys.executable

# Use in subprocess calls
subprocess.run([PYTHON_EXECUTABLE, 'script.py'])

# Use in agent mappings
AGENT_SCRIPTS = {
    'agent_type': [PYTHON_EXECUTABLE, 'path/to/agent.py']
}
```

**Prohibited Patterns**:
- ❌ `'python3'` - May not be available or wrong version
- ❌ `'venv/bin/python3'` - Platform-specific path
- ❌ `'/usr/bin/python3'` - Hardcoded system paths
- ❌ `'python'` - Ambiguous version

**Rationale**: Hardcoded environment paths cause coordination failures when:
- Developers use different virtual environment managers (venv, conda, pipenv)
- System runs on different platforms (macOS, Linux, Windows)
- Python installation paths vary between systems

**Enforcement**: This pattern is documented in `ARCHITECTURE_QUICK_REFERENCE.md` and should be verified during code review.

---

## 7. RISK MITIGATION

### **High Risk: Stage Implementation Complexity**
- **Mitigation**: Start with simple, working implementations
- **Fallback**: Placeholder implementations if LLM integration fails

### **Medium Risk: Architectural Refactoring Regression**
- **Mitigation**: Comprehensive regression testing after each extraction
- **Fallback**: Git rollback to working state

### **Low Risk: Input Specification Adoption**
- **Mitigation**: Clear migration guidance and helpful error messages
- **Fallback**: Temporary dual specification support

---

## 8. SUCCESS METRICS

### Phase A Success
- [ ] All gemini-2.5-flash references replaced with gemini-2.5-pro
- [ ] All 5 stages produce specification-compliant artifacts
- [ ] Cache hit ratio = 100% on identical experiment rerun
- [ ] Timeout handling produces partial manifests
- [ ] Metrics calculations accurate to ±1%
- [x] Environment-agnostic Python execution implemented (sys.executable pattern)

### Phase B Success  
- [ ] All components <150 lines (THIN compliance)
- [ ] No functionality regression
- [ ] Clear component responsibilities

### Phase C Success
- [ ] 100% specification compliance enforcement
- [ ] Helpful error messages for invalid inputs
- [ ] Zero ambiguous field interpretations

### Phase D Success
- [ ] System handles unseen frameworks/experiments
- [ ] Performance metrics within acceptable ranges
- [ ] Cost calculations accurate to ±5%

---

**Next Immediate Action**: Begin Phase A1 - Update Technical Contracts with all architect-specified requirements

This specification addresses all architect feedback and provides complete technical contracts for implementation. The system will be a "boringly reliable research appliance" that researchers can trust completely within defined constraints.