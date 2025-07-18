#!/usr/bin/env python3
"""
Data Extraction Agent - LLM-Assisted JSON Extraction
====================================================

THIN Principle: This agent uses LLM-to-LLM communication to extract clean JSON
from raw analysis responses. It leverages the LLMArchiveManager for accessing
archived responses and uses Gemini 2.5 Flash for fast, reliable extraction.

Key Features:
- Works with LLMArchiveManager archived responses
- Uses Gemini 2.5 Flash for JSON extraction (cost-effective)
- Proper retry logic with exponential backoff
- Graceful degradation on extraction failures
- Individual file processing (no monolithic blobs)
"""

import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
import json
import time

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from discernus.gateway.llm_gateway import LLMGateway
from discernus.core.llm_archive_manager import LLMArchiveManager

class DataExtractionAgent:
    """
    Uses LLM-to-LLM communication to extract clean JSON from raw analysis responses.
    Works with LLMArchiveManager for accessing archived responses and uses Gemini 2.5 Flash
    for fast, reliable extraction with proper retry logic.
    """

    def __init__(self, gateway: LLMGateway):
        """Initialize the agent with the LLM gateway."""
        self.gateway = gateway
        self.extraction_model = "vertex_ai/gemini-2.5-flash"  # Cost-effective "house LLM"
        self.max_retries = 3
        print("✅ DataExtractionAgent initialized")

    def execute(self, workflow_state: Dict[str, Any], step_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution method that extracts clean JSON from archived analysis responses.
        """
        print("🧹 Running DataExtractionAgent...")
        
        # Get analysis results - handle both dict and list formats
        raw_results = workflow_state.get('analysis_results', {})
        
        # Convert dict format to list format for processing
        if isinstance(raw_results, dict):
            results_list = list(raw_results.values())
        elif isinstance(raw_results, list):
            results_list = raw_results
        else:
            print("⚠️ No analysis results found to extract data from.")
            return {"extracted_results": []}

        if not results_list:
            print("⚠️ No analysis results found to extract data from.")
            return {"extracted_results": []}

        # Try to get archive manager from session path
        session_path = workflow_state.get('session_results_path')
        archive_manager = None
        if session_path:
            archive_manager = LLMArchiveManager(Path(session_path))

        extracted_results = []
        extraction_log = []
        
        for result in results_list:
            try:
                extraction_result = self._extract_json_from_result(result, archive_manager)
                extracted_results.append(extraction_result)
                extraction_log.append({
                    'agent_id': result.get('agent_id', 'unknown'),
                    'success': extraction_result.get('success', False),
                    'error': extraction_result.get('error')
                })
                
            except Exception as e:
                print(f"❌ Critical error processing result {result.get('agent_id', 'unknown')}: {e}")
                # Add failed result to maintain data integrity
                if isinstance(result, dict):
                    failed_result: Dict[str, Any] = result.copy()
                else:
                    failed_result: Dict[str, Any] = {'raw_data': str(result)}
                
                failed_result['success'] = False
                failed_result['error'] = f"Critical processing error: {e}"
                failed_result['json_output'] = None
                extracted_results.append(failed_result)
                extraction_log.append({
                    'agent_id': result.get('agent_id', 'unknown'),
                    'success': False,
                    'error': str(e)
                })

        # Calculate success statistics
        successful_count = sum(1 for r in extracted_results if r.get('success'))
        failed_count = len(extracted_results) - successful_count
        
        print(f"✅ DataExtractionAgent complete. {successful_count} successful, {failed_count} failed.")

        # Save extraction log if archive manager available
        if archive_manager and session_path:
            try:
                extraction_log_path = Path(session_path) / "extracted" / "extraction_log.jsonl"
                extraction_log_path.parent.mkdir(exist_ok=True)
                with open(extraction_log_path, 'w', encoding='utf-8') as f:
                    for log_entry in extraction_log:
                        f.write(json.dumps(log_entry) + '\n')
                print(f"✅ Extraction log saved to {extraction_log_path}")
            except Exception as e:
                print(f"⚠️ Failed to save extraction log: {e}")

        return {
            "analysis_results": extracted_results,
            "extraction_statistics": {
                "successful_count": successful_count,
                "failed_count": failed_count,
                "success_rate": successful_count / len(extracted_results) if extracted_results else 0
            }
        }

    def _extract_json_from_result(self, result: Dict[str, Any], archive_manager: Optional[LLMArchiveManager]) -> Dict[str, Any]:
        """
        Extract clean JSON from a single analysis result using LLM-to-LLM communication.
        """
        # Get the raw response text
        raw_response = result.get("content", "") or result.get("raw_response", "") or str(result)
        
        if not raw_response or len(raw_response.strip()) == 0:
            return self._create_failed_result(result, "No raw response content to extract from")

        # Try JSON extraction with retry logic
        for attempt in range(self.max_retries):
            try:
                extracted_json = self._llm_extract_json(raw_response, attempt)
                
                if extracted_json:
                    # Success! Create enriched result
                    enriched_result = result.copy()
                    enriched_result.update({
                        'success': True,
                        'error': None,
                        'json_output': extracted_json,
                        'extraction_attempts': attempt + 1
                    })
                    
                    # Save extracted JSON to individual file if archive manager available
                    if archive_manager:
                        self._save_extracted_json(archive_manager, result.get('agent_id', 'unknown'), extracted_json)
                    
                    return enriched_result
                    
            except Exception as e:
                if attempt == self.max_retries - 1:
                    # Final attempt failed
                    return self._create_failed_result(result, f"All {self.max_retries} extraction attempts failed. Last error: {e}")
                else:
                    # Retry with exponential backoff
                    wait_time = (2 ** attempt) * 0.1  # 0.1s, 0.2s, 0.4s
                    time.sleep(wait_time)
                    continue
        
        return self._create_failed_result(result, "Extraction failed after all retries")

    def _llm_extract_json(self, raw_response: str, attempt: int) -> Optional[Dict[str, Any]]:
        """
        Use Gemini 2.5 Flash to extract clean JSON from raw response.
        """
        extraction_prompt = self._get_extraction_prompt(attempt).format(faulty_response=raw_response)
        
        system_prompt = """You are a JSON extraction specialist. Your task is to find and extract valid JSON objects from messy text.

CRITICAL REQUIREMENTS:
1. Return ONLY a valid JSON object - no explanations, no markdown, no extra text
2. If you find multiple JSON objects, return the most complete one
3. If no valid JSON exists, return an empty object: {}
4. Preserve all original field names and structure
5. Handle common JSON errors (missing quotes, trailing commas, etc.)"""

        content, metadata = self.gateway.execute_call(
            model=self.extraction_model,
            prompt=extraction_prompt,
            system_prompt=system_prompt
        )

        if not metadata.get("success"):
            raise ValueError(f"LLM extraction call failed: {metadata.get('error')}")

        # Parse the extracted JSON
        try:
            cleaned_content = content.strip()
            # Remove any markdown code fences if present
            if cleaned_content.startswith('```'):
                lines = cleaned_content.split('\n')
                cleaned_content = '\n'.join(lines[1:-1])
            
            extracted_json = json.loads(cleaned_content)
            
            # Validate it's not empty
            if not extracted_json or (isinstance(extracted_json, dict) and len(extracted_json) == 0):
                return None
                
            return extracted_json
            
        except json.JSONDecodeError as e:
            raise ValueError(f"LLM returned invalid JSON: {e}")

    def _create_failed_result(self, result: Dict[str, Any], error_message: str) -> Dict[str, Any]:
        """Create a failed extraction result with error details."""
        failed_result = result.copy()
        failed_result.update({
            'success': False,
            'error': error_message,
            'json_output': None
        })
        return failed_result

    def _save_extracted_json(self, archive_manager: LLMArchiveManager, agent_id: str, extracted_json: Dict[str, Any]):
        """Save extracted JSON to individual file."""
        try:
            session_path = archive_manager.session_path
            extracted_path = session_path / "extracted"
            extracted_path.mkdir(exist_ok=True)
            
            # Use a sanitized filename
            safe_agent_id = agent_id.replace('/', '_').replace('\\', '_')
            json_file = extracted_path / f"{safe_agent_id}.json"
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(extracted_json, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"⚠️ Failed to save extracted JSON for {agent_id}: {e}")

    def _get_extraction_prompt(self, attempt: int = 0) -> str:
        """
        Get the LLM extraction prompt, with variations for retry attempts.
        """
        if attempt == 0:
            return """The following text contains a JSON object but it may be surrounded by explanations, markdown formatting, or other text. Extract ONLY the JSON object.

FAULTY RESPONSE:
{faulty_response}

Return the clean JSON object with no additional text or formatting."""

        elif attempt == 1:
            return """I need you to find and extract a valid JSON object from this messy text. The JSON might be wrapped in markdown code blocks, have extra explanations, or contain formatting errors.

MESSY TEXT:
{faulty_response}

Please extract and return ONLY the JSON object. Fix any obvious JSON syntax errors like missing quotes or trailing commas."""

        else:
            return """This is my final attempt to extract JSON from this text. Please be very careful and thorough.

The text below should contain a JSON object but it might be badly formatted or mixed with other content. Extract the JSON and fix any syntax errors.

PROBLEMATIC TEXT:
{faulty_response}

Return a valid JSON object. If you cannot find any JSON structure, return an empty object: {{}}"""