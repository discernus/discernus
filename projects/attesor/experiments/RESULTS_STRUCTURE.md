# Attesor Study Results Structure

This document defines the new results architecture that addresses the limitations of the current JSONL chronolog and synthesis-focused markdown approach.

## Problems with Current Results Format

### 1. JSONL Chronolog Issues
- **Too detailed**: Thousands of lines of agent conversations
- **Not human-readable**: Requires parsing tools to extract insights
- **Mixed signal/noise**: System events buried in conversational data
- **No analysis focus**: Captures process, not outcomes

### 2. Markdown Summary Issues  
- **Synthesis-focused**: Emphasizes adversarial discussion process
- **Not bias-relevant**: Doesn't capture bias isolation metrics
- **Process-oriented**: Focuses on agent interactions, not research findings
- **Academic mismatch**: Doesn't align with publication needs

## New Results Architecture

### Results by Experiment Type

**Smoketest** → **Infrastructure Validation**
- Focus: Orchestrator functionality
- Key outputs: Workflow validation, system logs
- Decision: Go/no-go for pilot

**Pilot** → **Methodology Validation**  
- Focus: Bias detection and statistical analysis
- Key outputs: Bias measurements, cross-linguistic correlations
- Decision: Go/no-go for full study

**Full Study** → **Academic Findings**
- Focus: Publication-ready research outcomes
- Key outputs: Comprehensive bias analysis, methodology papers
- Decision: Academic publication and field recommendations

### File Types by Purpose

#### 1. **Human-Readable Analysis** (.md files)
```
bias_detection_report.md         # What bias did we find?
cross_linguistic_validation.md   # Does Esperanto mitigation work?
academic_findings_report.md      # What are the implications?
```

#### 2. **Raw Data** (.json files)
```
raw_pdaf_scores.json            # Anchor scores for statistical analysis
pilot_summary.json              # Machine-readable decision data
model_metadata.json             # Provenance and replication info
```

#### 3. **Statistical Analysis** (.csv files)
```
bias_effect_sizes.csv           # Cohen's d calculations
correlation_matrices.csv        # Cross-linguistic correlations
significance_tests.csv          # p-values and confidence intervals
```

#### 4. **Academic Materials** (.md + supporting files)
```
publication_materials/          # Ready-to-submit papers
replication_package/           # Code and data for validation
methodology_appendix.md        # Complete technical documentation
```

#### 5. **Audit Trail** (.jsonl - minimal)
```
complete_audit_trail.jsonl     # Essential provenance only
system_logs.jsonl             # Technical debugging info
```

## Results Generation Strategy

### During Analysis (Real-time)
**Orchestrator generates**:
- Raw anchor scores (immediate collection)
- System events (minimal logging)
- Model metadata (costs, timestamps, versions)

### Post-Analysis (Automated)
**Statistical pipeline generates**:
- Bias effect calculations
- Correlation analyses  
- Significance testing
- Cross-model comparisons

### Pre-Publication (Semi-automated)
**Academic pipeline generates**:
- Human-readable summaries
- Publication drafts
- Methodology documentation
- Replication packages

## Implementation Changes Required

### 1. Orchestrator Modifications
**Current**: Saves synthesis discussions and agent conversations
**New**: Saves raw anchor scores and minimal system logs

**Example orchestrator output**:
```python
# Instead of synthesis discussion
self._save_synthesis_discussion(moderator_result, referee_result)

# Save raw bias-focused data
self._save_raw_analysis_data({
    "speech": speech_id,
    "model": model_name, 
    "condition": corpus_condition,
    "pdaf_scores": anchor_scores,
    "metadata": model_metadata
})
```

### 2. Results Processing Pipeline
**New component**: `BiasAnalysisProcessor`
- Reads raw anchor scores
- Generates statistical analysis
- Creates human-readable reports
- Prepares academic materials

### 3. File Organization
**Current**: Single results directory with mixed content
**New**: Experiment-specific results with purpose-built structure

```
experiments/
├── 01_smoketest/results/        # Infrastructure validation
├── 02_single_llm_pilot/results/ # Methodology validation  
├── 03_full_study/results/       # Academic findings
└── active/results/              # Current experiment outputs
```

## Benefits of New Structure

### For Research
- **Bias-focused**: Results directly support bias isolation research
- **Statistical clarity**: Raw data organized for academic analysis
- **Publication-ready**: Outputs align with academic publication needs
- **Reproducible**: Complete provenance without noise

### For Development  
- **Incremental validation**: Each experiment type validates different aspects
- **Clear decision points**: Go/no-go criteria for each phase
- **Cost control**: Understand resource usage at each stage
- **Debug-friendly**: Technical logs separated from research outputs

### For Collaboration
- **Academic standards**: Results format matches publication expectations
- **Transparent methodology**: Complete audit trail for peer review
- **Replication support**: Organized data for independent validation
- **Community adoption**: Clear examples for other researchers

## Migration Strategy

### Phase 1: Implement for Smoketest
- Modify orchestrator to generate infrastructure validation results
- Test new format with minimal scope
- Validate results structure before pilot

### Phase 2: Expand for Pilot
- Add bias analysis pipeline
- Generate statistical outputs
- Validate methodology with single-model test

### Phase 3: Complete for Full Study
- Implement comprehensive academic pipeline
- Generate publication materials
- Create replication packages

This new results structure transforms the Attesor study from process documentation to research outcomes, enabling the academic impact described in the strategic overview. 