# Framework Manager

**Module:** `src.framework_manager`
**File:** `/Volumes/dev/discernus/src/framework_manager.py`

Framework Manager for Narrative Gravity Wells

Manages multiple dipole frameworks and enables easy switching between them.

## Dependencies

- `argparse`
- `json`
- `os`
- `pathlib`
- `yaml`

## Table of Contents

### Classes
- [FrameworkManager](#frameworkmanager)

### Functions
- [main](#main)

## Classes

### FrameworkManager

#### Methods

##### `__init__`
```python
__init__(self, base_dir)
```

##### `list_frameworks`
```python
list_frameworks(self)
```

List available frameworks

##### `get_active_framework`
```python
get_active_framework(self)
```

Get currently active framework

##### `switch_framework`
```python
switch_framework(self, framework_name)
```

Switch to a different framework by name

##### `validate_framework`
```python
validate_framework(self, framework_name)
```

Validate a framework's structure

##### `create_framework_summary`
```python
create_framework_summary(self)
```

Create a summary of all frameworks

##### `load_framework`
```python
load_framework(self, framework_name: str) -> dict
```

Load framework data from filesystem with enhanced pattern matching.

This method was added to fix AttributeError: 'FrameworkManager' object has no attribute 'load_framework'
that was occurring in multiple scripts. It delegates to the same logic used by ConsolidatedFrameworkLoader.

Supports multiple framework file naming patterns:
- Descriptive names: *_framework.yaml, *_framework.json (highest priority)
- Standard names: framework.yaml, framework.json 
- Consolidated: framework_consolidated.json (legacy support)

Args:
    framework_name: Name of the framework to load
    
Returns:
    Dictionary containing framework data
    
Raises:
    FileNotFoundError: If framework files are not found
    json.JSONDecodeError: If framework files contain invalid JSON

---

## Functions

### `main`
```python
main()
```

---

*Generated on 2025-06-21 18:56:11*