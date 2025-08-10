"""
Classification Agent

This agent is responsible for applying a classification rubric to a set of
calculated metrics. It is a simple, deterministic agent with no LLM calls.
"""
from dataclasses import dataclass
from typing import Dict, Any, Optional, List

@dataclass
class ClassificationRequest:
    """Request to the ClassificationAgent."""
    calculated_metrics: Dict[str, float]
    classification_rubric: Dict[str, Dict[str, List[float]]]

@dataclass
class ClassificationResponse:
    """Response from the ClassificationAgent."""
    success: bool
    classifications: Optional[Dict[str, str]] = None
    error_message: Optional[str] = None

class ClassificationAgent:
    """Applies a classification rubric to calculated metrics."""

    def classify(self, request: ClassificationRequest) -> ClassificationResponse:
        """
        Applies the rubric to the metrics.

        Args:
            request: The request containing metrics and the rubric.

        Returns:
            The response containing the final classifications.
        """
        try:
            classifications = {}
            for metric_name, rubric in request.classification_rubric.items():
                if metric_name in request.calculated_metrics:
                    value = request.calculated_metrics[metric_name]
                    classified = False
                    for category, value_range in rubric.items():
                        if value_range[0] <= value <= value_range[1]:
                            classifications[f"{metric_name}_classification"] = category
                            classified = True
                            break
                    if not classified:
                        classifications[f"{metric_name}_classification"] = "Unclassified"
            
            return ClassificationResponse(success=True, classifications=classifications)

        except Exception as e:
            return ClassificationResponse(success=False, error_message=str(e))
