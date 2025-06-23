# Cost Manager

**Module:** `src.utils.cost_manager`
**File:** `/app/src/utils/cost_manager.py`
**Package:** `utils`

API Cost Management Utility - Updated for 2025 Models
Provides cost tracking, limits, and monitoring for OpenAI, Anthropic, Mistral, and Google AI APIs

## Dependencies

- `csv`
- `dataclasses`
- `datetime`
- `json`
- `os`
- `pathlib`
- `time`
- `typing`

## Table of Contents

### Classes
- [CostEntry](#costentry)
- [CostLimits](#costlimits)
- [CostManager](#costmanager)

## Classes

### CostEntry

Single cost entry

---

### CostLimits

Cost limits configuration

---

### CostManager

Manages API costs across all providers - Updated for 2025

#### Methods

##### `__init__`
```python
__init__(self, cost_file: str, limits_file: str)
```

##### `_load_costs`
```python
_load_costs(self)
```

Load cost history from file

##### `_load_limits`
```python
_load_limits(self)
```

Load cost limits from file

##### `_save_costs`
```python
_save_costs(self)
```

Save cost history to file

##### `_save_limits`
```python
_save_limits(self)
```

Save cost limits to file

##### `estimate_cost`
```python
estimate_cost(self, text: str, provider: str, model: str) -> Tuple[Any]
```

Estimate cost for analyzing text - Updated for 2025 models

##### `check_limits_before_request`
```python
check_limits_before_request(self, estimated_cost: float) -> Tuple[Any]
```

Check if request would exceed limits

##### `_get_spending_since`
```python
_get_spending_since(self, since_date: datetime) -> float
```

Get total spending since a specific date

##### `record_cost`
```python
record_cost(self, provider: str, model: str, actual_cost: float, tokens_input: int, tokens_output: int, request_type: str)
```

Record actual cost after API call

##### `_check_and_warn_limits`
```python
_check_and_warn_limits(self)
```

Check current spending against limits and warn if approaching

##### `get_spending_summary`
```python
get_spending_summary(self) -> Dict
```

Get summary of spending over different periods

##### `_get_usage_by_provider`
```python
_get_usage_by_provider(self) -> Dict
```

Get total usage grouped by provider

##### `_get_usage_by_model`
```python
_get_usage_by_model(self) -> Dict
```

Get usage breakdown by model

##### `set_limits`
```python
set_limits(self, daily: Optional[float], weekly: Optional[float], monthly: Optional[float], single_request: Optional[float])
```

Update cost limits

##### `export_costs`
```python
export_costs(self, filename: str)
```

Export cost data to CSV for analysis

##### `get_model_info`
```python
get_model_info(self, provider: str, model: str) -> Dict[Any]
```

Get detailed information about a specific model

##### `get_cost_comparison`
```python
get_cost_comparison(self, text: str, providers: List[str]) -> Dict[Any]
```

Compare costs across different models for the same text

##### `get_best_value_models`
```python
get_best_value_models(self, text: str, max_cost: float) -> List[Dict]
```

Get recommendations for best value models based on cost and capabilities

##### `add_cost`
```python
add_cost(self, provider: str, model: str, cost: float, tokens_input: int, tokens_output: int, request_type: str)
```

Add a new cost entry and save to file.

---

*Generated on 2025-06-23 10:38:43*