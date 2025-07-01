"""
DCS Metrics Package
==================

Mathematical validation and analysis metrics for Framework Specification v3.2+.
Supports the Mathematical Foundations v1.0 requirements for academic rigor.

Critical Path: Brazil 2018 Democratic Tension Axis Model validation.
"""

from .framework_validation import (
    calculate_territorial_coverage,
    calculate_anchor_independence_index,
    calculate_cartographic_resolution,
    calculate_framework_fitness_score
)

from .component_registry_validation import (
    validate_component_registry,
    validate_polar_constraint,
    validate_hybrid_architecture,
    validate_framework_v32_compliance
)

from .orthogonal_axis_metrics import (
    calculate_axis_independence,
    validate_orthogonal_design,
    calculate_quadrant_distribution
)

from .cross_methodology_metrics import (
    calculate_tamaki_fuks_compatibility,
    cross_validate_frameworks,
    compare_methodological_approaches,
    validate_brazil_2018_specific_requirements
)

__all__ = [
    # Framework Validation
    'calculate_territorial_coverage',
    'calculate_anchor_independence_index', 
    'calculate_cartographic_resolution',
    'calculate_framework_fitness_score',
    
    # Component Registry Validation  
    'validate_component_registry',
    'validate_polar_constraint',
    'validate_hybrid_architecture',
    'validate_framework_v32_compliance',
    
    # Orthogonal Axis Metrics
    'calculate_axis_independence',
    'validate_orthogonal_design',
    'calculate_quadrant_distribution',
    
    # Cross-Methodology Metrics
    'calculate_tamaki_fuks_compatibility',
    'cross_validate_frameworks',
    'compare_methodological_approaches',
    'validate_brazil_2018_specific_requirements'
] 