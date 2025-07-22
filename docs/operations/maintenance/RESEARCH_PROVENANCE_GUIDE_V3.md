# Research Provenance Guide v3.0

## Core Principle: Fault-Tolerant Academic Integrity

**Primary Goal:** Preserve expensive LLM analyses even when downstream processing fails.  
**Secondary Goal:** Enable forensic-grade peer review and replication.

## Directory Structure (MECE)

```
projects/
└── {PROJECT_NAME}/
    ├── PROJECT_CHRONOLOG_{PROJECT_NAME}.jsonl    # Tier 1: Cross-experiment timeline
    └── experiments/
        └── {EXPERIMENT_NAME}/
            ├── experiment_snapshot.md              # Frozen experiment definition
            ├── framework_snapshot.md               # Frozen framework used
            ├── corpus_manifest.json                # Corpus index at time of session
            └── sessions/
                └── {SESSION_ID}/
                    ├── SESSION_CHRONOLOG.jsonl     # Tier 2: Session timeline
                    ├── llm_archive/                 # Raw LLM data (immutable)
                    ├── analysis_results/            # Structured outputs
                    ├── system_state/                # Runtime state captures
                    └── fault_recovery/              # Crash recovery data
```

## File Type Roles (MECE)

### 1. LLM Archive (Immutable Raw Data)
**Purpose:** Preserve exact LLM interactions for forensic analysis  
**Location:** `sessions/{id}/llm_archive/`  
**Fault Tolerance:** Write-immediately on LLM response  

```
llm_archive/
├── call_001_prompt.txt              # Exact prompt sent
├── call_001_response.txt            # Exact response received
├── call_001_metadata.json           # Model forensics + timing
├── call_002_prompt.txt
├── call_002_response.txt
├── call_002_metadata.json
└── ...
```

#### LLM Metadata Schema (Per Call)
```json
{
  "llm_call_id": "001_b3f7d2a6_run1",
  "timestamp": "2025-07-17T20:31:45.123456Z",
  "model_forensics": {
    "requested_model": "vertex_ai/gemini-2.5-pro",
    "actual_model": "gemini-2.5-pro-002",
    "vendor": "Google",
    "api_version": "v1",
    "model_build_date": "2025-01-15",
    "deployment_region": "us-central1"
  },
  "request_params": {
    "temperature": 0.1,
    "max_tokens": 4000,
    "top_p": 0.95
  },
  "response_metadata": {
    "response_time_ms": 2847,
    "tokens_used": 2156,
    "cost_usd": 0.0431
  },
  "provenance_hash": "sha256:a1b2c3d4...",
  "corpus_file": "sanitized_speech_b3f7d2a6.md",
  "run_number": 1
}
```

### 2. Analysis Results (Structured Outputs)
**Purpose:** Human-readable research deliverables  
**Location:** `sessions/{id}/analysis_results/`  
**Fault Tolerance:** Generated from LLM archive, recoverable  

```
analysis_results/
├── individual_analyses/
│   ├── run1_b3f7d2a6_analysis.txt   # Human-readable analysis
│   ├── run1_b3f7d2a6_scores.json    # Structured scores
│   └── ...
├── aggregated_data/
│   ├── cohesion_matrix.csv          # Cross-run comparisons
│   └── reliability_report.txt       # Statistical analysis
└── final_deliverables/
    ├── experiment_report.md          # Main research output
    └── replication_package.zip       # Complete methodology
```

### 3. System State (Runtime Captures)
**Purpose:** Debug workflow failures and enable recovery  
**Location:** `sessions/{id}/system_state/`  
**Fault Tolerance:** Snapshots at each workflow stage  

```
system_state/
├── stage_1_analysis_complete.json   # State after AnalysisAgent
├── stage_2_extraction_complete.json # State after DataExtraction
├── stage_3_calculation_complete.json # State after Calculation
├── stage_4_synthesis_complete.json  # State after Synthesis
└── environment_snapshot.json        # System config at start
```

### 4. Session Chronolog (Workflow Timeline)
**Purpose:** Track workflow execution and timing  
**Location:** `sessions/{id}/SESSION_CHRONOLOG.jsonl`  
**Fault Tolerance:** Append-only, written in real-time  

```jsonl
{"timestamp": "2025-07-17T20:31:45.123456Z", "event": "session_start", "session_id": "session_20250717_203145_a4b8c2d3"}
{"timestamp": "2025-07-17T20:31:46.234567Z", "event": "agent_spawn", "agent": "AnalysisAgent", "corpus_file": "sanitized_speech_b3f7d2a6.md"}
{"timestamp": "2025-07-17T20:31:50.345678Z", "event": "llm_call_start", "call_id": "001_b3f7d2a6_run1"}
{"timestamp": "2025-07-17T20:31:53.456789Z", "event": "llm_call_complete", "call_id": "001_b3f7d2a6_run1", "success": true}
{"timestamp": "2025-07-17T20:31:53.567890Z", "event": "analysis_complete", "corpus_file": "sanitized_speech_b3f7d2a6.md", "run": 1}
```

### 5. Fault Recovery (Crash Recovery Data)
**Purpose:** Enable session resumption after failures  
**Location:** `sessions/{id}/fault_recovery/`  
**Fault Tolerance:** Progressive checkpoints  

```
fault_recovery/
├── resume_checkpoint.json           # Last successful state
├── pending_work_queue.json          # Remaining tasks
└── crash_report.txt                 # Failure diagnostics
```

## Fault Tolerance Strategy

### Primary Principle: **Immediate Persistence**
- **LLM responses:** Written to disk immediately upon receipt
- **Session events:** Appended to chronolog in real-time
- **State snapshots:** Saved after each workflow stage

### Recovery Hierarchy:
1. **Resume from last checkpoint** (ideal)
2. **Regenerate from LLM archive** (acceptable)
3. **Partial recovery with gap analysis** (emergency)

### Cost Protection:
- **Never re-call LLMs** if response exists in archive
- **Validate archive integrity** before expensive operations
- **Graceful degradation** when partial data available

## Academic Integrity Features

### Model Provenance Tracking
- **Exact model versions** and build dates
- **API parameters** and response metadata
- **Vendor-specific identifiers** for reproduction

### Cryptographic Integrity
- **HMAC-SHA256 signatures** on all archive files
- **Merkle tree validation** for session completeness
- **Tamper-evident chronologs** with hash chains

### Peer Review Support
- **Complete methodology snapshots** at session level
- **Replication packages** with exact dependencies
- **Forensic debugging** capabilities for disputed results

## Implementation Priorities

### Phase 1: Fault Tolerance (Critical)
1. Implement immediate LLM archive persistence
2. Add progressive state checkpointing
3. Build session resumption capability

### Phase 2: Model Provenance (Important)
1. Enhance LLM metadata capture
2. Add vendor-specific model identification
3. Implement cost tracking and optimization

### Phase 3: Academic Features (Nice-to-Have)
1. Complete cryptographic integrity system
2. Build automated replication packages
3. Add peer review audit tools

## Success Metrics

### Fault Tolerance Success:
- ✅ **Zero LLM data loss** during workflow failures
- ✅ **Session resumption** within 30 seconds of crash
- ✅ **Cost protection** - no duplicate expensive calls

### Academic Integrity Success:
- ✅ **Forensic reproducibility** of all results
- ✅ **Model provenance** for all LLM interactions
- ✅ **Peer review compatibility** with standard audit tools

---

*This guide prioritizes fault tolerance and cost protection while maintaining academic integrity standards.* 