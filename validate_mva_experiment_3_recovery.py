#!/usr/bin/env python3
"""
MVA Experiment 3 Data Recovery Validation Script
==============================================

This script processes the existing MVA Experiment 3 data to extract 
the real CFF anchor scores that are buried in the hierarchical JSON responses.

SAFETY FIRST: This script only READS existing data and creates NEW files.
It never modifies or deletes any original experiment data.

Purpose: Prove what data is actually recoverable from the "failed" experiment.
"""

import json
import pandas as pd
from pathlib import Path
from typing import Dict, Any, List
import csv
from datetime import datetime

# Paths to existing experiment data (READ ONLY)
EXPERIMENT_DIR = Path("projects/MVA/experiments/experiment_3")
RESULTS_DIR = EXPERIMENT_DIR / "results/2025-07-17_21-59-15"
STATE_FILE = RESULTS_DIR / "state_after_step_2_DataExtractionAgent.json"

# Output paths for recovered data (NEW FILES ONLY)
RECOVERY_DIR = RESULTS_DIR / "recovery_validation"
RECOVERY_DIR.mkdir(exist_ok=True)

def load_experiment_data() -> Dict[str, Any]:
    """Load the existing experiment state data."""
    print(f"📂 Loading experiment data from: {STATE_FILE}")
    
    if not STATE_FILE.exists():
        raise FileNotFoundError(f"State file not found: {STATE_FILE}")
    
    with open(STATE_FILE, 'r') as f:
        data = json.load(f)
    
    print(f"✅ Loaded experiment data: {len(data.get('analysis_results', []))} analysis results")
    return data

def extract_cff_scores(hierarchical_json: Dict[str, Any]) -> Dict[str, Any]:
    """Extract CFF anchor scores from hierarchical JSON structure."""
    
    # Initialize flat CFF scores dictionary
    cff_scores = {}
    
    # Look for CFF v4.1 Analysis structure
    cff_analysis = hierarchical_json.get("Cohesive Flourishing Framework v4.1 Analysis", {})
    
    if cff_analysis:
        # Extract Identity Axis scores
        identity_axis = cff_analysis.get("Identity Axis", {})
        if identity_axis:
            # Tribal Dominance
            tribal_dominance = identity_axis.get("Tribal Dominance", {})
            if tribal_dominance:
                cff_scores["tribal_dominance_score"] = tribal_dominance.get("Score", tribal_dominance.get("score"))
                cff_scores["tribal_dominance_reasoning"] = tribal_dominance.get("Reasoning", tribal_dominance.get("reasoning"))
                cff_scores["tribal_dominance_confidence"] = tribal_dominance.get("Confidence", tribal_dominance.get("confidence"))
            
            # Individual Dignity
            individual_dignity = identity_axis.get("Individual Dignity", {})
            if individual_dignity:
                cff_scores["individual_dignity_score"] = individual_dignity.get("Score", individual_dignity.get("score"))
                cff_scores["individual_dignity_reasoning"] = individual_dignity.get("Reasoning", individual_dignity.get("reasoning"))
        
        # Extract Fear-Hope Axis scores
        fear_hope_axis = cff_analysis.get("Fear-Hope Axis", {})
        if fear_hope_axis:
            # Fear Score
            fear_data = fear_hope_axis.get("Fear", {})
            if fear_data:
                cff_scores["fear_score"] = fear_data.get("Score", fear_data.get("score"))
                cff_scores["fear_reasoning"] = fear_data.get("Reasoning", fear_data.get("reasoning"))
            
            # Hope Score
            hope_data = fear_hope_axis.get("Hope", {})
            if hope_data:
                cff_scores["hope_score"] = hope_data.get("Score", hope_data.get("score"))
                cff_scores["hope_reasoning"] = hope_data.get("Reasoning", hope_data.get("reasoning"))
        
        # Extract other axes if present
        for axis_name in ["Envy-Compersion Axis", "Enmity-Amity Axis", "Goal Axis"]:
            axis_data = cff_analysis.get(axis_name, {})
            if axis_data:
                # Handle both nested and flat structures
                for component_name, component_data in axis_data.items():
                    if isinstance(component_data, dict):
                        score_key = f"{component_name.lower().replace(' ', '_').replace('-', '_')}_score"
                        reasoning_key = f"{component_name.lower().replace(' ', '_').replace('-', '_')}_reasoning"
                        cff_scores[score_key] = component_data.get("Score", component_data.get("score"))
                        cff_scores[reasoning_key] = component_data.get("Reasoning", component_data.get("reasoning"))
    
    # Also check for direct axis structures (alternative format)
    for axis_name in ["Identity Axis", "Fear-Hope Axis", "Envy-Compersion Axis", "Enmity-Amity Axis", "Goal Axis"]:
        axis_data = hierarchical_json.get(axis_name, {})
        if axis_data and not cff_scores:  # Only use if we didn't find CFF v4.1 structure
            for component_name, component_data in axis_data.items():
                if isinstance(component_data, dict):
                    score_key = f"{component_name.lower().replace(' ', '_').replace('-', '_')}_score"
                    reasoning_key = f"{component_name.lower().replace(' ', '_').replace('-', '_')}_reasoning"
                    cff_scores[score_key] = component_data.get("Score", component_data.get("score"))
                    cff_scores[reasoning_key] = component_data.get("Reasoning", component_data.get("reasoning"))
    
    # Extract Political Worldview if present
    political_worldview = hierarchical_json.get("Political Worldview Classification", {})
    if political_worldview:
        # Handle both string and dict formats
        if isinstance(political_worldview, dict):
            cff_scores["political_worldview"] = political_worldview.get("Worldview")
            cff_scores["political_worldview_reasoning"] = political_worldview.get("Reasoning")
        elif isinstance(political_worldview, str):
            cff_scores["political_worldview"] = political_worldview
    
    return cff_scores

def validate_recovery() -> Dict[str, Any]:
    """Main validation function that processes all experiment data."""
    
    print("🔍 Starting MVA Experiment 3 Recovery Validation")
    print("=" * 60)
    
    # Load experiment data
    experiment_data = load_experiment_data()
    analysis_results = experiment_data.get("analysis_results", [])
    
    # Process each analysis result
    recovered_data = []
    successful_extractions = 0
    failed_extractions = 0
    
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
        
        # Try to extract CFF scores
        if result.get("success") and result.get("json_output"):
            try:
                cff_scores = extract_cff_scores(result["json_output"])
                
                if cff_scores:
                    successful_extractions += 1
                    print(f"  ✅ Extracted {len(cff_scores)} CFF data points")
                    
                    # Log what we found
                    score_keys = [k for k in cff_scores.keys() if k.endswith("_score")]
                    print(f"  🎯 Scores found: {', '.join(score_keys)}")
                    
                    # Combine base data with extracted scores
                    combined_data = {**base_data, **cff_scores}
                    recovered_data.append(combined_data)
                else:
                    failed_extractions += 1
                    print(f"  ❌ No CFF scores found in JSON structure")
                    recovered_data.append(base_data)
            except Exception as e:
                failed_extractions += 1
                print(f"  ❌ Error extracting CFF scores: {e}")
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
        "success_rate": successful_extractions / len(analysis_results) * 100,
        "recovered_data": recovered_data
    }
    
    print(f"\n📈 RECOVERY VALIDATION SUMMARY")
    print(f"   Total analyses: {summary['total_analyses']}")
    print(f"   Successful CFF extractions: {summary['successful_extractions']}")
    print(f"   Failed extractions: {summary['failed_extractions']}")
    print(f"   Success rate: {summary['success_rate']:.1f}%")
    
    return summary

def save_recovered_data(summary: Dict[str, Any]) -> None:
    """Save recovered data to new files."""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save detailed CSV
    csv_path = RECOVERY_DIR / f"recovered_cff_scores_{timestamp}.csv"
    
    if summary["recovered_data"]:
        df = pd.DataFrame(summary["recovered_data"])
        df.to_csv(csv_path, index=False)
        print(f"\n💾 Saved recovered data to: {csv_path}")
        print(f"   Rows: {len(df)}")
        print(f"   Columns: {len(df.columns)}")
        
        # Show column summary
        print(f"\n📊 Column Summary:")
        for col in df.columns:
            non_null_count = df[col].notna().sum()
            print(f"   {col}: {non_null_count}/{len(df)} ({non_null_count/len(df)*100:.1f}%)")
    
    # Save summary report
    summary_path = RECOVERY_DIR / f"recovery_validation_report_{timestamp}.json"
    
    # Remove large data array from summary for clean report
    summary_for_report = {k: v for k, v in summary.items() if k != "recovered_data"}
    
    with open(summary_path, 'w') as f:
        json.dump(summary_for_report, f, indent=2)
    
    print(f"\n📝 Saved validation report to: {summary_path}")

def main():
    """Main execution function."""
    
    print("🚀 MVA Experiment 3 Recovery Validation Starting...")
    print(f"📍 Working directory: {Path.cwd()}")
    print(f"📂 Experiment directory: {EXPERIMENT_DIR}")
    print(f"💾 Recovery output directory: {RECOVERY_DIR}")
    
    try:
        # Validate recovery
        summary = validate_recovery()
        
        # Save results
        save_recovered_data(summary)
        
        print("\n🎉 Recovery validation completed successfully!")
        print(f"📊 Check results in: {RECOVERY_DIR}")
        
    except Exception as e:
        print(f"\n❌ Error during validation: {e}")
        raise

if __name__ == "__main__":
    main() 