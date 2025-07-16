#!/usr/bin/env python3
"""
True Validation Agent
=====================

THIN Principle: This agent is a specialized "Role-Playing" agent. Its entire
purpose is to adopt the persona of a rigorous academic peer reviewer. It is given
the project's core documents and a set of explicit, transparent rubrics, and it
uses its world knowledge to provide a qualitative assessment.
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from discernus.gateway.llm_gateway import LLMGateway
    from discernus.gateway.model_registry import ModelRegistry
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"TrueValidationAgent dependencies not available: {e}")
    DEPENDENCIES_AVAILABLE = False

class TrueValidationAgent:
    """
    Performs deep, rubric-based validation of framework and experiment specifications.
    """

    def __init__(self):
        if not DEPENDENCIES_AVAILABLE:
            raise ImportError("Could not import required dependencies for TrueValidationAgent")
        
        self.model_registry = ModelRegistry()
        self.gateway = LLMGateway(self.model_registry)
        self._load_rubrics()

    def _load_rubrics(self):
        """Loads the validation rubrics from the core directory."""
        self.framework_rubric = (project_root / "discernus/core/framework_specification_validation_rubric.md").read_text()
        self.experiment_rubric = (project_root / "discernus/core/experiment_specification_validation_rubric.md").read_text()

    async def validate_project_coherence(self, framework_content: str, experiment_content: str) -> Dict[str, Any]:
        """
        Validates the coherence and methodological soundness of the project assets.
        """
        validation_prompt = self._create_validation_prompt(framework_content, experiment_content)
        
        # Use a powerful model for this complex reasoning task
        model_name = self.model_registry.get_model_for_task('synthesis')
        if not model_name:
            return {"validation_passed": False, "error": "No suitable model found for validation."}
            
        response, _ = self.gateway.execute_call(model=model_name, prompt=validation_prompt)
        
        # In a real implementation, we would parse the response to get a structured
        # pass/fail result and detailed feedback. For now, we return the raw response.
        return {
            "validation_passed": "METHODOLOGICALLY SOUND" in response.upper(),
            "feedback": response
        }

    def _create_validation_prompt(self, framework_content: str, experiment_content: str) -> str:
        """Creates the comprehensive prompt for the validation LLM call."""
        return f"""
You are a meticulous, world-class academic peer reviewer. Your task is to perform a deep, methodological validation of a research project's core documents. You must assess the coherence, clarity, and soundness of the proposed research based on the provided framework, experiment, and a set of rigorous validation rubrics.

**YOUR TASK:**

1.  Read the **Framework Specification** provided below.
2.  Read the **Experiment Specification** provided below.
3.  Critically assess both documents against the **Framework Validation Rubric** and the **Experiment Validation Rubric**.
4.  Provide a holistic judgment. If the project is methodologically sound and ready for execution, respond with the single phrase: "METHODOLOGICALLY SOUND".
5.  If there are any issues, provide a detailed, constructive critique explaining the problems and offering concrete suggestions for improvement.

---
**FRAMEWORK VALIDATION RUBRIC**
---
{self.framework_rubric}
---

---
**EXPERIMENT VALIDATION RUBRIC**
---
{self.experiment_rubric}
---

---
**FRAMEWORK SPECIFICATION (USER-PROVIDED)**
---
{framework_content}
---

---
**EXPERIMENT SPECIFICATION (USER-PROVIDED)**
---
{experiment_content}
---

**FINAL INSTRUCTIONS:**

Review all provided materials. If the project meets the standards outlined in the rubrics, respond *only* with the phrase "METHODOLOGICALLY SOUND". Otherwise, provide your detailed peer review.
""" 