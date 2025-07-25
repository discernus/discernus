#!/usr/bin/env python3
"""
THIN LLM-to-LLM Data Recovery Script
===================================

This script uses LLM intelligence to extract data from the hierarchical JSON responses,
rather than hardcoded patterns. This is framework-agnostic and will work with any LLM
output format.

THIN Philosophy: Let the LLM do the intelligent work, not hardcoded parsing.
"""

import json
import pandas as pd
from pathlib import Path
from typing import Dict, Any, List
import csv
from datetime import datetime
import sys
import os

# Add the discernus package to the path
sys.path.append(str(Path(__file__).parent))

from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry

# Paths to existing experiment data (READ ONLY)
EXPERIMENT_DIR = Path("projects/MVA/experiments/experiment_3")
RESULTS_DIR = EXPERIMENT_DIR / "results/2025-07-17_21-59-15"
STATE_FILE = RESULTS_DIR / "state_after_step_2_DataExtractionAgent.json"

# Output paths for recovered data (NEW FILES ONLY)
RECOVERY_DIR = RESULTS_DIR / "thin_llm_recovery"
RECOVERY_DIR.mkdir(exist_ok=True)

# LLM configuration for data extraction
EXTRACTION_MODEL = "vertex_ai/gemini-2.5-pro"  # Fast and cheap for extraction
EXTRACTION_PROMPT = """
You are a data extraction specialist. Your job is to extract structured data from complex JSON responses.

I will provide you with a JSON response from a CFF (Cohesive Flourishing Framework) analysis. This JSON may have various nested structures, different field names, and inconsistent formatting.

Your task is to extract ALL the CFF-related data and flatten it into a consistent structure. Extract:

1. **CFF Anchor Scores**: Any numerical scores for CFF axes/anchors (tribal dominance, individual dignity, fear, hope, envy, compersion, enmity, amity, fragmentative goals, cohesive goals)
2. **Reasoning/Analysis**: Any explanatory text for the scores
3. **Confidence Levels**: Any confidence indicators
4. **Evidence/Quotations**: Any supporting quotes or evidence
5. **Political Worldview**: Any political classification data
6. **Other Analysis**: Any other analytical insights

OUTPUT FORMAT: Return a flat JSON object with consistent field names:
- Use lowercase with underscores: "tribal_dominance_score", "individual_dignity_reasoning"
- For arrays, join with " | " separator
- For nested data, flatten with descriptive names

IMPORTANT: Extract as much data as possible. Don't leave anything behind.

Here is the JSON to extract from:

{json_input}

Return only the extracted flat JSON, no other text.
"""

def load_experiment_data() -> Dict[str, Any]:
    """Load the existing experiment state data."""
    print(f"📂 Loading experiment data from: {STATE_FILE}")
    
    if not STATE_FILE.exists():
        raise FileNotFoundError(f"State file not found: {STATE_FILE}")
    
    with open(STATE_FILE, 'r') as f:
        data = json.load(f)
    
    print(f"✅ Loaded experiment data: {len(data.get('analysis_results', []))} analysis results")
    return data

def extract_with_llm(hierarchical_json: Dict[str, Any], llm_gateway: LLMGateway) -> Dict[str, Any]:
    """Use LLM to intelligently extract data from hierarchical JSON."""
    
    # Format the prompt with the JSON data
    prompt = EXTRACTION_PROMPT.format(json_input=json.dumps(hierarchical_json, indent=2))
    
    try:
        # Call the LLM to extract data
        response, metadata = llm_gateway.execute_call(
            model=EXTRACTION_MODEL,
            prompt=prompt,
            system_prompt="You are a precise data extraction specialist. Return only valid JSON."
        )
        
        if not response or not response.strip():
            return {}
        
        # Parse the LLM response as JSON
        try:
            extracted_data = json.loads(response.strip())
            if isinstance(extracted_data, dict):
                return extracted_data
            else:
                print(f"  ⚠️ LLM returned non-dict: {type(extracted_data)}")
                return {}
        except json.JSONDecodeError as e:
            print(f"  ⚠️ LLM returned invalid JSON: {e}")
            print(f"  Response: {response[:200]}...")
            return {}
            
    except Exception as e:
        print(f"  ❌ LLM extraction failed: {e}")
        return {}

def validate_thin_recovery() -> Dict[str, Any]:
    """Main validation function using THIN LLM-to-LLM approach."""
    
    print("🔍 Starting THIN LLM-to-LLM Recovery Validation")
    print("=" * 60)
    
    # Initialize LLM gateway
    model_registry = ModelRegistry()
    llm_gateway = LLMGateway(model_registry)
    
    # Load experiment data
    experiment_data = load_experiment_data()
    analysis_results = experiment_data.get("analysis_results", [])
    
    # Process each analysis result
    recovered_data = []
    successful_extractions = 0
    failed_extractions = 0
    llm_calls = 0
    
    for i, result in enumerate(analysis_results):
        print(f"\n📊 Processing analysis result {i+1}/{len(analysis_results)}")
        
        # Basic metadata
        base_data = {
            "agent_id": result.get("agent_id"),
            "corpus_file": result.get("corpus_file"),
            "model_name": result.get("model_name"),
            "run_num": result.get("run_num"),
            "success": result.get("success"),
            "extraction_attempts": result.get("extraction_attempts", 0)
        }
        
        # Try to extract with LLM
        if result.get("success") and result.get("json_output"):
            try:
                print(f"  🤖 Calling LLM for intelligent extraction...")
                llm_calls += 1
                
                extracted_data = extract_with_llm(result["json_output"], llm_gateway)
                
                if extracted_data:
                    successful_extractions += 1
                    print(f"  ✅ LLM extracted {len(extracted_data)} data points")
                    
                    # Show what we found
                    score_keys = [k for k in extracted_data.keys() if 'score' in k.lower()]
                    evidence_keys = [k for k in extracted_data.keys() if any(word in k.lower() for word in ['evidence', 'quotation', 'quote'])]
                    
                    print(f"  🎯 Scores: {', '.join(score_keys)}")
                    if evidence_keys:
                        print(f"  📝 Evidence: {', '.join(evidence_keys)}")
                    
                    # Combine base data with extracted data
                    combined_data = {**base_data, **extracted_data}
                    recovered_data.append(combined_data)
                else:
                    failed_extractions += 1
                    print(f"  ❌ LLM extraction returned empty result")
                    recovered_data.append(base_data)
                    
            except Exception as e:
                failed_extractions += 1
                print(f"  ❌ Error during LLM extraction: {e}")
                recovered_data.append(base_data)
        else:
            failed_extractions += 1
            print(f"  ❌ No valid JSON output")
            recovered_data.append(base_data)
    
    # Generate summary
    summary = {
        "total_analyses": len(analysis_results),
        "successful_extractions": successful_extractions,
        "failed_extractions": failed_extractions,
        "success_rate": successful_extractions / len(analysis_results) * 100 if analysis_results else 0,
        "llm_calls_made": llm_calls,
        "recovered_data": recovered_data
    }
    
    print(f"\n📈 THIN LLM RECOVERY SUMMARY")
    print(f"   Total analyses: {summary['total_analyses']}")
    print(f"   Successful LLM extractions: {summary['successful_extractions']}")
    print(f"   Failed extractions: {summary['failed_extractions']}")
    print(f"   Success rate: {summary['success_rate']:.1f}%")
    print(f"   LLM calls made: {summary['llm_calls_made']}")
    
    return summary

def save_recovered_data(summary: Dict[str, Any]) -> None:
    """Save recovered data to new files."""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save detailed CSV
    csv_path = RECOVERY_DIR / f"thin_llm_recovered_data_{timestamp}.csv"
    
    if summary["recovered_data"]:
        df = pd.DataFrame(summary["recovered_data"])
        df.to_csv(csv_path, index=False)
        print(f"\n💾 Saved THIN LLM recovery data to: {csv_path}")
        print(f"   Rows: {len(df)}")
        print(f"   Columns: {len(df.columns)}")
        
        # Show column summary
        print(f"\n📊 Column Summary:")
        for col in df.columns:
            non_null_count = df[col].notna().sum()
            print(f"   {col}: {non_null_count}/{len(df)} ({non_null_count/len(df)*100:.1f}%)")
    
    # Save summary report
    summary_path = RECOVERY_DIR / f"thin_llm_recovery_report_{timestamp}.json"
    
    # Remove large data array from summary for clean report
    summary_for_report = {k: v for k, v in summary.items() if k != "recovered_data"}
    
    with open(summary_path, 'w') as f:
        json.dump(summary_for_report, f, indent=2)
    
    print(f"\n📝 Saved THIN LLM recovery report to: {summary_path}")

def main():
    """Main execution function."""
    
    print("🚀 THIN LLM-to-LLM Data Recovery Starting...")
    print(f"📍 Working directory: {Path.cwd()}")
    print(f"📂 Experiment directory: {EXPERIMENT_DIR}")
    print(f"💾 Recovery output directory: {RECOVERY_DIR}")
    print(f"🤖 Using extraction model: {EXTRACTION_MODEL}")
    
    try:
        # Validate recovery
        summary = validate_thin_recovery()
        
        # Save results
        save_recovered_data(summary)
        
        print("\n🎉 THIN LLM recovery validation completed successfully!")
        print(f"📊 Check results in: {RECOVERY_DIR}")
        
    except Exception as e:
        print(f"\n❌ Error during validation: {e}")
        raise

if __name__ == "__main__":
    main() 