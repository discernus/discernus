#!/usr/bin/env python3
"""
Data Extraction Agent - THIN agent for tidying raw analysis data
================================================================

THIN Principle: This agent is a Hybrid Agent. It uses deterministic Python
for file I/O and orchestration, but it uses a specialized LLM call to perform
the intelligent, non-deterministic task of extracting structured JSON from
messy, conversational text. This avoids brittle parsing logic.
"""

import sys
import json
import csv
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
import asyncio

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from discernus.gateway.llm_gateway import LLMGateway
    from discernus.gateway.model_registry import ModelRegistry
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"DataExtractionAgent dependencies not available: {e}")
    DEPENDENCIES_AVAILABLE = False

class DataExtractionAgent:
    """
    Parses a conversation log to extract structured numerical data into a
    tidy CSV format, using an LLM to reliably extract JSON from text.
    """

    def __init__(self):
        if not DEPENDENCIES_AVAILABLE:
            raise ImportError("Could not import dependencies for DataExtractionAgent")
        self.model_registry = ModelRegistry()
        self.gateway = LLMGateway(self.model_registry)

    async def extract_tidy_data(self, workflow_state: Dict[str, Any], step_config: Dict[str, Any]):
        """
        Reads a JSONL conversation log, uses an LLM to extract analysis data, and writes a CSV.
        """
        session_results_path = workflow_state.get('session_results_path')
        if not session_results_path:
            raise ValueError("`session_results_path` not found in workflow_state.")

        # Construct paths from workflow state
        conversation_log_path = Path(session_results_path) / f"{workflow_state.get('conversation_id')}.jsonl"
        output_csv_path = Path(session_results_path) / "results.csv"
        framework_content = workflow_state.get('framework_content', '')

        if not conversation_log_path.exists():
            print(f"DataExtractionAgent: Conversation log not found at {conversation_log_path}. Skipping.")
            return

        print(f"DataExtractionAgent: Starting data extraction from {conversation_log_path}")

        records = []
        with open(conversation_log_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    log_entry = json.loads(line)
                    if not log_entry.get('speaker', '').startswith('analysis_agent'):
                        continue

                    message_content = log_entry.get('message', '')
                    
                    # Use an LLM to reliably extract the JSON
                    json_str = await self._extract_json_with_llm(message_content)
                    if not json_str:
                        continue
                        
                    analysis_data = json.loads(json_str)
                    
                    metadata = log_entry.get('metadata', {})
                    base_record = {
                        'session_id': metadata.get('session_id', 'unknown'),
                        'run_num': metadata.get('run_num', 1),
                        'model_name': metadata.get('model_name', 'unknown'),
                        'corpus_file': metadata.get('file_name', 'unknown'),
                    }

                    score_data = next((v for k, v in analysis_data.items() if 'scores' in k.lower()), None)
                    if not score_data:
                        continue

                    for anchor, values in score_data.items():
                        if isinstance(values, dict):
                            record = base_record.copy()
                            record['anchor'] = anchor
                            record['score'] = values.get('score')
                            record['classification'] = values.get('classification')
                            records.append(record)

                except (json.JSONDecodeError, AttributeError):
                    continue
        
        if not records:
            print("DataExtractionAgent: No valid analysis records found.")
            return

        headers = list(records[0].keys())
        
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(records)

        print(f"DataExtractionAgent: Successfully wrote {len(records)} records to {output_csv_path}")

    async def _extract_json_with_llm(self, text_with_json: str) -> Optional[str]:
        """Uses an LLM to extract a JSON object from a string."""
        prompt = f"""
You are an expert JSON extractor. Your sole task is to find and extract the valid JSON object embedded within the following text.
Respond with ONLY the raw, string-escaped JSON object and nothing else.

TEXT:
---
{text_with_json}
---

JSON:
"""
        model_name = self.model_registry.get_model_for_task('coordination')
        if not model_name:
            return None
            
        try:
            response, _ = self.gateway.execute_call(model=model_name, prompt=prompt)
            return response
        except Exception:
            return None

    def get_thin_compliance(self) -> Dict[str, Any]:
        """Returns THIN compliance information for this agent."""
        return {
            "thin_compliant": True,
            "archetype": "Hybrid",
            "description": "Uses a deterministic Python script for file I/O but uses a specialized LLM call for the non-deterministic task of extracting JSON from messy text.",
            "issues": []
        } 