"""
Experiment Validator
====================

Validates experiments against Experiment System Specification with embedded framework validation.
"""

from typing import Dict, Any, List, Optional
from .validation_errors import ExperimentValidationError, FrameworkValidationError
from .framework_validator import FrameworkValidator


class ExperimentValidator:
    """
    Validates experiments against Experiment System Specification.
    Includes validation of embedded frameworks.
    """
    
    def __init__(self):
        self.framework_validator = FrameworkValidator()
        self.required_sections = ['experiment_meta', 'framework', 'models']
        self.required_meta_fields = ['name', 'display_name', 'version']
        
    def validate_experiment(self, experiment_config: Dict[str, Any], experiment_file_path: str = None) -> Dict[str, Any]:
        """
        Validate complete experiment configuration.
        
        Args:
            experiment_config: Experiment configuration dictionary
            experiment_file_path: Optional file path for error reporting
            
        Returns:
            Normalized experiment configuration with validated framework
            
        Raises:
            ExperimentValidationError: If experiment violates specification
            FrameworkValidationError: If embedded framework violates specification
        """
        if not isinstance(experiment_config, dict):
            raise ExperimentValidationError(
                "Experiment configuration must be a dictionary",
                field_path=experiment_file_path
            )
        
        experiment_name = self._get_experiment_name(experiment_config)
        
        # Validate required sections
        self._validate_required_sections(experiment_config, experiment_name)
        
        # Validate experiment metadata
        self._validate_experiment_meta(experiment_config, experiment_name)
        
        # Validate embedded framework
        validated_framework = self._validate_embedded_framework(experiment_config, experiment_name)
        
        # Validate models configuration
        self._validate_models_config(experiment_config, experiment_name)
        
        # Validate corpus configuration if present
        if 'corpus' in experiment_config:
            self._validate_corpus_config(experiment_config, experiment_name)
        
        # Return normalized experiment with validated framework
        normalized_experiment = experiment_config.copy()
        normalized_experiment['framework'] = validated_framework
        
        return normalized_experiment
    
    def _get_experiment_name(self, experiment_config: Dict[str, Any]) -> str:
        """Extract experiment name for error reporting"""
        meta = experiment_config.get('experiment_meta', {})
        return meta.get('display_name') or meta.get('name') or 'unknown_experiment'
    
    def _validate_required_sections(self, experiment_config: Dict[str, Any], experiment_name: str):
        """Validate required experiment sections"""
        for section in self.required_sections:
            if section not in experiment_config:
                raise ExperimentValidationError(
                    f"Missing required section '{section}'",
                    experiment_name,
                    field_path=section
                )
    
    def _validate_experiment_meta(self, experiment_config: Dict[str, Any], experiment_name: str):
        """Validate experiment metadata section"""
        meta = experiment_config['experiment_meta']
        
        if not isinstance(meta, dict):
            raise ExperimentValidationError(
                "experiment_meta must be a dictionary",
                experiment_name,
                field_path='experiment_meta'
            )
        
        # Validate required meta fields
        for field in self.required_meta_fields:
            if field not in meta:
                raise ExperimentValidationError(
                    f"Missing required experiment_meta field '{field}'",
                    experiment_name,
                    field_path=f'experiment_meta.{field}'
                )
        
        # Validate study design if present
        if 'study_design' in meta:
            study_design = meta['study_design']
            if not isinstance(study_design, dict):
                raise ExperimentValidationError(
                    "study_design must be a dictionary",
                    experiment_name,
                    field_path='experiment_meta.study_design'
                )
    
    def _validate_embedded_framework(self, experiment_config: Dict[str, Any], experiment_name: str) -> Dict[str, Any]:
        """Validate embedded framework configuration"""
        framework_config = experiment_config['framework']
        
        if not isinstance(framework_config, dict):
            raise ExperimentValidationError(
                "framework section must be a dictionary",
                experiment_name,
                field_path='framework'
            )
        
        try:
            # Use framework validator with full Framework Specification v3.2 compliance
            validated_framework = self.framework_validator.validate_framework(
                framework_config,
                framework_name=framework_config.get('name', 'embedded_framework')
            )
            return validated_framework
            
        except FrameworkValidationError as e:
            # Re-raise with experiment context
            raise ExperimentValidationError(
                f"Embedded framework validation failed: {str(e)}",
                experiment_name,
                field_path='framework'
            )
    
    def _validate_models_config(self, experiment_config: Dict[str, Any], experiment_name: str):
        """Validate models configuration"""
        models_config = experiment_config['models']
        
        if not isinstance(models_config, dict):
            raise ExperimentValidationError(
                "models section must be a dictionary",
                experiment_name,
                field_path='models'
            )
        
        # Check for flagship_models section
        if 'flagship_models' in models_config:
            flagship_models = models_config['flagship_models']
            if not isinstance(flagship_models, dict):
                raise ExperimentValidationError(
                    "flagship_models must be a dictionary",
                    experiment_name,
                    field_path='models.flagship_models'
                )
            
            # Validate each model configuration
            for model_key, model_config in flagship_models.items():
                if not isinstance(model_config, dict):
                    raise ExperimentValidationError(
                        f"Model '{model_key}' configuration must be a dictionary",
                        experiment_name,
                        field_path=f'models.flagship_models.{model_key}'
                    )
                
                # Required model fields
                if 'model_id' not in model_config:
                    raise ExperimentValidationError(
                        f"Model '{model_key}' missing required 'model_id' field",
                        experiment_name,
                        field_path=f'models.flagship_models.{model_key}.model_id'
                    )
    
    def _validate_corpus_config(self, experiment_config: Dict[str, Any], experiment_name: str):
        """Validate corpus configuration if present"""
        corpus_config = experiment_config['corpus']
        
        if not isinstance(corpus_config, dict):
            raise ExperimentValidationError(
                "corpus section must be a dictionary",
                experiment_name,
                field_path='corpus'
            )
        
        # Required corpus fields for directory_collection
        if corpus_config.get('source_type') == 'directory_collection':
            if 'file_path' not in corpus_config:
                raise ExperimentValidationError(
                    "directory_collection corpus missing required 'file_path' field",
                    experiment_name,
                    field_path='corpus.file_path'
                )
    
    def get_framework_anchors(self, experiment_config: Dict[str, Any]) -> Dict[str, Any]:
        """Extract framework anchors from validated experiment"""
        validated = self.validate_experiment(experiment_config)
        return self.framework_validator.get_anchors(validated['framework'])
    
    def get_framework_anchor_count(self, experiment_config: Dict[str, Any]) -> int:
        """Get anchor count from validated experiment framework"""
        validated = self.validate_experiment(experiment_config)
        return len(validated['framework']['_extracted_anchors']) 