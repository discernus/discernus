# Optimize Framework Colors

**Module:** `scripts.utilities.optimize_framework_colors`
**File:** `/app/scripts/utilities/optimize_framework_colors.py`
**Package:** `utilities`

Framework Color Optimization Script
Optimizes well color schemes across all frameworks for:
1. Accessibility (color-blind compatibility)
2. Academic publication standards
3. Visual consistency across frameworks
4. Grayscale compatibility

Generated: June 14, 2025

## Dependencies

- `argparse`
- `datetime`
- `json`
- `os`
- `pathlib`
- `typing`

## Table of Contents

### Classes
- [FrameworkColorOptimizer](#frameworkcoloroptimizer)

### Functions
- [main](#main)

## Classes

### FrameworkColorOptimizer

Optimizes framework color schemes for accessibility and academic standards.

#### Methods

##### `__init__`
```python
__init__(self, project_root: str)
```

##### `get_framework_files`
```python
get_framework_files(self) -> List[Path]
```

Get all framework.json files.

##### `validate_color_accessibility`
```python
validate_color_accessibility(self, color: str) -> Dict[Any]
```

Validate color for accessibility standards.

##### `update_framework_colors`
```python
update_framework_colors(self, framework_file: Path, dry_run: bool) -> Dict[Any]
```

Update colors for a specific framework.

##### `generate_color_report`
```python
generate_color_report(self, changes: List[Dict[Any]]) -> str
```

Generate comprehensive color optimization report.

##### `_get_timestamp`
```python
_get_timestamp(self, full, readable)
```

Get timestamp in various formats.

---

## Functions

### `main`
```python
main()
```

Main execution function.

---

*Generated on 2025-06-21 20:19:04*