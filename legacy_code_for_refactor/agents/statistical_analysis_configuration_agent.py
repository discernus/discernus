#!/usr/bin/env python3
"""
Statistical Analysis Configuration Agent
========================================

THIN Principle: This agent validates that an experiment's statistical analysis
plan is well-defined and complete *before* any analysis is run. It translates
the researcher's plain-English methodology into a structured, machine-readable
plan for the SecureCodeExecutor.
"""

import sys
from pathlib import Path
import yaml
import re
import json
from typing import Dict, Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from discernus.gateway.llm_gateway import LLMGateway
    from discernus.gateway.model_registry import ModelRegistry
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"StatisticalAnalysisConfigurationAgent dependencies not available: {e}")
    DEPENDENCIES_AVAILABLE = False

class StatisticalAnalysisConfigurationAgent:
    """
    Validates and structures the statistical analysis plan for an experiment.
    """

    def __init__(self):
        if not DEPENDENCIES_AVAILABLE:
            raise ImportError("Could not import required dependencies for StatisticalAnalysisConfigurationAgent")
        self.model_registry = ModelRegistry()
        self.gateway = LLMGateway(self.model_registry)

    def generate_statistical_plan(self, workflow_state: Dict[str, Any], step_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Reads an experiment.md file from the workflow_state and generates a structured statistical plan.
        """
        experiment_md_path = workflow_state.get('experiment_md_path')
        if not experiment_md_path:
            return {"validation_status": "error", "notes": "experiment_md_path not found in workflow_state."}

        experiment_path = Path(experiment_md_path)
        if not experiment_path.exists():
            return {"validation_status": "error", "notes": "Experiment file not found."}

        content = experiment_path.read_text()
        
        return self._call_statistical_planner_llm(content)

    def _call_statistical_planner_llm(self, methodology_text: str) -> Dict[str, Any]:
        """Calls an LLM to generate the statistical plan as a JSON object."""
        prompt = f"""
You are an expert in computational social science methodology and statistics. Your task is to act as an intelligent research assistant. Read a researcher's full experiment specification and generate a structured JSON object representing their statistical analysis plan.

**Full Experiment Specification:**
---
{methodology_text}
---

**Your Task:**

1.  **Analyze the Experiment**: Carefully read the entire experiment specification to understand the researcher's goals, the number of models being tested, and the number of runs.
2.  **Identify Explicit Plan**: Look for an explicit statistical analysis plan. If the researcher has specified tests (e.g., "perform Cronbach's Alpha," "compare models using ANOVA"), use that as your primary guide.
3.  **Propose a Plan if Necessary**: If no explicit statistical plan is provided, you MUST infer a sensible default plan based on the experimental design.
    *   If `num_runs` > 1 for a single model, a test for inter-run reliability (like Cronbach's Alpha) is appropriate.
    *   If multiple `models` are listed, a test for inter-model comparison (like ANOVA or a T-test) is appropriate.
    *   If the experiment is simple, it may be that no statistical tests are needed. In that case, return an empty list for `required_tests`.
4.  **Generate JSON Output**: Generate a JSON object with the following structure:
    *   `required_tests`: A list of dictionaries, where each dictionary specifies a `test_name` and a `scope`.
    *   `validation_status`: Set to `"complete"` if the user provided a clear plan. Set to `"generated"` if you inferred the plan.
    *   `notes`: Provide a brief, human-readable explanation of your reasoning. Explain what you found or what you inferred.

**Output ONLY the raw JSON object, with no other text or explanation.**

Example output for an experiment with multiple runs:
{{
  "required_tests": [
    {{"test_name": "cronbach_alpha", "scope": "inter_run_reliability"}}
  ],
  "validation_status": "generated",
  "notes": "No explicit statistical plan was found. Based on the use of multiple runs, a Cronbach's Alpha test for inter-run reliability has been proposed."
}}
"""
        
        model_name = "anthropic/claude-3-haiku-20240307"

        try:
            response, _ = self.gateway.execute_call(model=model_name, prompt=prompt)
            if not response:
                return {"validation_status": "error", "notes": "LLM response was empty."}
            
            # Clean up the response to ensure it's valid JSON
            json_response = response.strip()
            if json_response.startswith('```json'):
                match = re.search(r'```json\n(.*?)\n```', json_response, re.DOTALL)
                if match:
                    json_response = match.group(1)
            
            return json.loads(json_response)
        except (Exception, json.JSONDecodeError) as e:
            return {"validation_status": "error", "notes": f"Error generating or parsing JSON from LLM: {e}"} 