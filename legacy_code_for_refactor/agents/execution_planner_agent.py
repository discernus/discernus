#!/usr/bin/env python3
"""
Execution Planner Agent
=======================

THIN Principle: This agent is the master planner or "Engine Control Unit" (ECU)
for the entire analysis pipeline. It takes the researcher's high-level goals
and converts them into a detailed, optimized, machine-readable execution plan.
It handles all complex resource management thinking (cost, time, rate limits,
batching) *before* the main orchestrator runs, allowing the orchestrator to be
a simple, mechanical executor.
"""

import sys
from pathlib import Path
import json
import math
from typing import Dict, Any, List, Union

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from discernus.gateway.llm_gateway import LLMGateway
    from discernus.gateway.model_registry import ModelRegistry
    import tiktoken
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"ExecutionPlannerAgent dependencies not available: {e}")
    DEPENDENCIES_AVAILABLE = False

class ExecutionPlannerAgent:
    """
    Designs a complete, optimized execution plan for an experiment.
    """

    def __init__(self):
        if not DEPENDENCIES_AVAILABLE:
            raise ImportError("Could not import required dependencies for ExecutionPlannerAgent")
        self.model_registry = ModelRegistry()
        self.gateway = LLMGateway(self.model_registry)
        try:
            self.tokenizer = tiktoken.get_encoding("cl100k_base")
        except:
            self.tokenizer = None

    def create_execution_plan(self, corpus_files: List[str], model_names: List[str], framework_text: str, analysis_instructions: str) -> List[Dict[str, Any]]:
        """
        Generates a comprehensive execution plan including cost/time estimates
        and a detailed run schedule.
        """
        if not self.tokenizer:
            print("Error: Tokenizer not available, cannot create plan.")
            return []

        framework_tokens = len(self.tokenizer.encode(framework_text))
        instruction_tokens = len(self.tokenizer.encode(analysis_instructions))
        
        total_estimated_cost = 0
        total_estimated_duration_seconds = 0
        run_schedule = []

        for model_name in model_names:
            model_details = self.model_registry.get_model_details(model_name)
            if not model_details:
                continue

            batch_size = model_details.get('optimal_batch_size', 1)
            rpm = model_details.get('rpm', 60)
            cost_input = model_details.get('costs', {}).get('input_per_million_tokens', 0)
            cost_output = model_details.get('costs', {}).get('output_per_million_tokens', 0)
            
            # Create batches of files
            file_batches = [corpus_files[i:i + batch_size] for i in range(0, len(corpus_files), batch_size)]
            
            delay_per_request = 60.0 / rpm if rpm > 0 else 0

            for i, batch in enumerate(file_batches):
                # 1. Estimate tokens and cost for this batch
                batch_files_content = {Path(f).name: Path(f).read_text() for f in batch}
                batch_content_str = json.dumps(batch_files_content)
                batch_tokens = len(self.tokenizer.encode(batch_content_str))
                
                input_tokens = framework_tokens + instruction_tokens + batch_tokens
                
                # Use an LLM to estimate the output tokens
                # For now, we'll use a simple heuristic: 500 tokens per file in the batch
                output_tokens_estimation = 500 * len(batch)

                total_estimated_cost += ((input_tokens / 1_000_000) * cost_input) + ((output_tokens_estimation / 1_000_000) * cost_output)

                # 2. Add to total duration
                total_estimated_duration_seconds += delay_per_request

                # 3. Add to the detailed run schedule
                agent_id = f"batch_{i+1}_{model_name.replace('/', '_')}"
                
                prompt = self._create_batch_prompt(framework_text, analysis_instructions, batch_files_content, agent_id)

                run_schedule.append({
                    "agent_id": agent_id,
                    "model": model_name,
                    "prompt": prompt,
                    "file_batch": [Path(f).name for f in batch],
                    "estimated_input_tokens": input_tokens,
                    "delay_after_seconds": delay_per_request
                })

        return run_schedule

    def _create_batch_prompt(self, framework_text: str, instructions: str, files_content: Dict[str, str], agent_id: str) -> str:
        """
        Creates the prompt for a batch of files, with instructions at the end
        to mitigate context fatigue, based on recent research.
        """
        
        file_block = "\n\n---\n\n".join([f"File: {name}\n\n{content}" for name, content in files_content.items()])

        # Structured prompt with instructions at the end for better model focus.
        return f"""You are {agent_id}, a framework analysis specialist.

Below you will find a framework specification and a batch of texts to analyze. Your task is to apply the framework to EACH text individually and provide a separate, complete analysis for each one as a single response.

[FRAMEWORK SPECIFICATION]
---
{framework_text}
---
[/FRAMEWORK SPECIFICATION]

[TEXTS TO ANALYZE]
---
{file_block}
---
[/TEXTS TO ANALYZE]

[ANALYSIS TASK]
---
TASK: Based on the framework and instructions provided above, apply the framework systematically to EACH of the {len(files_content)} texts in the batch. For each text, provide a distinct, structured output as required by the framework. Ensure your response clearly separates the analysis for each file.

ANALYSIS INSTRUCTIONS:
{instructions}
---
[/ANALYSIS TASK]
""" 