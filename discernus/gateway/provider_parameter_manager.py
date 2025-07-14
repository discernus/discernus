"""
Provider Parameter Manager for SOAR v2.0

Centralizes provider-specific parameter handling to avoid API parameter sensitivity issues.
Key insight: Different LLM providers have different parameter sensitivities that can trigger
unexpected behavior like safety filters or task drift.

THIN Philosophy: Simple parameter routing with provider intelligence externalized to configurations.
"""

from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)


class ProviderParameterManager:
    """
    Centralized management of provider-specific parameter sensitivities.
    
    Handles the critical issue where seemingly innocent parameters like max_tokens
    can trigger safety filters or other unexpected behaviors in certain providers.
    """
    
    # Provider-specific configurations
    PROVIDER_CONFIGS = {
        'vertex_ai': {
            'forbidden_params': ['max_tokens'],  # Triggers safety filters for political content
            'required_params': {
                'safety_settings': [
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
                ]
            },
            'default_params': {},  # Let provider use optimal defaults
            'timeout': 180  # Increased for large context processing (3 minutes)
        },
        'openai': {
            'forbidden_params': ['max_tokens'],  # Removed to avoid API sensitivity issues
            'required_params': {},
            'default_params': {},  # Let provider use optimal defaults
            'timeout': 120  # 2 minutes - 2x safety margin for large context processing
        },
        'anthropic': {
            'forbidden_params': ['max_tokens'],  # Removed to avoid API sensitivity issues
            'required_params': {},
            'default_params': {},  # Let provider use optimal defaults
            'timeout': 120  # 2 minutes - Claude is generally faster but needs margin for large context
        },
        'mistral': {
            'forbidden_params': ['max_tokens'],  # Removed to avoid API sensitivity issues
            'required_params': {},
            'default_params': {},  # Let provider use optimal defaults
            'timeout': 120  # 2 minutes - similar performance to other cloud providers
        },
        'perplexity': {
            # Placeholder for future implementation
            'forbidden_params': ['max_tokens'],  # Removed to avoid API sensitivity issues
            'required_params': {},
            'default_params': {},  # Let provider use optimal defaults
            'timeout': 120,  # 2 minutes - similar to other cloud providers
            'status': 'placeholder'  # Not yet implemented
        }
    }
    
    # Model-specific configurations for Ollama-hosted models
    # These are first-class citizens in the architecture
    MODEL_SPECIFIC_CONFIGS = {
        'ollama/llama3.2': {
            'provider': 'ollama',
            'forbidden_params': ['max_tokens'],  # Removed to avoid API sensitivity issues
            'required_params': {},
            'default_params': {},  # Let provider use optimal defaults
            'timeout': 600  # 10 minutes - local processing with large context requires more time
        },
        'ollama/mistral': {
            'provider': 'ollama',
            'forbidden_params': ['max_tokens'],  # Removed to avoid API sensitivity issues
            'required_params': {},
            'default_params': {},  # Let provider use optimal defaults
            'timeout': 120,  # 2 minutes - reduced from 10 minutes to prevent hangs
            'notes': 'Local model can be slow with complex prompts. Timeout set to 2 minutes to prevent hangs.'
        },
        'ollama/llama3.3': {
            'provider': 'ollama',
            'forbidden_params': ['max_tokens'],  # Removed to avoid API sensitivity issues
            'required_params': {},
            'default_params': {},  # Let provider use optimal defaults
            'timeout': 600  # 10 minutes - local processing with large context requires more time
        }
    }
    
    def __init__(self):
        """Initialize the parameter manager"""
        self.logger = logging.getLogger(__name__)
    
    def get_provider_from_model(self, model_name: str) -> str:
        """
        Extract provider from model name.
        
        First checks for model-specific configs (for Ollama-hosted models),
        then falls back to provider detection.
        """
        model_lower = model_name.lower()
        
        # Check for model-specific configurations first
        if model_name in self.MODEL_SPECIFIC_CONFIGS:
            return self.MODEL_SPECIFIC_CONFIGS[model_name]['provider']
        
        # Provider detection logic
        if model_lower.startswith("vertex_ai/"):
            return "vertex_ai"
        elif model_lower.startswith("ollama/"):
            return "ollama"
        elif any(x in model_lower for x in ["gpt", "openai", "o1", "o3", "o4"]):
            return "openai"
        elif any(x in model_lower for x in ["claude", "anthropic"]):
            return "anthropic"
        elif any(x in model_lower for x in ["mistral", "codestral"]):
            return "mistral"
        elif any(x in model_lower for x in ["gemini", "google"]):
            return "vertex_ai"  # Default Gemini to Vertex AI
        elif "perplexity" in model_lower:
            return "perplexity"
        else:
            self.logger.warning(f"Unknown provider for model: {model_name}")
            return "unknown"
    
    def get_clean_parameters(self, model_name: str, base_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clean parameters based on provider and model-specific sensitivities.
        
        This is the core function that prevents parameter sensitivity issues.
        """
        # Check for model-specific configuration first
        if model_name in self.MODEL_SPECIFIC_CONFIGS:
            config = self.MODEL_SPECIFIC_CONFIGS[model_name]
            self.logger.debug(f"Using model-specific config for {model_name}")
        else:
            # Fall back to provider configuration
            provider = self.get_provider_from_model(model_name)
            config = self.PROVIDER_CONFIGS.get(provider, {})
            self.logger.debug(f"Using provider config for {provider}")
        
        # Start with base parameters
        clean_params = base_params.copy()
        
        # Remove forbidden parameters
        forbidden_params = config.get('forbidden_params', [])
        for param in forbidden_params:
            if param in clean_params:
                removed_value = clean_params.pop(param)
                self.logger.info(f"Removed forbidden parameter {param}={removed_value} for {model_name}")
        
        # Add required parameters
        required_params = config.get('required_params', {})
        for param, value in required_params.items():
            clean_params[param] = value
            self.logger.debug(f"Added required parameter {param} for {model_name}")
        
        # Add default parameters if not already present
        default_params = config.get('default_params', {})
        for param, value in default_params.items():
            if param not in clean_params:
                clean_params[param] = value
                self.logger.debug(f"Added default parameter {param}={value} for {model_name}")
        
        # Add timeout if specified
        if 'timeout' in config:
            clean_params['timeout'] = config['timeout']
        
        self.logger.debug(f"Clean parameters for {model_name}: {list(clean_params.keys())}")
        return clean_params
    
    def get_provider_config(self, provider: str) -> Dict[str, Any]:
        """Get full configuration for a provider"""
        return self.PROVIDER_CONFIGS.get(provider, {})
    
    def get_model_config(self, model_name: str) -> Dict[str, Any]:
        """Get full configuration for a specific model"""
        return self.MODEL_SPECIFIC_CONFIGS.get(model_name, {})
    
    def is_provider_supported(self, provider: str) -> bool:
        """Check if a provider is supported"""
        config = self.PROVIDER_CONFIGS.get(provider, {})
        return config.get('status') != 'placeholder'
    
    def get_supported_providers(self) -> List[str]:
        """Get list of supported providers (excluding placeholders)"""
        return [
            provider for provider, config in self.PROVIDER_CONFIGS.items()
            if config.get('status') != 'placeholder'
        ]
    
    def get_timeout_for_model(self, model_name: str) -> int:
        """Get appropriate timeout for a model"""
        if model_name in self.MODEL_SPECIFIC_CONFIGS:
            return self.MODEL_SPECIFIC_CONFIGS[model_name].get('timeout', 60)
        
        provider = self.get_provider_from_model(model_name)
        config = self.PROVIDER_CONFIGS.get(provider, {})
        return config.get('timeout', 60)
    
    def log_parameter_decisions(self, model_name: str, original_params: Dict[str, Any], 
                               clean_params: Dict[str, Any]) -> None:
        """Log parameter cleaning decisions for debugging"""
        removed_params = set(original_params.keys()) - set(clean_params.keys())
        added_params = set(clean_params.keys()) - set(original_params.keys())
        
        if removed_params:
            self.logger.info(f"Parameters removed for {model_name}: {removed_params}")
        if added_params:
            self.logger.info(f"Parameters added for {model_name}: {added_params}")
        
        # Log any parameter value changes
        for param in set(original_params.keys()) & set(clean_params.keys()):
            if original_params[param] != clean_params[param]:
                self.logger.info(f"Parameter changed for {model_name}: {param} "
                               f"{original_params[param]} -> {clean_params[param]}")


# Convenience function for backward compatibility
def get_clean_parameters(model_name: str, base_params: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience function for parameter cleaning"""
    manager = ProviderParameterManager()
    return manager.get_clean_parameters(model_name, base_params) 