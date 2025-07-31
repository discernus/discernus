"""
Provider Parameter Manager for Discernus

Centralizes provider-specific parameter handling to avoid API parameter sensitivity issues.
Key insight: Different LLM providers have different parameter sensitivities that can trigger
unexpected behavior like safety filters or task drift.

THIN Philosophy: Simple parameter routing with provider intelligence externalized to configurations.
"""

from typing import Dict, Any, Optional, List
import logging
import yaml
from pathlib import Path

logger = logging.getLogger(__name__)


class ProviderParameterManager:
    """
    Centralized management of provider-specific parameter sensitivities.
    
    This class reads all configuration from models.yaml to act as a single
    source of truth for parameter cleaning, ensuring consistent and predictable
    API behavior across all providers.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the parameter manager by loading from the YAML config."""
        self.config_path = Path(config_path or Path(__file__).parent / 'models.yaml')
        self._load_config()
        self.logger = logging.getLogger(__name__)
        
    def _load_config(self):
        """Loads all configuration from the models.yaml file."""
        if not self.config_path.exists():
            self.logger.error(f"Configuration file not found at {self.config_path}")
            self.provider_defaults = {}
            self.models = {}
            return
            
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
            self.provider_defaults = config.get('provider_defaults', {})
            self.models = config.get('models', {})
    
    def get_provider_from_model(self, model_name: str) -> str:
        """
        Gets the provider directly from the model's definition in the registry.
        This is the single source of truth.
        """
        model_details = self.models.get(model_name)
        if model_details and 'provider' in model_details:
            return model_details['provider']
        
        # Fallback for models not explicitly in the `models` dictionary (e.g. wildcard)
        # This is less robust and should be avoided.
        if model_name.startswith("vertex_ai/"): return "vertex_ai"
        if model_name.startswith("ollama/"): return "ollama"
        if model_name.startswith("anthropic/"): return "anthropic"
        if model_name.startswith("openai/"): return "openai"

        self.logger.warning(f"Could not determine provider for model: {model_name}")
        return "unknown"
    
    def get_clean_parameters(self, model_name: str, base_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cleans parameters using provider defaults and model-specific overrides
        from the single source of truth: models.yaml.
        """
        provider = self.get_provider_from_model(model_name)
        
        # Start with the provider's default configuration
        clean_params = self.provider_defaults.get(provider, {}).copy()
        
        # Layer on any model-specific configurations
        model_config = self.models.get(model_name, {})
        clean_params.update(model_config)
        
        # Now, process the base parameters provided in the call
        final_params = base_params.copy()
        
        # Handle parameter mapping before forbidden parameter removal
        parameter_mapping = clean_params.get('parameter_mapping', {})
        for old_param, new_param in parameter_mapping.items():
            if old_param in final_params:
                final_params[new_param] = final_params[old_param]
                self.logger.debug(f"Mapped parameter '{old_param}' → '{new_param}' for {model_name} (value: {final_params[old_param]})")

        # Remove any forbidden parameters (after mapping)
        forbidden = clean_params.get('forbidden_params', [])
        for param in forbidden:
            if param in final_params:
                del final_params[param]
                self.logger.debug(f"Removed forbidden parameter '{param}' for model {model_name}")

        # Add any required parameters that are not already present
        required = clean_params.get('required_params', {})
        for param, value in required.items():
            if param not in final_params:
                final_params[param] = value
                
        # Set the timeout, using model-specific override if it exists
        final_params['timeout'] = model_config.get('timeout', clean_params.get('timeout', 60))

        self.logger.debug(f"Final clean parameters for {model_name}: {list(final_params.keys())}")
        return final_params

# Convenience function for backward compatibility
def get_clean_parameters(model_name: str, base_params: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function for parameter cleaning"""
    manager = ProviderParameterManager()
    return manager.get_clean_parameters(model_name, base_params) 