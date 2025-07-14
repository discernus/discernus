# Research Provenance Guide: Three-Tier Audit Trail
**Academic Integrity and Replication for Computational Social Science**

Version: 2.0  
Date: January 13, 2025  
Status: Production-ready for academic publication

---

## Overview

The SOAR v2.0 research provenance system implements a **three-tier audit trail** designed for academic integrity, peer review, and replication studies in computational social science. Each tier captures different aspects of the research process with cryptographic integrity guarantees.

### Research Integrity Guarantee
Every analysis run produces **complete, tamper-evident records** suitable for:
- Academic peer review and publication
- Replication studies by independent researchers  
- Statistical reliability analysis (Cronbach's alpha, IRR)
- Performance and methodological validation

---

## Three-Tier Architecture

### Tier 1: Project-Level Chronolog
**File**: `projects/{project}/PROJECT_CHRONOLOG_{project}.jsonl`  
**Scope**: Complete project lifecycle across all sessions  
**Purpose**: Cross-session continuity and project evolution

**Contains**:
- Project initialization and configuration
- All sessions from all analysis runs
- System events and timing across entire project
- Cross-run patterns and methodology evolution

**Use Cases**:
- "How has our methodology evolved over time?"
- "What sessions have been run on this project?"
- "When did we make configuration changes?"
- Long-term research program documentation

### Tier 2: Run-Specific Chronolog  
**File**: `results/{timestamp}/RUN_CHRONOLOG_{session_id}.jsonl`  
**Scope**: Single analysis run/session only  
**Purpose**: Statistical analysis and performance metrics

**Contains**:
- Session start/end timing
- Analysis agent spawning and completion
- System events and performance metrics
- Success/failure rates and error conditions

**Use Cases**:
- Cronbach's alpha calculations across multiple runs
- Performance analysis and optimization
- Debugging specific analysis runs
- Statistical reliability assessment

### Tier 3: Conversation Files
**File**: `conversations/conversation_{timestamp}_{id}.jsonl`  
**Scope**: LLM interactions for single session  
**Purpose**: Intellectual content and replication

**Contains**:
- Complete analysis agent prompts and instructions
- Full LLM responses with reasoning and evidence
- Framework application details and scoring
- Agent-to-agent communications

**Use Cases**:
- Replication by independent researchers
- Quality assessment of LLM reasoning
- Content analysis and scoring validation
- Methodological transparency for peer review

---

## Academic Research Workflows

### Statistical Reliability Analysis

**Cronbach's Alpha Calculation**:
```
1. Run same analysis multiple times (N=5-10)
2. Extract timing data from run chronologs
3. Extract content scores from conversation files  
4. Calculate alpha across runs for consistency measurement
```

**Files Needed**:
- Multiple `RUN_CHRONOLOG_session_*.jsonl` for timing consistency
- Multiple `conversation_*.jsonl` for content consistency
- `final_report.md` files for aggregated results

### Inter-Rater Reliability (IRR)

**Multi-Model Comparison**:
```
1. Configure different LLM models for same corpus
2. Compare conversation files across models
3. Extract framework scores for IRR calculation
4. Use run chronologs for performance comparison
```

### Replication Studies

**Complete Replication Package**:
```
Required Files (per run):
├── RUN_CHRONOLOG_{session}.jsonl     # Timing and system integrity
├── conversation_{session}.jsonl      # Complete intellectual content
├── final_report.md                   # Aggregated analysis results
├── session_metadata.json             # Configuration and provenance
└── framework.md + experiment.md      # Methodology specification
```

### Performance Analysis

**Model Consistency Studies**:
- **Timing Analysis**: Run chronologs show model response time patterns
- **Content Analysis**: Conversation files reveal reasoning consistency
- **Quality Metrics**: Success rates and error patterns across runs

---

## Academic Integrity Features

### Cryptographic Integrity
- **HMAC-SHA256 signatures** on every chronolog event
- **Tamper detection** through signature verification
- **Git commits** for distributed verification

### Temporal Provenance  
- **UTC timestamps** with microsecond precision
- **Event ordering** guarantees within sessions
- **Cross-session timing** for project evolution

### Content Provenance
- **Complete prompt capture** for exact replication
- **Full response preservation** including reasoning chains
- **Framework application documentation** with evidence citations

### Methodological Transparency
- **System configuration** captured in metadata
- **Model selection** and parameters documented  
- **Analysis workflow** decisions recorded with rationale

---

## Research Questions and File Selection

| Research Question | Primary Source | Supporting Sources |
|---|---|---|
| "How reliable is this model across runs?" | Run Chronologs | Conversation Files |
| "Can this analysis be replicated?" | Conversation Files | Run Chronologs + Metadata |
| "How long does analysis typically take?" | Run Chronologs | Session Metadata |
| "What evidence supports these scores?" | Conversation Files | Final Reports |
| "Has methodology changed over time?" | Project Chronolog | Run Chronologs |
| "Are there systematic performance issues?" | Run Chronologs | Project Chronolog |
| "What exactly did the LLM conclude?" | Conversation Files | Final Reports |

---

## File Format Specifications

### Chronolog Events (JSONL)
```json
{
  "timestamp": "2025-01-13T22:32:31.123456Z",
  "event": "ANALYSIS_AGENTS_COMPLETED", 
  "session_id": "session_20250113_223231",
  "project": "attesor",
  "data": {
    "successful_count": 2,
    "failed_count": 0,
    "analysis_duration_seconds": 43.2
  },
  "event_id": "uuid4-string",
  "signature": "hmac-sha256-signature"
}
```

### Conversation Messages (JSONL)
```json
{
  "timestamp": "2025-01-13T22:33:15.789012Z",
  "conversation_id": "conversation_20250113_223315_abc123",
  "speaker": "analysis_agent_1",
  "message": "Full LLM response with PDAF scores...",
  "metadata": {
    "type": "llm_response",
    "agent_id": "analysis_agent_1",
    "framework_version": "PDAF v1.1"
  }
}
```

---

## Best Practices for Researchers

### Multi-Run Studies
1. **Consistent Configuration**: Use identical framework and experiment files
2. **Clean Separation**: Each run gets separate results directory
3. **Statistical Power**: Minimum 5-10 runs for reliability analysis
4. **Documentation**: Record research questions and hypotheses before runs

### Academic Publication
1. **Cite All Tiers**: Reference chronologs, conversations, and reports
2. **Provide Checksums**: Include file hashes for integrity verification
3. **Archive Complete Package**: All files needed for replication
4. **Document Methodology**: Framework versions and configuration details

### Peer Review Support
1. **Chronolog Verification**: Reviewers can verify timing and events
2. **Content Inspection**: Full LLM reasoning available for assessment
3. **Replication Testing**: Complete methodology package for independent validation
4. **Statistical Validation**: Raw data for reliability and validity testing

---

## Troubleshooting and Validation

### Integrity Verification
```bash
# Verify chronolog signatures
python3 -c "
from discernus.core.project_chronolog import get_project_chronolog
chronolog = get_project_chronolog('projects/attesor')
result = chronolog.verify_integrity()
print(f'Verified: {result[\"verified\"]}')
print(f'Events: {result[\"verified_events\"]}')
"
```

### Missing Files Diagnosis
- **No run chronolog**: Session may have failed before completion
- **Empty conversation file**: LLM client connection issues
- **Missing final report**: Aggregation phase failed
- **Incomplete project chronolog**: Redis or Git commit issues

### Performance Analysis
```bash
# Extract timing statistics
grep "analysis_duration_seconds" RUN_CHRONOLOG_*.jsonl
grep "events_per_minute" RUN_CHRONOLOG_*.jsonl
```

---

## Integration with Academic Workflow

### Grant Applications
- Cite methodological transparency and integrity features
- Reference replication packages for validation studies
- Document statistical reliability measurement capabilities

### IRB and Ethics Reviews  
- Demonstrate complete audit trail for sensitive analysis
- Show data protection through anonymization features
- Provide methodology transparency for ethical assessment

### Publication Preparation
- Include provenance package as supplementary materials
- Reference chronolog signatures for integrity claims
- Provide replication instructions with file manifests

### Post-Publication
- Archive complete provenance package for long-term access
- Maintain Git repository for distributed verification
- Support replication requests with documented file locations

---

**Academic Contact**: For questions about research applications, methodological validation, or replication studies, reference the complete technical specification in `docs/CHRONOLOG_SYSTEM_SPECIFICATION.md`.

**Citation Format**: 
```
SOAR v2.0 Research Provenance System. Three-tier audit trail with cryptographic integrity. 
Project chronolog: [SHA256], Run chronolog: [SHA256], Conversations: [SHA256].
``` 