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
        
        # Get framework schema for framework-aware transformation
        framework_spec = workflow_state.get('framework', {})
        output_contract = framework_spec.get('output_contract', {})
        schema = output_contract.get('schema')
        
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
                extraction_result = self._extract_json_from_result(result, archive_manager, schema)
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

    def _extract_json_from_result(self, result: Dict[str, Any], archive_manager: Optional[LLMArchiveManager], framework_schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Extract clean JSON from a single analysis result using LLM-to-LLM communication.
        Enhanced with schema transformation to match framework output contracts.
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
                    # Transform hierarchical JSON to flat format if needed
                    transformed_json = self._transform_to_flat_schema(extracted_json, framework_schema)
                    
                    # Success! Create enriched result
                    enriched_result = result.copy()
                    enriched_result.update({
                        'success': True,
                        'error': None,
                        'json_output': transformed_json,
                        'extraction_attempts': attempt + 1
                    })
                    
                    # Save extracted JSON to individual file if archive manager available
                    if archive_manager:
                        self._save_extracted_json(archive_manager, result.get('agent_id', 'unknown'), transformed_json)
                    
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

    def _transform_to_flat_schema(self, hierarchical_json: Dict[str, Any], framework_schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Transform hierarchical JSON to flat schema format using LLM-to-LLM transformation.
        
        This THIN approach uses Gemini Flash to intelligently flatten any hierarchical JSON
        structure, making it framework-agnostic and compatible with any LLM provider.
        
        Instead of hardcoded patterns, we let the LLM understand the structure and
        flatten it appropriately, following THIN philosophy principles.
        """
        # Check if already reasonably flat - no transformation needed
        if self._is_reasonably_flat(hierarchical_json):
            return hierarchical_json
        
        # Use LLM-to-LLM transformation for complex hierarchical structures
        try:
            flattened_json = self._llm_flatten_json(hierarchical_json, framework_schema)
            return flattened_json if flattened_json else hierarchical_json
        except Exception as e:
            print(f"⚠️ LLM transformation failed: {e}")
            # Fallback to original if transformation fails
            return hierarchical_json
    
    def _llm_flatten_json(self, hierarchical_json: Dict[str, Any], framework_schema: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Use LLM to flatten hierarchical JSON structure in a framework-aware way.
        """
        # Import here to avoid circular imports
        from ..gateway.llm_gateway import LLMGateway
        from ..gateway.model_registry import get_model_registry
        
        # Create the flattening prompt (framework-aware if schema provided)
        prompt = self._create_json_flattening_prompt(hierarchical_json, framework_schema)
        
        # Use fast, cheap model for transformation
        model_registry = get_model_registry()
        llm_gateway = LLMGateway(model_registry)
        
        try:
            # Use Gemini Flash for fast, cheap transformation
            content, metadata = llm_gateway.execute_call(
                model="vertex_ai/gemini-2.5-flash",
                prompt=prompt,
                max_tokens=2000,
                temperature=0.0  # Deterministic transformation
            )
            
            if metadata.get("success") and content:
                # Debug: Show successful transformation
                print(f"✅ LLM transformation successful ({len(content)} chars)")
                
                # Clean the response - remove markdown code blocks
                clean_content = content.strip()
                if clean_content.startswith("```json"):
                    clean_content = clean_content[7:]  # Remove ```json
                if clean_content.startswith("```"):
                    clean_content = clean_content[3:]  # Remove ```
                if clean_content.endswith("```"):
                    clean_content = clean_content[:-3]  # Remove trailing ```
                clean_content = clean_content.strip()
                
                # Parse the JSON response
                import json
                try:
                    flattened = json.loads(clean_content)
                    return flattened if isinstance(flattened, dict) else None
                except json.JSONDecodeError as e:
                    print(f"⚠️ JSON parsing failed: {e}")
                    return None
            else:
                print(f"⚠️ LLM call failed or returned empty content")
                print(f"⚠️ Success: {metadata.get('success')}, Content length: {len(content) if content else 0}")
            
        except Exception as e:
            print(f"⚠️ LLM flattening call failed: {e}")
            
        return None
    
    def _create_json_flattening_prompt(self, hierarchical_json: Dict[str, Any], framework_schema: Optional[Dict[str, Any]] = None) -> str:
        """
        Create a framework-aware prompt for JSON flattening.
        """
        import json
        
        json_str = json.dumps(hierarchical_json, indent=2)
        
        # If framework schema is provided, use it to guide field naming
        if framework_schema:
            schema_fields = list(framework_schema.keys())
            schema_guidance = f"""
5. Use EXACT field names from the framework schema:
   - Required fields: {', '.join(schema_fields)}
   - Match field names exactly as specified in the schema
   - If the hierarchical JSON contains data for these fields, use the exact field names"""
        else:
            schema_guidance = """
5. Use STANDARD field naming for framework compatibility:
   - Anchor scores: tribal_dominance_score, individual_dignity_score, fear_score, hope_score, etc.
   - Confidence: tribal_dominance_confidence, individual_dignity_confidence, fear_confidence, hope_confidence, etc.
   - Evidence: tribal_dominance_evidence, individual_dignity_evidence, fear_evidence, hope_evidence, etc.
   - Other fields: envy_score, compersion_score, enmity_score, amity_score, fragmentative_goal_score, cohesive_goal_score"""
        
        return f"""You are a JSON transformation specialist. Your job is to flatten hierarchical JSON structures into a flat, analysis-ready format.

TASK: Transform the following hierarchical JSON into a flat structure suitable for data analysis.

RULES:
1. Convert nested paths to flat field names using underscores
2. Preserve all numeric values (scores, confidence, etc.) 
3. Preserve all text values (worldview, evidence, quotes, etc.)
4. Preserve all arrays (evidence lists, quotes, etc.){schema_guidance}
6. Remove unnecessary nesting but keep all meaningful data
7. Return ONLY valid JSON - no explanations or comments

INPUT JSON:
{json_str}

OUTPUT (flat JSON only):"""
    
    # THICK methods removed - replaced with LLM-to-LLM transformation
    
    def _is_reasonably_flat(self, data: Dict[str, Any]) -> bool:
        """Check if data structure is already reasonably flat and doesn't need transformation."""
        if not isinstance(data, dict):
            return True
            
        # Check if it has nested objects more than 2 levels deep
        max_depth = self._get_max_depth(data)
        return max_depth <= 2
    
    def _get_max_depth(self, data: Dict[str, Any], current_depth: int = 1) -> int:
        """Get maximum nesting depth of a dictionary."""
        if not isinstance(data, dict):
            return current_depth
            
        max_depth = current_depth
        for value in data.values():
            if isinstance(value, dict):
                depth = self._get_max_depth(value, current_depth + 1)
                max_depth = max(max_depth, depth)
                
        return max_depth

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