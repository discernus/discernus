#!/usr/bin/env python3
"""
Derived Metrics Calculation Agent

A THIN agent that takes framework definitions and raw scores,
then uses Flash Lite to calculate derived metrics directly.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
import re

from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway
from discernus.gateway.model_registry import ModelRegistry


class DerivedMetricsAgent:
    """THIN agent that calculates derived metrics using Flash Lite."""
    
    def __init__(self, experiment_dir: Path):
        self.experiment_dir = experiment_dir
        
        # Initialize core components
        self.security = ExperimentSecurityBoundary(experiment_dir)
        self.audit = AuditLogger(self.security, experiment_dir / "logs")
        self.storage = LocalArtifactStorage(self.security, experiment_dir / "artifacts")
        self.gateway = EnhancedLLMGateway(ModelRegistry())
        
        # Create logs directory
        (experiment_dir / "logs").mkdir(exist_ok=True)
        
    def load_framework(self, framework_path: Path) -> Dict[str, Any]:
        """Load framework and extract derived metrics definitions."""
        with open(framework_path, 'r') as f:
            content = f.read()
        
        # Extract YAML from markdown
        yaml_match = re.search(r'```yaml\n(.*?)\n```', content, re.DOTALL)
        if not yaml_match:
            raise ValueError("No YAML found in framework file")
        
        framework_data = yaml.safe_load(yaml_match.group(1))
        return framework_data
    
    def calculate_derived_metrics(self, framework_path: Path, dimensional_scores: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate derived metrics using Flash Lite."""
        
        # Load framework
        framework_data = self.load_framework(framework_path)
        
        # Extract derived metrics definitions
        derived_metrics = framework_data.get('derived_metrics', [])
        
        # Create calculation prompt
        prompt = self._create_calculation_prompt(framework_data, dimensional_scores, derived_metrics)
        
        # Make LLM call with Flash Lite
        response = self.gateway.execute_call(
            prompt=prompt,
            model="vertex_ai/gemini-2.5-flash-lite",
            max_tokens=2000
        )
        
        # Handle tuple response format
        if isinstance(response, tuple):
            content, metadata = response
        else:
            content = response.get('content', '')
            metadata = response.get('metadata', {})
        
        # Parse the response to extract calculated metrics
        return self._parse_metrics_response(content, derived_metrics)
    
    def _create_calculation_prompt(self, framework_data: Dict, dimensional_scores: Dict, derived_metrics: List[Dict]) -> str:
        """Create a prompt for calculating derived metrics."""
        
        # Format dimensional scores for the prompt
        scores_text = "DIMENSIONAL SCORES:\n"
        for dimension, scores in dimensional_scores.items():
            scores_text += f"- {dimension}: raw_score={scores['raw_score']}, salience={scores['salience']}, confidence={scores['confidence']}\n"
        
        # Format derived metrics definitions
        metrics_text = "DERIVED METRICS TO CALCULATE:\n"
        for metric in derived_metrics:
            metrics_text += f"- {metric['name']}: {metric['description']}\n"
            metrics_text += f"  Formula: {metric['formula']}\n\n"
        
        prompt = f"""You are a statistical analysis expert. Calculate the following derived metrics based on the provided dimensional scores.

{scores_text}

{metrics_text}

INSTRUCTIONS:
1. Calculate each derived metric using the provided formulas
2. Show your calculations step by step
3. Return the results in this exact JSON format:
{{
  "derived_metrics": {{
    "democratic_authoritarian_tension": <calculated_value>,
    "internal_external_focus_tension": <calculated_value>,
    "crisis_elite_attribution_tension": <calculated_value>,
    "populist_strategic_contradiction_index": <calculated_value>,
    "salience_weighted_core_populism_index": <calculated_value>,
    "salience_weighted_populism_mechanisms_index": <calculated_value>,
    "salience_weighted_boundary_distinctions_index": <calculated_value>,
    "salience_weighted_overall_populism_index": <calculated_value>
  }},
  "statistical_analysis": {{
    "total_populism_score": <calculated_value>,
    "dominant_dimensions": ["<dimension1>", "<dimension2>", "<dimension3>"],
    "tension_analysis": "<brief analysis of tensions>",
    "strategic_coherence": "<brief analysis of strategic coherence>"
  }},
  "calculations": {{
    "step_by_step": "<detailed calculation steps>",
    "formula_substitutions": "<showing how formulas were applied>"
  }}
}}

Calculate now:"""

        return prompt
    
    def _parse_metrics_response(self, content: str, derived_metrics: List[Dict]) -> Dict[str, Any]:
        """Parse the LLM response to extract calculated metrics."""
        
        try:
            # Try to find JSON in the response (look for the main structure)
            json_match = re.search(r'\{[^{}]*"derived_metrics"[^{}]*\{[^{}]*\}[^{}]*"statistical_analysis"[^{}]*\{[^{}]*\}[^{}]*\}', content, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group(0))
                return result
            else:
                # Try to extract just the derived_metrics section
                metrics_match = re.search(r'"derived_metrics":\s*\{[^}]*\}', content, re.DOTALL)
                stats_match = re.search(r'"statistical_analysis":\s*\{[^}]*\}', content, re.DOTALL)
                
                if metrics_match and stats_match:
                    # Reconstruct a minimal valid JSON
                    metrics_str = metrics_match.group(0)
                    stats_str = stats_match.group(0)
                    
                    # Extract the values using regex
                    metrics_values = {}
                    for metric in derived_metrics:
                        pattern = f'"{metric["name"]}":\\s*([0-9.]+)'
                        match = re.search(pattern, metrics_str)
                        if match:
                            metrics_values[metric["name"]] = float(match.group(1))
                    
                    return {
                        "derived_metrics": metrics_values,
                        "statistical_analysis": {"extracted_from_response": True},
                        "calculations": {"raw_response": content[:1000] + "..." if len(content) > 1000 else content}
                    }
                else:
                    # Fallback: return the raw content with basic structure
                    return {
                        "derived_metrics": {},
                        "statistical_analysis": {},
                        "calculations": {"raw_response": content[:1000] + "..." if len(content) > 1000 else content},
                        "error": "Could not parse JSON from response"
                    }
        except json.JSONDecodeError as e:
            return {
                "derived_metrics": {},
                "statistical_analysis": {},
                "calculations": {"raw_response": content[:1000] + "..." if len(content) > 1000 else content},
                "error": f"JSON parsing error: {str(e)}"
            }


def main():
    """Test the derived metrics calculation agent."""
    
    # Set up paths
    experiment_dir = Path("/Volumes/code/discernus/test_thin_approach")
    framework_path = experiment_dir / "framework" / "pdaf_v10.md"
    
    # Sample dimensional scores (from our previous test)
    sample_scores = {
        "manichaean_people_elite_framing": {"raw_score": 0.9, "salience": 0.9, "confidence": 0.9},
        "crisis_restoration_narrative": {"raw_score": 0.9, "salience": 0.9, "confidence": 0.9},
        "popular_sovereignty_claims": {"raw_score": 0.6, "salience": 0.6, "confidence": 0.8},
        "anti_pluralist_exclusion": {"raw_score": 0.9, "salience": 0.9, "confidence": 0.9},
        "elite_conspiracy_systemic_corruption": {"raw_score": 0.7, "salience": 0.7, "confidence": 0.8},
        "authenticity_vs_political_class": {"raw_score": 0.7, "salience": 0.6, "confidence": 0.7},
        "homogeneous_people_construction": {"raw_score": 0.9, "salience": 0.9, "confidence": 0.9},
        "nationalist_exclusion": {"raw_score": 0.9, "salience": 0.9, "confidence": 0.9},
        "economic_populist_appeals": {"raw_score": 0.9, "salience": 0.9, "confidence": 0.9}
    }
    
    # Test the agent
    print("=== Testing Derived Metrics Calculation with Flash Lite ===")
    agent = DerivedMetricsAgent(experiment_dir=experiment_dir)
    
    results = agent.calculate_derived_metrics(
        framework_path=framework_path,
        dimensional_scores=sample_scores
    )
    
    # Save results
    with open(experiment_dir / "artifacts" / "derived_metrics_results.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to {experiment_dir / 'artifacts' / 'derived_metrics_results.json'}")
    print(f"Derived metrics calculated: {len(results.get('derived_metrics', {}))}")
    print(f"Statistical analysis keys: {list(results.get('statistical_analysis', {}).keys())}")
    
    # Show a sample of the results
    if 'derived_metrics' in results and results['derived_metrics']:
        print("\nSample derived metrics:")
        for key, value in list(results['derived_metrics'].items())[:3]:
            print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
