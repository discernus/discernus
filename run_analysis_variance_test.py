#!/usr/bin/env python3
"""
Analysis Variance Test Script
=============================

Runs 20 analysis sessions using Gemini 2.5 Flash Lite to test variance between runs.
Uses the actual analysis prompt from the EnhancedAnalysisAgent.
"""

import json
import time
from pathlib import Path
from typing import Dict, Any, List
import pandas as pd
import sys

# Add project root to path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from scripts.prompt_engineering_harness import direct_model_call

def create_analysis_prompt(framework_content: str, corpus_content: str) -> str:
    """Create the analysis prompt based on the actual EnhancedAnalysisAgent prompt."""
    
    prompt = f"""You are an enhanced computational research analysis agent. Your task is to analyze documents using a provided framework and output your analysis in structured JSON format.

**CRITICAL SEPARATION OF CONCERNS (v6.0):**
- You are responsible for ONLY: raw dimensional scores, salience assessment, confidence levels, and evidence extraction
- You MUST NOT: perform mathematical calculations, compute derived metrics, calculate indices, or show mathematical work
- All mathematical calculations and derived metrics are handled by downstream code generation/execution

**CRITICAL DIMENSIONAL COMPLETENESS REQUIREMENT:**
- You MUST score EVERY dimension listed in the framework's dimensions (0.0-1.0 scale)
- Use the framework dimensions as the authoritative list
- NEVER invent or hallucinate dimension names that don't exist in the framework
- If you cannot confidently score a dimension, use 0.0 score with low confidence and provide explanation in evidence

**REQUIRED JSON OUTPUT STRUCTURE:**

{{
  "analysis_metadata": {{
    "framework_name": "Cohesive Flourishing Framework",
    "framework_version": "v8.0", 
    "analyst_confidence": "[0.0-1.0 overall confidence in analysis]",
    "analysis_notes": "[brief methodological notes]"
  }},
  "document_analyses": [
    {{
      "document_id": "test_document_001",
      "document_name": "alexandria_ocasio_cortez_2025_fighting_oligarchy.txt",
      "dimensional_scores": {{
        "tribal_dominance": {{
          "raw_score": "[0.0-1.0 dimensional intensity]",
          "salience": "[0.0-1.0 rhetorical prominence]", 
          "confidence": "[0.0-1.0 scoring confidence]"
        }},
        "individual_dignity": {{
          "raw_score": "[0.0-1.0 dimensional intensity]",
          "salience": "[0.0-1.0 rhetorical prominence]", 
          "confidence": "[0.0-1.0 scoring confidence]"
        }},
        "fear": {{
          "raw_score": "[0.0-1.0 dimensional intensity]",
          "salience": "[0.0-1.0 rhetorical prominence]", 
          "confidence": "[0.0-1.0 scoring confidence]"
        }},
        "hope": {{
          "raw_score": "[0.0-1.0 dimensional intensity]",
          "salience": "[0.0-1.0 rhetorical prominence]", 
          "confidence": "[0.0-1.0 scoring confidence]"
        }},
        "envy": {{
          "raw_score": "[0.0-1.0 dimensional intensity]",
          "salience": "[0.0-1.0 rhetorical prominence]", 
          "confidence": "[0.0-1.0 scoring confidence]"
        }},
        "compersion": {{
          "raw_score": "[0.0-1.0 dimensional intensity]",
          "salience": "[0.0-1.0 rhetorical prominence]", 
          "confidence": "[0.0-1.0 scoring confidence]"
        }},
        "enmity": {{
          "raw_score": "[0.0-1.0 dimensional intensity]",
          "salience": "[0.0-1.0 rhetorical prominence]", 
          "confidence": "[0.0-1.0 scoring confidence]"
        }},
        "amity": {{
          "raw_score": "[0.0-1.0 dimensional intensity]",
          "salience": "[0.0-1.0 rhetorical prominence]", 
          "confidence": "[0.0-1.0 scoring confidence]"
        }},
        "fragmentative_goals": {{
          "raw_score": "[0.0-1.0 dimensional intensity]",
          "salience": "[0.0-1.0 rhetorical prominence]", 
          "confidence": "[0.0-1.0 scoring confidence]"
        }},
        "cohesive_goals": {{
          "raw_score": "[0.0-1.0 dimensional intensity]",
          "salience": "[0.0-1.0 rhetorical prominence]", 
          "confidence": "[0.0-1.0 scoring confidence]"
        }}
      }},
      "evidence": [
        {{
          "dimension": "[dimension name]",
          "quote_text": "[strongest supporting quote]",
          "confidence": "[0.0-1.0 evidence confidence]",
          "context_type": "[quote context classification]"
        }}
      ]
    }}
  ]
}}

**IMPORTANT CONSTRAINTS:**
1. Provide ONLY raw dimensional scores - NO calculated metrics, tensions, indices, or mathematical derivations
2. Focus on evidence quality and confidence assessment
3. Follow the framework's dimensional definitions for interpretation
4. Ensure JSON is valid and parseable

---

**FRAMEWORK:**
{framework_content}

**DOCUMENT TO ANALYZE:**
{corpus_content}

---

Begin analysis now. Apply the framework to the document and return your analysis as valid JSON with raw scores and evidence only. Return ONLY the JSON, no explanations or additional text."""
    
    return prompt

def run_variance_test(num_runs: int = 20) -> List[Dict[str, Any]]:
    """Run the analysis variance test."""
    
    # Load framework content
    framework_path = Path("projects/simple_test/cff_v8.md")
    framework_content = framework_path.read_text()
    
    # Load corpus content
    corpus_path = Path("projects/simple_test/corpus/alexandria_ocasio_cortez_2025_fighting_oligarchy.txt")
    corpus_content = corpus_path.read_text()
    
    # Create the analysis prompt
    analysis_prompt = create_analysis_prompt(framework_content, corpus_content)
    
    results = []
    
    print(f"🚀 Starting analysis variance test with {num_runs} runs...")
    print(f"📊 Using Gemini 2.5 Flash Lite")
    print(f"📄 Analyzing: {corpus_path.name}")
    print("=" * 80)
    
    for run_num in range(1, num_runs + 1):
        print(f"🔄 Run {run_num}/{num_runs}...")
        
        try:
            # Make the analysis call
            response, metadata = direct_model_call(
                model="vertex_ai/gemini-2.5-flash-lite",
                prompt=analysis_prompt,
                system_prompt="You are an expert discourse analyst specializing in social cohesion and rhetorical strategy analysis."
            )
            
            # Parse the response
            try:
                # Try to extract JSON from the response
                json_start = response.find('{')
                json_end = response.rfind('}') + 1
                
                if json_start != -1 and json_end != -1:
                    json_str = response[json_start:json_end]
                    parsed_response = json.loads(json_str)
                    
                    # Extract key metrics for variance analysis
                    run_result = {
                        "run_number": run_num,
                        "success": True,
                        "response_length": len(response),
                        "token_usage": metadata.get("usage", {}),
                        "parsed_successfully": True,
                        "dimensional_scores": {},
                        "overall_confidence": None,
                        "raw_response": response
                    }
                    
                    # Extract dimensional scores if available
                    if "document_analyses" in parsed_response and len(parsed_response["document_analyses"]) > 0:
                        doc_analysis = parsed_response["document_analyses"][0]
                        if "dimensional_scores" in doc_analysis:
                            for dimension, scores in doc_analysis["dimensional_scores"].items():
                                if isinstance(scores, dict):
                                    run_result["dimensional_scores"][dimension] = {
                                        "raw_score": scores.get("raw_score"),
                                        "salience": scores.get("salience"),
                                        "confidence": scores.get("confidence")
                                    }
                    
                    # Extract overall confidence
                    if "analysis_metadata" in parsed_response:
                        run_result["overall_confidence"] = parsed_response["analysis_metadata"].get("analyst_confidence")
                    
                else:
                    run_result = {
                        "run_number": run_num,
                        "success": True,
                        "response_length": len(response),
                        "token_usage": metadata.get("usage", {}),
                        "parsed_successfully": False,
                        "dimensional_scores": {},
                        "overall_confidence": None,
                        "raw_response": response,
                        "error": "No JSON found in response"
                    }
                    
            except json.JSONDecodeError as e:
                run_result = {
                    "run_number": run_num,
                    "success": True,
                    "response_length": len(response),
                    "token_usage": metadata.get("usage", {}),
                    "parsed_successfully": False,
                    "dimensional_scores": {},
                    "overall_confidence": None,
                    "raw_response": response,
                    "error": f"JSON decode error: {str(e)}"
                }
            
        except Exception as e:
            run_result = {
                "run_number": run_num,
                "success": False,
                "response_length": 0,
                "token_usage": {},
                "parsed_successfully": False,
                "dimensional_scores": {},
                "overall_confidence": None,
                "raw_response": "",
                "error": str(e)
            }
        
        results.append(run_result)
        
        # Add delay between runs to avoid rate limiting
        if run_num < num_runs:
            time.sleep(2)
    
    return results

def analyze_variance(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze the variance in the results."""
    
    # Filter successful runs
    successful_runs = [r for r in results if r["success"] and r["parsed_successfully"]]
    
    if not successful_runs:
        return {"error": "No successful runs to analyze"}
    
    # Extract dimensional scores for analysis
    dimensions = ["tribal_dominance", "individual_dignity", "fear", "hope", "envy", 
                  "compersion", "enmity", "amity", "fragmentative_goals", "cohesive_goals"]
    
    variance_analysis = {}
    
    for dimension in dimensions:
        scores = []
        saliences = []
        confidences = []
        
        for run in successful_runs:
            if dimension in run["dimensional_scores"]:
                dim_data = run["dimensional_scores"][dimension]
                if dim_data.get("raw_score") is not None:
                    scores.append(float(dim_data["raw_score"]))
                if dim_data.get("salience") is not None:
                    saliences.append(float(dim_data["salience"]))
                if dim_data.get("confidence") is not None:
                    confidences.append(float(dim_data["confidence"]))
        
        if scores:
            variance_analysis[dimension] = {
                "raw_score": {
                    "count": len(scores),
                    "mean": sum(scores) / len(scores),
                    "min": min(scores),
                    "max": max(scores),
                    "range": max(scores) - min(scores),
                    "std_dev": (sum((x - (sum(scores) / len(scores))) ** 2 for x in scores) / len(scores)) ** 0.5 if len(scores) > 1 else 0
                }
            }
        
        if saliences:
            variance_analysis[dimension]["salience"] = {
                "count": len(saliences),
                "mean": sum(saliences) / len(saliences),
                "min": min(saliences),
                "max": max(saliences),
                "range": max(saliences) - min(saliences)
            }
        
        if confidences:
            variance_analysis[dimension]["confidence"] = {
                "count": len(confidences),
                "mean": sum(confidences) / len(confidences),
                "min": min(confidences),
                "max": max(confidences),
                "range": max(confidences) - min(confidences)
            }
    
    # Overall statistics
    overall_stats = {
        "total_runs": len(results),
        "successful_runs": len(successful_runs),
        "success_rate": len(successful_runs) / len(results),
        "parsing_success_rate": len([r for r in results if r["parsed_successfully"]]) / len(results),
        "average_response_length": sum(r["response_length"] for r in results) / len(results),
        "variance_analysis": variance_analysis
    }
    
    return overall_stats

def main():
    """Main function to run the variance test."""
    
    print("🔬 Discernus Analysis Variance Test")
    print("=" * 50)
    
    # Run the test
    results = run_variance_test(20)
    
    # Analyze variance
    variance_analysis = analyze_variance(results)
    
    # Save results
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    results_file = f"analysis_variance_test_results_{timestamp}.json"
    
    with open(results_file, 'w') as f:
        json.dump({
            "test_metadata": {
                "model": "vertex_ai/gemini-2.5-flash-lite",
                "corpus_file": "alexandria_ocasio_cortez_2025_fighting_oligarchy.txt",
                "framework": "cff_v8.md",
                "num_runs": 20,
                "timestamp": timestamp
            },
            "raw_results": results,
            "variance_analysis": variance_analysis
        }, f, indent=2)
    
    print(f"\n✅ Test completed! Results saved to: {results_file}")
    
    # Print summary
    print(f"\n📊 SUMMARY:")
    print(f"   Total runs: {variance_analysis.get('total_runs', 0)}")
    print(f"   Successful runs: {variance_analysis.get('successful_runs', 0)}")
    print(f"   Success rate: {variance_analysis.get('success_rate', 0):.1%}")
    print(f"   Parsing success rate: {variance_analysis.get('parsing_success_rate', 0):.1%}")
    
    if "variance_analysis" in variance_analysis:
        print(f"\n🔍 DIMENSIONAL VARIANCE ANALYSIS:")
        for dimension, data in variance_analysis["variance_analysis"].items():
            if "raw_score" in data:
                scores = data["raw_score"]
                print(f"   {dimension}:")
                print(f"     Mean: {scores['mean']:.3f}")
                print(f"     Range: {scores['min']:.3f} - {scores['max']:.3f}")
                print(f"     Std Dev: {scores['std_dev']:.3f}")

if __name__ == "__main__":
    main()
