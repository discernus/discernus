# Reliability

**Module:** `src.analysis.reliability`
**File:** `/Users/jeffwhatcott/Library/Mobile Documents/com~apple~CloudDocs/Coding Projects/discernus/src/analysis/reliability.py`
**Package:** `analysis`

Interrater Reliability Analysis System for Multi-LLM Narrative Gravity Analysis
Calculates ICC, Cronbach's Alpha, and other reliability metrics

## Dependencies

- `json`
- `logging`
- `numpy`
- `pandas`
- `pathlib`
- `scipy`
- `scipy.stats`
- `sklearn.metrics`
- `typing`
- `warnings`

## Table of Contents

### Classes
- [InterraterReliabilityAnalyzer](#interraterreliabilityanalyzer)

## Classes

### InterraterReliabilityAnalyzer

Interrater reliability analysis for multi-LLM studies.

#### Methods

##### `__init__`
```python
__init__(self)
```

Initialize the reliability analyzer.

##### `analyze_reliability`
```python
analyze_reliability(self, structured_results: Dict) -> Dict[Any]
```

Analyze interrater reliability for multi-LLM studies.

Args:
    structured_results: Dictionary containing structured data and metadata
    
Returns:
    Dictionary containing comprehensive reliability analysis

##### `_single_rater_analysis`
```python
_single_rater_analysis(self, df: pd.DataFrame, well_columns: List[str], metadata: Dict) -> Dict[Any]
```

Analysis for single-rater scenarios (descriptive only).

##### `calculate_icc`
```python
calculate_icc(self, df: pd.DataFrame, well_columns: List[str]) -> Dict[Any]
```

Calculate Intraclass Correlation Coefficient (ICC) for each well.

Args:
    df: DataFrame with analysis results
    well_columns: List of well score column names
    
Returns:
    Dictionary with ICC results for each well

##### `_calculate_icc_two_way`
```python
_calculate_icc_two_way(self, data: np.ndarray) -> Optional[float]
```

Calculate ICC(2,1) using ANOVA approach.

##### `_interpret_icc`
```python
_interpret_icc(self, icc_value: float) -> str
```

Interpret ICC value according to standard guidelines.

##### `calculate_cronbach_alpha`
```python
calculate_cronbach_alpha(self, df: pd.DataFrame, well_columns: List[str]) -> Dict[Any]
```

Calculate Cronbach's Alpha for internal consistency.

Args:
    df: DataFrame with analysis results
    well_columns: List of well score column names
    
Returns:
    Dictionary with Cronbach's Alpha results

##### `_interpret_cronbach_alpha`
```python
_interpret_cronbach_alpha(self, alpha: float) -> str
```

Interpret Cronbach's Alpha value.

##### `calculate_pairwise_correlations`
```python
calculate_pairwise_correlations(self, df: pd.DataFrame, well_columns: List[str], models: List[str]) -> Dict[Any]
```

Calculate pairwise correlations between raters (models).

##### `calculate_coefficient_of_variation`
```python
calculate_coefficient_of_variation(self, df: pd.DataFrame, well_columns: List[str]) -> Dict[Any]
```

Calculate coefficient of variation for each well across raters.

##### `_interpret_cv`
```python
_interpret_cv(self, cv: float) -> str
```

Interpret coefficient of variation.

##### `detect_outliers`
```python
detect_outliers(self, df: pd.DataFrame, well_columns: List[str], models: List[str]) -> Dict[Any]
```

Detect outliers in rater scores.

##### `analyze_systematic_bias`
```python
analyze_systematic_bias(self, df: pd.DataFrame, well_columns: List[str], models: List[str]) -> Dict[Any]
```

Analyze systematic bias between raters.

##### `calculate_descriptive_reliability_stats`
```python
calculate_descriptive_reliability_stats(self, df: pd.DataFrame, well_columns: List[str]) -> Dict[Any]
```

Calculate descriptive statistics for reliability assessment.

##### `calculate_internal_consistency`
```python
calculate_internal_consistency(self, df: pd.DataFrame, well_columns: List[str]) -> Dict[Any]
```

Calculate internal consistency measures for single rater.

##### `generate_reliability_summary`
```python
generate_reliability_summary(self, reliability_results: Dict) -> Dict[Any]
```

Generate overall reliability summary.

---

*Generated on 2025-06-21 12:44:47*