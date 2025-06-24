from typing import Tuple, Dict, Optional
import anthropic

from src.utils.cost_manager import CostManager

class AnthropicProvider:
    """Wrapper around the Anthropic client with cost tracking."""

    def __init__(self, api_key: str, cost_manager: Optional[CostManager] = None):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.cost_manager = cost_manager

    def _get_model_mapping(self, model_name: str) -> str:
        """Map legacy/alias model names to current API model names."""
        model_map = {
            # Legacy mappings updated to latest
            "claude": "claude-3-5-sonnet-20241022",
            "claude-3": "claude-3-5-sonnet-20241022",
            "claude-3-sonnet": "claude-3-5-sonnet-20241022",
            "claude-3-haiku": "claude-3-5-haiku-20241022",
            "anthropic": "claude-4-sonnet",
            
            # Claude 4 series (May 2025)
            "claude-4": "claude-4-sonnet",
            "claude-4-opus": "claude-4-opus",
            "claude-4-sonnet": "claude-4-sonnet",
            
            # Claude 3.7 with extended thinking (February 2025)
            "claude-3.7": "claude-3-7-sonnet",
            "claude-3.7-sonnet": "claude-3-7-sonnet",
            
            # Latest Claude 3.5 series
            "claude-3.5-sonnet": "claude-3-5-sonnet-20241022",
            "claude-3.5-haiku": "claude-3-5-haiku-20241022",
            
            # Production models
            "claude-3-5-sonnet-20241022": "claude-3-5-sonnet-20241022",
            "claude-3-5-haiku-20241022": "claude-3-5-haiku-20241022",
        }
        return model_map.get(model_name, "claude-3-5-sonnet-20241022")

    def _get_max_tokens(self, model: str) -> int:
        """Get model-specific max_tokens value."""
        if "claude-4" in model:
            return 4000  # Claude 4 has enhanced output capabilities
        elif "3.7" in model:
            return 3000  # Extended thinking models
        else:
            return 2000  # Standard models

    def _calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost with 2025 pricing model-specific rates."""
        if self.cost_manager and model in self.cost_manager.model_costs.get("anthropic", {}):
            costs = self.cost_manager.model_costs["anthropic"][model]
            if "per_operation" in costs:
                return costs["per_operation"]
            return (input_tokens * costs["input"] / 1000) + (output_tokens * costs["output"] / 1000)
        
        # Model-specific pricing (2025 rates)
        if "claude-4" in model:
            if "opus" in model:
                # Claude 4 Opus - premium model
                return (input_tokens * 0.025 / 1000) + (output_tokens * 0.125 / 1000)
            else:  # Claude 4 Sonnet
                return (input_tokens * 0.006 / 1000) + (output_tokens * 0.024 / 1000)
        elif "3.7" in model:
            # Claude 3.7 with extended thinking
            return (input_tokens * 0.004 / 1000) + (output_tokens * 0.018 / 1000)
        elif "3-5" in model or "3.5" in model:
            if "sonnet" in model:
                return (input_tokens * 0.003 / 1000) + (output_tokens * 0.015 / 1000)
            else:  # haiku
                return (input_tokens * 0.00025 / 1000) + (output_tokens * 0.00125 / 1000)
        else:
            # Fallback for older models
            return (input_tokens * 0.003 / 1000) + (output_tokens * 0.015 / 1000)

    def _analyze(self, prompt: str, model: str) -> Tuple[str, float, Dict[str, int]]:
        # Map model name to correct API model
        mapped_model = self._get_model_mapping(model)
        max_tokens = self._get_max_tokens(mapped_model)
        
        response = self.client.messages.create(
            model=mapped_model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,  # CRITICAL: This was missing!
            temperature=0.1,
        )
        content = response.content[0].text
        usage = response.usage
        cost = self._calculate_cost(mapped_model, usage.input_tokens, usage.output_tokens)
        if self.cost_manager:
            self.cost_manager.record_cost(
                provider="anthropic",
                model=mapped_model,
                actual_cost=cost,
                tokens_input=usage.input_tokens,
                tokens_output=usage.output_tokens,
                request_type="analysis",
            )
        return content, cost, {"prompt_tokens": usage.input_tokens, "completion_tokens": usage.output_tokens}
