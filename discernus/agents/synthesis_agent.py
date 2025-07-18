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
        """Constructs an efficient prompt for statistical synthesis without exceeding token limits."""
        
        # Extracting key data from the workflow state
        experiment = workflow_state.get('experiment', {})
        framework = workflow_state.get('framework', {})
        results_data = workflow_state.get('analysis_results', [])

        # Summary of analysis
        num_successful_runs = sum(1 for r in results_data if r.get('success'))
        
        # Efficient data extraction - create structured summary instead of full JSON dump
        data_summary = {
            'total_runs': num_successful_runs,
            'unique_corpus_files': len(set(r.get('corpus_file', '') for r in results_data if r.get('success'))),
            'numeric_dimensions': [],
            'sample_data': []
        }
        
        # Extract numeric dimensions from first successful result
        first_successful = next((r for r in results_data if r.get('success')), {})
        if first_successful:
            json_output = first_successful.get('json_output', {})
            for key, value in json_output.items():
                if isinstance(value, (int, float)):
                    data_summary['numeric_dimensions'].append(key)
        
        # Create compact sample data (first 10 results only)
        for i, res in enumerate(results_data[:10]):
            if res.get('success'):
                json_output = res.get('json_output', {})
                sample_entry = {
                    'corpus_file': res.get('corpus_file', '').split('/')[-1],  # Just filename
                    'run_num': res.get('run_num'),
                    'numeric_data': {k: v for k, v in json_output.items() if isinstance(v, (int, float))}
                }
                data_summary['sample_data'].append(sample_entry)
        
        # Extract hypotheses for systematic testing
        hypotheses = experiment.get('hypotheses', {})
        hypothesis_text = ""
        if hypotheses:
            hypothesis_text = "### Experiment Hypotheses\n"
            for h_id, h_text in hypotheses.items():
                hypothesis_text += f"- **{h_id}**: {h_text}\n"
            hypothesis_text += "\n"

        # Building the efficient prompt
        prompt = f"""
You are an expert computational social science researcher with Python code execution capabilities. Generate a comprehensive statistical analysis report.

## Experiment Context
- **Name**: {experiment.get('name', 'N/A')}
- **Framework**: {framework.get('name', 'N/A')}
- **Successful Runs**: {num_successful_runs}
- **Models Used**: {', '.join(experiment.get('models', []))}

{hypothesis_text}

## Data Summary
- **Total Runs**: {data_summary['total_runs']}
- **Unique Corpus Files**: {data_summary['unique_corpus_files']}
- **Numeric Dimensions**: {data_summary['numeric_dimensions']}

## Sample Data (First 10 Results)
```json
{json.dumps(data_summary['sample_data'], indent=2)}
```

## ANALYSIS REQUIREMENTS

Write Python code to:

1. **Recreate the full dataset** from the provided structure
2. **Compute real statistics**: ANOVA, t-tests, reliability analysis (Cronbach's α), correlations
3. **Test hypotheses systematically** with appropriate statistical methods
4. **Generate professional tables** with statistical results

## CRITICAL INSTRUCTIONS

- Use actual Python libraries (pandas, numpy, scipy.stats, pingouin)
- Execute code to get real results, don't fabricate numbers
- Include statistical significance testing and effect sizes
- Format results in professional ASCII tables
- Provide academic-quality interpretation

## EFFICIENCY REQUIREMENTS

- Focus on essential statistical analysis
- Use tabular format for results presentation
- Keep code execution efficient
- Provide clear, concise academic conclusions

Generate the complete analysis with executed Python code and results.
"""
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