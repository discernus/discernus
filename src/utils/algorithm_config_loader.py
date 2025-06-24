"""
Algorithm Configuration Loader for Discernus Framework v3.0
===========================================================

Handles loading, validation, and management of configurable algorithm parameters
from YAML framework specifications. Provides backward-compatible defaults and
comprehensive parameter validation for the LLM-prompting-amplification pipeline.

Features:
- Load algorithm config from YAML frameworks
- Backward-compatible defaults for existing frameworks
- Parameter validation and range checking
- Error handling for malformed configurations
- Academic transparency and documentation support
"""

import yaml
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path
import warnings
from dataclasses import dataclass, field


@dataclass
class DominanceAmplificationConfig:
    """Configuration for dominance amplification algorithm."""
    enabled: bool = True
    threshold: float = 0.7
    multiplier: float = 1.1
    rationale: str = "Enhances LLM-identified dominant themes for analytical clarity"
    
    def validate(self) -> List[str]:
        """Validate configuration parameters and return list of errors."""
        errors = []
        
        if not isinstance(self.enabled, bool):
            errors.append("enabled must be boolean (true/false)")
            
        if not isinstance(self.threshold, (int, float)):
            errors.append("threshold must be numeric")
        elif not (0.0 <= self.threshold <= 1.0):
            errors.append("threshold must be between 0.0 and 1.0")
            
        if not isinstance(self.multiplier, (int, float)):
            errors.append("multiplier must be numeric")
        elif self.multiplier < 1.0:
            errors.append("multiplier must be >= 1.0 (cannot reduce scores)")
        elif self.multiplier > 2.0:
            warnings.warn(f"multiplier {self.multiplier} > 2.0 may cause excessive amplification")
            
        if not isinstance(self.rationale, str) or not self.rationale.strip():
            errors.append("rationale must be non-empty string for academic transparency")
            
        return errors


@dataclass
class AdaptiveScalingConfig:
    """Configuration for adaptive scaling algorithm."""
    enabled: bool = True
    base_scaling: float = 0.65
    max_scaling: float = 0.95
    variance_factor: float = 0.3
    mean_factor: float = 0.1
    methodology: str = "Optimizes coordinate space utilization based on narrative characteristics"
    
    def validate(self) -> List[str]:
        """Validate configuration parameters and return list of errors."""
        errors = []
        
        if not isinstance(self.enabled, bool):
            errors.append("enabled must be boolean (true/false)")
            
        if not isinstance(self.base_scaling, (int, float)):
            errors.append("base_scaling must be numeric")
        elif not (0.3 <= self.base_scaling <= 0.8):
            errors.append("base_scaling must be between 0.3 and 0.8")
            
        if not isinstance(self.max_scaling, (int, float)):
            errors.append("max_scaling must be numeric")
        elif not (0.8 <= self.max_scaling <= 1.0):
            errors.append("max_scaling must be between 0.8 and 1.0")
            
        if self.base_scaling >= self.max_scaling:
            errors.append("base_scaling must be < max_scaling")
            
        if not isinstance(self.variance_factor, (int, float)):
            errors.append("variance_factor must be numeric")
        elif not (0.1 <= self.variance_factor <= 0.5):
            errors.append("variance_factor must be between 0.1 and 0.5")
            
        if not isinstance(self.mean_factor, (int, float)):
            errors.append("mean_factor must be numeric")
        elif not (0.05 <= self.mean_factor <= 0.2):
            errors.append("mean_factor must be between 0.05 and 0.2")
            
        if not isinstance(self.methodology, str) or not self.methodology.strip():
            errors.append("methodology must be non-empty string for documentation")
            
        return errors


@dataclass
class PromptingIntegrationConfig:
    """Configuration for LLM prompting integration."""
    dominance_instruction: str = "Identify hierarchical dominance patterns in the analyzed text"
    amplification_purpose: str = "Mathematical enhancement of computationally-identified dominance"
    methodology_reference: str = "LLM-prompting-amplification pipeline v3.0"
    
    def validate(self) -> List[str]:
        """Validate configuration parameters and return list of errors."""
        errors = []
        
        if not isinstance(self.dominance_instruction, str) or not self.dominance_instruction.strip():
            errors.append("dominance_instruction must be non-empty string")
            
        if not isinstance(self.amplification_purpose, str) or not self.amplification_purpose.strip():
            errors.append("amplification_purpose must be non-empty string")
            
        if not isinstance(self.methodology_reference, str) or not self.methodology_reference.strip():
            errors.append("methodology_reference must be non-empty string")
            
        return errors


@dataclass 
class AlgorithmConfig:
    """Complete algorithm configuration for Discernus coordinate engine."""
    dominance_amplification: DominanceAmplificationConfig = field(default_factory=DominanceAmplificationConfig)
    adaptive_scaling: AdaptiveScalingConfig = field(default_factory=AdaptiveScalingConfig)
    prompting_integration: PromptingIntegrationConfig = field(default_factory=PromptingIntegrationConfig)
    
    def validate(self) -> Tuple[bool, List[str]]:
        """Validate all configuration sections and return (is_valid, errors)."""
        all_errors = []
        
        all_errors.extend(self.dominance_amplification.validate())
        all_errors.extend(self.adaptive_scaling.validate())
        all_errors.extend(self.prompting_integration.validate())
        
        return len(all_errors) == 0, all_errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization/logging."""
        return {
            'dominance_amplification': {
                'enabled': self.dominance_amplification.enabled,
                'threshold': self.dominance_amplification.threshold,
                'multiplier': self.dominance_amplification.multiplier,
                'rationale': self.dominance_amplification.rationale
            },
            'adaptive_scaling': {
                'enabled': self.adaptive_scaling.enabled,
                'base_scaling': self.adaptive_scaling.base_scaling,
                'max_scaling': self.adaptive_scaling.max_scaling,
                'variance_factor': self.adaptive_scaling.variance_factor,
                'mean_factor': self.adaptive_scaling.mean_factor,
                'methodology': self.adaptive_scaling.methodology
            },
            'prompting_integration': {
                'dominance_instruction': self.prompting_integration.dominance_instruction,
                'amplification_purpose': self.prompting_integration.amplification_purpose,
                'methodology_reference': self.prompting_integration.methodology_reference
            }
        }


class AlgorithmConfigLoader:
    """
    Loads and validates algorithm configuration from YAML frameworks.
    
    Provides backward-compatible defaults for frameworks without algorithm_config sections
    and comprehensive validation for configurations that are present.
    """
    
    def __init__(self):
        self.default_config = AlgorithmConfig()
        
    def load_from_framework_path(self, framework_path: str) -> AlgorithmConfig:
        """
        Load algorithm configuration from YAML framework file.
        
        Args:
            framework_path: Path to YAML framework file
            
        Returns:
            AlgorithmConfig object with loaded or default configuration
            
        Raises:
            FileNotFoundError: If framework file doesn't exist
            yaml.YAMLError: If framework file has invalid YAML syntax
            ValueError: If algorithm configuration is invalid
        """
        framework_path = Path(framework_path)
        
        if not framework_path.exists():
            raise FileNotFoundError(f"Framework file not found: {framework_path}")
            
        try:
            with open(framework_path, 'r', encoding='utf-8') as f:
                framework_data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Invalid YAML in framework file {framework_path}: {e}")
            
        return self.load_from_framework_data(framework_data, str(framework_path))
    
    def load_from_framework_data(self, framework_data: Dict[str, Any], source_name: str = "framework") -> AlgorithmConfig:
        """
        Load algorithm configuration from framework data dictionary.
        
        Args:
            framework_data: Dictionary containing framework specification
            source_name: Name of source for error reporting
            
        Returns:
            AlgorithmConfig object with loaded or default configuration
            
        Raises:
            ValueError: If algorithm configuration is invalid
        """
        if 'algorithm_config' not in framework_data:
            # Backward compatibility: use defaults for frameworks without algorithm_config
            print(f"ℹ️  No algorithm_config found in {source_name}, using defaults")
            return self.default_config
            
        algo_config_data = framework_data['algorithm_config']
        
        try:
            config = self._parse_algorithm_config(algo_config_data)
            is_valid, errors = config.validate()
            
            if not is_valid:
                error_msg = f"Invalid algorithm configuration in {source_name}:\n" + "\n".join(f"  - {error}" for error in errors)
                raise ValueError(error_msg)
                
            print(f"✅ Loaded algorithm configuration from {source_name}")
            return config
            
        except Exception as e:
            if isinstance(e, ValueError):
                raise
            raise ValueError(f"Error parsing algorithm configuration in {source_name}: {e}")
    
    def _parse_algorithm_config(self, config_data: Dict[str, Any]) -> AlgorithmConfig:
        """Parse algorithm configuration data into structured configuration object."""
        
        # Parse dominance amplification
        dominance_config = DominanceAmplificationConfig()
        if 'dominance_amplification' in config_data:
            dom_data = config_data['dominance_amplification']
            if 'enabled' in dom_data:
                dominance_config.enabled = dom_data['enabled']
            if 'threshold' in dom_data:
                dominance_config.threshold = float(dom_data['threshold'])
            if 'multiplier' in dom_data:
                dominance_config.multiplier = float(dom_data['multiplier'])
            if 'rationale' in dom_data:
                dominance_config.rationale = str(dom_data['rationale'])
                
        # Parse adaptive scaling
        scaling_config = AdaptiveScalingConfig()
        if 'adaptive_scaling' in config_data:
            scale_data = config_data['adaptive_scaling']
            if 'enabled' in scale_data:
                scaling_config.enabled = scale_data['enabled']
            if 'base_scaling' in scale_data:
                scaling_config.base_scaling = float(scale_data['base_scaling'])
            if 'max_scaling' in scale_data:
                scaling_config.max_scaling = float(scale_data['max_scaling'])
            if 'variance_factor' in scale_data:
                scaling_config.variance_factor = float(scale_data['variance_factor'])
            if 'mean_factor' in scale_data:
                scaling_config.mean_factor = float(scale_data['mean_factor'])
            if 'methodology' in scale_data:
                scaling_config.methodology = str(scale_data['methodology'])
                
        # Parse prompting integration
        prompt_config = PromptingIntegrationConfig()
        if 'prompting_integration' in config_data:
            prompt_data = config_data['prompting_integration']
            if 'dominance_instruction' in prompt_data:
                prompt_config.dominance_instruction = str(prompt_data['dominance_instruction'])
            if 'amplification_purpose' in prompt_data:
                prompt_config.amplification_purpose = str(prompt_data['amplification_purpose'])
            if 'methodology_reference' in prompt_data:
                prompt_config.methodology_reference = str(prompt_data['methodology_reference'])
                
        return AlgorithmConfig(
            dominance_amplification=dominance_config,
            adaptive_scaling=scaling_config,
            prompting_integration=prompt_config
        )
    
    def get_default_config(self) -> AlgorithmConfig:
        """Get default algorithm configuration for backward compatibility."""
        return self.default_config
    
    def validate_config_dict(self, config_dict: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate algorithm configuration dictionary without loading.
        
        Args:
            config_dict: Dictionary containing algorithm_config section
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        try:
            config = self._parse_algorithm_config(config_dict)
            return config.validate()
        except Exception as e:
            return False, [f"Configuration parsing error: {e}"]


def load_algorithm_config(framework_path: str) -> AlgorithmConfig:
    """
    Convenience function to load algorithm configuration from framework path.
    
    Args:
        framework_path: Path to YAML framework file
        
    Returns:
        AlgorithmConfig object
        
    Raises:
        FileNotFoundError: If framework file doesn't exist
        ValueError: If configuration is invalid
    """
    loader = AlgorithmConfigLoader()
    return loader.load_from_framework_path(framework_path)


def get_default_algorithm_config() -> AlgorithmConfig:
    """
    Convenience function to get default algorithm configuration.
    
    Returns:
        AlgorithmConfig object with default values
    """
    return AlgorithmConfig()


if __name__ == '__main__':
    # Demo the algorithm config loader
    print("🎯 Algorithm Configuration Loader Demo")
    print("=" * 50)
    
    # Test default configuration
    default_config = get_default_algorithm_config()
    is_valid, errors = default_config.validate()
    print(f"Default configuration valid: {is_valid}")
    if errors:
        for error in errors:
            print(f"  ❌ {error}")
    
    # Test configuration dict validation
    loader = AlgorithmConfigLoader()
    
    # Valid configuration
    valid_config = {
        'dominance_amplification': {
            'enabled': True,
            'threshold': 0.8,
            'multiplier': 1.05,
            'rationale': 'Conservative amplification for traditional analysis'
        },
        'adaptive_scaling': {
            'enabled': True,
            'base_scaling': 0.7,
            'max_scaling': 0.9,
            'variance_factor': 0.2,
            'mean_factor': 0.05,
            'methodology': 'Conservative scaling for focused analysis'
        }
    }
    
    is_valid, errors = loader.validate_config_dict(valid_config)
    print(f"\nValid configuration test: {is_valid}")
    
    # Invalid configuration
    invalid_config = {
        'dominance_amplification': {
            'threshold': 1.5,  # Invalid: > 1.0
            'multiplier': 0.9,  # Invalid: < 1.0
            'rationale': ''     # Invalid: empty string
        }
    }
    
    is_valid, errors = loader.validate_config_dict(invalid_config)
    print(f"\nInvalid configuration test: {is_valid}")
    if errors:
        for error in errors:
            print(f"  ❌ {error}")
    
    print("\n✅ Algorithm configuration loader ready for use!") 