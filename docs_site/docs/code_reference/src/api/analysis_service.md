# Analysis Service

**Module:** `src.api.analysis_service`
**File:** `/app/src/api/analysis_service.py`
**Package:** `api`

Real Analysis Service - Integrates existing LLM and analysis components
Replaces fake/mock analysis with actual AI-powered narrative analysis

## Dependencies

- `datetime`
- `json`
- `math`
- `pathlib`
- `random`
- `re`
- `sqlalchemy`
- `sqlalchemy.orm`
- `src.api_clients.direct_api_client`
- `src.coordinate_engine`
- `src.framework_manager`
- `src.models.component_models`
- `src.prompts.template_manager`
- `src.utils.database`
- `time`
- `typing`
- `uuid`

## Table of Contents

### Classes
- [RealAnalysisService](#realanalysisservice)

## Classes

### RealAnalysisService

Real analysis service that uses existing working components instead of fake data.
Integrates DirectAPIClient + PromptTemplateManager + DiscernusCoordinateEngine.

#### Methods

##### `__init__`
```python
__init__(self)
```

Initialize with existing working components

##### `_parse_llm_response`
```python
_parse_llm_response(self, llm_response: Dict[Any], framework: str) -> Dict[Any]
```

Parse LLM response into structured well scores.
Uses existing DirectAPIClient parsing logic.

##### `_extract_scores_from_text`
```python
_extract_scores_from_text(self, response_text: str, framework: str) -> Dict[Any]
```

Fallback method to extract scores from text response.
Looks for patterns like "Dignity: 0.75" or "Truth: 7.5/10"

##### `_get_framework_wells`
```python
_get_framework_wells(self, framework: str) -> List[str]
```

🔒 FRAMEWORK COMPLIANCE: Get wells dynamically from framework configuration
Single Source of Truth: Database first, filesystem fallback for development

##### `_load_wells_from_database`
```python
_load_wells_from_database(self, framework_name: str) -> List[str]
```

🔒 SINGLE SOURCE OF TRUTH: Load wells from database FrameworkVersion table
This is the authoritative source for production framework definitions

##### `_normalize_framework_name`
```python
_normalize_framework_name(self, framework_config_id: str) -> str
```

Normalize framework name by removing version suffixes.
E.g., 'civic_virtue_v2025_06_04' -> 'civic_virtue'

##### `_get_framework_yaml_path`
```python
_get_framework_yaml_path(self, framework_name: str) -> Optional[str]
```

Map framework name to its YAML file path.
Searches research workspaces and main frameworks directory.

##### `_normalize_scores_for_framework`
```python
_normalize_scores_for_framework(self, scores: Dict[Any], framework: str) -> Dict[Any]
```

🔒 FRAMEWORK COMPLIANCE: Ensure all expected wells are present with reasonable default scores.
Uses dynamic framework loading to respect framework boundaries.

##### `_generate_default_scores`
```python
_generate_default_scores(self, framework: str) -> Dict[Any]
```

🔒 FRAMEWORK COMPLIANCE: Generate reasonable default scores if parsing completely fails
Uses dynamic framework loading to respect framework boundaries.

##### `_generate_hierarchical_ranking`
```python
_generate_hierarchical_ranking(self, raw_scores: Dict[Any]) -> Dict[Any]
```

Generate hierarchical ranking from well scores.
Finds top wells and calculates relative weights.

##### `_extract_well_justifications`
```python
_extract_well_justifications(self, llm_response: Dict[Any], raw_scores: Dict[Any], text_content: str) -> Dict[Any]
```

Extract evidence and reasoning for each well from LLM response.

##### `_extract_evidence_quotes`
```python
_extract_evidence_quotes(self, llm_response: Dict[Any], well: str, text_content: str) -> List[str]
```

🔒 FRAMEWORK COMPLIANCE: Extract relevant quotes from text that support the well score.
Uses framework-agnostic keyword extraction for any well type.

##### `_calculate_circular_metrics`
```python
_calculate_circular_metrics(self, x: float, y: float, raw_scores: Dict[Any]) -> Dict[Any]
```

Calculate metrics compatible with circular coordinate system.

##### `_generate_fallback_analysis`
```python
_generate_fallback_analysis(self, text_content: str, framework: str, model: str, analysis_id: str, start_time: float) -> Dict[Any]
```

🔒 FRAMEWORK COMPLIANCE: Generate reasonable fallback analysis if real LLM analysis fails completely.
Better than random data but clearly marked as fallback. Uses dynamic framework loading.

---

*Generated on 2025-06-21 20:19:04*