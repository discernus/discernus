# Evidence Index: Narrative Gravity Maps Paper

This document tracks all evidence supporting the paper "Narrative Gravity Maps: A Quantitative Framework for Discerning the Forces Driving Persuasive Narratives."

## Evidence Organization

### technical_validation/
**Purpose**: Documents technical implementation reliability and cross-LLM consistency
**Status**: ✅ Available for v1.0.0

#### Available Files:
- `system_test_results.json` - 99.5% test success rate documentation
- `cross_llm_correlation_matrix.json` - Correlation coefficients (r > 0.90) across GPT-4, Claude-4, Llama-3, Mixtral-8x7B
- `multi_run_statistical_analysis.json` - Variance analysis and confidence intervals

#### Paper Sections Supported:
- Abstract: "Technical implementation demonstrates cross-model consistency with correlation coefficients exceeding 0.90"
- Section 5.5: "Inter-Model Correlation Results"
- Section 6.1.1: "What Has Been Validated: Technical Consistency"

### case_studies/
**Purpose**: Analyzed political speeches demonstrating framework application
**Status**: ✅ Available for v1.0.0

#### Available Analyses:
- `trump_2017_inaugural_analysis.json` - Complete Civic Virtue Framework analysis
- `biden_2021_inaugural_analysis.json` - Comparative analysis with Trump
- `obama_2009_inaugural_multirun.json` - Multi-run statistical validation
- `comparative_distance_metrics.json` - Elliptical distance calculations

#### Paper Sections Supported:
- Section 5.2: "Individual Analysis: Trump's Second Inaugural Address"
- Section 5.3: "Statistical Reliability Analysis: Obama 2009 Inaugural Speech"
- Section 5.4: "Comparative Analysis: Trump vs. Biden Inaugural Addresses"

### figures/
**Purpose**: Visualizations and charts for paper presentation
**Status**: ✅ Available for v1.0.0

#### Available Visualizations:
- `civic_virtue_framework_diagram.png` - Framework well positioning
- `trump_vs_biden_comparison.png` - Comparative positioning analysis
- `obama_multirun_dashboard.png` - Statistical reliability visualization
- `elliptical_coordinate_system.png` - Mathematical framework diagram

### validation_studies/ 
**Purpose**: Human validation studies comparing LLM outputs to expert judgment
**Status**: ❌ CRITICAL GAP - Required for v1.1.0

#### Required Studies:
- **Expert Annotation Study**: Human experts score same texts using framework
- **Inter-Rater Reliability**: Agreement between human experts
- **Human-LLM Comparison**: Correlation between human and LLM scoring
- **Salience Ranking Validation**: Human vs. LLM theme prioritization
- **Cross-Cultural Validation**: Framework applicability across contexts

#### Planned Files:
- `expert_annotation_protocol.md` - Study design and procedures
- `expert_annotation_results.json` - Raw annotation data
- `human_llm_correlation_analysis.json` - Alignment statistics
- `inter_rater_reliability_results.json` - Human expert agreement
- `salience_ranking_comparison.json` - Theme prioritization validation

## Evidence Quality Standards

### Acceptable Evidence Criteria:
1. **Reproducible**: All analysis code and data available
2. **Documented**: Clear methodology and parameter specification  
3. **Quantified**: Statistical measures with confidence intervals
4. **Contextual**: Appropriate caveats and limitations noted

### Evidence Collection Checklist:
- [ ] Raw data files with clear provenance
- [ ] Analysis code with version information
- [ ] Statistical summaries with confidence intervals
- [ ] Methodology documentation
- [ ] Limitation acknowledgments
- [ ] Link to specific paper sections supported

## Current Evidence Status for Publication

### ✅ SUFFICIENT for Technical Consistency Claims:
- Cross-LLM reliability data
- System stability metrics
- Mathematical framework validation
- Case study demonstrations

### ❌ INSUFFICIENT for Human Alignment Claims:
- **No expert annotation studies**
- **No inter-rater reliability data**
- **No human-LLM correlation analysis**
- **No cross-cultural validation**

### ⚠️ MODERATE Evidence for Methodological Claims:
- Framework theoretical justification (needs peer review)
- Differential weighting rationale (needs expert validation)
- Case study interpretations (needs human validation)

## Evidence Gaps Analysis

### Critical for v1.1.0 (Human Validation):
1. **Expert Annotation Study** - At least 20 experts scoring 50+ texts
2. **Inter-Rater Reliability** - Cronbach's α > 0.80 required
3. **Human-LLM Correlation** - Pearson r analysis with significance testing
4. **Thematic Salience Validation** - Ranking correlation analysis

### Important for v1.2.0 (Generalizability):
1. **Cross-Cultural Studies** - Non-Western expert validation
2. **Temporal Consistency** - Historical text analysis
3. **Domain Adaptation** - Non-political narrative validation
4. **Framework Comparison** - Alternative moral frameworks tested

### Nice-to-Have for v1.3.0 (Robustness):
1. **Large-Scale Validation** - 1000+ text corpus
2. **Expert Consensus Studies** - Delphi methodology
3. **Longitudinal Tracking** - Framework stability over time
4. **Predictive Validation** - Outcome correlation studies

## Evidence Management Protocol

### Adding New Evidence:
1. Create appropriately named file with date stamp
2. Update this EVIDENCE_INDEX.md 
3. Link to relevant paper sections in PAPER_CHANGELOG.md
4. Ensure replication instructions included

### Quality Check Before Paper Version Update:
- [ ] All claims in paper have corresponding evidence files
- [ ] Evidence quality meets academic standards
- [ ] Statistical analyses include confidence intervals
- [ ] Limitations appropriately acknowledged
- [ ] Evidence supports conclusions (no overclaims)

---

*This evidence index ensures that every claim in the paper is backed by appropriate supporting materials and that evidence gaps are clearly identified for future research priorities.* 