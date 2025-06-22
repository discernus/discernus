from typing import Tuple, Dict
from mistralai.client import MistralClient

from src.utils.cost_manager import CostManager

class MistralProvider:
    """Wrapper around the Mistral client with cost tracking."""

    def __init__(self, api_key: str, cost_manager: CostManager | None = None):
        self.client = MistralClient(api_key=api_key)
        self.cost_manager = cost_manager

    def _get_model_mapping(self, model_name: str) -> str:
        """Map legacy/alias model names to current API model names."""
        model_map = {
            # Legacy mappings updated
            "mistral": "mistral-large-2411",
            "mistral-large": "mistral-large-2411",
            "mistral-medium": "mistral-medium-3",
            "mistral-small": "mistral-small-3.1",
            
            # 2025 Models
            "mistral-medium-3": "mistral-medium-3",  # May 2025 - frontier multimodal
            "mistral-small-3.1": "mistral-small-3.1",  # Latest small model
            "codestral-2501": "codestral-2501",  # January 2025 - coding
            "mistral-ocr-2505": "mistral-ocr-2505",  # May 2025 - OCR
            "mistral-saba-2502": "mistral-saba-2502",  # February 2025 - multilingual
            "devstral-small-2505": "devstral-small-2505",  # May 2025 - software engineering
            
            # Production models
            "mistral-large-2411": "mistral-large-2411",
            "mistral-small-2409": "mistral-small-2409",
        }
        return model_map.get(model_name, "mistral-large-2411")

    def _get_max_tokens(self, model: str) -> int:
        """Get model-specific max_tokens value."""
        if "medium-3" in model:
            return 4000  # Frontier model with enhanced capabilities
        elif "codestral" in model or "devstral" in model:
            return 3000  # Coding-optimized models
        else:
            return 2000  # Standard models

    def _calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost with 2025 pricing model-specific rates."""
        if self.cost_manager and model in self.cost_manager.model_costs.get("mistral", {}):
            costs = self.cost_manager.model_costs["mistral"][model]
            if "per_operation" in costs:
                return costs["per_operation"]
            return (input_tokens * costs["input"] / 1000) + (output_tokens * costs["output"] / 1000)
        
        # Model-specific pricing (2025 rates)
        if "medium-3" in model:
            # Frontier multimodal model - premium pricing
            return (input_tokens * 0.02 / 1000) + (output_tokens * 0.06 / 1000)
        elif "codestral-2501" in model or "devstral" in model:
            # Specialized coding models
            return (input_tokens * 0.012 / 1000) + (output_tokens * 0.036 / 1000)
        elif "ocr" in model:
            # OCR service pricing (per operation)
            return 0.02  # Flat rate per OCR operation
        elif "saba" in model:
            # Multilingual model
            return (input_tokens * 0.008 / 1000) + (output_tokens * 0.024 / 1000)
        elif "large-2411" in model:
            return (input_tokens * 0.008 / 1000) + (output_tokens * 0.024 / 1000)
        elif "small" in model:
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
        
        response = self.client.chat(
            model=mapped_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=max_tokens,  # CRITICAL: This was missing!
        )
        content = response.choices[0].message.content
        
        # Improved token estimation (more accurate than word splits)
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
