from typing import Tuple, Dict
import google.generativeai as genai

from src.utils.cost_manager import CostManager

class GoogleAIProvider:
    """Wrapper around the Google Generative AI client with cost tracking."""

    def __init__(self, api_key: str, cost_manager: CostManager | None = None):
        genai.configure(api_key=api_key)
        self.client = genai
        self.cost_manager = cost_manager

    def _get_model_mapping(self, model_name: str) -> str:
        """Map legacy/alias model names to current API model names."""
        model_map = {
            # Legacy mappings updated
            "gemini": "gemini-2-0-flash-exp",
            "gemini-pro": "gemini-2-0-flash-exp",
            "gemini-1.5-flash": "gemini-2-0-flash-exp",
            "gemini-1.5-pro": "gemini-2-0-flash-exp",
            "google": "gemini-2-0-flash-exp",
            
            # Gemini 2.5 series (2025)
            "gemini-2.5-pro": "gemini-2-5-pro-preview",  # June 2025 - most intelligent
            "gemini-2.5-flash": "gemini-2-5-flash-preview",  # May 2025 - adaptive thinking
            
            # Gemini 2.0 series
            "gemini-2.0-flash": "gemini-2-0-flash-exp",
            "gemini-2.0-pro": "gemini-2-0-flash-exp",
            
            # Production models (current availability)
            "gemini-2-0-flash-exp": "gemini-2-0-flash-exp",
            "gemini-2-5-pro-preview": "gemini-2-5-pro-preview",
            "gemini-2-5-flash-preview": "gemini-2-5-flash-preview",
        }
        return model_map.get(model_name, "gemini-2-0-flash-exp")

    def _get_generation_config(self, model: str) -> Dict:
        """Get model-specific generation configuration."""
        generation_config = {
            "temperature": 0.1,
            "max_output_tokens": 4000 if "2.5" in model else 2000,
        }
        
        # For Gemini 2.5, enable Deep Think reasoning
        if "2.5" in model:
            generation_config["reasoning_budget"] = "high"  # Enable adaptive thinking
        
        return generation_config

    def _calculate_cost(self, model: str, input_chars: int, output_chars: int) -> float:
        """Calculate cost with 2025 pricing model-specific rates."""
        if self.cost_manager and model in self.cost_manager.model_costs.get("google_ai", {}):
            costs = self.cost_manager.model_costs["google_ai"][model]
            return (input_chars * costs["input"] / 1000) + (output_chars * costs["output"] / 1000)
        
        # Model-specific pricing (2025 rates)
        if "2.5-pro" in model:
            # Gemini 2.5 Pro - premium with Deep Think
            return (input_chars * 0.002 / 1000) + (output_chars * 0.008 / 1000)
        elif "2.5-flash" in model:
            # Gemini 2.5 Flash - adaptive thinking
            return (input_chars * 0.001 / 1000) + (output_chars * 0.004 / 1000)
        elif "2.0" in model or "2-0" in model:
            # Gemini 2.0 series
            return (input_chars * 0.0008 / 1000) + (output_chars * 0.003 / 1000)
        else:
            # Fallback pricing
            return (input_chars * 0.0005 / 1000) + (output_chars * 0.0015 / 1000)

    def _analyze(self, prompt: str, model: str) -> Tuple[str, float, Dict[str, int]]:
        # Map model name to correct API model
        mapped_model = self._get_model_mapping(model)
        generation_config = self._get_generation_config(mapped_model)
        
        ai_model = self.client.GenerativeModel(
            model_name=mapped_model,
            generation_config=generation_config
        )
        response = ai_model.generate_content(prompt)
        content = response.text
        
        # Calculate cost based on character count (Google's pricing model)
        input_chars = len(prompt)
        output_chars = len(content)
        cost = self._calculate_cost(mapped_model, input_chars, output_chars)
        
        # Estimate tokens for recording (chars / 4 approximate)
        input_tokens = input_chars // 4
        output_tokens = output_chars // 4
        
        if self.cost_manager:
            self.cost_manager.record_cost(
                provider="google_ai",
                model=mapped_model,
                actual_cost=cost,
                tokens_input=input_tokens,
                tokens_output=output_tokens,
                request_type="analysis",
            )
        return content, cost, {"prompt_tokens": input_tokens, "completion_tokens": output_tokens}
