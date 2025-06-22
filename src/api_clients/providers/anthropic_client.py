from typing import Tuple, Dict
import anthropic

from src.utils.cost_manager import CostManager

class AnthropicProvider:
    """Wrapper around the Anthropic client with cost tracking."""

    def __init__(self, api_key: str, cost_manager: CostManager | None = None):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.cost_manager = cost_manager

    def _calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        if self.cost_manager and model in self.cost_manager.model_costs.get("anthropic", {}):
            costs = self.cost_manager.model_costs["anthropic"][model]
            if "per_operation" in costs:
                return costs["per_operation"]
            return (input_tokens * costs["input"] / 1000) + (output_tokens * costs["output"] / 1000)
        return (input_tokens * 0.003 / 1000) + (output_tokens * 0.015 / 1000)

    def _analyze(self, prompt: str, model: str) -> Tuple[str, float, Dict[str, int]]:
        response = self.client.messages.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            temperature=0.1,
        )
        content = response.content[0].text
        usage = response.usage
        cost = self._calculate_cost(model, usage.input_tokens, usage.output_tokens)
        if self.cost_manager:
            self.cost_manager.record_cost(
                provider="anthropic",
                model=model,
                actual_cost=cost,
                tokens_input=usage.input_tokens,
                tokens_output=usage.output_tokens,
                request_type="analysis",
            )
        return content, cost, {"prompt_tokens": usage.input_tokens, "completion_tokens": usage.output_tokens}
