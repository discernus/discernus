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
        
        framework_spec = workflow_state.get('framework', {})
        calculation_spec = framework_spec.get('calculation_spec')

        if not calculation_spec:
            print("- CalculationAgent: No 'calculation_spec' found in framework. Skipping.")
            # Pass through the results from the previous step
            return {"analysis_results": workflow_state.get('analysis_results', [])}

        analysis_results = workflow_state.get('analysis_results', [])

        if not analysis_results:
            print("- CalculationAgent: No 'analysis_results' in workflow_state. Skipping.")
            return {"analysis_results": []}
            
        # Handle both dictionary format (newer AnalysisAgent) and list format (older AnalysisAgent)
        if isinstance(analysis_results, dict):
            # Convert dictionary format to list format for processing
            results_list = list(analysis_results.values())
            was_dict_format = True
        elif isinstance(analysis_results, list):
            results_list = analysis_results
            was_dict_format = False
        else:
            print(f"- CalculationAgent: Invalid analysis_results format: {type(analysis_results)}. Skipping.")
            return {"analysis_results": analysis_results}
            
        # This agent should modify the results in place, adding new keys
        # rather than creating a whole new structure.
        for result in results_list:
            if not isinstance(result, dict) or not result.get('success'):
                continue

            json_output = result.get('json_output', {})
            if not isinstance(json_output, dict):
                continue
            
            # Prepare a local context for the secure executor
            # Framework-agnostic: find ALL numeric fields in json_output for calculations
            context = {}
            for key, value in json_output.items():
                if isinstance(value, dict):
                    # Add all numeric values from nested dictionaries (e.g., scores, dimension_scores, emotion_metrics)
                    for nested_key, nested_value in value.items():
                        if isinstance(nested_value, (int, float)):
                            context[nested_key] = nested_value
                elif isinstance(value, (int, float)):
                    # Add top-level numeric values
                    context[key] = value
            
            if not context:
                continue

            # Handle both dictionary format (name: formula) and list format
            if isinstance(calculation_spec, dict):
                # Framework format: {"name": "formula", ...}
                calculation_items = calculation_spec.items()
            else:
                # List format: [{"name": "...", "formula": "..."}, ...]
                calculation_items = [(calc.get('name'), calc.get('formula')) for calc in calculation_spec]

            for name, formula in calculation_items:
                if isinstance(formula, dict):
                    # Handle nested format where formula is a dict
                    if 'metric' in formula:
                        calc_data = formula['metric']
                        name = calc_data.get('name', name)
                        formula = calc_data.get('formula')
                    else:
                        formula = formula.get('formula')

                if not name or not formula:
                    print(f"- CalculationAgent: Skipping misconfigured calculation: {name} -> {formula}")
                    continue

                try:
                    # The SecureCodeExecutor runs the formula in the context of the scores
                    # The formula should be a valid Python expression.
                    # For example: "(score_identity_axis + score_goal_axis) / 2"
                    # The executor will make the keys of the context dict available as variables.
                    
                    # We need to prepend 'result_data = ' for the executor
                    code = f"result_data = {formula}"

                    execution_result = self.executor.execute_code(code, context)
                    
                    if execution_result.get('success'):
                        calculated_value = execution_result.get('result_data')
                        # Framework-agnostic: store calculated metrics at the top level
                        # This allows any framework to access them without assuming specific structure
                        json_output[name] = calculated_value
                    else:
                        error_message = execution_result.get('error', 'Unknown execution error')
                        # The orchestrator will handle logging failures
                        result['error'] = error_message
                        result['success'] = False


                except Exception as e:
                    result['error'] = f"Infrastructure error: {e}"
                    result['success'] = False

        print("✅ CalculationAgent finished.")
        
        # Return the results in the same format they came in
        if was_dict_format and isinstance(analysis_results, dict):
            # Convert back to dictionary format using agent_id as key
            results_dict = {}
            for result in results_list:
                agent_id = result.get('agent_id', f"unknown_{hash(str(result))}")
                results_dict[agent_id] = result
            return {"analysis_results": results_dict}
        else:
            return {"analysis_results": results_list} 