# Direct Api Client

**Module:** `src.api_clients.direct_api_client`
**File:** `/app/src/api_clients/direct_api_client.py`
**Package:** `api_clients`

Direct API Client for Flagship LLMs - Updated for 2025 Models
Integrates OpenAI, Anthropic, Mistral, and Google AI APIs with latest model versions

## Dependencies

- `anthropic`
- `dotenv`
- `google.generativeai`
- `json`
- `mistralai.client`
- `openai`
- `os`
- `pathlib`
- `re`
- `src.prompts.template_manager`
- `src.utils.cost_manager`
- `time`
- `typing`
- `utils.api_retry_handler`
- `utils.llm_quality_assurance`

## Table of Contents

### Classes
- [DirectAPIClient](#directapiclient)

## Classes

### DirectAPIClient

Direct API client for flagship LLMs - Updated with latest 2025 models

#### Methods

##### `__init__`
```python
__init__(self)
```

Initialize API clients

##### `test_connections`
```python
test_connections(self) -> Dict[Any]
```

Test all API connections with latest models

##### `_enforce_rate_limit`
```python
_enforce_rate_limit(self, provider: str)
```

Enforce rate limiting to be polite to API providers

##### `analyze_text`
```python
analyze_text(self, text: str, framework: str, model_name: str) -> Tuple[Any]
```

Analyze text using specified model and framework
Compatible with existing narrative gravity framework

##### `_get_provider_from_model`
```python
_get_provider_from_model(self, model_name: str) -> str
```

Get provider name from model name

##### `_analyze_with_openai`
```python
_analyze_with_openai(self, prompt: str, model_name: str) -> Tuple[Any]
```

Analyze with OpenAI models - Updated for 2025 with retry handling

##### `_openai_api_call_with_retry`
```python
_openai_api_call_with_retry(self, prompt: str, model: str) -> Tuple[Any]
```

OpenAI API call with retry logic.

##### `_openai_api_call_basic`
```python
_openai_api_call_basic(self, prompt: str, model: str) -> Tuple[Any]
```

Basic OpenAI API call with simple error handling (fallback).

##### `_analyze_with_anthropic`
```python
_analyze_with_anthropic(self, prompt: str, model_name: str) -> Tuple[Any]
```

Analyze with Anthropic models - Updated for 2025

##### `_analyze_with_mistral`
```python
_analyze_with_mistral(self, prompt: str, model_name: str) -> Tuple[Any]
```

Analyze with Mistral models - Updated for 2025

##### `_parse_response`
```python
_parse_response(self, content: str, text_input: str, framework: str) -> Dict[Any]
```

Parse LLM response with integrated quality assurance validation - supports both simple and hierarchical formats

##### `_is_hierarchical_response`
```python
_is_hierarchical_response(self, response: Dict[Any]) -> bool
```

Check if response is in hierarchical 3-stage format

##### `_extract_hierarchical_scores`
```python
_extract_hierarchical_scores(self, response: Dict[Any]) -> Dict[Any]
```

Extract scores from hierarchical 3-stage response format

##### `_extract_narrative_scores`
```python
_extract_narrative_scores(self, content: str) -> Dict[Any]
```

Extract narrative gravity scores from text response

##### `_analyze_with_google_ai`
```python
_analyze_with_google_ai(self, prompt: str, model_name: str) -> Tuple[Any]
```

Analyze with Google AI models - Updated for 2025

##### `get_available_models`
```python
get_available_models(self) -> Dict[Any]
```

Get list of available models - Updated for 2025

##### `get_retry_statistics`
```python
get_retry_statistics(self) -> Dict[Any]
```

Get comprehensive retry and reliability statistics.

##### `log_reliability_report`
```python
log_reliability_report(self)
```

Log comprehensive reliability report.

---

*Generated on 2025-06-21 20:19:04*