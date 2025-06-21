# Statistics

**Module:** `src.analysis.statistics`
**File:** `/app/src/analysis/statistics.py`
**Package:** `analysis`

Statistical Hypothesis Testing System for Narrative Gravity Analysis
Tests discriminative validity, ideological agnosticism, and ground truth alignment

## Dependencies

- `logging`
- `numpy`
- `pandas`
- `scipy`
- `scipy.stats`
- `typing`

## Table of Contents

### Classes
- [StatisticalHypothesisTester](#statisticalhypothesistester)

## Classes

### StatisticalHypothesisTester

Statistical hypothesis testing for narrative gravity analysis.

#### Methods

##### `__init__`
```python
__init__(self)
```

Initialize the hypothesis tester.

##### `test_hypotheses`
```python
test_hypotheses(self, structured_results: Dict) -> Dict[Any]
```

Test all three hypotheses on structured experiment results.

Args:
    structured_results: Dictionary containing structured data and metadata
    
Returns:
    Dictionary containing all hypothesis test results

##### `test_h1_discriminative_validity`
```python
test_h1_discriminative_validity(self, df: pd.DataFrame, well_columns: List[str]) -> Dict[Any]
```

H1: Test discriminative validity - dignity vs tribalism scores should differentiate expected text categories.

Args:
    df: DataFrame with analysis results
    well_columns: List of well score column names
    
Returns:
    Dictionary with H1 test results

##### `test_h2_ideological_agnosticism`
```python
test_h2_ideological_agnosticism(self, df: pd.DataFrame, well_columns: List[str]) -> Dict[Any]
```

H2: Test ideological agnosticism - framework should not systematically favor conservative vs progressive texts.

Args:
    df: DataFrame with analysis results
    well_columns: List of well score column names
    
Returns:
    Dictionary with H2 test results

##### `test_h3_ground_truth_alignment`
```python
test_h3_ground_truth_alignment(self, df: pd.DataFrame, well_columns: List[str]) -> Dict[Any]
```

H3: Test ground truth alignment - extreme control texts should score >0.8 on expected wells.

Args:
    df: DataFrame with analysis results
    well_columns: List of well score column names
    
Returns:
    Dictionary with H3 test results

##### `calculate_descriptive_statistics`
```python
calculate_descriptive_statistics(self, df: pd.DataFrame, well_columns: List[str]) -> Dict[Any]
```

Calculate comprehensive descriptive statistics.

##### `calculate_effect_sizes`
```python
calculate_effect_sizes(self, df: pd.DataFrame, well_columns: List[str]) -> Dict[Any]
```

Calculate Cohen's d and other effect sizes.

##### `_interpret_cohens_d`
```python
_interpret_cohens_d(self, d: float) -> str
```

Interpret Cohen's d effect size.

##### `generate_hypothesis_summary`
```python
generate_hypothesis_summary(self, h1_results: Dict, h2_results: Dict, h3_results: Dict) -> Dict[Any]
```

Generate overall summary of hypothesis testing results.

---

*Generated on 2025-06-21 20:19:04*