from typing import Tuple, Dict, Any
import openai

from src.utils.cost_manager import CostManager

class OpenAIProvider:
    """Wrapper around the OpenAI client with cost tracking."""

    def __init__(self, api_key: str, cost_manager: CostManager | None = None):
        self.client = openai.OpenAI(api_key=api_key)
        self.cost_manager = cost_manager

    def _calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        if self.cost_manager and model in self.cost_manager.model_costs.get("openai", {}):
            costs = self.cost_manager.model_costs["openai"][model]
            return (prompt_tokens * costs["input"] / 1000) + (completion_tokens * costs["output"] / 1000)
        return (prompt_tokens * 0.005 / 1000) + (completion_tokens * 0.015 / 1000)

    def _analyze(self, prompt: str, model: str) -> Tuple[str, float, Dict[str, int]]:
        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )
        content = response.choices[0].message.content
        usage = response.usage
        cost = self._calculate_cost(model, usage.prompt_tokens, usage.completion_tokens)
        if self.cost_manager:
            self.cost_manager.record_cost(
                provider="openai",
                model=model,
                actual_cost=cost,
                tokens_input=usage.prompt_tokens,
                tokens_output=usage.completion_tokens,
                request_type="analysis",
            )
        return content, cost, {"prompt_tokens": usage.prompt_tokens, "completion_tokens": usage.completion_tokens}
