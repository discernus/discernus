#!/usr/bin/env python3
"""
Automated Model Registry Updater

Updates discernus/gateway/models.yaml with latest available models from all providers.
Prevents manual maintenance errors and ensures model availability information is current.

Usage:
    python3 scripts/update_model_registry.py          # Full update
    python3 scripts/update_model_registry.py --check  # Check only, no changes
    python3 scripts/update_model_registry.py --dry-run # Show what would be updated
"""

import yaml
import requests
import os
import sys
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import json
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import litellm
except ImportError:
    print("⚠️  LiteLLM not installed. Install with: pip install litellm")
    sys.exit(1)

class ModelRegistryUpdater:
    def __init__(self, config_path: str = "discernus/gateway/models.yaml", dry_run: bool = False):
        self.config_path = Path(config_path)
        self.dry_run = dry_run
        self.changes_made = []
        self.current_config = self.load_current_config()
        
    def load_current_config(self) -> Dict[str, Any]:
        """Load current model configuration"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Model config not found: {self.config_path}")
            
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def log_change(self, change: str):
        """Log a change that was made or would be made"""
        self.changes_made.append(change)
        status = "🔄 WOULD" if self.dry_run else "✅ MADE"
        print(f"{status}: {change}")
    
    def get_vertex_ai_models(self) -> List[Dict[str, Any]]:
        """Query Vertex AI for available models"""
        models = []
        
        # Known Vertex AI model families with their regions
        vertex_models = {
            # Claude models
            "claude-3-5-sonnet@20240620": {
                "regions": ["us-east5", "europe-west1", "asia-southeast1"],
                "performance_tier": "top-tier",
                "context_window": 200000,
                "costs": {"input_per_million_tokens": 3.00, "output_per_million_tokens": 15.00}
            },
            "claude-3-7-sonnet@20250219": {
                "regions": ["us-east5", "europe-west1", "global"],
                "performance_tier": "top-tier", 
                "context_window": 200000,
                "costs": {"input_per_million_tokens": 3.00, "output_per_million_tokens": 15.00}
            },
            "claude-sonnet-4@20250514": {
                "regions": ["us-east5", "europe-west1", "asia-east1", "global"],
                "performance_tier": "top-tier",
                "context_window": 200000,
                "costs": {"input_per_million_tokens": 3.00, "output_per_million_tokens": 15.00}
            },
            # Gemini models
            "gemini-2.5-pro": {
                "regions": ["us-central1", "us-east1", "europe-west1"],
                "performance_tier": "top-tier",
                "context_window": 2000000,
                "costs": {"input_per_million_tokens": 3.50, "output_per_million_tokens": 10.50}
            },
            "gemini-2.5-pro": {
                "regions": ["us-central1", "us-east1", "europe-west1"],
                "performance_tier": "cost-effective",
                "context_window": 1000000,
                "costs": {"input_per_million_tokens": 0.35, "output_per_million_tokens": 1.05}
            },
        }
        
        for model_id, model_info in vertex_models.items():
            models.append({
                "id": model_id,
                "provider": "vertex_ai",
                "display_name": model_id,
                **model_info
            })
        
        return models
    
    def get_openrouter_models(self) -> List[Dict[str, Any]]:
        """Query OpenRouter for available models"""
        
        # We only want a curated list of models from OpenRouter, not all of them.
        whitelisted_models = [
            "mistralai/mistral-7b-instruct",
            "mistralai/mixtral-8x7b-instruct",
            "google/gemma-7b-it",
            "meta-llama/llama-3-8b-instruct",
            "meta-llama/llama-3-70b-instruct",
            "cohere/command-r-plus",
            "perplexity/r1-1776"
        ]

        try:
            print("🔍 Querying OpenRouter for available models...")
            response = requests.get("https://openrouter.ai/api/v1/models", timeout=10)
            if response.status_code == 200:
                data = response.json()
                models = []
                for model in data.get('data', []):
                    if model['id'] in whitelisted_models:
                        # Only extract the fields we need, don't dump the whole object
                        models.append({
                            "id": model.get('id'),
                            "display_name": model.get('name'),
                            "context_window": model.get('context_length'),
                            "costs": {
                                "input_per_million_tokens": round(float(model.get('pricing', {}).get('prompt', 0.0)) * 1000000, 4),
                                "output_per_million_tokens": round(float(model.get('pricing', {}).get('completion', 0.0)) * 1000000, 4)
                            }
                        })

                print(f"✅ Found {len(models)} whitelisted models on OpenRouter")
                return models
        except Exception as e:
            print(f"⚠️  Failed to query OpenRouter: {e}")
        return []
    
    def get_anthropic_models(self) -> List[Dict[str, Any]]:
        """Get known Anthropic models (no public API available)"""
        known_models = [
            {
                "id": "claude-3-5-sonnet-20240620",
                "provider": "anthropic",
                "display_name": "Claude 3.5 Sonnet",
                "performance_tier": "top-tier",
                "context_window": 200000,
                "costs": {"input_per_million_tokens": 3.00, "output_per_million_tokens": 15.00}
            },
            {
                "id": "claude-3-haiku-20240307",
                "provider": "anthropic", 
                "display_name": "Claude 3 Haiku",
                "performance_tier": "cost-effective",
                "context_window": 200000,
                "costs": {"input_per_million_tokens": 0.25, "output_per_million_tokens": 1.25}
            },
        ]
        return known_models
    
    def get_openai_models(self) -> List[Dict[str, Any]]:
        """Get known OpenAI models (rate limited API)"""
        known_models = [
            {
                "id": "gpt-4o",
                "provider": "openai",
                "display_name": "GPT-4o",
                "performance_tier": "top-tier",
                "context_window": 128000,
                "costs": {"input_per_million_tokens": 5.00, "output_per_million_tokens": 15.00}
            },
            {
                "id": "gpt-4o-mini",
                "provider": "openai",
                "display_name": "GPT-4o Mini", 
                "performance_tier": "cost-effective",
                "context_window": 128000,
                "costs": {"input_per_million_tokens": 0.15, "output_per_million_tokens": 0.60}
            },
        ]
        return known_models
    
    def infer_performance_tier(self, model_info: Dict[str, Any]) -> str:
        """Infer performance tier based on model information"""
        model_id = model_info.get('id', '').lower()
        
        if any(term in model_id for term in ['opus', 'ultra', 'large', 'pro']):
            return "top-tier"
        elif any(term in model_id for term in ['flash', 'mini', 'haiku', 'light']):
            return "cost-effective"
        elif any(term in model_id for term in ['instruct', 'chat']):
            return "general-purpose"
        else:
            return "general-purpose"
    
    def update_model_costs_from_litellm(self):
        """Update pricing information from LiteLLM's cost map"""
        try:
            cost_map = litellm.model_cost
            updated_count = 0
            
            for model_id, model_info in self.current_config.get('models', {}).items():
                # Check various possible LiteLLM cost keys
                cost_keys = [model_id, model_id.split('/')[-1]]
                
                for cost_key in cost_keys:
                    if cost_key in cost_map:
                        cost_info = cost_map[cost_key]
                        
                        # Update costs if they exist in LiteLLM
                        if 'input_cost_per_token' in cost_info:
                            new_input_cost = cost_info['input_cost_per_token'] * 1_000_000
                            old_input_cost = model_info.get('costs', {}).get('input_per_million_tokens', 0)
                            
                            if isinstance(new_input_cost, (int, float)) and isinstance(old_input_cost, (int, float)) and abs(new_input_cost - old_input_cost) > 0.01:
                                model_info.setdefault('costs', {})['input_per_million_tokens'] = new_input_cost
                                updated_count += 1
                                
                        if 'output_cost_per_token' in cost_info:
                            new_output_cost = cost_info['output_cost_per_token'] * 1_000_000
                            old_output_cost = model_info.get('costs', {}).get('output_per_million_tokens', 0)
                            
                            if isinstance(new_output_cost, (int, float)) and isinstance(old_output_cost, (int, float)) and abs(new_output_cost - old_output_cost) > 0.01:
                                model_info.setdefault('costs', {})['output_per_million_tokens'] = new_output_cost
                                updated_count += 1
                        
                        break
            
            if updated_count > 0:
                self.log_change(f"Updated pricing for {updated_count} models from LiteLLM cost map")
                
        except Exception as e:
            print(f"⚠️  Failed to update costs from LiteLLM: {e}")
    
    def check_model_availability(self, model_id: str) -> bool:
        """Test if a model is actually available"""
        try:
            # Make a minimal test call to check availability
            response = litellm.completion(
                model=model_id,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=1,
                timeout=5
            )
            return True
        except Exception:
            return False
    
    def add_new_models(self, discovered_models: Dict[str, List[Dict[str, Any]]]):
        """Add newly discovered models to registry"""
        new_models_added = 0
        
        for provider, models in discovered_models.items():
            for model in models:
                if provider == "openrouter":
                    model_key = model['id']
                else:
                    model_key = f"{provider}/{model['id']}"
                
                if model_key not in self.current_config.get('models', {}):
                    # Add new model to registry
                    new_model_entry = {
                        'provider': provider,
                        'performance_tier': model.get('performance_tier', 'general-purpose'),
                        'context_window': model.get('context_window', 4096),
                        'costs': model.get('costs', {
                            'input_per_million_tokens': 0.0,
                            'output_per_million_tokens': 0.0
                        }),
                        'utility_tier': 10,  # Default utility tier
                        'task_suitability': ['synthesis'],  # Default task suitability
                        'optimal_batch_size': 6,  # Default batch size
                        'last_updated': datetime.now().isoformat()[:10],
                        'review_by': (datetime.now() + timedelta(days=180)).isoformat()[:10],
                        'notes': f"Auto-discovered model from {provider}",
                        'auto_discovered': True
                    }
                    
                    # Add regional information for Vertex AI models
                    if provider == "vertex_ai" and 'regions' in model:
                        new_model_entry['regions'] = {}
                        for region in model['regions']:
                            new_model_entry['regions'][region] = {
                                'tpm': 100000,  # Default TPM
                                'rpm': 100     # Default RPM
                            }
                    
                    self.current_config.setdefault('models', {})[model_key] = new_model_entry
                    new_models_added += 1
                    self.log_change(f"Added new model: {model_key}")
        
        if new_models_added > 0:
            self.log_change(f"Added {new_models_added} new models to registry")
    
    def remove_deprecated_models(self):
        """Remove models that are no longer available"""
        models_to_remove = []
        
        for model_id, model_info in self.current_config.get('models', {}).items():
            # Check if model was auto-discovered and is old
            if model_info.get('auto_discovered') and model_info.get('last_updated'):
                try:
                    last_updated = datetime.fromisoformat(model_info['last_updated'])
                    if (datetime.now() - last_updated).days > 90:  # 90 days old
                        if not self.check_model_availability(model_id):
                            models_to_remove.append(model_id)
                except:
                    pass
        
        for model_id in models_to_remove:
            del self.current_config['models'][model_id]
            self.log_change(f"Removed deprecated model: {model_id}")
    
    def save_updated_config(self):
        """Save updated configuration back to file"""
        if self.dry_run:
            print("\n🔄 DRY RUN: Would save updated configuration")
            return
        
        # Create backup
        backup_path = self.config_path.with_suffix('.yaml.backup')
        if self.config_path.exists():
            import shutil
            shutil.copy2(self.config_path, backup_path)
        
        try:
            # Validate YAML before writing
            output_yaml = yaml.dump(self.current_config, default_flow_style=False, indent=2, sort_keys=False)
            yaml.safe_load(output_yaml) # Test if it's valid
        except Exception as e:
            print(f"❌ CRITICAL: Generated YAML is invalid! Aborting to prevent corruption. Error: {e}")
            return

        # Save updated configuration
        with open(self.config_path, 'w') as f:
            f.write(output_yaml)
        
        print(f"✅ Updated configuration saved to {self.config_path}")
        print(f"📄 Backup saved to {backup_path}")
    
    def run_update(self):
        """Run full model registry update"""
        print("🔄 Starting model registry update...")
        print(f"📁 Config file: {self.config_path}")
        print(f"🔧 Mode: {'DRY RUN' if self.dry_run else 'LIVE UPDATE'}")
        print()
        
        # Get models from all providers
        discovered_models = {
            'vertex_ai': self.get_vertex_ai_models(),
            'openrouter': self.get_openrouter_models(),
            'anthropic': self.get_anthropic_models(),
            'openai': self.get_openai_models()
        }
        
        # Report discovery results
        total_discovered = sum(len(models) for models in discovered_models.values())
        print(f"🔍 Discovered {total_discovered} models across all providers")
        for provider, models in discovered_models.items():
            print(f"   {provider}: {len(models)} models")
        print()
        
        # Update existing model information
        self.update_model_costs_from_litellm()
        
        # Add new models
        self.add_new_models(discovered_models)
        
        # Remove deprecated models
        self.remove_deprecated_models()
        
        # Save updated configuration
        if self.changes_made:
            self.save_updated_config()
            print(f"\n✅ Model registry update completed! Made {len(self.changes_made)} changes.")
        else:
            print("\n✅ Model registry is up to date! No changes needed.")
        
        return len(self.changes_made)

def main():
    parser = argparse.ArgumentParser(description='Update model registry with latest available models')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be updated without making changes')
    parser.add_argument('--check', action='store_true', help='Check for updates only, exit with code 1 if updates needed')
    parser.add_argument('--config', default='discernus/gateway/models.yaml', help='Path to models.yaml file')
    
    args = parser.parse_args()
    
    try:
        updater = ModelRegistryUpdater(config_path=args.config, dry_run=args.dry_run or args.check)
        changes = updater.run_update()
        
        if args.check:
            if changes > 0:
                print(f"\n⚠️  Model registry needs {changes} updates!")
                sys.exit(1)
            else:
                print("\n✅ Model registry is current!")
                sys.exit(0)
        
    except Exception as e:
        print(f"❌ Error updating model registry: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 