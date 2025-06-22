from typing import Tuple, Dict
import google.generativeai as genai

from src.utils.cost_manager import CostManager

class GoogleAIProvider:
    """Wrapper around the Google Generative AI client with cost tracking."""

    def __init__(self, api_key: str, cost_manager: CostManager | None = None):
        genai.configure(api_key=api_key)
        self.client = genai
        self.cost_manager = cost_manager

    def _calculate_cost(self, model: str, input_chars: int, output_chars: int) -> float:
        if self.cost_manager and model in self.cost_manager.model_costs.get("google_ai", {}):
            costs = self.cost_manager.model_costs["google_ai"][model]
            return (input_chars * costs["input"] / 1000) + (output_chars * costs["output"] / 1000)
        return (input_chars * 0.0005 / 1000) + (output_chars * 0.0015 / 1000)

    def _analyze(self, prompt: str, model: str) -> Tuple[str, float, Dict[str, int]]:
        ai_model = self.client.GenerativeModel(model)
        response = ai_model.generate_content(prompt)
        content = response.text
        cost = self._calculate_cost(model, len(prompt), len(content))
        if self.cost_manager:
            self.cost_manager.record_cost(
                provider="google_ai",
                model=model,
                actual_cost=cost,
                tokens_input=len(prompt) // 4,
                tokens_output=len(content) // 4,
                request_type="analysis",
            )
        return content, cost, {"prompt_tokens": len(prompt) // 4, "completion_tokens": len(content) // 4}
