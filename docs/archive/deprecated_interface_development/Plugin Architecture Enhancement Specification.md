<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# Narrative Gravity Wells: Plugin Architecture Enhancement Specification

**Version**: 1.0.0
**Date**: June 11, 2025
**Status**: Future Enhancement - Post-Validation Implementation
**Priority**: Medium (After Academic Validation Completion)

## Executive Summary

This document specifies a comprehensive plugin architecture enhancement for the Narrative Gravity Wells system, enabling framework creators to develop custom metrics, weighting algorithms, and visualizations without modifying core system code. The enhancement transforms the project from a specific analytical framework into a platform for building analytical frameworks while maintaining the rigor and reliability of the current system.

**Implementation Timeline**: Post-Milestone 2 completion (after LLM reliability validation and human subject studies)

## Table of Contents

1. [Architectural Vision](#architectural-vision)
2. [Current System Analysis](#current-system-analysis)
3. [Plugin Framework Specification](#plugin-framework-specification)
4. [Custom Metrics System](#custom-metrics-system)
5. [Weighting Algorithm Framework](#weighting-algorithm-framework)
6. [Declarative Visualization Schema](#declarative-visualization-schema)
7. [Security and Validation](#security-and-validation)
8. [Framework Package Structure](#framework-package-structure)
9. [Implementation Phases](#implementation-phases)
10. [Migration Strategy](#migration-strategy)
11. [Performance Considerations](#performance-considerations)
12. [Developer Experience](#developer-experience)
13. [Quality Assurance](#quality-assurance)
14. [Future Extensions](#future-extensions)
15. [Resource Requirements](#resource-requirements)

## Architectural Vision

### Core Philosophy

Transform the Narrative Gravity Wells system from a collection of specific analytical frameworks into a **meta-framework** for building analytical frameworks. Enable unlimited innovation in political narrative analysis while maintaining system stability, security, and academic rigor.

### Design Principles

1. **Extensibility Without Modification**: New frameworks require no changes to core system code
2. **Constrained Innovation**: Plugin guardrails prevent security issues and performance degradation
3. **Backward Compatibility**: Existing frameworks continue functioning unchanged
4. **Academic Rigor**: Plugin validation ensures analytical quality and reproducibility
5. **Developer Experience**: Framework creation should be accessible to researchers with basic programming skills

### Strategic Benefits

- **Research Scalability**: Academic community can contribute novel analytical approaches
- **System Longevity**: Core infrastructure remains stable while supporting unlimited innovation
- **Reduced Maintenance**: Framework-specific bugs isolated from core system
- **Academic Adoption**: Lower barriers to framework development increase research usage
- **Methodological Diversity**: Support for emerging analytical approaches in political communication


## Current System Analysis

### Existing Architecture Strengths

The current system provides an excellent foundation for plugin architecture:

```python
# Current modular design
class FrameworkManager:
    def load_framework(self, framework_name: str) -> Dict
    def validate_framework_config(self, config: Dict) -> bool
    def get_available_frameworks(self) -> List[str]

class NarrativeGravityElliptical:
    def calculate_elliptical_metrics(self, x: float, y: float, scores: Dict) -> Dict
    def calculate_narrative_position(self, well_scores: Dict) -> Tuple[float, float]
    def create_visualization_data(self, data: Dict) -> Dict
```


### Framework Configuration Pattern

```json
{
  "framework_name": "civic_virtue", 
  "dipoles": [...],
  "wells": {...},
  "metrics": {
    "com": {"name": "Center of Mass", "description": "..."},
    "nps": {"name": "Narrative Polarity Score", "description": "..."}
  }
}
```


### Extension Points

Current system already supports:

- **Hot-swappable frameworks**: JSON-driven configuration
- **Universal metrics**: Framework-agnostic calculation engine
- **Multi-LLM compatibility**: Unified prompt generation and result processing
- **Flexible visualization**: Framework-independent data export


### Limitations Requiring Enhancement

1. **Custom Metrics**: Currently hardcoded in `narrativegravityelliptical.py`
2. **Weighting Systems**: Limited to basic well weight multiplication
3. **Visualization Types**: Fixed elliptical and polar charts
4. **Validation Logic**: Framework-specific validation requires core code changes
5. **Mathematical Algorithms**: No support for custom positioning or metric calculations

## Plugin Framework Specification

### Core Plugin Interface

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Type
from dataclasses import dataclass
from enum import Enum

class PluginType(Enum):
    METRIC_CALCULATOR = "metric_calculator"
    WEIGHTING_ALGORITHM = "weighting_algorithm" 
    VISUALIZATION_RENDERER = "visualization_renderer"
    VALIDATION_RULE = "validation_rule"

@dataclass
class PluginMetadata:
    name: str
    version: str
    author: str
    description: str
    plugin_type: PluginType
    framework_compatibility: List[str]
    python_requirements: List[str]
    academic_citations: List[str]

class FrameworkPlugin(ABC):
    """Base class for all framework plugins"""
    
    @property
    @abstractmethod
    def metadata(self) -> PluginMetadata:
        """Plugin identification and compatibility information"""
        pass
    
    @abstractmethod
    def validate_configuration(self, config: Dict[str, Any]) -> 'ValidationResult':
        """Validate framework-specific configuration"""
        pass
    
    @abstractmethod
    def register_components(self) -> Dict[str, Any]:
        """Register custom components with the system"""
        pass
```


### Plugin Registry System

```python
class PluginRegistry:
    def __init__(self):
        self.registered_plugins: Dict[str, FrameworkPlugin] = {}
        self.component_registry: Dict[PluginType, Dict[str, Type]] = {
            PluginType.METRIC_CALCULATOR: {},
            PluginType.WEIGHTING_ALGORITHM: {},
            PluginType.VISUALIZATION_RENDERER: {},
            PluginType.VALIDATION_RULE: {}
        }
    
    def register_plugin(self, plugin: FrameworkPlugin) -> bool:
        """Register a plugin and its components"""
        try:
            # Validate plugin security and compatibility
            if not self._validate_plugin_security(plugin):
                return False
            
            # Register plugin
            self.registered_plugins[plugin.metadata.name] = plugin
            
            # Register components
            components = plugin.register_components()
            for component_type, component_map in components.items():
                self.component_registry[component_type].update(component_map)
            
            return True
        except Exception as e:
            logger.error(f"Plugin registration failed: {e}")
            return False
    
    def get_component(self, component_type: PluginType, name: str) -> Optional[Type]:
        """Retrieve registered component by type and name"""
        return self.component_registry[component_type].get(name)
    
    def list_plugins(self) -> List[PluginMetadata]:
        """List all registered plugins"""
        return [plugin.metadata for plugin in self.registered_plugins.values()]
```


### Framework Package Structure

```
frameworks/
├── mft_persuasive_force/
│   ├── framework.json              # Core framework configuration
│   ├── dipoles.json               # Narrative dipole definitions
│   ├── prompt.md                  # LLM analysis prompt
│   ├── plugin.py                  # Custom plugin implementation
│   ├── visualizations.json       # Visualization definitions
│   ├── tests/                     # Framework-specific tests
│   │   ├── test_metrics.py
│   │   ├── test_weighting.py
│   │   └── validation_data.json
│   ├── docs/                      # Framework documentation
│   │   ├── README.md
│   │   ├── theoretical_foundation.md
│   │   └── validation_studies.md
│   └── examples/                  # Usage examples and demos
│       ├── sample_analyses.json
│       └── cultural_comparison.py
```


## Custom Metrics System

### Metric Calculator Interface

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class MetricOutputType(Enum):
    SCALAR = "scalar"           # Single numerical value
    VECTOR = "vector"           # Multiple related values
    COORDINATE = "coordinate"   # X,Y position
    CATEGORICAL = "categorical" # Discrete categories

@dataclass
class MetricDefinition:
    name: str
    display_name: str
    description: str
    output_type: MetricOutputType
    output_range: Tuple[float, float]
    required_inputs: List[str]
    optimal_inputs: List[str]
    academic_references: List[str]

class MetricCalculator(ABC):
    """Abstract base class for custom metric calculations"""
    
    @property
    @abstractmethod
    def definition(self) -> MetricDefinition:
        """Metric specification and metadata"""
        pass
    
    @abstractmethod
    def calculate(self, 
                  well_scores: Dict[str, float],
                  context: Optional[Dict[str, Any]] = None) -> Any:
        """
        Calculate metric value from well scores and optional context
        
        Args:
            well_scores: Framework-specific well scores {well_name: score}
            context: Optional contextual information (cultural segments, etc.)
            
        Returns:
            Metric value matching declared output_type
        """
        pass
    
    @abstractmethod
    def validate_inputs(self, 
                        well_scores: Dict[str, float],
                        context: Optional[Dict[str, Any]] = None) -> bool:
        """Validate that inputs are suitable for this metric"""
        pass
    
    def explain_calculation(self, 
                           well_scores: Dict[str, float],
                           context: Optional[Dict[str, Any]] = None) -> str:
        """Optional: Provide human-readable explanation of calculation"""
        return f"Calculated {self.definition.name} from {len(well_scores)} well scores"
```


### Example Custom Metric Implementation

```python
class CulturalResonanceCalculator(MetricCalculator):
    """Calculate alignment between narrative appeals and cultural priorities"""
    
    @property
    def definition(self) -> MetricDefinition:
        return MetricDefinition(
            name="cultural_resonance_score",
            display_name="Cultural Resonance Score",
            description="Measures alignment between narrative moral appeals and target demographic moral foundation priorities",
            output_type=MetricOutputType.SCALAR,
            output_range=(0.0, 1.0),
            required_inputs=["well_scores", "cultural_segment"],
            optimal_inputs=["narrative_context", "demographic_metadata"],
            academic_references=[
                "Haidt, J. (2012). The righteous mind: Why good people are divided by politics and religion",
                "Graham, J., et al. (2013). Moral foundations theory: The pragmatic validity of moral pluralism"
            ]
        )
    
    def calculate(self, 
                  well_scores: Dict[str, float],
                  context: Optional[Dict[str, Any]] = None) -> float:
        if not context or "cultural_segment" not in context:
            raise ValueError("Cultural segment required for resonance calculation")
        
        cultural_segment = context["cultural_segment"]
        cultural_weights = self._get_cultural_weights(cultural_segment)
        
        # Calculate weighted correlation between narrative and cultural priorities
        resonance_score = 0.0
        total_weight = 0.0
        
        for well_name, narrative_score in well_scores.items():
            if well_name in cultural_weights:
                cultural_weight = cultural_weights[well_name]
                resonance_score += narrative_score * abs(cultural_weight)
                total_weight += abs(cultural_weight)
        
        return resonance_score / total_weight if total_weight > 0 else 0.0
    
    def validate_inputs(self, 
                        well_scores: Dict[str, float],
                        context: Optional[Dict[str, Any]] = None) -> bool:
        if not well_scores:
            return False
        if not context or "cultural_segment" not in context:
            return False
        if context["cultural_segment"] not in self._get_available_segments():
            return False
        return True
    
    def explain_calculation(self, 
                           well_scores: Dict[str, float],
                           context: Optional[Dict[str, Any]] = None) -> str:
        cultural_segment = context.get("cultural_segment", "unknown")
        return f"Calculated cultural alignment for {cultural_segment} segment using weighted correlation of {len(well_scores)} moral foundation scores"
    
    def _get_cultural_weights(self, segment: str) -> Dict[str, float]:
        # Load cultural weight matrices from framework configuration
        cultural_matrices = {
            "progressive_urban": {
                "compassion": 1.0, "equity": 0.95, "solidarity": 0.4,
                "hierarchy": 0.2, "purity": 0.15
            },
            "conservative_religious": {
                "compassion": 0.8, "equity": 0.6, "solidarity": 0.9,
                "hierarchy": 1.0, "purity": 1.0
            }
            # ... additional segments
        }
        return cultural_matrices.get(segment, {})
    
    def _get_available_segments(self) -> List[str]:
        return ["progressive_urban", "conservative_religious", "libertarian_independent", 
                "working_class_traditional", "multicultural_urban", "rural_traditional"]
```


### Metric Integration System

```python
class MetricEngine:
    def __init__(self):
        self.builtin_metrics = {
            "com": CenterOfMassCalculator(),
            "nps": NarrativePolarityCalculator(),
            "dps": DirectionalPurityCalculator()
        }
        self.custom_metrics: Dict[str, MetricCalculator] = {}
    
    def register_metric(self, calculator: MetricCalculator) -> bool:
        """Register a custom metric calculator"""
        try:
            metric_name = calculator.definition.name
            
            # Validate metric implementation
            if not self._validate_metric_calculator(calculator):
                return False
            
            # Check for name conflicts
            if metric_name in self.builtin_metrics:
                logger.warning(f"Metric {metric_name} conflicts with builtin metric")
                return False
            
            self.custom_metrics[metric_name] = calculator
            return True
        except Exception as e:
            logger.error(f"Metric registration failed: {e}")
            return False
    
    def calculate_metrics(self, 
                          well_scores: Dict[str, float],
                          framework_config: Dict[str, Any],
                          context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate all applicable metrics for framework"""
        results = {}
        
        # Calculate builtin metrics
        for name, calculator in self.builtin_metrics.items():
            if self._metric_applicable(name, framework_config):
                try:
                    results[name] = calculator.calculate(well_scores, context)
                except Exception as e:
                    logger.error(f"Builtin metric {name} calculation failed: {e}")
        
        # Calculate custom metrics
        for name, calculator in self.custom_metrics.items():
            if self._metric_applicable(name, framework_config):
                try:
                    if calculator.validate_inputs(well_scores, context):
                        results[name] = calculator.calculate(well_scores, context)
                    else:
                        logger.warning(f"Custom metric {name} input validation failed")
                except Exception as e:
                    logger.error(f"Custom metric {name} calculation failed: {e}")
        
        return results
```


## Weighting Algorithm Framework

### Weighting Algorithm Interface

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class WeightingDefinition:
    name: str
    display_name: str
    description: str
    algorithm_type: str
    input_requirements: List[str]
    parameters: Dict[str, Any]
    academic_references: List[str]

class WeightingAlgorithm(ABC):
    """Abstract base class for custom weighting algorithms"""
    
    @property
    @abstractmethod
    def definition(self) -> WeightingDefinition:
        """Weighting algorithm specification"""
        pass
    
    @abstractmethod
    def apply_weights(self, 
                      well_scores: Dict[str, float],
                      parameters: Dict[str, Any]) -> Dict[str, float]:
        """
        Apply framework-specific weighting to well scores
        
        Args:
            well_scores: Original well scores {well_name: score}
            parameters: Algorithm-specific parameters
            
        Returns:
            Weighted well scores {well_name: weighted_score}
        """
        pass
    
    @abstractmethod
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """Validate algorithm parameters"""
        pass
    
    def get_effective_weights(self, parameters: Dict[str, Any]) -> Dict[str, float]:
        """Return the actual weights that would be applied"""
        return {}
```


### Example Weighting Algorithm

```python
class CulturalMatrixWeighting(WeightingAlgorithm):
    """Apply cultural demographic-specific weighting to well scores"""
    
    @property
    def definition(self) -> WeightingDefinition:
        return WeightingDefinition(
            name="cultural_matrix_weighting",
            display_name="Cultural Matrix Weighting",
            description="Applies demographic-specific weights based on empirical moral foundation research",
            algorithm_type="matrix_multiplication",
            input_requirements=["well_scores", "cultural_segment"],
            parameters={"cultural_matrices": "framework_defined"},
            academic_references=[
                "Graham, J., et al. (2011). Mapping the moral domain",
                "Haidt, J., & Graham, J. (2007). When morality opposes justice"
            ]
        )
    
    def apply_weights(self, 
                      well_scores: Dict[str, float],
                      parameters: Dict[str, Any]) -> Dict[str, float]:
        cultural_segment = parameters.get("cultural_segment")
        cultural_matrices = parameters.get("cultural_matrices", {})
        
        if not cultural_segment or cultural_segment not in cultural_matrices:
            return well_scores  # Return unmodified if no valid cultural context
        
        cultural_weights = cultural_matrices[cultural_segment]
        weighted_scores = {}
        
        for well_name, score in well_scores.items():
            cultural_multiplier = cultural_weights.get(well_name, 1.0)
            weighted_scores[well_name] = score * cultural_multiplier
        
        return weighted_scores
    
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        required = ["cultural_segment", "cultural_matrices"]
        return all(param in parameters for param in required)
    
    def get_effective_weights(self, parameters: Dict[str, Any]) -> Dict[str, float]:
        cultural_segment = parameters.get("cultural_segment")
        cultural_matrices = parameters.get("cultural_matrices", {})
        
        if cultural_segment in cultural_matrices:
            return cultural_matrices[cultural_segment]
        return {}
```


## Declarative Visualization Schema

### Visualization Definition Format

```json
{
  "visualization_definitions": {
    "cultural_comparison_polar": {
      "id": "cultural_comparison_polar",
      "name": "Cultural Demographic Comparison (Polar)",
      "description": "Multi-segment polar chart showing cultural resonance patterns",
      "base_type": "polar_chart",
      "version": "1.0.0",
      "parameters": {
        "radius_metric": "cultural_resonance_score",
        "angle_mapping": "foundation_weights",
        "color_scheme": "cultural_segment_colors",
        "interactive_elements": ["cultural_selector", "foundation_tooltip"],
        "normalization": "z_score_by_segment"
      },
      "layout": {
        "title_template": "Cultural Resonance Analysis: {cultural_segment}",
        "subtitle_template": "Foundation prioritization across demographic segments",
        "legend_position": "bottom",
        "grid_style": "radial",
        "axis_labels": "foundation_names"
      },
      "data_requirements": {
        "required_metrics": ["cultural_resonance_score"],
        "required_context": ["cultural_segment", "foundation_weights"],
        "minimum_wells": 5
      },
      "export_formats": ["png", "svg", "interactive_html", "pdf"]
    },
    "foundation_heatmap": {
      "id": "foundation_heatmap",
      "name": "Cross-Cultural Foundation Heatmap",
      "description": "Matrix heatmap showing foundation activation across cultural segments",
      "base_type": "matrix_heatmap",
      "version": "1.0.0",
      "parameters": {
        "rows": "cultural_segments",
        "columns": "foundation_names",
        "values": "weighted_scores",
        "color_scale": "diverging_red_blue",
        "clustering": "hierarchical_by_similarity"
      },
      "layout": {
        "title_template": "Foundation Activation Heatmap",
        "color_bar_label": "Weighted Score",
        "annotation_threshold": 0.1
      },
      "data_requirements": {
        "required_metrics": ["weighted_scores"],
        "minimum_segments": 2,
        "minimum_foundations": 3
      }
    }
  }
}
```


### Visualization Engine Architecture

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class VisualizationRenderer(ABC):
    """Abstract base class for visualization renderers"""
    
    @property
    @abstractmethod
    def supported_base_type(self) -> str:
        """Base visualization type this renderer supports"""
        pass
    
    @abstractmethod
    def create(self, 
               definition: Dict[str, Any],
               data: Dict[str, Any],
               context: Optional[Dict[str, Any]] = None) -> go.Figure:
        """Create visualization from definition and data"""
        pass
    
    @abstractmethod
    def validate_definition(self, definition: Dict[str, Any]) -> bool:
        """Validate visualization definition"""
        pass
    
    @abstractmethod
    def validate_data(self, 
                      definition: Dict[str, Any],
                      data: Dict[str, Any]) -> bool:
        """Validate data meets visualization requirements"""
        pass

class PolarVisualizationRenderer(VisualizationRenderer):
    """Render polar chart visualizations"""
    
    @property
    def supported_base_type(self) -> str:
        return "polar_chart"
    
    def create(self, 
               definition: Dict[str, Any],
               data: Dict[str, Any],
               context: Optional[Dict[str, Any]] = None) -> go.Figure:
        
        params = definition["parameters"]
        layout_config = definition.get("layout", {})
        
        # Extract visualization data
        radius_values = data.get(params["radius_metric"], [])
        angle_values = data.get(params["angle_mapping"], [])
        
        # Create polar scatter plot
        fig = go.Figure()
        
        if context and "cultural_segments" in context:
            # Multi-segment comparison
            for segment in context["cultural_segments"]:
                segment_data = data.get(segment, {})
                fig.add_trace(go.Scatterpolar(
                    r=segment_data.get(params["radius_metric"], []),
                    theta=segment_data.get(params["angle_mapping"], []),
                    mode='markers+lines',
                    name=segment.replace("_", " ").title(),
                    line=dict(width=2),
                    marker=dict(size=8)
                ))
        else:
            # Single visualization
            fig.add_trace(go.Scatterpolar(
                r=radius_values,
                theta=angle_values,
                mode='markers+lines',
                name='Narrative Position',
                line=dict(width=3),
                marker=dict(size=10)
            ))
        
        # Apply layout configuration
        title = layout_config.get("title_template", "Polar Visualization")
        if context:
            title = title.format(**context)
        
        fig.update_layout(
            title=title,
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 1]),
                angularaxis=dict(visible=True)
            ),
            showlegend=True
        )
        
        return fig
    
    def validate_definition(self, definition: Dict[str, Any]) -> bool:
        required_params = ["radius_metric", "angle_mapping"]
        params = definition.get("parameters", {})
        return all(param in params for param in required_params)
    
    def validate_data(self, 
                      definition: Dict[str, Any],
                      data: Dict[str, Any]) -> bool:
        params = definition["parameters"]
        required_data = [params["radius_metric"], params["angle_mapping"]]
        return all(key in data for key in required_data)

class VisualizationEngine:
    def __init__(self):
        self.renderers: Dict[str, VisualizationRenderer] = {
            "polar_chart": PolarVisualizationRenderer(),
            "matrix_heatmap": HeatmapVisualizationRenderer(),
            "elliptical": EllipticalVisualizationRenderer(),
            "radial_bar": RadialBarVisualizationRenderer()
        }
        self.custom_renderers: Dict[str, VisualizationRenderer] = {}
    
    def register_renderer(self, renderer: VisualizationRenderer) -> bool:
        """Register custom visualization renderer"""
        try:
            base_type = renderer.supported_base_type
            if base_type in self.renderers:
                logger.warning(f"Overriding existing renderer for {base_type}")
            
            self.custom_renderers[base_type] = renderer
            return True
        except Exception as e:
            logger.error(f"Renderer registration failed: {e}")
            return False
    
    def create_visualization(self, 
                           definition: Dict[str, Any],
                           data: Dict[str, Any],
                           context: Optional[Dict[str, Any]] = None) -> go.Figure:
        """Create visualization from definition"""
        base_type = definition.get("base_type")
        
        # Try custom renderers first
        if base_type in self.custom_renderers:
            renderer = self.custom_renderers[base_type]
        elif base_type in self.renderers:
            renderer = self.renderers[base_type]
        else:
            raise ValueError(f"No renderer available for base_type: {base_type}")
        
        # Validate definition and data
        if not renderer.validate_definition(definition):
            raise ValueError(f"Invalid visualization definition for {base_type}")
        
        if not renderer.validate_data(definition, data):
            raise ValueError(f"Data does not meet requirements for {base_type}")
        
        return renderer.create(definition, data, context)
```


## Security and Validation

### Security Framework

```python
import ast
import sys
import resource
from typing import Set, List
import importlib.util
from pathlib import Path

class PluginSecurityValidator:
    """Comprehensive security validation for plugin code"""
    
    ALLOWED_IMPORTS = {
        'math', 'statistics', 'numpy', 'scipy', 'pandas',
        'typing', 'dataclasses', 'enum', 'abc', 'logging',
        'json', 'csv', 're', 'collections', 'itertools'
    }
    
    FORBIDDEN_FUNCTIONS = {
        'exec', 'eval', 'compile', '__import__', 'open',
        'file', 'input', 'raw_input', 'reload', 'vars',
        'dir', 'globals', 'locals', 'memoryview'
    }
    
    FORBIDDEN_MODULES = {
        'os', 'sys', 'subprocess', 'shutil', 'socket',
        'urllib', 'requests', 'pickle', 'marshal'
    }
    
    MAX_COMPUTATION_TIME = 10.0  # seconds
    MAX_MEMORY_USAGE = 256 * 1024 * 1024  # 256MB
    MAX_FILE_SIZE = 1024 * 1024  # 1MB
    
    def validate_plugin_file(self, plugin_path: Path) -> 'SecurityValidationResult':
        """Comprehensive plugin file validation"""
        try:
            # File size check
            if plugin_path.stat().st_size > self.MAX_FILE_SIZE:
                return SecurityValidationResult(
                    is_valid=False,
                    error="Plugin file exceeds maximum size limit"
                )
            
            # Parse AST for static analysis
            with open(plugin_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            tree = ast.parse(code)
            
            # Check for forbidden operations
            security_issues = self._analyze_ast(tree)
            if security_issues:
                return SecurityValidationResult(
                    is_valid=False,
                    error=f"Security violations found: {security_issues}"
                )
            
            # Test plugin loading in sandboxed environment
            sandbox_result = self._test_plugin_in_sandbox(plugin_path)
            if not sandbox_result.is_valid:
                return sandbox_result
            
            return SecurityValidationResult(is_valid=True)
            
        except Exception as e:
            return SecurityValidationResult(
                is_valid=False,
                error=f"Plugin validation failed: {str(e)}"
            )
    
    def _analyze_ast(self, tree: ast.AST) -> List[str]:
        """Static analysis of AST for security issues"""
        issues = []
        
        for node in ast.walk(tree):
            # Check for forbidden function calls
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in self.FORBIDDEN_FUNCTIONS:
                        issues.append(f"Forbidden function: {node.func.id}")
            
            # Check for forbidden imports
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in self.FORBIDDEN_MODULES:
                        issues.append(f"Forbidden import: {alias.name}")
                    elif alias.name not in self.ALLOWED_IMPORTS:
                        issues.append(f"Unauthorized import: {alias.name}")
            
            elif isinstance(node, ast.ImportFrom):
                if node.module in self.FORBIDDEN_MODULES:
                    issues.append(f"Forbidden import from: {node.module}")
                elif node.module not in self.ALLOWED_IMPORTS:
                    issues.append(f"Unauthorized import from: {node.module}")
        
        return issues
    
    def _test_plugin_in_sandbox(self, plugin_path: Path) -> 'SecurityValidationResult':
        """Test plugin loading with resource limits"""
        try:
            # Set memory limit
            resource.setrlimit(resource.RLIMIT_AS, (self.MAX_MEMORY_USAGE, self.MAX_MEMORY_USAGE))
            
            # Set CPU time limit
            resource.setrlimit(resource.RLIMIT_CPU, (int(self.MAX_COMPUTATION_TIME), int(self.MAX_COMPUTATION_TIME)))
            
            # Load plugin module
            spec = importlib.util.spec_from_file_location("test_plugin", plugin_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Test basic plugin functionality
            if hasattr(module, 'FrameworkPlugin'):
                plugin_class = getattr(module, 'FrameworkPlugin')
                test_plugin = plugin_class()
                
                # Test metadata access
                metadata = test_plugin.metadata
                
                # Test component registration
                components = test_plugin.register_components()
                
                return SecurityValidationResult(is_valid=True)
            else:
                return SecurityValidationResult(
                    is_valid=False,
                    error="Plugin does not contain required FrameworkPlugin class"
                )
                
        except Exception as e:
            return SecurityValidationResult(
                is_valid=False,
                error=f"Sandbox testing failed: {str(e)}"
            )

@dataclass
class SecurityValidationResult:
    is_valid: bool
    error: Optional[str] = None
    warnings: List[str] = None
```


### Framework Validation System

```python
class FrameworkValidator:
    """Comprehensive framework package validation"""
    
    def __init__(self):
        self.security_validator = PluginSecurityValidator()
        self.schema_validator = FrameworkSchemaValidator()
        self.academic_validator = AcademicValidityValidator()
    
    def validate_framework_package(self, framework_path: Path) -> 'FrameworkValidationResult':
        """Complete validation of framework package"""
        results = []
        
        # 1. Package structure validation
        structure_result = self._validate_package_structure(framework_path)
        results.append(structure_result)
        
        # 2. Configuration schema validation
        config_result = self.schema_validator.validate_configuration(framework_path)
        results.append(config_result)
        
        # 3. Plugin security validation
        plugin_file = framework_path / "plugin.py"
        if plugin_file.exists():
            security_result = self.security_validator.validate_plugin_file(plugin_file)
            results.append(security_result)
        
        # 4. Academic validity validation
        academic_result = self.academic_validator.validate_theoretical_foundation(framework_path)
        results.append(academic_result)
        
        # 5. Test suite validation
        test_result = self._validate_test_suite(framework_path)
        results.append(test_result)
        
        # 6. Performance benchmarking
        performance_result = self._validate_performance(framework_path)
        results.append(performance_result)
        
        return FrameworkValidationResult.aggregate(results)
    
    def _validate_package_structure(self, framework_path: Path) -> 'ValidationResult':
        """Validate required files and structure"""
        required_files = [
            "framework.json",
            "dipoles.json", 
            "prompt.md",
            "README.md"
        ]
        
        required_dirs = [
            "docs",
            "tests"
        ]
        
        missing_files = []
        missing_dirs = []
        
        for file_name in required_files:
            if not (framework_path / file_name).exists():
                missing_files.append(file_name)
        
        for dir_name in required_dirs:
            if not (framework_path / dir_name).is_dir():
                missing_dirs.append(dir_name)
        
        if missing_files or missing_dirs:
            return ValidationResult(
                is_valid=False,
                error=f"Missing required files: {missing_files}, directories: {missing_dirs}"
            )
        
        return ValidationResult(is_valid=True)
```


## Implementation Phases

### Phase 1: Core Plugin Infrastructure (4-6 weeks)

**Week 1-2: Plugin Registry and Base Classes**

```python
# Deliverables:
- PluginRegistry class with component management
- Abstract base classes (MetricCalculator, WeightingAlgorithm, VisualizationRenderer)
- SecurityValidationFramework with AST analysis
- Basic plugin loading and registration system
```

**Week 3-4: Metric System Enhancement**

```python
# Deliverables:
- Extended MetricEngine with custom metric support
- Integration with existing calculation pipeline
- Validation and error handling for custom metrics
- Example implementations (CulturalResonanceCalculator)
```

**Week 5-6: Framework Package Structure**

```python
# Deliverables:
- Extended framework.json schema with plugin definitions
- Automatic plugin discovery and loading
- Framework validation pipeline
- Migration tools for existing frameworks
```


### Phase 2: Declarative Visualization System (3-4 weeks)

**Week 1-2: Visualization Engine Architecture**

```python
# Deliverables:
- Base visualization renderer system
- Parametric visualization definitions (JSON schema)
- Integration with existing Plotly infrastructure
- Support for polar, heatmap, and radial visualizations
```

**Week 3-4: Custom Visualization Support**

```python
# Deliverables:
- Custom visualization renderer registration
- Visualization validation and error handling
- Export format support for custom visualizations
- Documentation and examples
```


### Phase 3: Advanced Features and Validation (2-3 weeks)

**Week 1-2: Performance and Security**

```python
# Deliverables:
- Comprehensive security validation system
- Performance monitoring and limits
- Resource usage constraints
- Sandbox testing environment
```

**Week 3: Integration and Testing**

```python
# Deliverables:
- Full integration with existing system
- Comprehensive test suite for plugin architecture
- Performance benchmarking
- Documentation and migration guides
```


## Migration Strategy

### Backward Compatibility Plan

**Existing Framework Preservation**

```python
# All existing frameworks continue working unchanged
frameworks/
├── civic_virtue/           # No changes required
├── political_spectrum/     # No changes required  
├── fukuyama_identity/      # No changes required
└── mft_persuasive_force/   # New plugin-enhanced framework
```

**Gradual Enhancement Path**

1. **Phase 1**: Deploy plugin infrastructure alongside existing system
2. **Phase 2**: Create plugin-enhanced versions of existing frameworks
3. **Phase 3**: Migrate user configurations to plugin-enhanced versions
4. **Phase 4**: Deprecate legacy framework loading system

**Configuration Migration**

```python
class FrameworkMigrator:
    def migrate_legacy_framework(self, legacy_config: Dict) -> Dict:
        """Convert legacy framework config to plugin-enhanced format"""
        enhanced_config = legacy_config.copy()
        
        # Add plugin configuration section
        enhanced_config["plugin_configuration"] = {
            "custom_metrics": [],
            "weighting_algorithms": ["default"],
            "visualization_types": ["elliptical"]
        }
        
        # Preserve existing well definitions and metrics
        return enhanced_config
```


### User Experience Continuity

**API Compatibility**

```python
# Existing API calls continue working
analyzer = NarrativeGravityAnalyzer("civic_virtue")
result = analyzer.analyze(narrative_text)

# Enhanced API provides additional options
analyzer = NarrativeGravityAnalyzer("mft_persuasive_force")
result = analyzer.analyze(narrative_text, cultural_context="progressive_urban")
```

**UI/UX Preservation**

- Existing Streamlit interface remains unchanged
- Plugin-enhanced features appear as optional advanced settings
- Framework selection dropdown includes both legacy and enhanced frameworks
- Results display adapts automatically to available metrics


## Performance Considerations

### Computational Overhead

**Plugin Loading Optimization**

```python
class PluginCache:
    """Cache compiled plugins to avoid repeated loading"""
    
    def __init__(self):
        self._plugin_cache: Dict[str, FrameworkPlugin] = {}
        self._compilation_cache: Dict[str, Any] = {}
    
    def get_plugin(self, framework_name: str) -> Optional[FrameworkPlugin]:
        if framework_name in self._plugin_cache:
            return self._plugin_cache[framework_name]
        
        # Load and cache plugin
        plugin = self._load_plugin(framework_name)
        if plugin:
            self._plugin_cache[framework_name] = plugin
        
        return plugin
```

**Metric Calculation Efficiency**

```python
class MetricBatch:
    """Batch metric calculations for efficiency"""
    
    def calculate_all_metrics(self, 
                              well_scores: Dict[str, float],
                              framework_config: Dict,
                              context: Optional[Dict] = None) -> Dict[str, Any]:
        """Calculate all applicable metrics in single pass"""
        
        # Identify applicable metrics
        applicable_metrics = self._get_applicable_metrics(framework_config)
        
        # Batch calculations to minimize redundant operations
        shared_calculations = self._compute_shared_values(well_scores, context)
        
        results = {}
        for metric_name, calculator in applicable_metrics.items():
            try:
                results[metric_name] = calculator.calculate_with_shared(
                    well_scores, context, shared_calculations
                )
            except Exception as e:
                logger.error(f"Metric {metric_name} calculation failed: {e}")
        
        return results
```


### Memory Management

**Resource Monitoring**

```python
import psutil
import threading
from contextlib import contextmanager

class ResourceMonitor:
    """Monitor and limit plugin resource usage"""
    
    def __init__(self, max_memory_mb: int = 256, max_cpu_seconds: int = 10):
        self.max_memory = max_memory_mb * 1024 * 1024
        self.max_cpu_seconds = max_cpu_seconds
    
    @contextmanager
    def monitor_plugin_execution(self, plugin_name: str):
        """Context manager for monitoring plugin resource usage"""
        process = psutil.Process()
        start_memory = process.memory_info().rss
        start_time = time.time()
        
        try:
            yield
        finally:
            end_memory = process.memory_info().rss
            end_time = time.time()
            
            memory_used = end_memory - start_memory
            cpu_time = end_time - start_time
            
            if memory_used > self.max_memory:
                logger.warning(f"Plugin {plugin_name} exceeded memory limit: {memory_used / 1024 / 1024:.1f}MB")
            
            if cpu_time > self.max_cpu_seconds:
                logger.warning(f"Plugin {plugin_name} exceeded CPU time limit: {cpu_time:.1f}s")
```


## Developer Experience

### Framework Creation Workflow

**1. Framework Template Generation**

```bash
$ narrative-gravity create-framework mft_persuasive_force
Creating framework package: mft_persuasive_force
├── framework.json (template generated)
├── dipoles.json (template generated)
├── prompt.md (template generated)
├── plugin.py (template generated)
├── tests/ (test templates generated)
└── docs/ (documentation templates generated)

Framework template created. Edit configuration files and implement custom logic.
```

**2. Development Environment Setup**

```python
# frameworks/mft_persuasive_force/plugin.py
from narrative_gravity.plugins import FrameworkPlugin, MetricCalculator
from narrative_gravity.validation import ValidationResult

class MFTFrameworkPlugin(FrameworkPlugin):
    @property
    def metadata(self):
        return PluginMetadata(
            name="mft_persuasive_force",
            version="1.0.0",
            author="Research Team",
            description="MFT-based persuasive force analysis",
            plugin_type=PluginType.FRAMEWORK,
            framework_compatibility=["mft_persuasive_force"],
            python_requirements=["numpy>=1.20.0"],
            academic_citations=[
                "Haidt, J. (2012). The righteous mind"
            ]
        )
    
    def register_components(self):
        return {
            PluginType.METRIC_CALCULATOR: {
                "cultural_resonance_score": CulturalResonanceCalculator,
                "foundation_diversity_index": FoundationDiversityCalculator
            },
            PluginType.WEIGHTING_ALGORITHM: {
                "cultural_matrix_weighting": CulturalMatrixWeighting
            }
        }
```

**3. Testing and Validation**

```bash
$ narrative-gravity validate-framework mft_persuasive_force
Validating framework package: mft_persuasive_force

✓ Package structure validation passed
✓ Configuration schema validation passed  
✓ Plugin security validation passed
✓ Academic validity validation passed
✓ Test suite validation passed
✓ Performance benchmarking passed

Framework validation successful. Ready for deployment.
```

**4. Local Testing Environment**

```python
# frameworks/mft_persuasive_force/tests/test_integration.py
import unittest
from narrative_gravity import NarrativeGravityAnalyzer

class TestMFTFrameworkIntegration(unittest.TestCase):
    def setUp(self):
        self.analyzer = NarrativeGravityAnalyzer("mft_persuasive_force")
    
    def test_cultural_resonance_calculation(self):
        """Test cultural resonance metric calculation"""
        test_narrative = "We must protect our vulnerable communities..."
        
        result = self.analyzer.analyze(
            test_narrative,
            cultural_context="progressive_urban"
        )
        
        self.assertIn("cultural_resonance_score", result.metrics)
        self.assertBetween(result.metrics["cultural_resonance_score"], 0.0, 1.0)
    
    def test_cross_cultural_comparison(self):
        """Test cross-cultural analysis capabilities"""
        test_narrative = "We must respect traditional authority..."
        
        results = {}
        for culture in ["progressive_urban", "conservative_religious", "rural_traditional"]:
            results[culture] = self.analyzer.analyze(
                test_narrative,
                cultural_context=culture
            )
        
        # Verify different cultural responses
        progressive_score = results["progressive_urban"].metrics["cultural_resonance_score"]
        conservative_score = results["conservative_religious"].metrics["cultural_resonance_score"]
        
        self.assertGreater(conservative_score, progressive_score)
```


### IDE Integration and Tooling

**VS Code Extension Support**

```json
{
    "name": "narrative-gravity-framework-dev",
    "displayName": "Narrative Gravity Framework Development",
    "description": "Development support for Narrative Gravity Wells frameworks",
    "version": "1.0.0",
    "contributes": {
        "languages": [{
            "id": "framework-json",
            "aliases": ["Framework JSON"],
            "extensions": [".framework.json"]
        }],
        "jsonValidation": [{
            "fileMatch": "*/frameworks/*/framework.json", 
            "url": "./schemas/framework-schema.json"
        }],
        "commands": [{
            "command": "narrativeGravity.validateFramework",
            "title": "Validate Framework Package"
        }]
    }
}
```

**Schema Validation and Autocomplete**

```json
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Narrative Gravity Framework Configuration",
    "type": "object",
    "required": ["framework_name", "version", "dipoles", "wells"],
    "properties": {
        "framework_name": {
            "type": "string",
            "pattern": "^[a-z][a-z0-9_]*$",
            "description": "Unique framework identifier"
        },
        "custom_metrics": {
            "type": "array",
            "items": {
                "$ref": "#/definitions/metric_definition"
            }
        }
    },
    "definitions": {
        "metric_definition": {
            "type": "object",
            "required": ["name", "calculator_class", "output_type"],
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Metric identifier"
                },
                "calculator_class": {
                    "type": "string",
                    "description": "Python class name for metric calculator"
                }
            }
        }
    }
}
```


## Quality Assurance

### Automated Testing Framework

**Plugin Validation Pipeline**

```python
class PluginTestSuite:
    """Comprehensive automated testing for framework plugins"""
    
    def __init__(self, framework_path: Path):
        self.framework_path = framework_path
        self.test_results = []
    
    def run_full_test_suite(self) -> 'TestResults':
        """Execute all plugin validation tests"""
        
        # 1. Static Analysis Tests
        self.test_results.append(self._run_static_analysis())
        
        # 2. Security Validation Tests
        self.test_results.append(self._run_security_tests())
        
        # 3. Functional Testing
        self.test_results.append(self._run_functional_tests())
        
        # 4. Performance Testing
        self.test_results.append(self._run_performance_tests())
        
        # 5. Integration Testing
        self.test_results.append(self._run_integration_tests())
        
        # 6. Regression Testing
        self.test_results.append(self._run_regression_tests())
        
        return TestResults.aggregate(self.test_results)
    
    def _run_functional_tests(self) -> 'TestResult':
        """Test all custom metrics and algorithms"""
        plugin = self._load_test_plugin()
        test_data = self._generate_test_data()
        
        results = []
        
        # Test each custom metric
        for metric_name, calculator in plugin.register_components()[PluginType.METRIC_CALCULATOR].items():
            try:
                # Test with valid inputs
                result = calculator.calculate(test_data["well_scores"], test_data["context"])
                
                # Validate output range
                if hasattr(calculator.definition, 'output_range'):
                    min_val, max_val = calculator.definition.output_range
                    if not (min_val <= result <= max_val):
                        results.append(TestResult(
                            test_name=f"{metric_name}_output_range",
                            passed=False,
                            error=f"Output {result} outside range [{min_val}, {max_val}]"
                        ))
                
                # Test input validation
                invalid_inputs = self._generate_invalid_inputs()
                for invalid_input in invalid_inputs:
                    should_reject = not calculator.validate_inputs(**invalid_input)
                    if not should_reject:
                        results.append(TestResult(
                            test_name=f"{metric_name}_input_validation",
                            passed=False,
                            error=f"Should reject invalid input: {invalid_input}"
                        ))
                
                results.append(TestResult(
                    test_name=f"{metric_name}_functional_test",
                    passed=True
                ))
                
            except Exception as e:
                results.append(TestResult(
                    test_name=f"{metric_name}_functional_test",
                    passed=False,
                    error=str(e)
                ))
        
        return TestResult.aggregate(results)
```


### Peer Review Process

**Academic Review Workflow**

```python
class AcademicReviewProcess:
    """Framework for academic peer review of framework packages"""
    
    def __init__(self):
        self.review_criteria = [
            "theoretical_foundation",
            "methodological_rigor", 
            "empirical_validation",
            "reproducibility",
            "academic_citations",
            "ethical_considerations"
        ]
    
    def initiate_review(self, framework_package: Path, reviewers: List[str]) -> str:
        """Start academic review process"""
        review_id = self._generate_review_id()
        
        # Package framework for review
        review_package = self._create_review_package(framework_package)
        
        # Send to reviewers
        for reviewer_email in reviewers:
            self._send_review_request(reviewer_email, review_package, review_id)
        
        # Create review tracking
        self._create_review_tracking(review_id, framework_package, reviewers)
        
        return review_id
    
    def submit_review(self, review_id: str, reviewer_id: str, review_data: Dict) -> bool:
        """Submit individual review"""
        
        # Validate review completeness
        if not self._validate_review_completeness(review_data):
            return False
        
        # Store review
        self._store_review(review_id, reviewer_id, review_data)
        
        # Check if all reviews submitted
        if self._all_reviews_submitted(review_id):
            self._compile_final_review(review_id)
        
        return True
    
    def _validate_review_completeness(self, review_data: Dict) -> bool:
        """Ensure review covers all required criteria"""
        required_sections = [
            "theoretical_assessment",
            "methodological_evaluation", 
            "technical_implementation_review",
            "reproducibility_check",
            "ethical_considerations",
            "overall_recommendation"
        ]
        
        return all(section in review_data for section in required_sections)
```


## Future Extensions

### Advanced Plugin Capabilities

**Machine Learning Integration**

```python
class MLEnhancedMetricCalculator(MetricCalculator):
    """Base class for ML-enhanced metrics"""
    
    def __init__(self, model_path: Optional[Path] = None):
        self.model = self._load_model(model_path) if model_path else None
    
    def calculate_with_ml_enhancement(self,
                                      well_scores: Dict[str, float],
                                      narrative_text: str,
                                      context: Optional[Dict] = None) -> float:
        """Calculate metric using both rule-based and ML approaches"""
        
        # Traditional calculation
        base_score = self.calculate(well_scores, context)
        
        # ML enhancement
        if self.model and narrative_text:
            ml_features = self._extract_ml_features(narrative_text, well_scores, context)
            ml_adjustment = self.model.predict(ml_features)
            
            # Combine base score with ML adjustment
            enhanced_score = self._combine_scores(base_score, ml_adjustment)
            return enhanced_score
        
        return base_score
```

**Real-time Analysis Capabilities**

```python
class StreamingAnalysisPlugin(FrameworkPlugin):
    """Plugin supporting real-time narrative analysis"""
    
    def register_streaming_components(self) -> Dict[str, Any]:
        return {
            "stream_processors": {
                "social_media_stream": SocialMediaStreamProcessor,
                "news_feed_stream": NewsFeedStreamProcessor
            },
            "real_time_metrics": {
                "trending_narratives": TrendingNarrativesCalculator,
                "narrative_velocity": NarrativeVelocityCalculator
            }
        }
    
    def create_stream_analyzer(self, stream_config: Dict) -> 'StreamAnalyzer':
        """Create real-time stream analyzer"""
        return StreamAnalyzer(
            framework=self,
            stream_config=stream_config,
            buffer_size=stream_config.get("buffer_size", 1000),
            analysis_interval=stream_config.get("interval", 60)
        )
```

**Cross-Framework Comparison Tools**

```python
class FrameworkComparator:
    """Advanced tools for comparing frameworks and their outputs"""
    
    def compare_framework_outputs(self,
                                  narrative: str,
                                  frameworks: List[str],
                                  comparison_metrics: List[str]) -> 'ComparisonResult':
        """Compare how different frameworks analyze the same narrative"""
        
        results = {}
        
        for framework_name in frameworks:
            analyzer = NarrativeGravityAnalyzer(framework_name)
            results[framework_name] = analyzer.analyze(narrative)
        
        # Calculate cross-framework correlations
        correlations = self._calculate_cross_framework_correlations(results, comparison_metrics)
        
        # Identify framework agreement/disagreement
        consensus_analysis = self._analyze_framework_consensus(results)
        
        # Generate comparative visualization
        comparison_viz = self._create_comparison_visualization(results)
        
        return ComparisonResult(
            framework_results=results,
            correlations=correlations,
            consensus_analysis=consensus_analysis,
            visualization=comparison_viz
        )
```


### Ecosystem Development

**Framework Marketplace**

```python
class FrameworkMarketplace:
    """Central repository for community-contributed frameworks"""
    
    def __init__(self, registry_url: str):
        self.registry_url = registry_url
        self.local_cache = FrameworkCache()
    
    def search_frameworks(self, 
                          query: str,
                          filters: Optional[Dict] = None) -> List['FrameworkListing']:
        """Search available frameworks by topic, author, or capability"""
        
        search_params = {
            "query": query,
            "filters": filters or {},
            "sort_by": "popularity",
            "limit": 50
        }
        
        response = requests.get(f"{self.registry_url}/search", params=search_params)
        return [FrameworkListing.from_dict(item) for item in response.json()]
    
    def install_framework(self, framework_id: str, version: str = "latest") -> bool:
        """Install framework from marketplace"""
        
        # Download framework package
        package_url = f"{self.registry_url}/packages/{framework_id}/{version}"
        package_data = requests.get(package_url).content
        
        # Validate package security
        if not self._validate_package_security(package_data):
            logger.error(f"Security validation failed for {framework_id}")
            return False
        
        # Install to local frameworks directory
        framework_path = Path(f"frameworks/{framework_id}")
        self._extract_package(package_data, framework_path)
        
        # Validate installation
        validator = FrameworkValidator()
        validation_result = validator.validate_framework_package(framework_path)
        
        if not validation_result.is_valid:
            logger.error(f"Framework validation failed: {validation_result.error}")
            shutil.rmtree(framework_path)
            return False
        
        # Update local registry
        self.local_cache.register_framework(framework_id, version, framework_path)
        
        return True
```

**Community Contribution Tools**

```python
class FrameworkContributor:
    """Tools for contributing frameworks to the community"""
    
    def package_framework(self, framework_path: Path) -> Path:
        """Package framework for distribution"""
        
        # Validate framework completeness
        validator = FrameworkValidator()
        validation_result = validator.validate_framework_package(framework_path)
        
        if not validation_result.is_valid:
            raise ValueError(f"Framework validation failed: {validation_result.error}")
        
        # Create distribution package
        package_path = self._create_distribution_package(framework_path)
        
        # Generate package metadata
        metadata = self._generate_package_metadata(framework_path)
        
        # Sign package for authenticity
        signature = self._sign_package(package_path)
        
        return package_path
    
    def submit_framework(self, 
                         package_path: Path,
                         submission_metadata: Dict) -> str:
        """Submit framework to community marketplace"""
        
        # Upload package
        upload_response = self._upload_package(package_path)
        
        # Submit for review
        review_request = {
            "package_id": upload_response["package_id"],
            "metadata": submission_metadata,
            "author_info": self._get_author_info(),
            "review_level": "community"  # or "academic" for academic review
        }
        
        review_response = requests.post(
            f"{self.marketplace_url}/submit",
            json=review_request
        )
        
        return review_response.json()["submission_id"]
```


## Resource Requirements

### Development Resources

**Personnel Requirements**

- **Senior Software Engineer**: 0.8 FTE for 12 weeks (plugin architecture, security)
- **Research Software Engineer**: 0.6 FTE for 8 weeks (visualization system, integration)
- **Academic Researcher**: 0.3 FTE for 16 weeks (validation, documentation)
- **QA Engineer**: 0.4 FTE for 6 weeks (testing, validation pipeline)

**Total Estimated Effort**: ~40 person-weeks

### Infrastructure Requirements

**Development Environment**

- Enhanced CI/CD pipeline with plugin validation
- Expanded test infrastructure for cross-framework validation
- Security scanning and analysis tools
- Performance monitoring and benchmarking systems

**Storage and Compute**

- Additional 50GB storage for framework packages and caches
- Increased memory allocation for parallel framework testing
- Sandbox environments for plugin security validation


### Budget Estimation

**Development Phase** (12 weeks)

- Personnel: \$180,000 (blended rates)
- Infrastructure: \$5,000 (enhanced CI/CD, security tools)
- External Security Audit: \$15,000
- Academic Review Process: \$8,000

**Total Estimated Cost**: \$208,000

**Post-Launch Maintenance** (Annual)

- Framework review and validation: \$25,000
- Community support and marketplace maintenance: \$15,000
- Security updates and monitoring: \$10,000

**Annual Maintenance Cost**: \$50,000

---

## Conclusion

The Plugin Architecture Enhancement represents a transformative evolution of the Narrative Gravity Wells system, enabling unlimited innovation in political narrative analysis while maintaining the academic rigor and reliability that distinguishes the platform. By implementing this architecture after successful validation studies, the project can evolve from a specific analytical tool into a platform for building analytical tools—creating lasting value for the academic community and establishing a foundation for continued innovation in computational political communication research.

The comprehensive specification provided here ensures that when the time comes for implementation, the development team will have a clear roadmap for creating a secure, efficient, and academically rigorous plugin system that respects both the technical constraints of software development and the methodological requirements of academic research.

**Implementation Recommendation**: Proceed with current validation studies using existing architecture, then implement this plugin enhancement as a post-publication priority to maximize both academic impact and long-term system sustainability.

<div style="text-align: center">⁂</div>

[^1]: readme.md

