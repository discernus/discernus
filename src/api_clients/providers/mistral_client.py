from typing import Tuple, Dict, Optional
from mistralai import Mistral

from src.utils.cost_manager import CostManager

class MistralProvider:
    """Wrapper around the Mistral client with cost tracking."""

    def __init__(self, api_key: str, cost_manager: Optional[CostManager] = None):
        self.client = Mistral(api_key=api_key)
        self.cost_manager = cost_manager

    def _get_model_mapping(self, model_name: str) -> str:
        """Map legacy/alias model names to current API model names."""
        model_map = {
            # Legacy mappings to REAL working models
            "mistral": "mistral-large-latest",
            "mistral-large": "mistral-large-latest",
            "mistral-medium": "mistral-large-latest",  # No medium model, use large
            "mistral-small": "mistral-small-latest",
            
            # Real working models (June 2025 - CONFIRMED)
            "mistral-large-latest": "mistral-large-latest",
            "mistral-small-latest": "mistral-small-latest", 
            "codestral-latest": "codestral-latest",
            "mistral-large-2411": "mistral-large-2411",
            "pixtral-large-latest": "pixtral-large-latest",
            
            # Cursor-compatible names
            "mistral-large-2412": "mistral-large-latest",  # Map to latest
            "codestral-2501": "codestral-latest",  # Map to latest
        }
        return model_map.get(model_name, "mistral-large-latest")

    def _get_max_tokens(self, model: str) -> int:
        """Get model-specific max_tokens value."""
        if "large" in model:
            return 4000  # Large models with enhanced capabilities
        elif "codestral" in model or "pixtral" in model:
            return 3000  # Specialized models (coding, vision)
        else:
            return 2000  # Standard models

    def _calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost with current Mistral pricing."""
        if self.cost_manager and model in self.cost_manager.model_costs.get("mistral", {}):
            costs = self.cost_manager.model_costs["mistral"][model]
            if "per_operation" in costs:
                return costs["per_operation"]
            return (input_tokens * costs["input"] / 1000) + (output_tokens * costs["output"] / 1000)
        
        # Model-specific pricing (current rates)
        if "large" in model:
            # Large models - premium pricing
            return (input_tokens * 0.008 / 1000) + (output_tokens * 0.024 / 1000)
        elif "codestral" in model:
            # Coding-specialized models
            return (input_tokens * 0.006 / 1000) + (output_tokens * 0.018 / 1000)
        elif "pixtral" in model:
            # Vision models - premium pricing
            return (input_tokens * 0.012 / 1000) + (output_tokens * 0.036 / 1000)
        elif "small" in model:
            # Small models - cost-effective
            return (input_tokens * 0.002 / 1000) + (output_tokens * 0.006 / 1000)
        else:
            # Fallback pricing
            return (input_tokens * 0.008 / 1000) + (output_tokens * 0.024 / 1000)

    def _estimate_tokens(self, text: str) -> int:
        """Estimate tokens using more accurate method (1.3x word count)."""
        return int(len(text.split()) * 1.3)

    def _analyze(self, prompt: str, model: str) -> Tuple[str, float, Dict[str, int]]:
        # Map model name to correct API model
        mapped_model = self._get_model_mapping(model)
        max_tokens = self._get_max_tokens(mapped_model)
        
        response = self.client.chat.complete(
            model=mapped_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=max_tokens,
        )
        content = response.choices[0].message.content
        
        # Get actual token usage if available, otherwise estimate
        if hasattr(response, 'usage') and response.usage:
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
        else:
            # Fallback to estimation
            input_tokens = self._estimate_tokens(prompt)
            output_tokens = self._estimate_tokens(content)
        
        cost = self._calculate_cost(mapped_model, input_tokens, output_tokens)
        if self.cost_manager:
            self.cost_manager.record_cost(
                provider="mistral",
                model=mapped_model,
                actual_cost=cost,
                tokens_input=input_tokens,
                tokens_output=output_tokens,
                request_type="analysis",
            )
        return content, cost, {"prompt_tokens": input_tokens, "completion_tokens": output_tokens}
