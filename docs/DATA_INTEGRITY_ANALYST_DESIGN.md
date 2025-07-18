# DataIntegrityAnalyst Agent Design

**Status:** 🟡 PROPOSED  
**Priority:** High  
**Architectural Impact:** Significant (adds quality gate to workflow)

## Problem Statement

While we've fixed the immediate synthesis agent data contamination issue, we identified a broader architectural concern: **data quality assurance should happen before statistical analysis, not during it**.

### Current Risk Factors
- Failed analysis runs create incomplete datasets
- Missing `json_output` fields can cause extraction errors  
- Invalid score ranges (outside 0.0-1.0) could skew statistics
- Duplicate runs could artificially inflate sample sizes
- No visibility into data quality issues until analysis fails

## Proposed Solution: DataIntegrityAnalyst Agent

### Core Responsibility
**"Ensure experimental data meets quality standards before statistical analysis"**

### THIN Architecture Alignment
- ✅ **Single Responsibility:** Data quality validation only
- ✅ **Framework Agnostic:** Works with any experimental data structure
- ✅ **LLM Intelligence:** AI determines data quality patterns and issues
- ✅ **Thin Software:** Simple routing and validation logic

## Functional Specification

### 1. Data Quality Checks

**Completeness Validation:**
```python
- Missing json_output fields → Flag for exclusion
- Failed runs (success=False) → Document failure reasons  
- Incomplete run sequences → Detect missing run numbers
- Missing metadata → Check corpus_file, run_num, agent_id
```

**Consistency Validation:**
```python
- Data types → Ensure scores are numeric
- Range validation → Scores must be 0.0-1.0
- Duplicate detection → Same corpus_file + run_num
- Schema compliance → Match framework output_contract
```

**Quality Metrics:**
```python
- Success rate per corpus file
- Missing data patterns by framework dimension
- Statistical outliers (scores >3 std dev from mean)
- Cross-run consistency within same corpus_file
```

### 2. Data Cleansing Actions

**Automatic Fixes:**
- Remove incomplete records (missing json_output)
- Standardize corpus_file paths (relative vs absolute)
- Type conversion (string scores → float)
- Duplicate removal (keep first occurrence)

**Flag for Review:**
- Success rate < 80% for any corpus file
- Scores outside 0.0-1.0 range (potential framework bugs)
- Perfect consistency (all runs identical - possible caching issue)
- Extreme outliers (potential analysis errors)

### 3. Reporting & Provenance

**Data Quality Report:**
```yaml
data_quality_assessment:
  total_runs: 47
  successful_runs: 46
  success_rate: 97.9%
  
  quality_issues:
    - type: "missing_json_output"
      count: 1
      affected_files: ["sanitized_speech_xyz.md"]
      action: "excluded_from_analysis"
      
    - type: "score_outlier"  
      count: 2
      details: "fear_score > 0.95 (unusual for this framework)"
      action: "flagged_for_review"
      
  cleansing_actions:
    - "Removed 1 incomplete record"
    - "Standardized 8 corpus file paths"
    - "No duplicates detected"
    
  final_dataset:
    clean_runs: 45
    corpus_files: 8
    avg_runs_per_corpus: 5.6
    estimated_statistical_power: "adequate"
```

## Implementation Architecture

### Workflow Integration
```
CalculationAgent → DataIntegrityAnalyst → SynthesisAgent
                     ↓
                 Quality Report
                 Cleansed Dataset
```

### Agent Interface
```python
class DataIntegrityAnalyst(BaseAgent):
    def analyze_data_quality(self, workflow_state: Dict) -> Dict:
        """
        Returns:
        {
            'clean_analysis_results': [...],  # Cleansed data ready for synthesis
            'quality_report': {...},          # Detailed quality assessment
            'issues_detected': [...],         # Problems found
            'cleansing_actions': [...],       # Actions taken
            'recommendations': [...]          # Suggestions for improvement
        }
        """
```

### LLM Prompt Strategy
```python
def _build_quality_assessment_prompt(self, raw_data):
    """
    You are a data quality analyst for experimental research.
    
    Analyze this experimental dataset and identify:
    1. Data completeness issues
    2. Statistical anomalies that might indicate problems
    3. Patterns suggesting system issues vs. legitimate variance
    4. Recommendations for data cleansing
    
    Focus on research integrity - flag anything that could compromise
    statistical validity while preserving legitimate experimental variance.
    """
```

## Benefits Analysis

### Data Quality Benefits
- ✅ **Early Detection:** Catch data issues before they affect analysis
- ✅ **Explicit Quality Gates:** Make data quality visible and measurable
- ✅ **Research Integrity:** Prevent contaminated data from reaching conclusions
- ✅ **Debugging Support:** Clear reporting of what went wrong where

### Architectural Benefits  
- ✅ **Separation of Concerns:** SynthesisAgent focuses purely on statistics
- ✅ **Reusability:** Other agents can benefit from clean data
- ✅ **Framework Agnostic:** Works with any experimental data structure
- ✅ **THIN Compliance:** Specialized agent with clear responsibility

### Operational Benefits
- ✅ **Proactive Issue Detection:** Find problems before analysis fails
- ✅ **Automated Remediation:** Fix simple issues automatically
- ✅ **Audit Trail:** Document all data quality decisions
- ✅ **Continuous Improvement:** Learn from quality patterns over time

## Implementation Plan

### Phase 1: Core Validation
1. Create `DataIntegrityAnalyst` agent class
2. Implement basic completeness and consistency checks
3. Add to workflow between CalculationAgent and SynthesisAgent
4. Test with MVA Experiment 3 data

### Phase 2: Advanced Analytics
1. Add statistical outlier detection
2. Implement cross-run consistency analysis
3. Add framework-specific quality rules
4. Create quality trend reporting

### Phase 3: Intelligence Enhancement
1. LLM-powered anomaly detection
2. Adaptive quality thresholds
3. Predictive quality assessment
4. Integration with continuous learning

## Decision Recommendation

**✅ RECOMMENDED:** This aligns perfectly with THIN architecture principles and adds significant value to research integrity.

**Rationale:**
1. **Defense in Depth:** Multiple quality gates prevent issues from propagating
2. **Research Integrity:** Critical for academic/scientific applications  
3. **System Robustness:** Makes the pipeline more resilient to data quality issues
4. **THIN Alignment:** Each agent has a clear, specialized responsibility

**Alternative Consideration:**
Could implement as data cleansing methods within SynthesisAgent, but this violates separation of concerns and makes the synthesis agent too complex.

---

**Next Steps:** Approve architectural direction and begin Phase 1 implementation 