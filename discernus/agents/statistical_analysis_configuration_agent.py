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

    def generate_statistical_plan(self, experiment_md_path: str) -> Dict[str, Any]:
        """
        Reads an experiment.md file and generates a structured statistical plan.
        """
        experiment_path = Path(experiment_md_path)
        if not experiment_path.exists():
            print(f"❌ Experiment file not found at: {experiment_path}")
            return {"validation_status": "error", "notes": "Experiment file not found."}

        content = experiment_path.read_text()
        methodology_section = self._extract_methodology(content)
        if not methodology_section:
            return {"validation_status": "error", "notes": "Could not find a methodology/design section."}

        return self._call_statistical_planner_llm(methodology_section)

    def _extract_methodology(self, content: str) -> str:
        """Extracts the relevant methodology section from the markdown."""
        match = re.search(r'(#+)\s*(Methodology|Experimental Design|Analysis Plan|Statistical Analysis)\s*#*', content, re.IGNORECASE)
        if not match:
            return content
        
        start_index = match.start()
        next_header_match = re.search(r'^#{{{level_num},}}\s+'.format(level_num=len(match.group(1))), content[start_index + len(match.group(0)):], re.MULTILINE)
        if next_header_match:
            end_index = start_index + len(match.group(0)) + next_header_match.start()
            return content[start_index:end_index]
        else:
            return content[start_index:]

    def _call_statistical_planner_llm(self, methodology_text: str) -> Dict[str, Any]:
        """Calls an LLM to generate the statistical plan as a JSON object."""
        prompt = f"""
You are an expert in computational social science methodology and statistics. Your task is to read a researcher's methodology and generate a structured JSON object representing their statistical analysis plan.

**Researcher's Methodology:**
---
{methodology_text}
---

**Your Task:**
Based on the researcher's methodology, generate a JSON object that specifies the required statistical tests.

- Identify all statistical tests mentioned (e.g., Cronbach's Alpha, ANOVA, T-Test, Chi-squared).
- For each test, specify its name and its purpose or scope (e.g., "inter-run reliability", "inter-model_comparison").
- If the plan is clear and sufficient, set `validation_status` to "complete".
- If the plan is ambiguous or missing key information, set `validation_status` to "incomplete" and provide notes on what is missing.

**Output ONLY the raw JSON object, with no other text or explanation.**

Example output:
{{
  "required_tests": [
    {{"test_name": "cronbach_alpha", "scope": "inter_run_reliability"}},
    {{"test_name": "anova", "scope": "inter_model_comparison"}}
  ],
  "validation_status": "complete",
  "notes": "The experiment clearly specifies the required statistical tests."
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

if __name__ == '__main__':
    agent = StatisticalAnalysisConfigurationAgent()
    plan = agent.generate_statistical_plan("projects/attesor/experiments/04_deep_smoke_test/experiment.md")
    print(json.dumps(plan, indent=2)) 