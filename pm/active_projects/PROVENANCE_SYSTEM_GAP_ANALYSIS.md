# Provenance System Gap Analysis
## Current State → Research Provenance Guide v3.0

**Date:** January 13, 2025  
**Context:** Post-MVA Experiment 2 failure analysis  
**Priority:** Critical - Fault tolerance blocking research progress

## Executive Summary

**Current System Status:** 🟡 **Partial Implementation**
- ✅ **Three-tier architecture exists** and captures comprehensive data
- ❌ **Fault tolerance fails** - expensive LLM analyses lost on crashes
- ❌ **MECE violations** - overlapping file responsibilities cause confusion
- ❌ **Model provenance gaps** - insufficient forensic detail for replication

**Cost Impact:** ~$50+ in wasted LLM calls per failed experiment

## Detailed Gap Analysis

### 1. Directory Structure Issues

#### Current State (Problematic):
```
projects/MVA/experiment_2/
├── conversations/              # Mix of LLM + workflow events
├── logs/                       # Mix of system + session data
├── results/                    # Mix of raw + processed data
├── experiment_2.md             # Live file, not snapshot
└── Cohesive Flourishing Framework (CFF) v4.1.md  # Live file
```

#### Required Changes for v3.0:
```diff
projects/MVA/
+ ├── PROJECT_CHRONOLOG_MVA.jsonl
+ └── experiments/
+     └── experiment_2/
+         ├── experiment_snapshot.md         # NEW: Frozen definition
+         ├── framework_snapshot.md          # NEW: Frozen framework
+         ├── corpus_manifest.json           # NEW: Corpus index
+         └── sessions/
+             └── session_20250717_155122/
+                 ├── SESSION_CHRONOLOG.jsonl    # RESTRUCTURE
+                 ├── llm_archive/                # NEW: Immediate persistence
+                 ├── analysis_results/           # RESTRUCTURE
+                 ├── system_state/               # NEW: Recovery checkpoints
+                 └── fault_recovery/             # NEW: Crash recovery
```

**Gap:** Complete directory restructure required

### 2. Fault Tolerance Failures

#### Current Behavior (Broken):
1. **AnalysisAgent** completes 46 analyses → stored in memory
2. **DataExtractionAgent** crashes on parsing error
3. **ALL 46 analyses lost** - no recoverable persistence
4. **Researcher must re-run** expensive LLM calls

#### Required v3.0 Behavior:
1. **AnalysisAgent** completes analysis → **immediately persists to disk**
2. **DataExtractionAgent** crashes → **analyses remain safe**
3. **Session resumes** from last checkpoint without LLM re-calls
4. **Cost protection** - zero duplicate API calls

**Gap:** Need immediate LLM persistence and checkpoint system

### 3. File Role Confusion (MECE Violations)

#### Current Overlap Problems:
| File Type | Current Contents | MECE Violations |
|-----------|------------------|-----------------|
| `conversations/` | LLM responses + workflow events | Mixed purposes |
| `logs/machine.jsonl` | System events + analysis results | Mixed purposes |
| `results/state_*.json` | Everything dumped together | Single responsibility violation |
| `session_run.log` | Random placement | Unclear purpose |

#### Required v3.0 Separation:
| File Type | Single Purpose | Location |
|-----------|---------------|----------|
| `llm_archive/` | **Only** raw LLM request/response pairs | `sessions/{id}/llm_archive/` |
| `SESSION_CHRONOLOG.jsonl` | **Only** workflow timing events | `sessions/{id}/SESSION_CHRONOLOG.jsonl` |
| `analysis_results/` | **Only** structured human-readable outputs | `sessions/{id}/analysis_results/` |
| `system_state/` | **Only** runtime state for recovery | `sessions/{id}/system_state/` |

**Gap:** Complete file role separation required

### 4. Model Provenance Gaps

#### Current Metadata (Insufficient):
```json
{
  "model": "vertex_ai/gemini-2.5-pro",
  "temperature": 0.1
}
```

#### Required v3.0 Forensics:
```json
{
  "model_forensics": {
    "requested_model": "vertex_ai/gemini-2.5-pro",
    "actual_model": "gemini-2.5-pro-002",
    "vendor": "Google",
    "api_version": "v1",
    "model_build_date": "2025-01-15",
    "deployment_region": "us-central1"
  },
  "response_metadata": {
    "response_time_ms": 2847,
    "tokens_used": 2156,
    "cost_usd": 0.0431
  }
}
```

**Gap:** Enhanced LLM metadata capture system needed

### 5. Real-Time Persistence Gaps

#### Current Pattern (Vulnerable):
```python
# All analyses stored in memory
results = []
for corpus_file in corpus_files:
    for run in range(6):
        analysis = llm_gateway.complete(prompt)  # $$$
        results.append(analysis)  # MEMORY ONLY
        
# Single batch write at end
save_results(results)  # CRASH HERE = LOSE EVERYTHING
```

#### Required v3.0 Pattern:
```python
# Immediate persistence per call
for corpus_file in corpus_files:
    for run in range(6):
        analysis = llm_gateway.complete(prompt)  # $$$
        
        # IMMEDIATE PERSISTENCE
        llm_archive.save_call(prompt, analysis, metadata)
        checkpoint.update_progress(corpus_file, run)
        
        # Continue even if downstream fails
```

**Gap:** Immediate persistence implementation needed

## Implementation Roadmap

### Phase 1: Critical Fault Tolerance (Week 1)
**Goal:** Prevent LLM data loss during workflow failures

#### 1.1 Immediate LLM Archive Persistence
- [ ] Create `LLMArchiveManager` class
- [ ] Implement write-immediately on LLM response
- [ ] Add metadata capture for each call
- [ ] **Test:** Crash during DataExtraction - analyses should survive

#### 1.2 Progressive Checkpointing
- [ ] Create `CheckpointManager` class  
- [ ] Save state after each workflow stage
- [ ] Implement session resumption logic
- [ ] **Test:** Resume from any checkpoint without duplicate LLM calls

#### 1.3 Cost Protection
- [ ] Never re-call LLMs if response exists
- [ ] Validate archive integrity before operations
- [ ] Graceful degradation with partial data
- [ ] **Test:** Zero duplicate API calls on recovery

### Phase 2: Directory Restructure (Week 2)
**Goal:** Implement MECE file organization

#### 2.1 New Directory Structure
- [ ] Create migration script for existing data
- [ ] Implement new directory layout
- [ ] Update all path references in code
- [ ] **Test:** All existing experiments accessible in new structure

#### 2.2 Snapshot System
- [ ] Create experiment/framework snapshots at session start
- [ ] Implement corpus manifest generation
- [ ] Add snapshot integrity validation
- [ ] **Test:** Complete methodology reproduction from snapshots

### Phase 3: Enhanced Provenance (Week 3)
**Goal:** Forensic-grade model tracking

#### 3.1 Model Forensics
- [ ] Enhance LLM metadata capture
- [ ] Add vendor-specific model identification
- [ ] Implement cost tracking per call
- [ ] **Test:** Complete model provenance for replication

#### 3.2 Academic Integrity Features
- [ ] Add cryptographic integrity validation
- [ ] Implement replication package generation
- [ ] Create peer review audit tools
- [ ] **Test:** Pass academic integrity audit

## Success Criteria

### Phase 1 Success (Critical):
- ✅ **Zero LLM data loss** during any workflow failure
- ✅ **Session resumption** within 30 seconds of crash
- ✅ **Cost protection** - no duplicate expensive calls

### Phase 2 Success (Important):
- ✅ **MECE file organization** - clear single responsibilities
- ✅ **Complete methodology snapshots** at session level
- ✅ **Migration compatibility** - all existing data accessible

### Phase 3 Success (Nice-to-Have):
- ✅ **Forensic model provenance** for all LLM interactions
- ✅ **Academic integrity compliance** with standard audit tools
- ✅ **Automated replication packages** for peer review

## Risk Assessment

### High Risk:
- **Data migration complexity** - existing experiments may break
- **Performance impact** - immediate persistence may slow workflow
- **Integration complexity** - multiple systems need coordination

### Mitigation Strategies:
- **Incremental migration** - phase implementation carefully
- **Parallel testing** - maintain current system during transition
- **Rollback plan** - ability to revert to current system if needed

## Resource Requirements

### Development Time:
- **Phase 1:** 3-4 days (critical fault tolerance)
- **Phase 2:** 2-3 days (directory restructure)
- **Phase 3:** 3-4 days (enhanced provenance)

### Testing Requirements:
- **Unit tests** for each component
- **Integration tests** for workflow recovery
- **Performance benchmarks** to ensure no degradation
- **Academic compliance validation** with sample audit

---

**Next Steps:**
1. Approve this gap analysis and implementation plan
2. Begin Phase 1 implementation (fault tolerance)
3. Test with controlled MVA experiment reproduction
4. Proceed to Phase 2 once fault tolerance validated 