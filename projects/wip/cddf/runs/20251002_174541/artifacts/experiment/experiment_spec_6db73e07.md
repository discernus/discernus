# CDDF v10.2 Mode Validation Experiment

**Experiment ID**: cddf_mode_validation
**Created**: 2025-10-01
**Framework**: CDDF v10.2.0
**Purpose**: Test hypothesis that spontaneous discourse exhibits restraint failures absent in formal speeches

## Research Questions

**Primary:** Does the strategy-inventory gap differ systematically between formal and spontaneous discourse genres?

**Secondary:**
1. Do restraint failure metrics correlate with discourse genre?
2. Does the framework's modal interpretation improve corpus fit scores?
3. Are dimensional profiles stable across genres, or do genres enable different rhetorical tactics?

## Hypotheses

**Hâ‚ (Genre Differentiation):** Spontaneous discourse will show significantly higher strategy-inventory gaps than formal discourse (Cohen's d > 0.8).

**Hâ‚‚ (Contamination Detection):** Rhetorical contamination index will be significantly higher in spontaneous discourse (Mann-Whitney U test, p < .05).

**Hâ‚ƒ (Mode-Appropriate Fit):** Framework-corpus fit scores will be higher when mode matches genre (formal mode for speeches, spontaneous mode for debates).

**Hâ‚„ (Dimensional Stability):** Core dimensional correlations (constructive cluster, destructive cluster) will remain consistent across genres, validating framework structure.

**Hâ‚… (Restraint Intensity):** When contamination occurs in spontaneous discourse, restraint_failure_intensity will be moderate (0.4-0.6), suggesting lapses rather than strategic destructiveness.

## Corpus Design

### Required Corpus (N=20)

**Formal Discourse Group (N=10):**
- 5 inaugural addresses (high message discipline)
- 3 prepared floor speeches (moderate message discipline)
- 2 written op-eds (highest message discipline)

*Selection Criteria:* Text verified as delivered from prepared script, no ad-libs

**Spontaneous Discourse Group (N=10):**
- 4 primary debate exchanges (opening statement + rebuttal + response)
- 3 town hall Q&A exchanges (question + answer + follow-up)
- 3 Twitter/X thread collections (initial tweet + replies to critics)

*Selection Criteria:* Real-time production, no script, includes reactive/responsive elements

### Corpus Balance Requirements

**Ideological Balance:** Each group should contain:
- 3-4 progressive/left speakers
- 3-4 conservative/right speakers
- 2-3 centrist/establishment speakers

**Temporal Balance:** Each group should span:
- 3-4 texts from 2015-2020
- 3-4 texts from 2021-2025
- 2-3 texts from 2008-2014

**Topic Balance:** Texts should address comparable policy domains to control for content effects:
- Economic policy (4 texts across both groups)
- Social policy (4 texts across both groups)
- Foreign policy (4 texts across both groups)
- Other (8 texts across both groups)

## Methodology

### Experimental Design

**Design Type:** Between-subjects quasi-experimental design with matched content controls

**Independent Variable:** Discourse Genre (Formal vs. Spontaneous)

**Dependent Variables:**
- Primary: `strategy_inventory_gap`
- Secondary: `rhetorical_contamination_index`, `restraint_failure_intensity`, framework fit score

**Control Variables:** Ideology, time period, policy domain (balanced across groups)

### Analysis Plan

**Stage 1: Baseline Validation (Formal Mode Analysis of Formal Corpus)**
- Analyze 10 formal texts using formal_speech mode
- Expected: Low strategy-inventory gaps (M < 0.1)
- Expected: High framework-corpus fit (> 0.5)
- Validates v10.1 findings

**Stage 2: Mode Hypothesis Test (Spontaneous Mode Analysis of Spontaneous Corpus)**
- Analyze 10 spontaneous texts using spontaneous_discourse mode
- Expected: Elevated strategy-inventory gaps (M > 0.2)
- Expected: High rhetorical contamination indices (M > 0.3)
- Tests central hypothesis

**Stage 3: Cross-Mode Comparison**
- Compare Stage 1 and Stage 2 results
- Statistical tests:
  - Mann-Whitney U for strategy-inventory gap comparison
  - Effect size (Cohen's d) for gap magnitude
  - Chi-square for contamination presence/absence
  - Spearman correlation between genre and restraint metrics

**Stage 4: Mode-Mismatch Control**
- Analyze formal corpus with spontaneous mode
- Analyze spontaneous corpus with formal mode
- Expected: Framework fit scores decline when mode mismatched
- Validates mode-specific interpretation

### Statistical Power

**Sample Size Justification (N=20, 10 per group):**
- Power = 0.80 for detecting large effects (d > 0.8) at α = .05
- Adequate for Mann-Whitney U tests with expected large effects
- Sufficient for correlation analysis (stable at N=20)
- Pilot study sizing for future larger validation

**Statistical Approach:**
- Non-parametric tests (no normality assumption)
- Effect sizes always reported
- 95% confidence intervals for all point estimates
- Bonferroni correction for multiple comparisons (α = .05/5 = .01 for 5 tests)

## Expected Outcomes

### Quantitative Predictions

**Formal Discourse (Formal Mode):**
- Strategy-Inventory Gap: M = 0.03 (SD = 0.05), consistent with v10.1
- Rhetorical Contamination Index: M = 0.10 (SD = 0.08)
- Framework Fit: 0.65 (adequate fit with appropriate mode)

**Spontaneous Discourse (Spontaneous Mode):**
- Strategy-Inventory Gap: M = 0.25 (SD = 0.12), significantly higher
- Rhetorical Contamination Index: M = 0.38 (SD = 0.15), elevated
- Framework Fit: 0.70 (strong fit with appropriate mode)

**Effect Sizes:**
- Cohen's d for gap difference: 2.5 (very large effect)
- Mann-Whitney U: p < .001 (highly significant)

### Qualitative Predictions

**Pattern 1 - Opening Statement Discipline:**
Debate opening statements will show formal-like coherence (low contamination), but rebuttals will show elevated contamination as speakers respond to attacks.

**Pattern 2 - Platform Dependency:**
Twitter threads will show highest contamination in replies (reactive) compared to initial tweets (composed).

**Pattern 3 - Individual Variation:**
Some speakers maintain discipline even in spontaneous settings. Framework will identify these as low-gap outliers.

## Success Criteria

**Technical Success:**
- All 20 documents successfully scored
- Mode parameters correctly applied
- Fit scores calculated for each mode-genre combination

**Statistical Success:**
- Hâ‚ confirmed: d > 0.8 for strategy-inventory gap difference
- Hâ‚‚ confirmed: p < .05 for contamination index difference
- Hâ‚ƒ confirmed: Fit scores higher when mode matches genre

**Theoretical Success:**
- Hâ‚„ confirmed: Dimensional structure stable across genres
- Findings interpretable through genre theory and message discipline research

**Framework Validation Success:**
- v10.2 modes demonstrably useful (not just conceptually)
- Clear guidance emerges for future mode selection
- Any limitations identified and documented

## Experiment Specification

```yaml
# --- Machine-Readable Experiment Spec ---

metadata:
  experiment_name: "cddf_mode_validation"
  experiment_id: "cddf_v10_2_mode_test"
  author: "Discernus Research Team"
  created: "2025-10-01"
  framework_version: "10.2.0"
  spec_version: "10.0"

components:
  framework: "cddf_v10_2.md"
  corpus: "mode_validation_corpus.md"  # To be assembled

# CRITICAL: Mode specification
analysis_configuration:
  # Stage 1: Formal corpus, formal mode
  stage_1_formal:
    mode: "formal_speech"
    corpus_filter: "genre:formal"
    expected_fit_threshold: 0.5
    
  # Stage 2: Spontaneous corpus, spontaneous mode  
  stage_2_spontaneous:
    mode: "spontaneous_discourse"
    corpus_filter: "genre:spontaneous"
    expected_fit_threshold: 0.6
    
  # Stage 3: Cross-mode controls
  stage_3_formal_spontaneous_mode:
    mode: "spontaneous_discourse"
    corpus_filter: "genre:formal"
    expected_fit_threshold: 0.2  # Expect poor fit
    
  stage_3_spontaneous_formal_mode:
    mode: "formal_speech"
    corpus_filter: "genre:spontaneous"
    expected_fit_threshold: 0.2  # Expect poor fit

reliability_filtering:
  salience_threshold: 0.0
  confidence_threshold: 0.0
  reliability_threshold: 0.0
  reliability_calculation: "confidence_x_salience"
  framework_fit_required: true
  framework_fit_threshold: 0.3

statistical_analysis:
  primary_comparison:
    test: "mann_whitney_u"
    groups: ["formal", "spontaneous"]
    dependent_variable: "strategy_inventory_gap"
    alpha: 0.01  # Bonferroni corrected
    
  secondary_comparisons:
    - test: "mann_whitney_u"
      groups: ["formal", "spontaneous"]
      dependent_variable: "rhetorical_contamination_index"
      alpha: 0.01
      
  effect_sizes:
    - cohens_d: ["strategy_inventory_gap", "rhetorical_contamination_index"]
    - rank_biserial: ["all_continuous_variables"]
    
  correlations:
    - spearman: 
        variables: ["genre", "strategy_inventory_gap", "contamination_index"]
        
  framework_validation:
    - compare_fit_scores:
        stage_1: "formal_formal_mode"
        stage_2: "spontaneous_spontaneous_mode"
        stage_3a: "formal_spontaneous_mode"
        stage_3b: "spontaneous_formal_mode"

# --- End Machine-Readable Spec ---
```

## Risk Mitigation

**Risk 1: Genre Ambiguity**
- Mitigation: Strict inclusion criteria, multiple reviewers for classification
- Contingency: Hybrid mode for ambiguous cases, sensitivity analysis

**Risk 2: Small Sample Size**
- Mitigation: Large expected effect sizes, non-parametric tests
- Contingency: Report findings as exploratory if underpowered

**Risk 3: Content Confounding**
- Mitigation: Topic balance across groups
- Contingency: Content analysis as covariate

**Risk 4: Platform Effects**
- Mitigation: Limit Twitter to ~30% of spontaneous group
- Contingency: Platform subgroup analysis if effects detected

## Timeline & Deliverables

**Phase 1 (Week 1):** Corpus assembly and validation
**Phase 2 (Week 2):** Stage 1 & 2 analysis execution
**Phase 3 (Week 3):** Stage 3 & 4 analysis, statistical testing
**Phase 4 (Week 4):** Report generation and framework revision

**Deliverables:**
1. Complete dimensional scores for all 20 texts
2. Statistical comparison report with effect sizes
3. Framework fit assessment across all mode-genre combinations
4. Recommendations for v10.3 (if needed) or validation of v10.2