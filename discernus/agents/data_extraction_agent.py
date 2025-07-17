#!/usr/bin/env python3
"""
Data Extraction Agent
=====================

THIN Principle: This agent is a specialized "parser" that uses an LLM to
extract structured JSON from unstructured, messy text. It follows the
"Capture Raw, Process Later" pattern, ensuring that the initial, expensive
analysis phase is not blocked by formatting errors.
"""

import sys
from pathlib import Path
from typing import Dict, Any, List
import json

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from discernus.gateway.llm_gateway import LLMGateway

class DataExtractionAgent:
    """
    Takes a list of raw text responses from the AnalysisAgent and uses an
    LLM to extract the clean, valid JSON from each one.
    """

    def __init__(self, gateway: LLMGateway):
        """Initialize the agent with the LLM gateway."""
        self.gateway = gateway
        print("✅ DataExtractionAgent initialized")

    def execute(self, workflow_state: Dict[str, Any], step_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution method that iterates through raw analysis results and
        extracts clean JSON.
        """
        print("🧹 Running DataExtractionAgent...")
        
        raw_results = workflow_state.get('analysis_results', [])
        if not raw_results:
            print("⚠️ No analysis results found to extract data from.")
            return {"extracted_results": []}

        extraction_prompt_template = self._get_extraction_prompt()
        
        cleaned_results = []
        for result in raw_results:
            # THIN: Just pass whatever we get to the LLM - let it figure it out
            if isinstance(result, dict):
                raw_response = result.get("content", "") or result.get("raw_response", "") or str(result)
            else:
                raw_response = str(result)
            
            if not raw_response:
                # If there's nothing to extract, just carry forward the result
                cleaned_results.append(result)
                continue

            final_prompt = extraction_prompt_template.format(faulty_response=raw_response)

            try:
                # Use a powerful model for the critical extraction task
                extraction_model = "openai/gpt-4o"
                
                content, metadata = self.gateway.execute_call(
                    model=extraction_model,
                    prompt=final_prompt,
                    system_prompt="You are a JSON formatting expert. Your only task is to extract and return a valid JSON object from the provided text."
                )

                if not metadata.get("success"):
                    raise ValueError(f"Extraction LLM call failed: {metadata.get('error')}")

                parsed_json = json.loads(content)

                # Update the original result with the cleaned data
                result["json_output"] = parsed_json
                result["success"] = True # Mark as successful after extraction
                result.pop("raw_response", None) # Remove the raw response
                result.pop("error", None) # Remove any previous error
                cleaned_results.append(result)

            except (json.JSONDecodeError, ValueError) as e:
                print(f"❌ Data extraction failed for agent {result.get('agent_id')}: {e}")
                result["success"] = False
                result["error"] = f"Final extraction attempt failed: {e}"
                cleaned_results.append(result)
        
        successful_count = sum(1 for r in cleaned_results if r.get('success'))
        print(f"✅ DataExtractionAgent complete. {successful_count} successful, {len(cleaned_results) - successful_count} failed.")

        return {"analysis_results": cleaned_results}

    def _get_extraction_prompt(self) -> str:
        """
        Returns the prompt used to instruct the LLM to fix a faulty JSON response.
        """
        return (
            "The following is a response that contains a valid JSON object, but it is surrounded by other text, explanations, and markdown code fences. "
            "Your task is to extract and return ONLY the JSON object.\n\n"
            "IMPORTANT: Your response MUST be a single, valid JSON object and nothing else. Do not include any text, explanations, or markdown code fences before or after the JSON object.\n\n"
            "--- FAULTY RESPONSE ---\n"
            "{faulty_response}\n"
            "--- END FAULTY RESPONSE ---"
        ) 