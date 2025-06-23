# Llm Quality Assurance

**Module:** `src.utils.llm_quality_assurance`
**File:** `/app/src/utils/llm_quality_assurance.py`
**Package:** `utils`

LLM Quality Assurance System
============================

🚨 AI ASSISTANT WARNING: This is the PRODUCTION quality assurance system.
❌ DO NOT build new QA systems - enhance this one instead!
❌ DO NOT use "AI Academic Advisor" (deprecated file-checking in deprecated/)
✅ USE THIS: LLMQualityAssuranceSystem (production 6-layer validation)

Multi-layered validation system for LLM analysis results to prevent silent failures
and artificial precision. Implements "virtual eyes on" principle with systematic
quality checks and confidence scoring.

Enhanced with experiment-specific QA that validates against research goals and hypotheses.

Addresses the critical issue where LLM parsing failures create mathematically valid
but artificially precise results (e.g., Roosevelt 1933 at exactly (0.000, 0.000)
with 80% artificial data).

## Dependencies

- `coordinate_engine`
- `dataclasses`
- `datetime`
- `json`
- `logging`
- `numpy`
- `pathlib`
- `re`
- `typing`

## Table of Contents

### Classes
- [QualityCheck](#qualitycheck)
- [QualityAssessment](#qualityassessment)
- [ExperimentContext](#experimentcontext)
- [ExperimentSpecificQualityAssurance](#experimentspecificqualityassurance)
- [LLMQualityAssuranceSystem](#llmqualityassurancesystem)

## Classes

### QualityCheck

Individual quality check result.

---

### QualityAssessment

Complete quality assessment result.

---

### ExperimentContext

Experiment context for hypothesis-aware validation.

---

### ExperimentSpecificQualityAssurance

Layer 2: Experiment-Specific Quality Assurance

Validates analysis results against researcher-defined goals, hypotheses,
and success criteria. Generates dynamic QA checks based on experiment definition.

#### Methods

##### `__init__`
```python
__init__(self)
```

##### `validate_experiment_alignment`
```python
validate_experiment_alignment(self, analysis_results: List[Dict[Any]], experiment_context: [ExperimentContext](scripts/applications/comprehensive_experiment_orchestrator.md#experimentcontext), framework_id: str) -> List[[QualityCheck](src/utils/llm_quality_assurance.md#qualitycheck)]
```

Validate analysis results against experiment-specific requirements.

Args:
    analysis_results: List of individual analysis results
    experiment_context: Experiment definition and goals
    framework_id: Framework being used for analysis
    
Returns:
    List of experiment-specific quality checks

##### `_validate_hypotheses_alignment`
```python
_validate_hypotheses_alignment(self, results: List[Dict[Any]], hypotheses: List[str], framework_id: str) -> List[[QualityCheck](src/utils/llm_quality_assurance.md#qualitycheck)]
```

Validate that results can meaningfully test stated hypotheses.

##### `_validate_success_criteria`
```python
_validate_success_criteria(self, results: List[Dict[Any]], success_criteria: List[str]) -> List[[QualityCheck](src/utils/llm_quality_assurance.md#qualitycheck)]
```

Validate that results meet stated success criteria.

##### `_validate_research_alignment`
```python
_validate_research_alignment(self, results: List[Dict[Any]], research_context: str, framework_id: str) -> List[[QualityCheck](src/utils/llm_quality_assurance.md#qualitycheck)]
```

Validate analysis aligns with research context and questions.

##### `_assess_framework_research_fit`
```python
_assess_framework_research_fit(self, research_context: str, framework_id: str) -> Dict[Any]
```

Assess how well the framework fits the research context.

##### `_validate_framework_corpus_fit`
```python
_validate_framework_corpus_fit(self, results: List[Dict[Any]], experiment_context: [ExperimentContext](scripts/applications/comprehensive_experiment_orchestrator.md#experimentcontext), framework_id: str) -> List[[QualityCheck](src/utils/llm_quality_assurance.md#qualitycheck)]
```

Validate framework is appropriate for the corpus being analyzed.

##### `_validate_statistical_requirements`
```python
_validate_statistical_requirements(self, results: List[Dict[Any]], experiment_context: [ExperimentContext](scripts/applications/comprehensive_experiment_orchestrator.md#experimentcontext)) -> List[[QualityCheck](src/utils/llm_quality_assurance.md#qualitycheck)]
```

Validate statistical power and requirements.

---

### LLMQualityAssuranceSystem

Multi-layered quality assurance system for LLM analysis results.

Implements 6 layers of validation:
1. Input Validation
2. LLM Response Validation  
3. Statistical Coherence Validation
4. Mathematical Consistency Verification
5. LLM Second Opinion Cross-Validation
6. Anomaly Detection

Enhanced with experiment-specific validation layer.

#### Methods

##### `__init__`
```python
__init__(self)
```

##### `validate_llm_analysis`
```python
validate_llm_analysis(self, text_input: str, framework: str, llm_response: Dict[Any], parsed_scores: Dict[Any], experiment_context: [ExperimentContext](scripts/applications/comprehensive_experiment_orchestrator.md#experimentcontext)) -> [QualityAssessment](src/utils/llm_quality_assurance.md#qualityassessment)
```

Run complete quality assurance validation on LLM analysis.

Args:
    text_input: Original text that was analyzed
    framework: Framework used for analysis
    llm_response: Raw LLM response
    parsed_scores: Parsed well scores
    experiment_context: Experiment definition for specific validation
    
Returns:
    QualityAssessment with confidence scoring and validation results

##### `_validate_input`
```python
_validate_input(self, text: str, framework: str) -> List[[QualityCheck](src/utils/llm_quality_assurance.md#qualitycheck)]
```

Layer 1: Input Validation.

##### `_validate_llm_response`
```python
_validate_llm_response(self, llm_response: Dict[Any], parsed_scores: Dict[Any], framework: str) -> List[[QualityCheck](src/utils/llm_quality_assurance.md#qualitycheck)]
```

Layer 2: LLM Response Validation.

##### `_validate_statistical_coherence`
```python
_validate_statistical_coherence(self, parsed_scores: Dict[Any]) -> Tuple[Any]
```

Layer 3: Statistical Coherence Validation.

##### `_validate_mathematical_consistency`
```python
_validate_mathematical_consistency(self, parsed_scores: Dict[Any], framework: str) -> List[[QualityCheck](src/utils/llm_quality_assurance.md#qualitycheck)]
```

Layer 4: Mathematical Consistency Verification.

##### `_detect_anomalies`
```python
_detect_anomalies(self, parsed_scores: Dict[Any]) -> Tuple[Any]
```

Layer 6: Anomaly Detection.

##### `_calculate_confidence_score`
```python
_calculate_confidence_score(self, quality_checks: List[[QualityCheck](src/utils/llm_quality_assurance.md#qualitycheck)]) -> float
```

Calculate overall confidence score from individual checks.

##### `_determine_confidence_level`
```python
_determine_confidence_level(self, confidence_score: float) -> str
```

Determine confidence level category.

##### `_needs_second_opinion`
```python
_needs_second_opinion(self, quality_checks: List[[QualityCheck](src/utils/llm_quality_assurance.md#qualitycheck)], anomalies: List[str]) -> bool
```

Determine if second opinion validation is needed.

##### `_generate_quality_summary`
```python
_generate_quality_summary(self, confidence_level: str, quality_checks: List[[QualityCheck](src/utils/llm_quality_assurance.md#qualitycheck)], anomalies: List[str], experiment_issues: List[str]) -> str
```

Generate human-readable quality summary.

##### `_get_framework_yaml_path`
```python
_get_framework_yaml_path(self, framework_name: str) -> Optional[str]
```

Map framework name to its YAML file path for framework-aware QA.

##### `_get_expected_wells`
```python
_get_expected_wells(self, framework: str) -> List[str]
```

Get expected wells for a framework.

##### `_detect_uniform_pattern`
```python
_detect_uniform_pattern(self, scores: List[float]) -> bool
```

Detect if scores follow a uniform pattern.

##### `_detect_perfect_symmetry`
```python
_detect_perfect_symmetry(self, parsed_scores: Dict[Any]) -> bool
```

Detect perfect mathematical symmetry that suggests artificial generation.

##### `_detect_outliers`
```python
_detect_outliers(self, scores: List[float]) -> List[float]
```

Detect statistical outliers in scores.

---

*Generated on 2025-06-23 10:38:43*