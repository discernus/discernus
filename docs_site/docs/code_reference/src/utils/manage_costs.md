# Manage Costs

**Module:** `src.utils.manage_costs`
**File:** `/Volumes/dev/discernus/src/utils/manage_costs.py`
**Package:** `utils`

API Cost Management CLI - Updated for 2025 Models
Command-line tool for managing API costs and limits with advanced model comparison

## Dependencies

- `argparse`
- `json`
- `pathlib`
- `src.utils.cost_manager`
- `sys`
- `time`

## Table of Contents

### Functions
- [show_status](#show-status)
- [set_limits](#set-limits)
- [estimate_cost](#estimate-cost)
- [compare_models](#compare-models)
- [get_recommendations](#get-recommendations)
- [model_info](#model-info)
- [export_data](#export-data)
- [reset_costs](#reset-costs)
- [monitor_mode](#monitor-mode)
- [list_models](#list-models)
- [main](#main)

## Functions

### `show_status`
```python
show_status(cost_manager: [CostManager](src/utils/cost_manager.md#costmanager))
```

Show current cost status

---

### `set_limits`
```python
set_limits(cost_manager: [CostManager](src/utils/cost_manager.md#costmanager), args)
```

Set cost limits

---

### `estimate_cost`
```python
estimate_cost(cost_manager: [CostManager](src/utils/cost_manager.md#costmanager), args)
```

Estimate cost for text analysis

---

### `compare_models`
```python
compare_models(cost_manager: [CostManager](src/utils/cost_manager.md#costmanager), args)
```

Compare models for cost and capabilities

---

### `get_recommendations`
```python
get_recommendations(cost_manager: [CostManager](src/utils/cost_manager.md#costmanager), args)
```

Get model recommendations based on value

---

### `model_info`
```python
model_info(cost_manager: [CostManager](src/utils/cost_manager.md#costmanager), args)
```

Show detailed information about a specific model

---

### `export_data`
```python
export_data(cost_manager: [CostManager](src/utils/cost_manager.md#costmanager), args)
```

Export cost data

---

### `reset_costs`
```python
reset_costs(cost_manager: [CostManager](src/utils/cost_manager.md#costmanager))
```

Reset cost tracking (with confirmation)

---

### `monitor_mode`
```python
monitor_mode(cost_manager: [CostManager](src/utils/cost_manager.md#costmanager))
```

Interactive monitoring mode

---

### `list_models`
```python
list_models(cost_manager: [CostManager](src/utils/cost_manager.md#costmanager))
```

List all available models with their capabilities

---

### `main`
```python
main()
```

Main CLI function

---

*Generated on 2025-06-21 18:56:11*