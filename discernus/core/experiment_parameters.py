#!/usr/bin/env python3
"""
Experiment Parameters Parser
===========================

Parses reliability filtering parameters from experiment specifications.
Supports both YAML and markdown formats with sensible defaults.
"""

import yaml
import re
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ReliabilityFilteringParams:
    """
    Reliability filtering parameters for statistical analysis.
    
    NOTE: Reliability filtering is OPT-IN ONLY. If no filtering parameters are specified
    in the experiment, ALL dimensions will be included in the analysis (no filtering).
    
    To enable filtering, explicitly specify threshold values in your experiment specification.
    """
    salience_threshold: float = None
    confidence_threshold: float = None
    reliability_threshold: float = None
    reliability_calculation: str = "confidence_x_salience"
    framework_fit_required: bool = False
    framework_fit_threshold: float = 0.3
    
    def is_filtering_enabled(self) -> bool:
        """Check if any filtering is enabled (opt-in)."""
        return (self.salience_threshold is not None or 
                self.confidence_threshold is not None or 
                self.reliability_threshold is not None)


@dataclass
class AdvancedFilteringParams:
    """Advanced filtering parameters for per-dimension control."""
    dimension_specific_thresholds: Dict[str, float] = None
    exclude_dimensions: list = None
    include_dimensions: list = None
    
    def __post_init__(self):
        if self.dimension_specific_thresholds is None:
            self.dimension_specific_thresholds = {}
        if self.exclude_dimensions is None:
            self.exclude_dimensions = []
        if self.include_dimensions is None:
            self.include_dimensions = []


@dataclass
class ExperimentParameters:
    """Complete experiment parameters including reliability filtering."""
    reliability_filtering: ReliabilityFilteringParams
    advanced_filtering: AdvancedFilteringParams = None
    
    def __post_init__(self):
        if self.advanced_filtering is None:
            self.advanced_filtering = AdvancedFilteringParams()


def parse_experiment_parameters(experiment_path: Path) -> ExperimentParameters:
    """
    Parse reliability filtering parameters from experiment specification.
    
    Args:
        experiment_path: Path to experiment directory containing experiment.md
        
    Returns:
        ExperimentParameters object with parsed parameters and defaults
    """
    experiment_file = experiment_path / "experiment.md"
    
    if not experiment_file.exists():
        # Return defaults if no experiment file
        return ExperimentParameters(
            reliability_filtering=ReliabilityFilteringParams()
        )
    
    # Read experiment file
    with open(experiment_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Try to extract YAML configuration
    yaml_config = _extract_yaml_config(content)
    
    if yaml_config:
        return _parse_yaml_parameters(yaml_config)
    else:
        # Fallback to markdown parsing
        return _parse_markdown_parameters(content)


def _extract_yaml_config(content: str) -> Optional[Dict[str, Any]]:
    """Extract YAML configuration from markdown content."""
    # Look for YAML code block
    yaml_pattern = r'```yaml\s*\n(.*?)\n```'
    match = re.search(yaml_pattern, content, re.DOTALL)
    
    if match:
        yaml_content = match.group(1)
        try:
            return yaml.safe_load(yaml_content)
        except yaml.YAMLError:
            return None
    
    return None


def _parse_yaml_parameters(config: Dict[str, Any]) -> ExperimentParameters:
    """Parse parameters from YAML configuration."""
    # Parse reliability filtering parameters
    reliability_config = config.get('reliability_filtering', {})
    reliability_params = ReliabilityFilteringParams(
        salience_threshold=reliability_config.get('salience_threshold', 0.0),
        confidence_threshold=reliability_config.get('confidence_threshold', 0.0),
        reliability_threshold=reliability_config.get('reliability_threshold', 0.0),
        reliability_calculation=reliability_config.get('reliability_calculation', 'confidence_x_salience'),
        framework_fit_required=reliability_config.get('framework_fit_required', False),
        framework_fit_threshold=reliability_config.get('framework_fit_threshold', 0.3)
    )
    
    # Parse advanced filtering parameters
    advanced_config = config.get('advanced_filtering', {})
    advanced_params = AdvancedFilteringParams(
        dimension_specific_thresholds=advanced_config.get('dimension_specific_thresholds', {}),
        exclude_dimensions=advanced_config.get('exclude_dimensions', []),
        include_dimensions=advanced_config.get('include_dimensions', [])
    )
    
    return ExperimentParameters(
        reliability_filtering=reliability_params,
        advanced_filtering=advanced_params
    )


def _parse_markdown_parameters(content: str) -> ExperimentParameters:
    """Parse parameters from markdown content (fallback method)."""
    # Look for reliability filtering section
    reliability_section = _extract_section(content, "Reliability Filtering Parameters")
    
    if not reliability_section:
        return ExperimentParameters(
            reliability_filtering=ReliabilityFilteringParams()
        )
    
    # Parse individual parameters
    params = {}
    
    # Extract salience threshold
    salience_match = re.search(r'salience_threshold.*?(\d+\.?\d*)', reliability_section)
    if salience_match:
        params['salience_threshold'] = float(salience_match.group(1))
    
    # Extract confidence threshold
    confidence_match = re.search(r'confidence_threshold.*?(\d+\.?\d*)', reliability_section)
    if confidence_match:
        params['confidence_threshold'] = float(confidence_match.group(1))
    
    # Extract reliability threshold
    reliability_match = re.search(r'reliability_threshold.*?(\d+\.?\d*)', reliability_section)
    if reliability_match:
        params['reliability_threshold'] = float(reliability_match.group(1))
    
    # Extract reliability calculation method
    calc_match = re.search(r'reliability_calculation.*?"([^"]*)"', reliability_section)
    if calc_match:
        params['reliability_calculation'] = calc_match.group(1)
    
    # Extract framework fit required
    fit_required_match = re.search(r'framework_fit_required.*?(true|false)', reliability_section, re.IGNORECASE)
    if fit_required_match:
        params['framework_fit_required'] = fit_required_match.group(1).lower() == 'true'
    
    # Extract framework fit threshold
    fit_threshold_match = re.search(r'framework_fit_threshold.*?(\d+\.?\d*)', reliability_section)
    if fit_threshold_match:
        params['framework_fit_threshold'] = float(fit_threshold_match.group(1))
    
    # Create parameters with defaults for missing values
    reliability_params = ReliabilityFilteringParams(
        salience_threshold=params.get('salience_threshold', 0.0),
        confidence_threshold=params.get('confidence_threshold', 0.0),
        reliability_threshold=params.get('reliability_threshold', 0.0),
        reliability_calculation=params.get('reliability_calculation', 'confidence_x_salience'),
        framework_fit_required=params.get('framework_fit_required', False),
        framework_fit_threshold=params.get('framework_fit_threshold', 0.3)
    )
    
    return ExperimentParameters(
        reliability_filtering=reliability_params
    )


def _extract_section(content: str, section_name: str) -> Optional[str]:
    """Extract a section from markdown content."""
    # Look for section header
    pattern = rf'## {re.escape(section_name)}(.*?)(?=##|\Z)'
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        return match.group(1).strip()
    
    return None


def validate_parameters(params: ExperimentParameters) -> None:
    """
    Validate experiment parameters for correctness.
    
    Args:
        params: Experiment parameters to validate
        
    Raises:
        ValueError: If parameters are invalid
    """
    # Validate reliability filtering parameters
    rf = params.reliability_filtering
    
    if not 0.0 <= rf.salience_threshold <= 1.0:
        raise ValueError(f"salience_threshold must be between 0.0 and 1.0, got {rf.salience_threshold}")
    
    if not 0.0 <= rf.confidence_threshold <= 1.0:
        raise ValueError(f"confidence_threshold must be between 0.0 and 1.0, got {rf.confidence_threshold}")
    
    if not 0.0 <= rf.reliability_threshold <= 1.0:
        raise ValueError(f"reliability_threshold must be between 0.0 and 1.0, got {rf.reliability_threshold}")
    
    if rf.reliability_calculation not in ['confidence_x_salience', 'confidence', 'salience']:
        raise ValueError(f"reliability_calculation must be one of ['confidence_x_salience', 'confidence', 'salience'], got {rf.reliability_calculation}")
    
    if not 0.0 <= rf.framework_fit_threshold <= 1.0:
        raise ValueError(f"framework_fit_threshold must be between 0.0 and 1.0, got {rf.framework_fit_threshold}")
    
    # Validate advanced filtering parameters
    if params.advanced_filtering:
        af = params.advanced_filtering
        
        # Validate dimension-specific thresholds
        for dimension, threshold in af.dimension_specific_thresholds.items():
            if not 0.0 <= threshold <= 1.0:
                raise ValueError(f"dimension_specific_threshold for {dimension} must be between 0.0 and 1.0, got {threshold}")
        
        # Validate that exclude and include dimensions don't overlap
        overlap = set(af.exclude_dimensions) & set(af.include_dimensions)
        if overlap:
            raise ValueError(f"Dimensions cannot be both excluded and included: {overlap}")


def get_default_parameters() -> ExperimentParameters:
    """Get default experiment parameters."""
    return ExperimentParameters(
        reliability_filtering=ReliabilityFilteringParams()
    )
