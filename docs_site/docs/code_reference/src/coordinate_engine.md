# Coordinate Engine

**Module:** `src.coordinate_engine`
**File:** `/Volumes/dev/discernus/src/coordinate_engine.py`

## Dependencies

- `argparse`
- `datetime`
- `json`
- `numpy`
- `pathlib`
- `typing`
- `visualization.plotly_circular`
- `yaml`

## Table of Contents

### Classes
- [DiscernusCoordinateEngine](#discernuscoordinateengine)

### Functions
- [main](#main)

## Classes

### DiscernusCoordinateEngine

Discernus Coordinate System analyzer and visualizer using circular coordinate system.

Version 2.1.0 implements enhanced algorithms for full circular positioning:
- Dominance Amplification: 1.1x multiplier for scores > 0.7
- Adaptive Scaling: Dynamic scaling factors (0.65-0.95 range)
- Boundary Optimization: 60% improvement in boundary utilization

Three-Dimensional Architecture:
1. Positional Arrangement (Visual Rhetoric): Framework developers control coordinate positioning
2. Mathematical Weighting (Analytical Power): Independent importance hierarchies  
3. Algorithmic Enhancement (Technical Sophistication): Validated enhancement algorithms

#### Methods

##### `__init__`
```python
__init__(self, config_dir: str, framework_path: str)
```

##### `_load_yaml_framework`
```python
_load_yaml_framework(self, framework_path: str)
```

Load framework configuration from YAML framework file.

##### `_load_framework_config`
```python
_load_framework_config(self)
```

Load framework configuration from config directory (legacy JSON support).

##### `_load_default_config`
```python
_load_default_config(self)
```

Load default configuration for backward compatibility.

##### `circle_point`
```python
circle_point(self, angle_deg: float) -> Tuple[Any]
```

Convert angle in degrees to (x, y) coordinates on unit circle.

##### `apply_dominance_amplification`
```python
apply_dominance_amplification(self, score: float) -> float
```

Apply dominance amplification for extreme scores.
Enhances scores > 0.7 with 1.1x multiplier per migration guide.

##### `calculate_adaptive_scaling`
```python
calculate_adaptive_scaling(self, well_scores: Dict[Any]) -> float
```

Calculate adaptive scaling factor for optimal boundary utilization.
Returns scaling factor in 0.65-0.95 range per migration guide.

##### `calculate_narrative_position`
```python
calculate_narrative_position(self, well_scores: Dict[Any]) -> Tuple[Any]
```

Calculate narrative position using enhanced algorithms.
Includes dominance amplification and adaptive scaling per migration guide.

##### `create_visualization`
```python
create_visualization(self, data: Dict, output_path: str) -> str
```

Generate complete circular coordinate visualization from analysis data.

##### `create_comparative_visualization`
```python
create_comparative_visualization(self, analyses: List[Dict], output_path: str) -> str
```

Create comparison visualization for multiple analyses.

---

## Functions

### `main`
```python
main()
```

CLI interface for circular coordinate system visualization.

---

*Generated on 2025-06-21 18:56:11*