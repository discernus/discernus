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
        
        # Handle max_tokens intelligently - warn if too low, use safe defaults
        self._handle_max_tokens(model_name, final_params, clean_params)
        
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
    
    def _handle_max_tokens(self, model_name: str, final_params: Dict[str, Any], clean_params: Dict[str, Any]) -> None:
        """
        Intelligently handle max_tokens parameters with logging and safe defaults.
        
        This method:
        1. Warns when max_tokens is too low (likely to truncate)
        2. Uses safe_max_tokens from config when no max_tokens is specified
        3. Logs when token limits are being applied
        """
        original_max_tokens = final_params.get('max_tokens')
        safe_max_tokens = clean_params.get('safe_max_tokens')
        
        # Define threshold for "dangerously low" token limits
        DANGEROUSLY_LOW_THRESHOLD = 2000
        
        if original_max_tokens is not None:
            if original_max_tokens < DANGEROUSLY_LOW_THRESHOLD:
                # Log warning for dangerously low token limits
                print(f"⚠️  WARNING: max_tokens={original_max_tokens} for {model_name} may truncate responses")
                self.logger.warning(f"Dangerously low max_tokens={original_max_tokens} for {model_name} - may cause truncation")
            
            # Keep the original value but log it
            self.logger.info(f"Using explicit max_tokens={original_max_tokens} for {model_name}")
        
        elif safe_max_tokens is not None:
            # No max_tokens specified, use safe default
            final_params['max_tokens'] = safe_max_tokens
            self.logger.debug(f"Applied safe max_tokens={safe_max_tokens} for {model_name}")
        
        else:
            # No safe_max_tokens configured for this provider
            self.logger.debug(f"No max_tokens configuration for {model_name} - letting provider handle defaults")

# Convenience function for backward compatibility
def get_clean_parameters(model_name: str, base_params: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function for parameter cleaning"""
    manager = ProviderParameterManager()
    return manager.get_clean_parameters(model_name, base_params) 