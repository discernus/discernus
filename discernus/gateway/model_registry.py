#!/usr/bin/env python3
"""
Model Registry
==============

THIN Principle: This component is a pure "knowledge" provider. It knows everything
about the available LLM models but has no execution capabilities. It serves as a
single source of truth for other agents that need to make intelligent decisions
about which models to use.
"""

import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional

class ModelRegistry:
    """
    A registry for discovering and querying available LLM models and their capabilities.
    """

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = Path(config_path or Path(__file__).parent / 'models.yaml')
        self.models = self._load_models()

    def _load_models(self) -> Dict[str, Any]:
        """Loads the model configurations from the YAML file."""
        if not self.config_path.exists():
            print(f"⚠️ Model configuration not found at {self.config_path}. Using empty registry.")
            return {}
        
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f).get('models', {})

    def list_models(self) -> List[str]:
        """Returns a list of all available model identifiers."""
        return list(self.models.keys())

    def get_model_details(self, model_name: str) -> Optional[Dict[str, Any]]:
        """Returns the full details for a specific model."""
        return self.models.get(model_name)

    def list_models_by_tier(self, tier: str) -> List[str]:
        """Returns a list of models belonging to a specific performance tier."""
        return [
            name for name, details in self.models.items()
            if details.get('performance_tier') == tier
        ]

    def get_model_provider(self, model_name: str) -> Optional[str]:
        """Returns the provider for a specific model."""
        details = self.get_model_details(model_name)
        return details.get('provider') if details else None

# Singleton instance to be used across the application
_model_registry_instance = None

def get_model_registry() -> ModelRegistry:
    """Factory function to get the singleton ModelRegistry instance."""
    global _model_registry_instance
    if _model_registry_instance is None:
        _model_registry_instance = ModelRegistry()
    return _model_registry_instance

if __name__ == '__main__':
    # Demo of how to use the ModelRegistry
    registry = get_model_registry()
    
    print("Available Models:")
    for model in registry.list_models():
        print(f"- {model}")
        
    print("\nTop-Tier Models:")
    for model in registry.list_models_by_tier('top-tier'):
        print(f"- {model}")

    print("\nDetails for 'claude-3-5-sonnet-20240620':")
    print(registry.get_model_details('claude-3-5-sonnet-20240620')) 