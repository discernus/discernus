#!/usr/bin/env python3
"""
Methodological Overwatch Agent
==============================

THIN Principle: This agent acts as an intelligent, automated quality control
checkpoint in the middle of an analysis pipeline. It reviews partial or
complete results and decides if the experiment is methodologically sound enough
to continue, preventing wasted resources on flawed analyses.
"""

import sys
from pathlib import Path
import json
from typing import Dict, Any, List
import re

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from discernus.gateway.llm_gateway import LLMGateway
    from discernus.gateway.model_registry import ModelRegistry
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"MethodologicalOverwatchAgent dependencies not available: {e}")
    DEPENDENCIES_AVAILABLE = False

class MethodologicalOverwatchAgent:
    """
    Reviews in-flight analysis results to decide whether to proceed or terminate.
    """

    def __init__(self):
        if not DEPENDENCIES_AVAILABLE:
            raise ImportError("Could not import required dependencies for MethodologicalOverwatchAgent")
        self.model_registry = ModelRegistry()
        self.gateway = LLMGateway(self.model_registry)

    def review_analysis_results(self, workflow_state: Dict[str, Any], step_config: Dict[str, Any]) -> Dict[str, str]:
        """
        Reviews a list of analysis results and decides whether to continue.
        """
        params = step_config.get('params', {})
        results_key = params.get('analysis_results_key', 'analysis_results')
        analysis_results = workflow_state.get(results_key, [])

        if not analysis_results:
            return {"decision": "TERMINATE", "reason": "No analysis results were provided to the overwatch agent."}

        # For efficiency, we'll only sample a few results if the collection is very long
        sample_size = 5
        if isinstance(analysis_results, dict):
            # Handle dictionary of results (keyed by filename or similar)
            results_items = list(analysis_results.items())
            results_sample = dict(results_items[:sample_size])
        elif isinstance(analysis_results, list):
            # Handle list of results
            results_sample = analysis_results[:sample_size]
        else:
            # Fallback for other types
            results_sample = analysis_results

        prompt = f"""
You are a "Methodological Overwatch" agent, an expert in computational social science with a mandate to prevent wasted resources. You have been activated at a mid-flight checkpoint to review the initial results of an analysis.

Your task is to determine if there are signs of systemic failure that justify terminating the experiment now, before more expensive synthesis and interpretation steps are run.

**Initial Analysis Results (Sample of {len(results_sample) if hasattr(results_sample, '__len__') else 'N/A'} out of {len(analysis_results) if hasattr(analysis_results, '__len__') else 'N/A'} total):**
---
{json.dumps(results_sample, indent=2)}
---

**Audit Checklist:**
1.  **Systemic Errors:** Are there a large number of exceptions or error messages in the results?
2.  **Low-Quality Output:** Do the `analysis_response` fields contain gibberish, nonsensical text, or content that is clearly off-topic from the analysis instructions?
3.  **Misaligned Scores:** If the responses are structured (e.g., JSON with scores), are the scores nonsensical (e.g., all zero, all the same, or outside the expected range)?
4.  **Framework Ignored:** Is there evidence that the analysis agents are consistently failing to follow the core instructions of the analytical framework?

**Your Decision:**
Based on your audit of this sample, should the process continue?
-   If the results look plausible enough to proceed, respond with `PROCEED`.
-   If you see strong evidence of a systemic, unrecoverable flaw, respond with `TERMINATE`.

**Respond with ONLY a JSON object containing two keys:**
1.  `"decision"`: Your one-word decision (`"PROCEED"` or `"TERMINATE"`).
2.  `"reason"`: A brief, single-sentence explanation for your decision.

Example response:
{{
  "decision": "TERMINATE",
  "reason": "The analysis agents are consistently failing to produce structured JSON output as required by the framework."
}}
"""
        
        model_name = self.model_registry.get_model_for_task('coordination')
        if not model_name:
            model_name = "anthropic/claude-3-haiku-20240307"

        try:
            response, _ = self.gateway.execute_call(model=model_name, prompt=prompt)
            if not response:
                return {"decision": "TERMINATE", "reason": "The Overwatch Agent's LLM returned an empty response."}

            # Clean up the response to ensure it's valid JSON
            json_response = response.strip()
            if json_response.startswith('```json'):
                match = re.search(r'```json\n(.*?)\n```', json_response, re.DOTALL)
                if match:
                    json_response = match.group(1)

            return json.loads(json_response)
        except (Exception, json.JSONDecodeError) as e:
            return {"decision": "TERMINATE", "reason": f"Overwatch Agent failed to get a valid decision from the LLM: {e}"} 