# Issue #297: Provenance-First File Organization Design

**Version**: 1.0  
**Status**: Design Phase  
**Purpose**: Transform hostile hash-based artifact storage into academic-grade provenance architecture

---

## Current State Problems

**Academic Hostility**:
- Artifacts named `b8d95bda8af38db280f7bc6fa8198a6a3a95b292b97419caa98fb9307e0831f5`
- Researchers must be detectives to trace their own work
- External reviewers can't validate findings quickly
- Fraud auditors can't efficiently verify academic integrity

**Scattered Organization**:
```
runs/20250804T000659Z/
├── manifest.json          # Technical metadata
├── results/               # Some outputs
│   └── analysis.json      # Raw data dump
└── logs/                  # System logs

shared_cache/artifacts/
├── artifact_registry.json # Technical registry  
└── [50+ hash files]       # Incomprehensible to humans
```

---

## Provenance-First Architecture

### Academic-Grade Structure

```
runs/20250804T000659Z/
├── FINAL_REPORT.md              # Main deliverable
├── METHODOLOGY_SUMMARY.md       # Framework + corpus + model decisions
├── STATISTICAL_SUMMARY.md       # Reliability metrics + confidence intervals
├── data/
│   ├── scores.csv               # Quantitative results  
│   ├── evidence.csv             # Supporting quotes
│   └── reliability_metrics.csv  # Multi-run consistency data
├── artifacts/                   # HUMAN-READABLE ARTIFACT ORGANIZATION
│   ├── analysis_plans/
│   │   ├── raw_data_plan.md     # → symlink to shared_cache/artifacts/abc123...
│   │   └── mathematical_plan.md # → symlink to shared_cache/artifacts/def456...
│   ├── statistical_results/
│   │   ├── anova_results.json   # → symlink to shared_cache/artifacts/ghi789...
│   │   └── reliability_alpha.json # → symlink to shared_cache/artifacts/jkl012...
│   ├── evidence/
│   │   ├── curated_quotes.json  # → symlink to shared_cache/artifacts/mno345...
│   │   └── raw_evidence.json    # → symlink to shared_cache/artifacts/pqr678...
│   └── provenance.json          # Human-readable artifact map
├── technical/
│   ├── manifest.json            # Complete execution record
│   ├── logs/                    # Detailed system logs
│   └── model_interactions/      # LLM API call logs
└── README.md                    # Navigation guide for researchers

shared_cache/artifacts/          # PERFORMANCE LAYER (unchanged)
├── artifact_registry.json      # Technical registry
└── [hash files]                # Content-addressable storage
```

### Key Design Principles

1. **Complete Transparency**: All artifacts visible from run directory
2. **Human-Readable Names**: `anova_results.json` vs `b8d95bda8af3...`
3. **Logical Organization**: Group by pipeline stage and artifact type
4. **Performance Maintained**: Symlinks to shared cache for deduplication
5. **Academic Standards**: Structure matches researcher mental models
6. **External Review Ready**: Clear provenance trails for peer review

---

## Artifact Classification System

### By Pipeline Stage
- **analysis_plans/**: What the LLM planned to analyze
- **statistical_results/**: Mathematical computations and metrics
- **evidence/**: Curated quotes and supporting data
- **reports/**: Final synthesis outputs

### By Academic Purpose
- **Primary Deliverables**: `FINAL_REPORT.md`, `scores.csv`, `evidence.csv`
- **Methodology Validation**: `METHODOLOGY_SUMMARY.md`, `model_interactions/`
- **Statistical Rigor**: `STATISTICAL_SUMMARY.md`, `reliability_metrics.csv`
- **Replication Materials**: `artifacts/`, `technical/manifest.json`

### By Stakeholder Need
- **Primary Researcher**: `FINAL_REPORT.md`, `data/` directory
- **Internal Reviewer**: `METHODOLOGY_SUMMARY.md`, `STATISTICAL_SUMMARY.md`
- **Replication Researcher**: `artifacts/`, `technical/`, `README.md`
- **Fraud Auditor**: `technical/manifest.json`, `logs/`, `provenance.json`
- **LLM Skeptic**: `model_interactions/`, `reliability_metrics.csv`

---

## Implementation Strategy

### Phase 1: Core Infrastructure
1. **Artifact Symlink System**: Map human names to hash files
2. **Provenance Metadata**: `provenance.json` with descriptions
3. **Directory Templates**: Standard structure for all runs
4. **Integration Points**: Modify `ThinOrchestrator` to create structure

### Phase 2: Academic Enhancements  
1. **README Generation**: Navigation guides for each run
2. **Methodology Summaries**: Auto-generated research documentation
3. **Statistical Summaries**: Reliability metrics and confidence intervals
4. **Model Interaction Logs**: Complete LLM provenance tracking

### Phase 3: Publication Ready
1. **One-Command Export**: Complete replication packages
2. **LaTeX Integration**: Publication-ready tables and figures
3. **Citation Generation**: Methodology descriptions for papers
4. **Cross-Run Analysis**: Multi-experiment reliability studies

---

## Technical Implementation

### Artifact Mapping Logic
```python
def create_human_readable_artifacts(run_dir: Path, artifact_registry: Dict):
    """Map hash-based artifacts to human-readable structure"""
    artifacts_dir = run_dir / "artifacts"
    
    # Group by artifact type from registry metadata
    by_type = defaultdict(list)
    for hash_id, metadata in artifact_registry.items():
        artifact_type = metadata["metadata"].get("artifact_type", "unknown")
        by_type[artifact_type].append((hash_id, metadata))
    
    # Create human-readable symlinks
    for artifact_type, artifacts in by_type.items():
        type_dir = artifacts_dir / ARTIFACT_TYPE_MAPPING[artifact_type]
        type_dir.mkdir(parents=True, exist_ok=True)
        
        for hash_id, metadata in artifacts:
            human_name = generate_human_name(metadata)
            symlink_path = type_dir / human_name
            target_path = shared_cache_dir / "artifacts" / hash_id
            symlink_path.symlink_to(target_path)
```

### Provenance JSON Structure
```json
{
  "run_metadata": {
    "experiment_name": "Character Heuristics Framework Test",
    "run_timestamp": "2025-08-04T00:06:59Z",
    "framework_version": "CHF v6.0",
    "model_used": "vertex_ai/gemini-2.5-flash-lite"
  },
  "pipeline_stages": {
    "analysis": {
      "input_artifacts": ["corpus_documents", "framework_content"],
      "output_artifacts": ["raw_analysis_scores", "evidence_extracts"],
      "duration_seconds": 127.3,
      "cost_usd": 0.0234
    },
    "synthesis": {
      "input_artifacts": ["raw_analysis_scores", "evidence_extracts"],
      "output_artifacts": ["statistical_results", "curated_evidence", "final_report"],
      "duration_seconds": 89.7,
      "cost_usd": 0.0456
    }
  },
  "artifact_descriptions": {
    "anova_results.json": "Statistical ANOVA analysis of framework dimensions",
    "curated_quotes.json": "Highest-confidence evidence supporting findings",
    "reliability_alpha.json": "Cronbach's alpha across multiple runs"
  }
}
```

---

## Success Metrics

### Alpha Release Goals
- [ ] Every run directory contains complete artifact visibility
- [ ] Researchers understand full provenance without leaving run directory  
- [ ] Performance maintained through shared cache backend
- [ ] External reviewers can navigate provenance intuitively
- [ ] Clear documentation explains artifact organization

### Academic Acceptance Goals
- [ ] Methodology skeptics become advocates
- [ ] Replication studies succeed flawlessly  
- [ ] Fraud auditors find transparent excellence
- [ ] Traditional "3 undergrads + pizza" methods look primitive

---

**Next Steps**: Implement core symlink system and integrate into `ThinOrchestrator`