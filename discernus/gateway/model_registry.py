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

    def get_model_for_task(self, task_type: str) -> Optional[str]:
        """
        Gets the best available model for a given task, based on utility tier.
        """
        # Filter models that are suitable for the task
        suitable_models = [
            name for name, details in self.models.items()
            if task_type in details.get('task_suitability', [])
        ]
        
        if not suitable_models:
            return None
            
        # Sort by utility tier (lower is better)
        sorted_models = sorted(suitable_models, key=lambda name: self.models[name].get('utility_tier', 99))
        
        return sorted_models[0]

    def get_fallback_model(self, failed_model_name: str) -> Optional[str]:
        """
        Gets the next best model in the fallback chain.
        """
        failed_model_details = self.get_model_details(failed_model_name)
        if not failed_model_details:
            return None

        current_tier = failed_model_details.get('utility_tier')
        if current_tier is None:
            return None

        # Find all models with a higher utility tier number (lower priority)
        fallback_candidates = [
            name for name, details in self.models.items()
            if details.get('utility_tier', 99) > current_tier
        ]

        if not fallback_candidates:
            return None

        # Return the best of the fallback options
        return sorted(fallback_candidates, key=lambda name: self.models[name].get('utility_tier', 99))[0]

    def get_provider_fallback_model(self, failed_model_name: str) -> Optional[str]:
        """
        Gets the next best model within the same provider (provider-consistent fallback).
        This maintains research integrity by avoiding cross-provider bias.
        
        Fallback strategy:
        - Flash (tier 2) → Pro (tier 1) 
        - Lite (tier 4) → Flash (tier 2)
        - Pro (tier 1) → No fallback (highest tier)
        """
        failed_model_details = self.get_model_details(failed_model_name)
        if not failed_model_details:
            return None

        current_provider = failed_model_details.get('provider')
        current_tier = failed_model_details.get('utility_tier')
        
        if not current_provider or current_tier is None:
            return None

        # Find models from the same provider with lower utility_tier (higher priority)
        provider_fallback_candidates = [
            name for name, details in self.models.items()
            if (details.get('provider') == current_provider and 
                details.get('utility_tier', 99) < current_tier)
        ]

        if not provider_fallback_candidates:
            return None

        # Return the next best (highest utility_tier among fallback candidates)
        # This ensures Lite → Flash instead of Lite → Pro
        return sorted(provider_fallback_candidates, key=lambda name: self.models[name].get('utility_tier', 99), reverse=True)[0]

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

    print("\nDetails for 'anthropic/claude-sonnet-4-20250514':")
    print(registry.get_model_details('anthropic/claude-sonnet-4-20250514')) 