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
        model_name = "vertex_ai/gemini-2.5-pro" 

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
        """Constructs an enhanced prompt for statistical synthesis with code execution."""
        
        # Extracting key data from the workflow state
        experiment = workflow_state.get('experiment', {})
        framework = workflow_state.get('framework', {})
        analysis_results = workflow_state.get('analysis_results', [])

        # Filter successful runs and extract structured data
        successful_runs = [r for r in analysis_results if r.get('success', False)]
        
        # Create a structured data representation that can be directly used by the LLM
        structured_data = []
        for result in successful_runs:
            json_output = result.get('json_output', {})
            if json_output:
                record = {
                    'corpus_file': result.get('corpus_file', ''),
                    'run_num': result.get('run_num', 0),
                    'tribal_dominance_score': json_output.get('tribal_dominance_score', 0),
                    'individual_dignity_score': json_output.get('individual_dignity_score', 0),
                    'fear_score': json_output.get('fear_score', 0),
                    'hope_score': json_output.get('hope_score', 0),
                    'envy_score': json_output.get('envy_score', 0),
                    'compersion_score': json_output.get('compersion_score', 0),
                    'enmity_score': json_output.get('enmity_score', 0),
                    'amity_score': json_output.get('amity_score', 0),
                    'fragmentative_goal_score': json_output.get('fragmentative_goal_score', 0),
                    'cohesive_goal_score': json_output.get('cohesive_goal_score', 0),
                    'descriptive_cohesion_index': json_output.get('descriptive_cohesion_index', 0),
                    'motivational_cohesion_index': json_output.get('motivational_cohesion_index', 0),
                    'full_cohesion_index': json_output.get('full_cohesion_index', 0)
                }
                structured_data.append(record)

        # Create experiment summary
        unique_corpus_files = list(set(r['corpus_file'] for r in structured_data))
        
        data_summary = {
            'total_runs': len(analysis_results),
            'successful_runs': len(successful_runs),
            'unique_corpus_files': len(unique_corpus_files),
            'corpus_files': unique_corpus_files
        }

        prompt = f"""You are a computational social science researcher with expertise in statistical analysis. 

## EXPERIMENT SUMMARY
- Framework: {framework.get('display_name', 'Unknown')}
- Total runs: {data_summary['total_runs']}
- Successful runs: {data_summary['successful_runs']}
- Unique corpus files: {data_summary['unique_corpus_files']}

## REAL EXPERIMENTAL DATA
The following data represents the complete set of successful experimental runs. This is REAL data extracted from the workflow state.

```python
experimental_data = {str(structured_data)}
```

## CRITICAL INSTRUCTIONS
1. **Use ONLY the provided experimental_data** - do not simulate, generate, or create additional data points
2. **Load the data directly** into a pandas DataFrame using the provided list of dictionaries
3. **Perform statistical analysis** on the actual data you receive
4. **Report real computed statistics** - F-statistics, p-values, Cronbach's alpha values

## YOUR TASK
Write and execute Python code to:
1. Load the experimental_data into a pandas DataFrame
2. Perform ANOVA analysis to test for differences across corpus files
3. Calculate Cronbach's alpha for inter-run reliability
4. Report the actual computed statistical results

## EXPECTED RESULTS
Based on the nature of this data, you should expect:
- F-statistics in reasonable ranges (typically 1-10 for social science data)
- Some p-values > 0.05 (not all differences will be significant)
- Cronbach's alpha values in the 0.6-0.9 range for good reliability

Begin by loading the experimental_data into a DataFrame and performing the analysis."""

        return prompt

    def _generate_csv_results(self, workflow_state: Dict[str, Any], results_path: Path, filename: str) -> Path:
        """
        Generates a structured CSV file from the analysis results.
        """
        print("  - Generating structured CSV results...")
        csv_path = results_path / filename
        
        results_data = workflow_state.get('analysis_results', [])
        if not results_data:
            # Create an empty file to satisfy the return type and workflow expectations
            df = pd.DataFrame()
            df.to_csv(csv_path, index=False)
            print("  - No analysis results found. Generated empty CSV.")
            return csv_path
            
        # We need to flatten the nested JSON structure into a tabular format.
        # This is a classic data wrangling task.
        
        records = []
        for result in results_data:
            if not result.get('success'):
                continue

            json_output = result.get('json_output', {})

            base_info = {
                'agent_id': result.get('agent_id'),
                'model_name': result.get('model_name'),
                'corpus_file': Path(result.get('corpus_file')).name,
                'run_num': result.get('run_num'),
            }
            
            # Framework-agnostic: extract all data from the JSON output
            if isinstance(json_output, dict):
                for key, value in json_output.items():
                    if isinstance(value, dict):
                        # Handle nested dictionaries (e.g., scores, dimension_scores, emotion_metrics)
                        for nested_key, nested_value in value.items():
                            if isinstance(nested_value, (str, int, float, bool)):
                                base_info[f"{key}_{nested_key}"] = nested_value
                    elif isinstance(value, (str, int, float, bool)):
                        # Handle top-level values
                        base_info[key] = value
                    elif isinstance(value, list) and all(isinstance(item, str) for item in value):
                        # Handle string lists (e.g., evidence, themes)
                        base_info[key] = '; '.join(value)

            records.append(base_info)
            
        df = pd.DataFrame(records)
        df.to_csv(csv_path, index=False)
        
        return csv_path 