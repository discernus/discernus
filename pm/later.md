# Discernus Deferred Items

**Purpose**: Track complex features and approaches that are not immediately actionable but represent future strategic directions.

**Usage**: 
- Items that require significant orchestrator changes
- Complex ensemble approaches that need more research
- Features that would destabilize current working system
- Strategic directions for future major versions

---

## Ensemble Analysis Approaches

### Multi-Model Independent Self-Consistency Analysis

**Description**: Implement independent self-consistency using multiple different LLM models (Claude, GPT-4o, Gemini Pro) with confidence-weighted median aggregation

**Why Deferred**:
- Requires orchestrator changes to manage multiple model APIs
- Significant cost increase (8-12x baseline)
- Complex confidence extraction and weighting logic
- Would destabilize current working analysis pipeline

**Strategic Value**: 
- Maximum accuracy (95-98% of theoretical ceiling)
- Publication-ready methodological rigor
- Systematic error compensation across model architectures

**Implementation Requirements**:
- Multi-model orchestration layer
- Confidence-weighted aggregation system
- Cross-model consensus validation
- Comprehensive statistical validation

**Reference**: See [academic_ensemble_strategy.md](pm/active_projects/academic_ensemble_strategy.md) for detailed methodology

**Timeline**: Future major version (v11+)

---

## Synthesis Enhancement Approaches

### Multi-Report Synthesis Agent

**Description**: Generate 3 different synthesis reports from same analysis data, then use a "report synthesis agent" to combine best aspects of each

**Why Deferred**:
- Requires orchestrator changes to manage multiple synthesis runs
- Adds complexity to synthesis pipeline
- Synthesis variance is manageable with current approach
- Analysis variance is the primary concern

**Strategic Value**:
- Higher quality final reports
- Better coverage of different analytical perspectives
- Reduced synthesis variance through aggregation

**Implementation Requirements**:
- Multiple synthesis orchestration
- Report comparison and selection logic
- Report synthesis agent implementation
- Quality assessment metrics

**Timeline**: Post-analysis variance reduction (Phase 2)

---

## Advanced Statistical Analysis

### Ensemble Statistical Validation

**Description**: Implement statistical analysis using multiple independent runs with consensus validation and outlier detection

**Why Deferred**:
- Requires significant changes to statistical analysis pipeline
- Statistical analysis is currently stable and reliable
- Analysis variance is the primary concern, not statistical analysis variance

**Strategic Value**:
- More robust statistical conclusions
- Better handling of edge cases
- Publication-ready statistical rigor

**Implementation Requirements**:
- Multi-run statistical analysis orchestration
- Consensus measurement and validation
- Outlier detection and filtering
- Statistical significance testing across runs

**Timeline**: Future enhancement phase

---

## CLI Enhancement Features

### Analysis Mode Selection Flag

**Description**: Add CLI flag to allow researchers to choose between single run and internal multi-run analysis modes

**Why Deferred**:
- Current 3-run median aggregation is working well as the default
- Requires CLI argument parsing changes and prompt switching logic
- Need to validate that single-run mode maintains quality
- Should wait until 3-run mode is fully validated across diverse frameworks

**Strategic Value**:
- Flexibility for researchers who prefer single-run analysis
- Cost optimization for preliminary/exploratory experiments
- A/B testing capability between single and multi-run approaches
- Researcher choice and control over analysis depth

**Implementation Requirements**:
- CLI argument parsing for `--analysis-mode` flag
- Dynamic prompt loading (single vs. 3-run prompts)
- Validation that both modes produce compatible output formats
- Documentation of mode differences and use cases
- Cost and quality comparison metrics

**Timeline**: Post-3-run validation across diverse frameworks (Phase 3)

---

## Notes

- **Priority Order**: Analysis variance reduction → Synthesis enhancement → CLI enhancements → Advanced statistical analysis
- **Implementation Strategy**: Start with low-risk internal self-consistency, evaluate results, then consider more complex approaches
- **Risk Assessment**: Current system is working well, avoid changes that could destabilize core functionality
- **Cost-Benefit**: Focus on high-impact, low-risk improvements first
