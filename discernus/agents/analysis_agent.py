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

from discernus.gateway.model_registry import ModelRegistry
from discernus.gateway.llm_gateway import LLMGateway
from discernus.core.secure_code_executor import SecureCodeExecutor
from discernus.core.conversation_logger import ConversationLogger
from discernus.core.project_chronolog import log_project_event
import yaml # Add yaml import

class AnalysisAgent:
    """
    Executes a framework-defined analysis prompt against corpus files.
    This agent is a "dumb" executor. All intelligence resides in the
    framework's YAML configuration block.
    """

    def __init__(self):
        """Initialize the agent with necessary components."""
        self.model_registry = ModelRegistry()
        self.gateway = LLMGateway(self.model_registry)

    def _extract_config_from_framework(self, framework_text: str) -> Dict[str, Any]:
        """Parses the framework markdown to find the embedded YAML config."""
        match = re.search(r'# --- Discernus Configuration ---\n```yaml\n(.*?)\n```', framework_text, re.DOTALL)
        if not match:
            raise ValueError("Framework file is missing the '# --- Discernus Configuration ---' YAML block.")
        
        try:
            return yaml.safe_load(match.group(1))
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing framework YAML: {e}")

    async def run_analysis(self, workflow_state: Dict[str, Any], step_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Main execution method that runs analysis on all corpus files based on the
        framework's embedded YAML configuration.
        """
        project_path = Path(workflow_state.get('project_path', ''))
        corpus_path = project_path / "corpus"
        framework_path = project_path / "framework.md"
        
        if not corpus_path.exists():
            raise ValueError(f"Corpus directory not found: {corpus_path}")
        if not framework_path.exists():
            raise ValueError(f"Framework file not found: {framework_path}")
        
        framework_text = framework_path.read_text()
        framework_config = self._extract_config_from_framework(framework_text)
        
        corpus_files = [f for f in corpus_path.rglob('*') if f.is_file() and f.suffix in ['.txt', '.md']]
        
        if not corpus_files:
            raise ValueError(f"No corpus files found in {corpus_path}")
        
        experiment_config = workflow_state.get('experiment_config', {})
        analysis_variant_name = experiment_config.get('analysis_variant', 'default')
        analysis_variant = framework_config.get('analysis_variants', {}).get(analysis_variant_name)

        if not analysis_variant:
            raise ValueError(f"Analysis variant '{analysis_variant_name}' not found in framework configuration.")
        
        analysis_prompt_template = analysis_variant.get('analysis_prompt')
        if not analysis_prompt_template:
            raise ValueError(f"Variant '{analysis_variant_name}' is missing the 'analysis_prompt'.")
            
        models = experiment_config.get('models', ['openai/gpt-4o'])
        num_runs = experiment_config.get('num_runs', 1)
        
        analysis_tasks = []
        for run in range(num_runs):
            for model_name in models:
                for i, corpus_file in enumerate(corpus_files):
                    agent_id = f"analysis_agent_run{run+1}_{model_name.replace('/', '_')}_{i+1}"
                    task = self._run_single_analysis(
                        agent_id=agent_id,
                        corpus_file_path=str(corpus_file),
                        framework_text=framework_text,
                        prompt_template=analysis_prompt_template,
                        model_name=model_name,
                        run_num=run + 1,
                        project_path=str(project_path),
                        session_id=workflow_state.get('session_id', 'unknown'),
                        framework_config=framework_config
                    )
                    analysis_tasks.append(task)
        
        print(f"🔬 Executing {len(analysis_tasks)} analysis tasks in parallel")
        raw_results = await asyncio.gather(*analysis_tasks, return_exceptions=True)
        
        successful_results = []
        failed_count = 0
        
        for result in raw_results:
            if isinstance(result, Exception):
                failed_count += 1
                print(f"❌ Analysis task failed: {result}")
            elif isinstance(result, dict):
                successful_results.append(result)
        
        print(f"✅ Analysis complete. {len(successful_results)} successful, {failed_count} failed.")
        
        if failed_count > 0 and len(successful_results) == 0:
            raise ValueError(f"All analysis tasks failed. No results to process.")
        
        return successful_results

    async def _run_single_analysis(self, agent_id: str, corpus_file_path: str, framework_text: str, 
                                   prompt_template: str, model_name: str, run_num: int, 
                                   project_path: str, session_id: str, framework_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs a single analysis by populating the prompt template and validating the response.
        """
        try:
            log_project_event(project_path, "ANALYSIS_AGENT_SPAWNED", session_id, {
                "agent_id": agent_id,
                "corpus_file": Path(corpus_file_path).name,
                "model_name": model_name,
                "run_num": run_num
            })
            
            corpus_text = Path(corpus_file_path).read_text()
            
            # Populate the prompt template
            final_prompt = prompt_template.format(
                framework_text=framework_text,
                corpus_text=corpus_text,
                domain=framework_config.get('display_name', 'analysis') # Example of another variable
            )
            
            # Call the LLM
            raw_response = await self._call_llm_async(final_prompt, agent_id, model_name)

            # --- Post-processing: Strict JSON validation, no fallbacks ---
            try:
                parsed_response = json.loads(raw_response)
                
                # Basic validation, can be enhanced by reading schema from framework
                if not isinstance(parsed_response, dict) or ("scores" not in parsed_response and "summary" not in parsed_response):
                    raise ValueError("LLM response is valid JSON but does not match the required structure.")

            except json.JSONDecodeError as e:
                error_msg = f"LLM response was not valid JSON. Error: {e}\nRaw response: {raw_response[:500]}"
                log_project_event(project_path, "JSON_DECODE_ERROR", session_id, {"agent_id": agent_id, "error": error_msg})
                raise ValueError(error_msg)

            # Log successful completion and return the full, rich JSON object
            log_project_event(project_path, "ANALYSIS_AGENT_COMPLETED", session_id, {
                "agent_id": agent_id,
                "corpus_file": Path(corpus_file_path).name
            })
            
            # Add metadata to the results
            parsed_response['agent_metadata'] = {
                "agent_id": agent_id,
                "corpus_file": corpus_file_path,
                "file_name": Path(corpus_file_path).name,
                "model_name": model_name,
                "run_num": run_num
            }
            return parsed_response
            
        except Exception as e:
            log_project_event(project_path, "ANALYSIS_AGENT_ERROR", session_id, {
                "agent_id": agent_id,
                "error": str(e),
                "corpus_file": Path(corpus_file_path).name
            })
            raise e

    async def _call_llm_async(self, prompt: str, agent_id: str, model_name: str) -> str:
        """Call LLM via gateway with proper error handling."""
        # This method remains largely the same, but logging is now even more critical
        try:
            content, metadata = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.gateway.execute_call(model=model_name, prompt=prompt)
            )
            
            if not metadata.get("success", True):
                raise Exception(f"LLM Gateway returned an error: {metadata.get('error', 'Unknown error')}")
            
            return content
            
        except Exception as e:
            # Re-raise the exception to be caught by the calling function
            raise Exception(f"LLM call failed for {agent_id} with model {model_name}: {str(e)}") 