# Experiment Specification (v7.0)

**Version**: 7.0  
**Status**: Active  
**Major Change**: Gasket Architecture Integration and Raw Analysis Log Workflow

The `experiment.md` file is a simple, human-readable YAML file that defines the complete scope of an analysis run. It acts as the **single source of truth** for experiment configuration, telling the Discernus system what framework to use, what corpus to analyze, and how to run it.

**🚀 NEW IN V7.0: Gasket Architecture Workflow**

Version 7.0 aligns with Framework Specification v7.0 and Corpus Specification v7.0 to support the complete gasket architecture workflow: Raw Analysis Log → Intelligent Extractor → Mathematical Processing → Evidence Distillation → Human-Readable Results.

---

## 1. File Structure

The experiment file MUST be a valid YAML file named `experiment.md` containing a YAML configuration block with the header `# --- Discernus Configuration ---`.

---

## 2. Recommended Project Structure

The system uses a **single-source-of-truth** architecture where the experiment file defines all paths and configuration:

```
my_research_project/
├── framework.md                  # Framework v7.0 with gasket_schema
├── experiment.md                 # Experiment v7.0 with gasket workflow
└── corpus/                       # Corpus v7.0 with enhanced manifest
    ├── corpus.md                 # Corpus specification compliance
    ├── document_01.txt
    ├── document_02.txt
    └── ...
```

To run an experiment, execute the CLI with a single parameter:

```bash
python3 -m discernus.cli run experiment.md
```

The experiment file defines the framework and corpus paths, eliminating parameter conflicts.

---

## 3. Schema

```yaml
---
# --- Discernus Configuration ---

# REQUIRED: A unique, machine-readable name for the experiment.
name: my_gasket_experiment

# REQUIRED: A human-readable description emphasizing v7.0 gasket architecture validation.
description: |
  Experiment description that clearly states it validates the v7.0 gasket architecture
  with Raw Analysis Log processing and MECE Trinity coherence.

# REQUIRED: Primary falsifiable hypothesis about the research question.
hypothesis: |
  Your primary research hypothesis that will be tested using the gasket architecture.

# REQUIRED: Path to Framework v7.0 specification file with gasket_schema
framework: "framework_v7.0.md"

# REQUIRED: Path to Corpus v7.0 directory with enhanced manifest
corpus_path: "corpus/"

# REQUIRED: List of LiteLLM-compatible model identifiers
# Default: Flash Lite for integration testing, Pro for production analysis
models:
  - "vertex_ai/gemini-2.5-flash-lite"

# REQUIRED: Number of analysis runs per model (integer ≥ 1)
runs_per_model: 1

# OPTIONAL: Framework variant to use (defaults to 'default')
analysis_variant: "default"

# 🆕 V7.0 GASKET ARCHITECTURE CONFIGURATION
gasket_workflow:
  # Validate MECE Trinity coherence before execution
  validate_trinity_coherence: true
  
  # Enable Raw Analysis Log processing
  raw_analysis_log_processing: true
  
  # Enable Intelligent Extractor (Gasket #2)
  intelligent_extractor_enabled: true
  
  # Parallel stream processing (quantitative + qualitative)
  parallel_streams: true

# Enhanced v7.0 Analysis Configuration
analysis:
  evaluations_per_document: 2
  statistical_confidence: 0.95
  variance_threshold: 0.20

# V7.0 Statistical Validation
validation:
  cronbachs_alpha_threshold: 0.70
  variance_coefficient_threshold: 0.25
  missing_data_threshold: 0.10

# V7.0 Reporting Configuration  
reporting:
  sections:
    - "executive_summary"
    - "methodology"
    - "raw_analysis_log_samples"
    - "gasket_extraction_validation"
    - "statistical_analysis"
    - "evidence_distillation"
    - "conclusions"
    - "replication_package"
  show_statistical_work: true
  include_confidence_metrics: true
  include_gasket_provenance: true

# REQUIRED: Workflow steps for v7.0 gasket architecture
workflow:
  # Step 1: Raw Analysis Log generation
  - agent: EnhancedAnalysisAgent
    inputs:
      - experiment
      - framework_v7
      - corpus_v7
    outputs:
      - raw_analysis_logs

  # Step 2: Intelligent Extractor (Gasket #2)
  - agent: IntelligentExtractorAgent
    inputs:
      - raw_analysis_logs
      - framework_gasket_schema
    outputs:
      - extracted_scores
      - extraction_validation

  # Step 3: Mathematical Processing
  - agent: MathematicalProcessingAgent
    inputs:
      - extracted_scores
      - framework_calculation_spec
    outputs:
      - calculated_metrics
      - statistical_analysis

  # Step 4: Evidence Distillation
  - agent: EvidenceDistillationAgent
    inputs:
      - raw_analysis_logs
      - statistical_analysis
    outputs:
      - curated_evidence

  # Step 5: Results Synthesis
  - agent: EnhancedSynthesisAgent
    inputs:
      - calculated_metrics
      - curated_evidence
      - experiment
      - framework_v7
    outputs:
      - final_report.md
      - results.csv
      - replication_package

# V7.0 Hypothesis Framework
hypotheses:
  H1_Research: "Primary research hypothesis about the subject matter"
  H2_Framework: "Framework v7.0 will successfully process the analysis with gasket architecture"
  H3_Architecture: "The v7.0 gasket architecture will demonstrate MECE Trinity coherence and reliable Raw Analysis Log processing"

---

# Human-Readable Experiment Description

This section contains the full human-readable description of the experiment,
including methodology, expected outcomes, and analysis rationale. The v7.0
specification enables gasket architecture validation through MECE Trinity
coherence (Framework + Experiment + Corpus) and Raw Analysis Log processing.
```

## 4. Field Specifications

### Required Fields

- **`name`**: Unique identifier for the experiment (snake_case recommended)
- **`description`**: Human-readable purpose statement emphasizing v7.0 gasket architecture
- **`hypothesis`**: Primary falsifiable hypothesis being tested  
- **`framework`**: Relative path to Framework v7.0 specification file
- **`corpus_path`**: Relative path to Corpus v7.0 directory
- **`models`**: List of LiteLLM-compatible model identifiers
- **`runs_per_model`**: Number of analysis runs per model (integer ≥ 1)
- **`workflow`**: Ordered list of gasket architecture agent execution steps

### New v7.0 Configuration Sections

#### Gasket Workflow Configuration
- **`validate_trinity_coherence`**: Enable MECE Trinity validation before execution
- **`raw_analysis_log_processing`**: Enable Raw Analysis Log paradigm
- **`intelligent_extractor_enabled`**: Enable Intelligent Extractor (Gasket #2)
- **`parallel_streams`**: Enable parallel quantitative/qualitative processing

#### Analysis Configuration
- **`analysis.evaluations_per_document`**: Number of independent evaluations per document (default: 1)

#### Validation Configuration
- **`validation.cronbachs_alpha_threshold`**: Minimum reliability threshold (default: 0.70)
- **`validation.variance_coefficient_threshold`**: Maximum variance threshold (default: 0.25)

#### Reporting Configuration
- **`reporting.include_gasket_provenance`**: Include gasket operation audit trail
- **`reporting.show_statistical_work`**: Include mathematical calculations

## 5. V7.0 Workflow Requirements

The v7.0 workflow MUST include these gasket architecture components:

1. **Raw Analysis Log Generation**: Framework v7.0 produces human-readable analysis
2. **Intelligent Extractor**: Gasket #2 extracts structured data from Raw Analysis Logs
3. **Mathematical Processing**: Code-based calculations using extracted data
4. **Evidence Distillation**: LLM-native evidence curation from Raw Analysis Logs
5. **Results Synthesis**: Human-readable final reports with replication packages

## 6. MECE Trinity Coherence

Experiment v7.0 requires coherence with:
- **Framework v7.0**: Must include gasket_schema and raw_analysis_log output_contract
- **Corpus v7.0**: Must include enhanced manifest with field naming consistency
- **Experiment v7.0**: Must specify gasket workflow and validation requirements

## 7. Migration from v3.0

### Key Changes from v3.0

1. **🚨 PARADIGM SHIFT**: Gasket architecture workflow replaces direct JSON processing
2. **Added Gasket Workflow**: New gasket_workflow configuration section
3. **Enhanced Validation**: MECE Trinity coherence validation
4. **Raw Analysis Log Support**: Workflow supports Framework v7.0 paradigm
5. **Parallel Streams**: Quantitative and qualitative processing streams

### Migration Guide

To convert a v3.0 experiment to v7.0:

1. **Update version** to "v7.0" in framework reference
2. **Add gasket_workflow section** with v7.0 configuration
3. **Update workflow steps** to include Intelligent Extractor and Evidence Distillation
4. **Update hypotheses** to reference v7.0 gasket architecture
5. **Add gasket provenance** to reporting configuration
6. **Test with MECE Trinity validation** to ensure coherence

---

## Conclusion

The Experiment Specification v7.0 completes the MECE Trinity alignment with Framework v7.0 and Corpus v7.0. Together, they enable the full gasket architecture workflow: human-readable analysis → intelligent extraction → mathematical processing → evidence distillation → reliable results.

Your v7.0 experiment validates not just your research hypothesis, but the gasket architecture itself, ensuring that the MECE Trinity forms a coherent, reliable analytical system.