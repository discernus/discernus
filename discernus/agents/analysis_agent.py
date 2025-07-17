#!/usr/bin/env python3
"""
Analysis Agent - Framework-Based Text Analysis with "Show Your Work" Pattern
============================================================================

THIN Principle: This agent applies analytical frameworks to text documents,
using the "Show Your Work" pattern to extract verifiable numerical scores.
The agent prompts the LLM to return both qualitative analysis and code-generated
scores, then uses SecureCodeExecutor to verify the calculation.
"""

import sys
import json
import re # Add re import
import asyncio
from pathlib import Path
from typing import Dict, Any, List

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from discernus.gateway.llm_gateway import LLMGateway
from discernus.core.project_chronolog import log_project_event
import yaml # Add yaml import

class AnalysisAgent:
    """
    Executes a framework-defined analysis prompt against corpus files.
    This agent is a "dumb" executor. All intelligence resides in the
    framework's analysis prompt and the experiment's configuration.
    """

    def __init__(self, gateway: LLMGateway):
        """Initialize the agent with necessary components."""
        self.gateway = gateway
        print("✅ AnalysisAgent initialized")

    def execute(self, workflow_state: Dict[str, Any], step_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution method that runs analysis on all corpus files based on the
        workflow state.
        """
        print("🔬 Running AnalysisAgent...")
        
        project_path = Path(workflow_state.get('project_path', ''))
        corpus_path = Path(workflow_state.get('corpus_path', ''))
        
        corpus_files = [f for f in corpus_path.rglob('*') if f.is_file() and f.suffix in ['.txt', '.md']]
        
        if not corpus_files:
            raise ValueError(f"No corpus files found in {corpus_path}")

        experiment_config = workflow_state.get('experiment', {})
        analysis_prompt_template = workflow_state.get('analysis_agent_instructions', '')

        if not analysis_prompt_template:
            raise ValueError("AnalysisAgent requires 'analysis_agent_instructions' in the workflow_state.")
            
        models = experiment_config.get('models', [])
        num_runs = experiment_config.get('num_runs', 1)
        
        if not models:
            raise ValueError("Experiment config must specify at least one model.")

        all_results = []
        for run_num in range(1, num_runs + 1):
            for model_name in models:
                for corpus_file in corpus_files:
                    agent_id = f"analysis_agent_run{run_num}_{model_name.replace('/', '_')}_{corpus_file.stem}"
                    
                    try:
                        result = self._run_single_analysis(
                            agent_id=agent_id,
                            corpus_file_path=corpus_file,
                            prompt_template=analysis_prompt_template,
                            model_name=model_name,
                            run_num=run_num,
                            project_path=project_path,
                            session_id=workflow_state.get('session_id', 'unknown')
                        )
                        all_results.append(result)
                    except Exception as e:
                        print(f"❌ Analysis task failed for {agent_id}: {e}")
                        # Optionally log the failure or append an error structure to results
                        all_results.append({
                            "agent_id": agent_id,
                            "corpus_file": str(corpus_file),
                            "model_name": model_name,
                            "run_num": run_num,
                            "success": False,
                            "error": str(e)
                        })

        successful_count = sum(1 for r in all_results if r.get('success', True))
        print(f"✅ AnalysisAgent complete. {successful_count} successful, {len(all_results) - successful_count} failed.")
        
        return {"analysis_results": all_results}

    def _run_single_analysis(self, agent_id: str, corpus_file_path: Path, 
                                   prompt_template: str, model_name: str, run_num: int, 
                                   project_path: Path, session_id: str) -> Dict[str, Any]:
        """
        Runs a single analysis by populating the prompt template and validating the response.
        """
        log_project_event(str(project_path), "ANALYSIS_AGENT_SPAWNED", session_id, {
            "agent_id": agent_id,
            "corpus_file": corpus_file_path.name,
            "model_name": model_name,
            "run_num": run_num
        })
        
        corpus_text = corpus_file_path.read_text(encoding='utf-8')
        
        # Populate the prompt template
        final_prompt = prompt_template.format(
            corpus_text=corpus_text,
            file_name=corpus_file_path.name
        )
        
        # Call the LLM synchronously
        content, metadata = self.gateway.execute_call(
            model=model_name,
            prompt=final_prompt,
            system_prompt="You are a framework analysis specialist."
        )

        if not metadata.get("success"):
            raise Exception(f"LLM Gateway returned an error: {metadata.get('error', 'Unknown error')}")

        # --- Post-processing: Strict JSON validation ---
        try:
            # The raw response from the LLM should be a JSON string
            parsed_json = json.loads(content)
        except json.JSONDecodeError as e:
            error_msg = f"LLM response was not valid JSON. Error: {e}\nRaw response: {content[:500]}"
            log_project_event(str(project_path), "JSON_DECODE_ERROR", session_id, {"agent_id": agent_id, "error": error_msg})
            raise ValueError(error_msg)

        # Log successful completion and return the result object
        log_project_event(str(project_path), "ANALYSIS_AGENT_COMPLETED", session_id, {
            "agent_id": agent_id,
            "corpus_file": corpus_file_path.name
        })
        
        return {
            "agent_id": agent_id,
            "corpus_file": str(corpus_file_path),
            "model_name": model_name,
            "run_num": run_num,
            "success": True,
            "json_output": parsed_json,
            "llm_metadata": metadata
        } 