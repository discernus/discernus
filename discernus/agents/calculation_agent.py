#!/usr/bin/env python3
"""
CalculationAgent - Deterministic Mathematical Operations
========================================================

THIN Principle: This agent performs deterministic mathematical calculations
based on a 'calculation_spec' defined within a framework.md file. It takes
the structured JSON output from the AnalysisAgent and applies predefined
formulas. All logic is declarative and specified by the researcher in the
framework, not hardcoded in the agent.
"""

import sys
from pathlib import Path
from typing import Dict, Any, List

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from discernus.core.secure_code_executor import SecureCodeExecutor

class CalculationAgent:
    """
    A THIN agent for performing deterministic calculations.
    """

    def __init__(self, gateway=None, model_registry=None):
        """
        Initializes the CalculationAgent.
        Note: This agent does not require LLM capabilities.
        """
        self.executor = SecureCodeExecutor()
        print("✅ CalculationAgent initialized")

    def execute(self, workflow_state: Dict[str, Any], step_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the calculation step of the workflow.

        Args:
            workflow_state: The current state of the workflow.
            step_config: The configuration for this specific step (not used by this agent).

        Returns:
            A dictionary containing the calculated results.
        """
        print("🔬 Running CalculationAgent...")
        
        analysis_results = workflow_state.get('analysis_results', [])
        framework_spec = workflow_state.get('framework', {})
        calculation_spec = framework_spec.get('calculation_spec')

        if not calculation_spec:
            print("- CalculationAgent: No 'calculation_spec' found in framework. Skipping.")
            return {"calculation_results": {}}

        if not analysis_results:
            print("- CalculationAgent: No 'analysis_results' in workflow_state. Skipping.")
            return {"calculation_results": {}}
            
        calculated_metrics = {}

        for calculation in calculation_spec:
            name = calculation.get('name')
            formula = calculation.get('formula')
            data_source = calculation.get('data_source') # e.g., 'scores' from analysis

            if not all([name, formula, data_source]):
                print(f"- CalculationAgent: Skipping misconfigured calculation: {calculation}")
                continue

            # This example assumes we are processing a list of results,
            # and the formula applies to values extracted from them.
            # A more sophisticated implementation would handle various data shapes.
            
            # We'll prepare a local context for the secure executor
            # For now, let's assume 'data_source' points to a key in each result's JSON
            
            # This is a simplified example. A real implementation needs to be
            # more robust about how it prepares the context for the formula.
            # For instance, it might aggregate all scores into a list.
            
            # Let's try to pass all scores as a list to the executor context
            scores_list = []
            for result in analysis_results:
                json_output = result.get('result', {}).get('json_output', {})
                if isinstance(json_output, dict):
                    scores = json_output.get(data_source)
                    if scores is not None:
                         # This part is tricky and depends on the score format.
                         # Assuming scores is a dict of key:value
                         if isinstance(scores, dict):
                             scores_list.extend(scores.values())


            if not scores_list:
                print(f"- CalculationAgent: Could not find any data for '{data_source}'")
                continue

            # The user's formula is executed in a context where 'scores' is a list of numbers.
            # The result of the formula must be assigned to the 'result_data' variable.
            code = f"""
import numpy as np
scores = {scores_list}
result_data = {formula}
"""
            
            try:
                # The SecureCodeExecutor runs the code and returns a dictionary.
                execution_result_dict = self.executor.execute_code(code)

                if execution_result_dict.get('success'):
                    # The actual calculated value is in the 'result_data' key.
                    calculated_value = execution_result_dict.get('result_data')
                    calculated_metrics[name] = calculated_value
                    print(f"  - Calculated '{name}': {calculated_value}")
                else:
                    error_message = execution_result_dict.get('error', 'Unknown execution error')
                    print(f"❌ CalculationAgent: Error executing formula for '{name}': {error_message}")
                    calculated_metrics[name] = {"error": error_message}

            except Exception as e:
                print(f"❌ CalculationAgent: Infrastructure error executing formula for '{name}': {e}")
                calculated_metrics[name] = {"error": str(e)}


        print("✅ CalculationAgent finished.")
        return {"calculation_results": calculated_metrics} 