# 05: Statistical Comparison MVP Fixes & Extensions

## Executive Summary

Based on the cranky-but-correct feedback from our statistical review, this document outlines the minimum viable fixes required to legitimately answer the research question "*Do different flagship cloud LLMs produce statistically similar results for a substantive text?*" plus extra credit extensions for robust research infrastructure.

## Current State Assessment

### ✅ What We Built Right
- **Solid Engineering Foundation**: PostgreSQL persistence, FastAPI endpoints, concurrent execution
- **Database Schema**: Advanced V2 schema with proper job/result tracking
- **Multi-Model Pipeline**: Can run multiple models on same text concurrently
- **Visualization Infrastructure**: Report generation with dual-model circular plots
- **Well-Organized Corpus**: 32 validation texts across 6 categories in `src/reboot/corpus/validation_set/`

### ❌ Critical Statistical Deficiencies
1. **Cheap Models, Not Flagship**: Currently using `gpt-4o-mini` and `gpt-3.5-turbo` (budget models)
2. **No Statistical Testing**: Just Euclidean distance calculations, no hypothesis testing
3. **Arbitrary Similarity Thresholds**: No empirical basis for "similar" vs "different" classifications
4. **Single-Text Analysis**: Not statistically valid sample sizes
5. **Missing Statistical Persistence**: `StatisticalComparison` table empty despite claims

### 🔧 Technical Issues
1. **Incomplete Statistical Methods**: 60% are `NotImplementedError` stubs
2. **Database Consistency**: Analysis results stored but statistical conclusions aren't
3. **No Validation Framework**: No tests against known datasets

## Research Question Breakdown

**Target Question**: *"Do different flagship cloud LLMs produce statistically similar results for a substantive text?"*

**What "Flagship" Actually Means**:
- OpenAI: `gpt-4o` (full, not mini)
- Anthropic: `claude-3-5-sonnet-20241022` 
- Google: `gemini-1.5-pro`
- NOT: `gpt-4o-mini`, `gpt-3.5-turbo`, `claude-haiku`

**What "Statistically Similar" Actually Means**:
- Hypothesis testing with p-values
- Effect size measurements (Cohen's d)
- Confidence intervals
- Power analysis
- NOT: "Distance < 0.1 looks similar"

## Minimum Viable Fixes (MVP)

### Phase 1: Fix the Statistical Persistence Bug (Week 1)
**Priority**: CRITICAL - Data integrity failure

**Current Problem**: 
```python
# Analysis results are being saved...
db.add_all(db_results_to_save)
db.commit()

# But statistical comparisons are NOT being saved!
# No StatisticalComparison records in database
```

**Fix Required**:
```python
# After statistical analysis, persist the results
statistical_comparison = StatisticalComparison(
    id=str(uuid.uuid4()),
    comparison_type=request.comparison_type,
    source_job_ids=[job_id],
    comparison_dimension="model",
    similarity_metrics=final_statistical_metrics,
    significance_tests=statistical_tests,
    similarity_classification=classification,
    confidence_level=confidence
)
db.add(statistical_comparison)
db.commit()
```

**Deliverable**: All statistical comparisons properly persisted to database

### Phase 2: Implement Real Statistical Tests (Week 2)
**Priority**: CRITICAL - Core research validity

**Current Problem**: 
```python
# This is NOT statistics
mean_distance = np.mean(distances)
if mean_distance < 0.1:
    classification = "SIMILAR"  # Says who?
```

**Required Statistical Methods**:

1. **Paired t-test for Centroid Differences**:
```python
def test_centroid_similarity(centroids_a, centroids_b):
    """Test if two sets of centroids are statistically similar"""
    # Paired t-test for x and y coordinates
    t_stat_x, p_val_x = stats.ttest_rel([c[0] for c in centroids_a], 
                                        [c[0] for c in centroids_b])
    t_stat_y, p_val_y = stats.ttest_rel([c[1] for c in centroids_a], 
                                        [c[1] for c in centroids_b])
    
    # Bonferroni correction for multiple comparisons
    alpha = 0.05 / 2  # Corrected alpha
    
    return {
        'x_axis': {'t_stat': t_stat_x, 'p_value': p_val_x, 'significant': p_val_x < alpha},
        'y_axis': {'t_stat': t_stat_y, 'p_value': p_val_y, 'significant': p_val_y < alpha},
        'overall_similar': p_val_x >= alpha and p_val_y >= alpha
    }
```

2. **Effect Size Calculation (Cohen's d)**:
```python
def calculate_effect_size(group_a, group_b):
    """Calculate Cohen's d for effect size"""
    pooled_std = np.sqrt(((len(group_a) - 1) * np.var(group_a) + 
                         (len(group_b) - 1) * np.var(group_b)) / 
                        (len(group_a) + len(group_b) - 2))
    
    cohens_d = (np.mean(group_a) - np.mean(group_b)) / pooled_std
    
    # Cohen's interpretation
    if abs(cohens_d) < 0.2:
        interpretation = "negligible"
    elif abs(cohens_d) < 0.5:
        interpretation = "small"
    elif abs(cohens_d) < 0.8:
        interpretation = "medium"
    else:
        interpretation = "large"
    
    return {'cohens_d': cohens_d, 'interpretation': interpretation}
```

3. **Confidence Intervals**:
```python
def calculate_confidence_intervals(data, confidence=0.95):
    """Calculate confidence intervals for means"""
    n = len(data)
    mean = np.mean(data)
    std_err = stats.sem(data)
    t_val = stats.t.ppf((1 + confidence) / 2, n - 1)
    
    margin_error = t_val * std_err
    return {
        'mean': mean,
        'ci_lower': mean - margin_error,
        'ci_upper': mean + margin_error,
        'confidence_level': confidence
    }
```

**Deliverable**: Replace distance-based similarity with proper statistical testing

### Phase 3: Use Flagship Models (Week 3)
**Priority**: HIGH - Research question validity

**Current Problem**: Comparing budget models, not flagship ones

**Model Upgrade Plan**:
```python
FLAGSHIP_MODELS = {
    "openai_flagship": "gpt-4o",              # NOT gpt-4o-mini
    "anthropic_flagship": "claude-3-5-sonnet-20241022",  # NOT claude-haiku
    "google_flagship": "gemini-1.5-pro",     # NOT gemini-flash
    "meta_flagship": "llama-3.1-405b"        # Via Together AI or similar
}

BUDGET_MODELS = {
    "openai_budget": "gpt-4o-mini",
    "anthropic_budget": "claude-3-5-haiku-20241022", 
    "google_budget": "gemini-1.5-flash"
}
```

**Cost Implications**:
- Flagship models: ~$0.01-0.03 per text analysis
- Budget models: ~$0.001-0.003 per text analysis
- For 32 texts × 4 models = 128 analyses: ~$1.28-3.84 (flagship) vs ~$0.13-0.38 (budget)

**Deliverable**: Multi-flagship model comparison capability

### Phase 4: Multi-Text Statistical Analysis (Week 4)
**Priority**: HIGH - Statistical validity requires proper sample sizes

**Current Problem**: Single-text comparisons aren't statistically valid

**Solution**: Corpus-Based Statistical Analysis

```python
async def run_corpus_statistical_comparison(
    corpus_path: str = "src/reboot/corpus/validation_set",
    models: List[str] = ["gpt-4o", "claude-3-5-sonnet-20241022"],
    sample_size: int = 20  # Minimum for statistical validity
):
    """
    Run statistical comparison across multiple texts
    """
    # Load random sample of texts from corpus
    text_files = list(Path(corpus_path).rglob("*.txt"))
    sample_texts = random.sample(text_files, min(sample_size, len(text_files)))
    
    # Run all model×text combinations
    results = []
    for text_file in sample_texts:
        text_content = text_file.read_text()
        for model in models:
            result = await analyze_text(text_content, model)
            results.append({
                'text_id': text_file.stem,
                'model': model,
                'centroid': result['centroid'],
                'scores': result['scores']
            })
    
    # Group by model for statistical comparison
    model_results = {}
    for result in results:
        model = result['model']
        if model not in model_results:
            model_results[model] = []
        model_results[model].append(result)
    
    # Run statistical tests
    return run_pairwise_statistical_tests(model_results)
```

**Deliverable**: Multi-text statistical comparison capability

## Extra Credit Extensions

### Extension 1: Academic Research Pipeline
**Research Question**: *"How do flagship LLMs compare across different political discourse categories?"*

**Implementation**:
1. **Stratified Sampling**: Sample texts from each category (conservative_dignity, progressive_tribalism, etc.)
2. **ANOVA Testing**: Test for significant differences across categories
3. **Post-hoc Analysis**: Identify where specific differences occur
4. **Academic Reporting**: Generate research-ready statistical reports

### Extension 2: Temporal Stability Analysis
**Research Question**: *"Do LLM results remain consistent across multiple runs?"*

**Implementation**:
1. **Repeated Measures**: Run same text through same model 5-10 times
2. **Intra-class Correlation**: Measure consistency within models
3. **Reliability Analysis**: Calculate Cronbach's alpha for internal consistency

### Extension 3: Cross-Framework Validation
**Research Question**: *"Do different analytical frameworks yield consistent model rankings?"*

**Implementation**:
1. **Multi-Framework Analysis**: Run same texts through civic_virtue, moral_foundations, etc.
2. **Rank Correlation**: Compare model rankings across frameworks
3. **Framework Sensitivity**: Identify which frameworks are most discriminating

### Extension 4: Cost-Effectiveness Analysis
**Research Question**: *"What's the optimal balance between model quality and cost?"*

**Implementation**:
1. **Quality Metrics**: Measure consistency, distinctiveness, interpretability
2. **Cost Tracking**: Precise per-analysis cost calculations
3. **ROI Analysis**: Quality points per dollar spent

### Extension 5: Human-AI Comparison
**Research Question**: *"How do LLM analyses compare to human expert annotations?"*

**Implementation**:
1. **Expert Annotation**: Get human ratings for subset of texts
2. **Inter-rater Reliability**: Measure human consistency first
3. **Human-AI Correlation**: Compare LLM results to human consensus

## Implementation Roadmap

### Sprint 1 (Week 1): Critical Bug Fixes
- [ ] Fix StatisticalComparison persistence bug
- [ ] Add proper error handling for statistical calculations
- [ ] Implement basic statistical testing framework

### Sprint 2 (Week 2): Statistical Methods
- [ ] Implement paired t-tests for centroid comparison
- [ ] Add effect size calculations (Cohen's d)
- [ ] Create confidence interval calculations
- [ ] Replace arbitrary thresholds with statistical significance

### Sprint 3 (Week 3): Flagship Model Integration
- [ ] Add flagship model configurations 
- [ ] Implement cost tracking for expensive models
- [ ] Add model tier selection (flagship vs budget)
- [ ] Test with actual flagship models

### Sprint 4 (Week 4): Multi-Text Analysis
- [ ] Implement corpus sampling strategies
- [ ] Add multi-text statistical comparison
- [ ] Create proper experimental controls
- [ ] Generate research-quality reports

### Sprint 5+ (Extensions): Research Pipeline
- [ ] Choose and implement 1-2 extra credit extensions
- [ ] Add academic export functionality
- [ ] Create publication-ready visualizations

## Success Criteria

### Minimum Viable Product (MVP)
- [ ] **Statistical Rigor**: Real hypothesis testing with p-values, effect sizes, confidence intervals
- [ ] **Flagship Models**: Actual comparison of top-tier models, not budget alternatives  
- [ ] **Proper Sample Sizes**: Multi-text analysis with n≥20 for statistical validity
- [ ] **Data Integrity**: All statistical results properly persisted and reproducible
- [ ] **Clear Classification**: Evidence-based similarity thresholds, not arbitrary cutoffs

### Extra Credit Success
- [ ] **Academic Quality**: Research-grade methodology suitable for peer review
- [ ] **Reproducibility**: Complete experimental controls and documentation
- [ ] **Practical Impact**: Actionable insights about model selection and usage
- [ ] **Cost Efficiency**: Optimal balance between analytical quality and resource usage

## Risk Mitigation

### Technical Risks
- **Statistical Method Accuracy**: Validate against known datasets and literature
- **Model API Reliability**: Implement retry logic and fallback strategies
- **Cost Control**: Set spending limits and monitoring for flagship model usage

### Research Risks
- **Multiple Comparisons**: Apply appropriate corrections (Bonferroni, FDR)
- **Publication Bias**: Pre-register hypotheses and report all results
- **Overfitting**: Use cross-validation and hold-out test sets

## Next Steps

1. **Immediate**: Fix the StatisticalComparison persistence bug (30 minutes)
2. **This Week**: Implement proper statistical tests (2-3 days)
3. **Next Week**: Upgrade to flagship models and test cost implications
4. **Following Week**: Implement multi-text analysis pipeline
5. **Month 2**: Choose and implement 1-2 extra credit extensions

This plan transforms the current "engineering demo" into a legitimate research tool that can actually answer the statistical questions we claim to address. 