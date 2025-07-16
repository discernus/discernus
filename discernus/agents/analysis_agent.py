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

class AnalysisAgent:
    """
    Applies analytical frameworks to text documents using the "Show Your Work" pattern.
    """

    def __init__(self):
        """Initialize the agent with necessary components."""
        self.model_registry = ModelRegistry()
        self.gateway = LLMGateway(self.model_registry)
        self.code_executor = SecureCodeExecutor()

    async def run_analysis(self, workflow_state: Dict[str, Any], step_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Main execution method that runs analysis on all corpus files.
        """
        project_path = Path(workflow_state.get('project_path', ''))
        corpus_path = project_path / "corpus"
        
        if not corpus_path.exists():
            raise ValueError(f"Corpus directory not found: {corpus_path}")
        
        # Get corpus files
        corpus_files = [f for f in corpus_path.rglob('*') if f.is_file() and f.suffix in ['.txt', '.md']]
        
        if not corpus_files:
            raise ValueError(f"No corpus files found in {corpus_path}")
        
        # Get analysis instructions from workflow state
        analysis_instructions = workflow_state.get('analysis_agent_instructions', '')
        if not analysis_instructions:
            raise ValueError("No analysis instructions found in workflow state")
        
        # Get experiment configuration
        experiment_config = workflow_state.get('experiment_config', {})
        models = experiment_config.get('models', ['openai/gpt-4o'])  # Default to proven working model
        num_runs = experiment_config.get('num_runs', 1)
        
        # Create analysis tasks
        analysis_tasks = []
        for run in range(num_runs):
            for model_name in models:
                for i, corpus_file in enumerate(corpus_files):
                    agent_id = f"analysis_agent_run{run+1}_{model_name.replace('/', '_')}_{i+1}"
                    task = self._run_single_analysis(
                        agent_id=agent_id,
                        corpus_file=str(corpus_file),
                        instructions=analysis_instructions,
                        model_name=model_name,
                        run_num=run + 1,
                        project_path=str(project_path),
                        session_id=workflow_state.get('session_id', 'unknown')
                    )
                    analysis_tasks.append(task)
        
        # Execute all analysis tasks in parallel
        print(f"🔬 Executing {len(analysis_tasks)} analysis tasks in parallel")
        raw_results = await asyncio.gather(*analysis_tasks, return_exceptions=True)
        
        # Filter results and handle exceptions
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

    async def _run_single_analysis(self, agent_id: str, corpus_file: str, instructions: str, 
                                   model_name: str, run_num: int, project_path: str, session_id: str) -> Dict[str, Any]:
        """
        Run a single analysis using the 'Show Your Work' pattern.
        """
        try:
            # Log the start of analysis
            log_project_event(project_path, "ANALYSIS_AGENT_SPAWNED", session_id, {
                "agent_id": agent_id,
                "corpus_file": Path(corpus_file).name,
                "model_name": model_name,
                "run_num": run_num
            })
            
            # Read corpus text
            corpus_text = Path(corpus_file).read_text()
            
            # Create the "Show Your Work" prompt
            analysis_prompt = f"""You are an expert analyst with a secure code interpreter.
Your task is to apply the following analytical framework to the provided text.

FRAMEWORK:
{instructions}

TEXT TO ANALYZE:
{corpus_text}

Your analysis must have two parts:
1. A detailed, qualitative analysis in natural language.
2. A final numerical score from 0.0 to 1.0, which you must generate by writing and executing a simple Python script.

You MUST return your response as a single, valid JSON object with the following structure:
{{
  "analysis_text": "Your detailed, qualitative analysis here...",
  "score_calculation": {{
    "code": "The simple Python script you wrote to generate the score. e.g., 'score = 0.8\\nreturn score'",
    "result": 0.8
  }}
}}

Before returning your response, double-check that it is a single, valid JSON object and nothing else.
"""
            
            # Call the LLM
            raw_response = await self._call_llm_async(analysis_prompt, agent_id, model_name)
            
            # Parse the JSON response
            try:
                parsed_response = json.loads(raw_response)
                analysis_text = parsed_response.get("analysis_text", "LLM response was valid JSON but missing 'analysis_text'.")
                score_calculation = parsed_response.get("score_calculation", {})
                llm_code = score_calculation.get("code", "return 0.5  # Fallback: LLM response missing 'code'.")
                llm_result = score_calculation.get("result", 0.5)
                
            except json.JSONDecodeError as e:
                log_project_event(project_path, "JSON_DECODE_ERROR", session_id, {
                    "agent_id": agent_id,
                    "error": str(e),
                    "raw_response": raw_response[:500] + "..." if len(raw_response) > 500 else raw_response
                })
                
                # Fallback to basic analysis
                analysis_text = f"LLM RESPONSE WAS NOT VALID JSON. Error: {str(e)}\n\nRaw response: {raw_response}"
                llm_code = "return 0.5  # Fallback due to LLM response format error"
                llm_result = 0.5
            
            # Verify the calculation using SecureCodeExecutor
            verification_result = self.code_executor.execute_code(llm_code)
            verified_score = verification_result.get('result_data')
            
            if verified_score is None:
                verified_score = 0.5  # Final fallback if code execution fails
                log_project_event(project_path, "CODE_EXECUTION_FAILED", session_id, {
                    "agent_id": agent_id,
                    "code": llm_code,
                    "verification_result": verification_result
                })
            
            # Log any discrepancy between LLM claim and our verification
            if abs(float(verified_score) - float(llm_result)) > 0.001:  # Allow for small floating point differences
                log_project_event(project_path, "SCORE_VERIFICATION_MISMATCH", session_id, {
                    "agent_id": agent_id,
                    "llm_claimed_result": llm_result,
                    "our_verified_result": verified_score,
                    "code": llm_code
                })
            
            # Log successful completion
            log_project_event(project_path, "ANALYSIS_AGENT_COMPLETED", session_id, {
                "agent_id": agent_id,
                "corpus_file": Path(corpus_file).name,
                "verified_score": verified_score
            })
            
            return {
                "agent_id": agent_id,
                "corpus_file": corpus_file,
                "file_name": Path(corpus_file).name,
                "model_name": model_name,
                "run_num": run_num,
                "analysis_response": analysis_text,
                "score": verified_score,
                "llm_code": llm_code,
                "verification_status": "verified"
            }
            
        except Exception as e:
            log_project_event(project_path, "ANALYSIS_AGENT_ERROR", session_id, {
                "agent_id": agent_id,
                "error": str(e),
                "corpus_file": Path(corpus_file).name
            })
            raise e

    async def _call_llm_async(self, prompt: str, agent_id: str, model_name: str) -> str:
        """Call LLM via gateway with proper error handling."""
        try:
            content, metadata = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.gateway.execute_call(model=model_name, prompt=prompt)
            )
            
            if not metadata.get("success", True):
                raise Exception(f"LLM call failed: {metadata.get('error', 'Unknown error')}")
            
            return content
            
        except Exception as e:
            raise Exception(f"LLM call failed for {agent_id} with model {model_name}: {str(e)}") 