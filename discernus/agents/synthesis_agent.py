#!/usr/bin/env python3
"""
SynthesisAgent - Final Report and Artifact Generation
=====================================================

THIN Principle: This agent uses LLM intelligence to synthesize a final,
human-readable report from the various data points collected throughout the
workflow. It also generates structured data artifacts (e.g., CSV files) for
use with external tools. The 'smarts' are in the prompting, not the code.
"""

import sys
import json
import pandas as pd
from pathlib import Path
from typing import Dict, Any, List

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from discernus.gateway.llm_gateway import LLMGateway

class SynthesisAgent:
    """
    A THIN agent for synthesizing final reports and data artifacts.
    """

    def __init__(self, gateway: LLMGateway, model_registry=None):
        """
        Initializes the SynthesisAgent.
        """
        self.gateway = gateway
        print("✅ SynthesisAgent initialized")

    def execute(self, workflow_state: Dict[str, Any], step_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the synthesis step of the workflow.

        Args:
            workflow_state: The current state of the workflow.
            step_config: The configuration for this specific step.

        Returns:
            A dictionary containing the paths to the generated artifacts.
        """
        print("✍️  Running SynthesisAgent...")
        
        output_artifacts = step_config.get('config', {}).get('output_artifacts', [])
        session_results_path = Path(workflow_state.get('session_results_path', './results'))
        generated_artifacts = {}

        for artifact in output_artifacts:
            if artifact.endswith('.md'):
                report_content = self._generate_markdown_report(workflow_state)
                report_path = session_results_path / artifact
                report_path.write_text(report_content, encoding='utf-8')
                generated_artifacts['final_report_path'] = str(report_path)
                print(f"  - Generated Markdown report: {report_path}")

            elif artifact.endswith('.csv'):
                csv_path = self._generate_csv_results(workflow_state, session_results_path, artifact)
                generated_artifacts['csv_results_path'] = str(csv_path)
                print(f"  - Generated CSV results: {csv_path}")

        print("✅ SynthesisAgent finished.")
        return {"synthesis_results": generated_artifacts}

    def _generate_markdown_report(self, workflow_state: Dict[str, Any]) -> str:
        """
        Uses an LLM to generate a human-readable summary report.
        """
        print("  - Synthesizing Markdown report with LLM...")
        
        # This prompt is the core "intelligence" of the agent.
        # It needs to be sophisticated to produce a high-quality report.
        prompt = self._build_synthesis_prompt(workflow_state)
        
        # For synthesis, we typically want a powerful model.
        # This could be made configurable.
        model_name = "openai/gpt-4o" 

        try:
            # The gateway's method is synchronous and returns a tuple (content, metadata)
            content, metadata = self.gateway.execute_call(
                model=model_name,
                prompt=prompt,
                system_prompt="You are an expert academic research assistant.",
                # Higher temperature for more creative/fluent report writing
                temperature=0.7,
            )
            
            if metadata.get('success'):
                return content
            else:
                error_message = metadata.get('error', 'LLM failed to generate report.')
                print(f"❌ SynthesisAgent: LLM call failed: {error_message}")
                return f"# Synthesis Error\n\nAn error occurred while generating the report: {error_message}"

        except Exception as e:
            print(f"❌ SynthesisAgent: LLM infrastructure error: {e}")
            return f"# Synthesis Error\n\nAn infrastructure error occurred while generating the report: {e}"

    def _build_synthesis_prompt(self, workflow_state: Dict[str, Any]) -> str:
        """Constructs the prompt for the synthesis LLM call."""
        
        # Extracting key data from the workflow state
        experiment = workflow_state.get('experiment', {})
        framework = workflow_state.get('framework', {})
        analysis_results = workflow_state.get('analysis_results', [])
        calculation_results = workflow_state.get('calculation_results', {})

        # We'll serialize parts of the state to include in the prompt
        # Be mindful of token limits. We should summarize where possible.
        
        # Summary of analysis
        num_successful_runs = len(analysis_results)
        
        # Example of extracting qualitative data
        qualitative_summaries = [
            res.get('result', {}).get('json_output', {}).get('summary', 'No summary provided.')
            for res in analysis_results
        ]
        
        # Building the prompt string
        prompt = f"""
You are an expert academic research assistant. Your task is to write a final, comprehensive report for a computational social science experiment.

Synthesize the following information into a clear, well-structured, and insightful academic report in Markdown format.

## Experiment Overview
- **Name**: {experiment.get('name', 'N/A')}
- **Description**: {experiment.get('description', 'N/A')}
- **Hypothesis**: {experiment.get('hypothesis', 'N/A')}

## Framework Details
- **Name**: {framework.get('name', 'N/A')}
- **Description**: {framework.get('description', 'N/A')}

## Execution Summary
- **Number of successful analysis runs**: {num_successful_runs}
- **Models Used**: {', '.join(experiment.get('models', []))}

## Key Findings

### Qualitative Analysis Summary
Synthesize the key themes and insights from the following qualitative summaries generated by the AnalysisAgent. Do not just list them; weave them into a coherent narrative.
---
{json.dumps(qualitative_summaries, indent=2)}
---

### Quantitative & Calculated Results
Here are the calculated metrics. Interpret these findings in the context of the experiment's hypothesis.
---
{json.dumps(calculation_results, indent=2)}
---

## Conclusion
Provide a final conclusion that addresses the original hypothesis. Discuss the implications of the findings, potential limitations of the study, and suggest directions for future research.
"""
        return prompt

    def _generate_csv_results(self, workflow_state: Dict[str, Any], results_path: Path, filename: str) -> Path:
        """
        Generates a structured CSV file from the analysis results.
        """
        print("  - Generating structured CSV results...")
        csv_path = results_path / filename
        
        analysis_results = workflow_state.get('analysis_results', [])
        if not analysis_results:
            # Create an empty file to satisfy the return type and workflow expectations
            df = pd.DataFrame()
            df.to_csv(csv_path, index=False)
            print("  - No analysis results found. Generated empty CSV.")
            return csv_path
            
        # We need to flatten the nested JSON structure into a tabular format.
        # This is a classic data wrangling task.
        
        records = []
        for result in analysis_results:
            base_info = {
                'agent_id': result.get('agent_id'),
                'model_name': result.get('model_name'),
                'corpus_file': Path(result.get('corpus_file')).name,
                'run_num': result.get('run_num'),
                'execution_time': result.get('result', {}).get('execution_time', 0),
                'success': result.get('result', {}).get('success', False),
            }
            
            # Extract scores from the JSON output
            json_output = result.get('result', {}).get('json_output', {})
            if isinstance(json_output, dict) and 'scores' in json_output:
                scores = json_output['scores']
                if isinstance(scores, dict):
                    # Add each score as a separate column
                    for key, value in scores.items():
                        base_info[f"score_{key}"] = value

            records.append(base_info)
            
        df = pd.DataFrame(records)
        df.to_csv(csv_path, index=False)
        
        return csv_path 