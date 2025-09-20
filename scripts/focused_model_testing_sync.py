#!/usr/bin/env python3
"""
Focused Model Testing Harness (Synchronous)
===========================================

This script is a simplified, synchronous version for testing the Analysis Agent's
scoring models. It allows for direct interaction with the LLM gateway to test
different prompts and models without running the full experiment pipeline.

Purpose:
- Isolate and measure scoring variance from the LLM.
- Test the stability of the 3-shot median aggregation prompt.
- Compare the performance of different models (Pro vs. Flash).
- Evaluate the impact of prompt modifications on scoring consistency.

Usage:
    python3 scripts/focused_model_testing_sync.py
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime, timezone
import yaml

# Ensure the script can find the discernus module
sys.path.append(str(Path(__file__).parent.parent.parent))

from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway
from discernus.core.audit_logger import AuditLogger
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.cli_console import rich_console

# --- Configuration ---
TEST_CONFIG = {
    "malcolm_x_speech_path": "projects/mlkmx/corpus/malcolm_x_ballot_or_bullet.txt",
    "prompt_3_shot_path": "discernus/agents/analysis_agent/prompt.yaml",
    "framework_path": "projects/mlkmx/cff_v10.md",
    "output_dir": "projects/mlkmx/tmp/model_testing",
    "runs_per_test": 3,
}

# --- Helper Functions ---

def load_text_file(file_path: str) -> str:
    """Loads a text file from the given path."""
    try:
        return Path(file_path).read_text(encoding='utf-8')
    except FileNotFoundError:
        rich_console.print_error(f"❌ File not found: {file_path}")
        sys.exit(1)
    except Exception as e:
        rich_console.print_error(f"❌ Error reading file {file_path}: {e}")
        sys.exit(1)

def create_modified_prompt(base_prompt: str) -> str:
    """Removes the 3-shot median aggregation requirement from the prompt."""
    modified_prompt = base_prompt
    
    modified_prompt = modified_prompt.replace(
        '**THREE INDEPENDENT ANALYTICAL APPROACHES (NEW REQUIREMENT):**', 
        '**ANALYTICAL APPROACH:**'
    )
    
    start_phrase = 'For each document, you MUST generate THREE completely independent analytical perspectives.'
    end_phrase = 'This ensures robust internal self-consistency.'
    start_index = modified_prompt.find(start_phrase)
    end_index = modified_prompt.find(end_phrase)
    if start_index != -1 and end_index != -1:
        modified_prompt = modified_prompt[:start_index] + "Generate a single, comprehensive analysis for each document." + modified_prompt[end_index + len(end_phrase):]

    start_phrase = 'STEP 1: Apply the framework to all {num_documents} documents using THREE INDEPENDENT ANALYTICAL APPROACHES'
    end_phrase = 'Each approach must maintain the same high quality standards as the original single-run analysis.'
    start_index = modified_prompt.find(start_phrase)
    end_index = modified_prompt.find(end_phrase)
    if start_index != -1 and end_index != -1:
         modified_prompt = modified_prompt[:start_index] + "STEP 1: Apply the framework to all {num_documents} documents.\nSTEP 2: Return the result in the exact format specified above." + modified_prompt[end_index + len(end_phrase):]

    modified_prompt = modified_prompt.replace('"internal_consistency_approach": "3-run median aggregation"', '"internal_consistency_approach": "single-run analysis"')
    modified_prompt = modified_prompt.replace('"raw_score": "[MEDIAN of 3 approaches - 0.0-1.0 dimensional intensity]"', '"raw_score": "[0.0-1.0 dimensional intensity]"')
    modified_prompt = modified_prompt.replace('"salience": "[MEDIAN of 3 approaches - 0.0-1.0 rhetorical prominence]"', '"salience": "[0.0-1.0 rhetorical prominence]"')
    modified_prompt = modified_prompt.replace('"quote_text": "[BEST supporting quote from 3 approaches]"', '"quote_text": "[Supporting quote]"')
    
    return modified_prompt

def extract_scores_from_response(response_content: str) -> Dict[str, Any]:
    """Extracts the dimensional_scores from the LLM's JSON response."""
    try:
        json_str = response_content[response_content.find('{'):response_content.rfind('}')+1]
        data = json.loads(json_str)
        return data["document_analyses"][0]["dimensional_scores"]
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        rich_console.print_warning(f"⚠️  Could not parse scores from response: {e}\nResponse:\n{response_content[:500]}...")
        return {}

def print_scores_table(title: str, results: List[Dict[str, Any]]):
    """Prints a Rich table comparing scores across runs."""
    if not results or not all(results):
        rich_console.print_warning(f"Skipping table for '{title}' due to missing results.")
        return
        
    table = rich_console.create_table(title, ["Dimension", "Metric"] + [f"Run {i+1}" for i in range(len(results))])
    dimensions = sorted(results[0].keys())
    for dim in dimensions:
        table.add_row(dim, "raw_score", *[str(res.get(dim, {}).get("raw_score", "N/A")) for res in results])
        table.add_row("", "salience", *[str(res.get(dim, {}).get("salience", "N/A")) for res in results])
        table.add_section()
    rich_console.print_table(table)

# --- Test Runner ---

class ModelTestRunner:
    def __init__(self):
        self.speech_text = load_text_file(TEST_CONFIG["malcolm_x_speech_path"])
        self.framework_text = load_text_file(TEST_CONFIG["framework_path"])
        
        prompt_template_yaml = load_text_file(TEST_CONFIG["prompt_3_shot_path"])
        self.prompt_3_shot = yaml.safe_load(prompt_template_yaml)['template']
        self.modified_prompt = create_modified_prompt(self.prompt_3_shot)

        run_name = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        self.output_dir = Path(TEST_CONFIG["output_dir"]) / run_name
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        mock_security = ExperimentSecurityBoundary(Path.cwd() / "projects" / "mlkmx")
        mock_storage = LocalArtifactStorage(mock_security, self.output_dir, run_name)
        mock_audit = AuditLogger(mock_security, self.output_dir)
        
        self.gateway = EnhancedLLMGateway(mock_audit)

    def run_test(self, test_name: str, model: str, prompt: str) -> List[Dict[str, Any]]:
        """Runs a single test configuration multiple times."""
        rich_console.print_section(f"🔬 Running Test: {test_name}")
        rich_console.print_info(f"   Model: {model}, Runs: {TEST_CONFIG['runs_per_test']}")

        results = []
        for i in range(TEST_CONFIG['runs_per_test']):
            rich_console.print_info(f"--- Starting {test_name} Run {i+1} ---")
            full_prompt = prompt.replace('{framework_content}', self.framework_text)
            full_prompt = full_prompt.replace('{document_content}', self.speech_text)
            full_prompt = full_prompt.replace('{analysis_id}', f"test_{test_name}_{i+1}")
            full_prompt = full_prompt.replace('{num_documents}', str(1))

            response = self.gateway.execute_call(model=model, prompt=full_prompt)
            
            if isinstance(response, tuple):
                content, metadata = response
            else:
                content = response.get('content', '')

            (self.output_dir / f"{test_name}_run_{i+1}.txt").write_text(content, encoding='utf-8')
            scores = extract_scores_from_response(content)
            results.append(scores)
            rich_console.print_info(f"--- Finished {test_name} Run {i+1} ---")
        
        return results

def main():
    """Main function to orchestrate the tests."""
    runner = ModelTestRunner()

    pro_3_shot_results = runner.run_test(
        test_name="pro_3_shot",
        model="vertex_ai/gemini-2.5-pro",
        prompt=runner.prompt_3_shot
    )
    print_scores_table("Gemini 2.5 Pro - 3-Shot Median Prompt", pro_3_shot_results)

    flash_3_shot_results = runner.run_test(
        test_name="flash_3_shot",
        model="vertex_ai/gemini-2.5-flash",
        prompt=runner.prompt_3_shot
    )
    print_scores_table("Gemini 2.5 Flash - 3-Shot Median Prompt", flash_3_shot_results)
    
    flash_modified_results = runner.run_test(
        test_name="flash_modified_prompt",
        model="vertex_ai/gemini-2.5-flash",
        prompt=runner.modified_prompt
    )
    print_scores_table("Gemini 2.5 Flash - Modified Single-Run Prompt", flash_modified_results)
    
    rich_console.print_success(f"✅ All tests completed. Raw outputs saved in: {runner.output_dir}")

if __name__ == "__main__":
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    main()
