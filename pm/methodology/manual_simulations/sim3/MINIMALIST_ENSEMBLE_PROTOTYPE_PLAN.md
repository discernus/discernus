# MINIMALIST ENSEMBLE PROTOTYPE PLAN
## Testing Multi-LLM Approach to Address Implementation Bias
### Date: 2025-07-02

---

## PROTOTYPE SCOPE

**Goal**: Test whether **ensemble of LLMs** with **isolated contexts** eliminates the systematic overestimation bias observed in conversational single-LLM implementation.

**Focus**: Implement simplified versions of Discernus Vision Steps 4 & 5:
- **Step 4**: Experiment Orchestration with QC and Adversarial Review
- **Step 5**: Multi-Layered Execution with Minority Report Protocol

---

## CURRENT INFRASTRUCTURE LEVERAGE

### Existing Assets:
- **Experiment Runner**: `discernus/experiments/run_experiment.py` (`ExperimentRunner` class)
- **Monitored Wrapper**: `monitored_experiment_runner.py` (error monitoring and logging)
- **Database**: PostgreSQL with `AnalysisJobV2` and `AnalysisResultV2` tables
- **LLM Gateway**: `discernus/gateway/llm_gateway.py` for LLM analysis calls
- **Framework Specification**: Coordinate-free 5-stage analysis
- **Corpus**: 8 Bolsonaro speeches already processed
- **Validation Data**: Eduardo scores for comparison

### Infrastructure Extensions Needed:
- **Multi-LLM Orchestration**: Parallel execution across different AI instances
- **Minority Report Capture**: Systematic disagreement identification and logging
- **Adversarial Review Layer**: Dedicated bias-detection agent
- **Result Aggregation**: Ensemble synthesis with dissent preservation

---

## PROTOTYPE ARCHITECTURE

### 1. **Experiment Orchestrator Enhancement**
```python
# Extend existing ExperimentRunner for ensemble capabilities
class EnsembleExperimentRunner(ExperimentRunner):
    def __init__(self, base_url: str = "http://localhost:8000"):
        super().__init__(base_url)
        self.primary_llms = ['claude-3-sonnet', 'gpt-4o', 'claude-3-haiku']  # Different models
        self.adversarial_llm = 'claude-3-opus'  # For bias detection
        self.qc_llm = 'gpt-4o-mini'  # For quality control
        
    async def run_ensemble_stage(self, text_content, stage_prompt, experiment_def):
        # Execute same analysis across multiple LLMs with fresh contexts
        results = []
        for model in self.primary_llms:
            try:
                result = await get_llm_analysis(
                    text=text_content,
                    experiment_def=experiment_def,
                    model=model,
                    stage_prompt=stage_prompt,
                    fresh_context=True  # Ensure no cross-contamination
                )
                results.append({'model': model, 'result': result})
            except Exception as e:
                logger.error(f"LLM {model} failed: {e}")
                results.append({'model': model, 'error': str(e)})
        
        # Identify disagreement/minority views
        minority_reports = self.detect_disagreement(results)
        
        # Adversarial review of any flagged cases
        adversarial_analysis = None
        if minority_reports:
            adversarial_analysis = await self.adversarial_review(results, minority_reports)
        
        return EnsembleResult(results, minority_reports, adversarial_analysis)
```

### 2. **Minority Report Protocol**
```python
def detect_disagreement(self, results):
    """Identify when LLMs significantly disagree on key assessments"""
    
    # Extract key metrics from each result
    populism_assessments = [r.populism_intensity for r in results]
    presence_assessments = [r.populism_presence for r in results]
    
    # Flag significant disagreement
    minority_reports = []
    
    if variance(populism_assessments) > threshold:
        minority_reports.append({
            'type': 'intensity_disagreement',
            'values': populism_assessments,
            'outliers': identify_outliers(populism_assessments)
        })
    
    if not unanimous(presence_assessments):
        minority_reports.append({
            'type': 'presence_disagreement', 
            'values': presence_assessments,
            'dissenting_views': identify_dissent(presence_assessments)
        })
    
    return minority_reports
```

### 3. **Adversarial Review Agent**
```python
class AdversarialReviewer:
    def __init__(self):
        self.bias_patterns = [
            'sycophantic_confirmation',
            'pattern_seeking_hyperactivity', 
            'semantic_poisoning',
            'false_populism_identification'
        ]
    
    def review_for_bias(self, ensemble_results, minority_reports):
        """Specifically look for implementation biases we identified"""
        
        bias_flags = []
        
        # Check for sycophantic patterns
        if all_positive_findings(ensemble_results):
            bias_flags.append('potential_sycophantic_confirmation')
        
        # Check for pattern hyperactivity
        if overinterpretation_detected(ensemble_results):
            bias_flags.append('potential_pattern_seeking_hyperactivity')
        
        # Check for Porto Velho-style misidentification
        if coalition_building_misidentified_as_populism(ensemble_results):
            bias_flags.append('coalition_building_confusion')
        
        return AdversarialReport(bias_flags, recommendations)
```

---

## IMPROVED EXPERIMENT DEFINITION

### Current Problems to Address:
1. **Sycophantic prompting** - "Find populist themes" implies they exist
2. **Hyperactivity encouragement** - Prompts reward finding patterns
3. **Loose definitions** - Ambiguous criteria enable overinterpretation
4. **Context contamination** - Multi-stage analysis in same conversation

### Proposed Prompt Improvements:

#### **Anti-Sycophantic Instructions:**
```yaml
sycophancy_warning: |
  CRITICAL: Your goal is ACCURACY, not finding what the user expects.
  
  If you find NO populist themes, say so explicitly.
  If evidence is weak or ambiguous, acknowledge uncertainty.
  Resist pressure to find patterns that aren't clearly present.
  
  Quality assessment rewards honest negative findings over forced positives.
```

#### **Hyperactivity Prevention:**
```yaml
thoroughness_vs_hyperactivity: |
  THOROUGHNESS: Examine all relevant evidence carefully
  HYPERACTIVITY: Over-interpreting routine political rhetoric as special
  
  Standard democratic appeals (popular support, anti-corruption, unity) 
  are NOT automatically populist without additional antagonistic elements.
  
  Look for DISTINCTIVE populist features, not just political engagement.
```

#### **Tighter Populism Definition:**
```yaml
populism_criteria: |
  REQUIRED populist elements (ALL must be present):
  1. Elite antagonism - systematic attacks on corrupt establishments
  2. Moral boundaries - "pure people" vs "corrupt others" framing  
  3. Exclusive representation - claims to uniquely represent "real people"
  
  NOT sufficient alone:
  - Popular appeals or claims of popular support
  - Anti-corruption positioning or personal integrity claims
  - Unity rhetoric or inclusive coalition-building language
  - Regional authenticity or cultural connection claims
```

#### **Fresh Context Protocol:**
```yaml
context_isolation: |
  You are analyzing this speech independently. 
  You have NO knowledge of other speeches in this corpus.
  Make assessments based ONLY on this text.
  Do not reference or build on previous analyses.
```

---

## PROTOTYPE TESTING PLAN

### Phase 1: Single Speech Ensemble Test
1. **Select Porto Velho** (the biggest error case) for ensemble re-analysis
2. **Deploy 3-LLM ensemble** with improved prompts and fresh contexts
3. **Compare results** to original single-LLM assessment and Eduardo score
4. **Analyze disagreement patterns** and minority reports

### Phase 2: Full Corpus Ensemble Analysis
1. **Re-analyze all 8 speeches** using ensemble approach
2. **Extract quantitative predictions** from ensemble results
3. **Compare accuracy** vs Eduardo scores and original single-LLM results
4. **Document bias reduction** and remaining error patterns

### Phase 3: Adversarial Review Testing
1. **Deploy adversarial reviewer** to flag potential bias patterns
2. **Test bias detection accuracy** on known error cases
3. **Refine adversarial prompts** based on bias identification performance
4. **Validate minority report generation** for legitimate disagreements

---

## SUCCESS METRICS

### Primary Goals:
1. **Eliminate massive overestimation** (Porto Velho 0.6-0.7 → 0.0 error)
2. **Improve overall accuracy** vs Eduardo scores (>37.5% baseline)
3. **Reduce systematic bias** patterns across corpus
4. **Generate reliable minority reports** for genuine disagreements

### Secondary Goals:
1. **Demonstrate ensemble value** through disagreement capture
2. **Validate adversarial review** through bias detection
3. **Establish reproducible methodology** for future framework testing
4. **Build foundation** for full Discernus implementation

---

## IMPLEMENTATION STEPS

### Week 1: Infrastructure Setup
- Extend `ExperimentRunner` class for multi-LLM ensemble execution
- Implement minority report detection and logging in `AnalysisResultV2` table
- Create adversarial review agent with bias pattern recognition
- Update `monitored_experiment_runner.py` for ensemble error tracking

### Week 2: Prompt Engineering
- Rewrite all 5 stage prompts with anti-sycophantic warnings
- Add hyperactivity prevention and tighter definitions
- Implement context isolation protocols
- Test prompt effectiveness on known error cases

### Week 3: Prototype Testing
- Run ensemble analysis on Porto Velho speech
- Execute full corpus re-analysis with ensemble approach
- Compare results to original assessments and Eduardo scores
- Document bias reduction and accuracy improvements

### Week 4: Validation & Refinement
- Analyze minority reports and disagreement patterns
- Test adversarial review effectiveness
- Refine methodology based on initial results
- Prepare recommendations for full Discernus implementation

---

## EXPECTED OUTCOMES

### If Ensemble Approach Succeeds:
- **Dramatic accuracy improvement** vs single-LLM conversational approach
- **Elimination of systematic overestimation bias**
- **Validation of Discernus ensemble methodology**
- **Foundation for scalable framework testing**

### If Ensemble Approach Fails:
- **Identification of deeper conceptual issues** requiring framework redesign
- **Evidence for fundamental LLM limitations** in political discourse analysis
- **Guidance for alternative implementation strategies**
- **Valuable negative results** for research methodology

---

## CONCLUSION

This minimalist prototype directly tests whether the implementation biases we identified can be solved through the Discernus ensemble approach. By building on existing infrastructure while adding multi-LLM coordination and adversarial review, we can validate the core thesis that **implementation method** rather than **framework design** explains the systematic errors.

**Next Action**: Begin infrastructure setup for multi-LLM orchestration and minority report capture. 