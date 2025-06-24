from typing import Tuple, Dict, Any, Optional
import openai

from src.utils.cost_manager import CostManager

class OpenAIProvider:
    """Wrapper around the OpenAI client with cost tracking."""

    def __init__(self, api_key: str, cost_manager: Optional[CostManager] = None):
        self.client = openai.OpenAI(api_key=api_key)
        self.cost_manager = cost_manager

    def _get_model_mapping(self, model_name: str) -> str:
        """Map legacy/alias model names to current API model names."""
        model_map = {
            # Legacy mappings to REAL models
            "gpt-4": "gpt-4o",
            "gpt-3.5-turbo": "gpt-4o-mini",
            "openai": "gpt-4o",
            
            # Real GPT-4o series (current production)
            "gpt-4o": "gpt-4o",
            "gpt-4o-mini": "gpt-4o-mini",
            
            # GPT-4 Turbo series
            "gpt-4-turbo": "gpt-4-turbo",
            "gpt-4-turbo-2024-04-09": "gpt-4-turbo-2024-04-09",
            
            # Surprisingly working models (might be aliases)
            "gpt-4.1": "gpt-4.1",
            "gpt-4.1-mini": "gpt-4.1-mini", 
            
            # Open-source models (map to real models)
            "deepseek-r1": "gpt-4o",
            "qwen3-235b": "gpt-4o",
            "llama-4-scout": "gpt-4o",
            "llama-3.3-70b": "gpt-4o",
        }
        return model_map.get(model_name, "gpt-4o")

    def _get_max_tokens(self, model: str) -> int:
        """Get model-specific max_tokens value."""
        if "4.1" in model:
            return 4000  # GPT-4.1 series supports longer outputs
        elif model.startswith("o"):
            return 3000  # o-series optimized for reasoning
        else:
            return 2000  # Standard models

    def _calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        """Calculate cost with 2025 pricing model-specific rates."""
        if self.cost_manager and model in self.cost_manager.model_costs.get("openai", {}):
            costs = self.cost_manager.model_costs["openai"][model]
            return (prompt_tokens * costs["input"] / 1000) + (completion_tokens * costs["output"] / 1000)
        
        # Updated pricing for 2025 models (significantly reduced costs)
        if "4.1" in model:
            if "mini" in model:
                return (prompt_tokens * 0.00015 / 1000) + (completion_tokens * 0.0006 / 1000)
            elif "nano" in model:
                return (prompt_tokens * 0.0001 / 1000) + (completion_tokens * 0.0004 / 1000)
            else:  # GPT-4.1 standard
                return (prompt_tokens * 0.005 / 1000) + (completion_tokens * 0.015 / 1000)
        elif model.startswith("o"):
            # o-series reasoning models (premium pricing for reasoning)
            if "mini" in model:
                return (prompt_tokens * 0.003 / 1000) + (completion_tokens * 0.012 / 1000)
            else:
                return (prompt_tokens * 0.015 / 1000) + (completion_tokens * 0.06 / 1000)
        elif "4o" in model:
            if "mini" in model:
                return (prompt_tokens * 0.00015 / 1000) + (completion_tokens * 0.0006 / 1000)
            else:
                return (prompt_tokens * 0.0025 / 1000) + (completion_tokens * 0.01 / 1000)
        else:
            # Fallback pricing for older models
            return (prompt_tokens * 0.01 / 1000) + (completion_tokens * 0.03 / 1000)

    def _analyze(self, prompt: str, model: str) -> Tuple[str, float, Dict[str, int]]:
        # Map model name to correct API model
        mapped_model = self._get_model_mapping(model)
        max_tokens = self._get_max_tokens(mapped_model)
        
        response = self.client.chat.completions.create(
            model=mapped_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=max_tokens,  # CRITICAL: This was missing!
        )
        content = response.choices[0].message.content
        usage = response.usage
        cost = self._calculate_cost(mapped_model, usage.prompt_tokens, usage.completion_tokens)
        if self.cost_manager:
            self.cost_manager.record_cost(
                provider="openai",
                model=mapped_model,
                actual_cost=cost,
                tokens_input=usage.prompt_tokens,
                tokens_output=usage.completion_tokens,
                request_type="analysis",
            )
        return content, cost, {"prompt_tokens": usage.prompt_tokens, "completion_tokens": usage.completion_tokens}
