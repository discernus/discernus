from typing import Tuple, Dict
from mistralai.client import MistralClient

from src.utils.cost_manager import CostManager

class MistralProvider:
    """Wrapper around the Mistral client with cost tracking."""

    def __init__(self, api_key: str, cost_manager: CostManager | None = None):
        self.client = MistralClient(api_key=api_key)
        self.cost_manager = cost_manager

    def _calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        if self.cost_manager and model in self.cost_manager.model_costs.get("mistral", {}):
            costs = self.cost_manager.model_costs["mistral"][model]
            if "per_operation" in costs:
                return costs["per_operation"]
            return (input_tokens * costs["input"] / 1000) + (output_tokens * costs["output"] / 1000)
        return (input_tokens * 0.008 / 1000) + (output_tokens * 0.024 / 1000)

    def _analyze(self, prompt: str, model: str) -> Tuple[str, float, Dict[str, int]]:
        response = self.client.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )
        content = response.choices[0].message.content
        # Mistral API may not return token usage; estimate from text
        input_tokens = len(prompt.split())
        output_tokens = len(content.split())
        cost = self._calculate_cost(model, input_tokens, output_tokens)
        if self.cost_manager:
            self.cost_manager.record_cost(
                provider="mistral",
                model=model,
                actual_cost=cost,
                tokens_input=input_tokens,
                tokens_output=output_tokens,
                request_type="analysis",
            )
        return content, cost, {"prompt_tokens": input_tokens, "completion_tokens": output_tokens}
