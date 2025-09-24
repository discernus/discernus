#!/usr/bin/env python3
"""
Hybrid Analysis Agent

Combines tool calling (Flash) for dimensional scoring and evidence gathering
with THIN approach (Flash Lite) for derived metrics calculation.
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


class HybridAnalysisAgent:
    """Hybrid agent combining tool calling and THIN approaches."""
    
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
        """Load framework and extract tool calling schema."""
        with open(framework_path, 'r') as f:
            content = f.read()
        
        # Extract YAML from markdown
        yaml_match = re.search(r'```yaml\n(.*?)\n```', content, re.DOTALL)
        if not yaml_match:
            raise ValueError("No YAML found in framework file")
        
        framework_data = yaml.safe_load(yaml_match.group(1))
        
        # Extract tool calling schema
        if 'tool_calling_schema' not in framework_data:
            raise ValueError("No tool_calling_schema found in framework")
        
        return framework_data['tool_calling_schema']
    
    def create_tools_from_schema(self, schema: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Convert tool calling schema to LLM tools format."""
        tools = []
        for tool_name, tool_def in schema['tools'].items():
            tool = {
                "type": "function",
                "function": {
                    "name": tool_def['name'],
                    "description": tool_def['description'],
                    "parameters": tool_def['parameters']
                }
            }
            tools.append(tool)
        return tools
    
    def analyze_document(self, framework_path: Path, document_path: Path, document_id: str) -> Dict[str, Any]:
        """Analyze document using hybrid approach."""
        
        # Load framework and extract schema
        schema = self.load_framework(framework_path)
        tools = self.create_tools_from_schema(schema)
        
        # Load document
        with open(document_path, 'r') as f:
            document_content = f.read()
        
        # Load framework content for context
        with open(framework_path, 'r') as f:
            framework_content = f.read()
        
        results = {}
        
        # Step 1: Dimensional Scoring (Flash with tool calling)
        print("Step 1: Making dimensional scoring call with Flash...")
        scores_result = self._make_scoring_call(framework_content, document_content, document_id, tools)
        results['dimensional_scores'] = scores_result
        
        # Step 2: Evidence Gathering (Flash with tool calling)
        print("Step 2: Making evidence gathering call with Flash...")
        evidence_result = self._make_evidence_call(framework_content, document_content, document_id, tools)
        results['evidence_quotes'] = evidence_result
        
        # Step 3: Derived Metrics Calculation (Flash Lite with THIN approach)
        print("Step 3: Calculating derived metrics with Flash Lite...")
        if scores_result:  # Only if we got scores
            metrics_result = self._calculate_derived_metrics(framework_path, scores_result)
            results['derived_metrics'] = metrics_result
        else:
            print("Skipping derived metrics - no dimensional scores available")
            results['derived_metrics'] = {}
        
        return results
    
    def _make_scoring_call(self, framework_content: str, document_content: str, document_id: str, tools: List[Dict]) -> Dict[str, Any]:
        """Make tool call for dimensional scoring using Flash."""
        
        prompt = f"""You are an expert discourse analyst. Analyze the document using the provided framework and make exactly 1 tool call to record_analysis_scores.

**ANALYSIS REQUIREMENTS:**
- Apply the framework's dimensional definitions precisely
- Score each dimension on a 0.0-1.0 scale for intensity, salience, and confidence
- Use the document_id provided: {document_id}
- Ensure all dimension names match the framework exactly

**FRAMEWORK:**
{framework_content}

**DOCUMENT:**
{document_content}

Make the record_analysis_scores tool call now."""

        response = self.gateway.execute_call_with_tools(
            prompt=prompt,
            model="vertex_ai/gemini-2.5-flash",
            tools=tools,
            max_tokens=4000
        )
        
        # Handle tuple response format
        if isinstance(response, tuple):
            content, metadata = response
        else:
            content = response.get('content', '')
            metadata = response.get('metadata', {})
        
        # Extract tool call results
        print(f"DEBUG: metadata keys: {list(metadata.keys())}")
        if 'tool_calls' in metadata and metadata['tool_calls'] is not None:
            tool_calls = metadata['tool_calls']
            print(f"DEBUG: Found {len(tool_calls)} tool calls")
            if tool_calls and len(tool_calls) > 0:
                tool_call = tool_calls[0]
                print(f"DEBUG: Tool call name: {tool_call.function.name}")
                print(f"DEBUG: Tool call arguments: {tool_call.function.arguments}")
                if tool_call.function.name == 'record_analysis_scores':
                    args = json.loads(tool_call.function.arguments)
                    print(f"DEBUG: Parsed args: {args}")
                    return args.get('dimensional_scores', {})
        else:
            print("DEBUG: No tool_calls in metadata or tool_calls is None")
        
        return {}
    
    def _make_evidence_call(self, framework_content: str, document_content: str, document_id: str, tools: List[Dict]) -> List[Dict[str, Any]]:
        """Make tool call for evidence gathering using Flash."""
        
        prompt = f"""You are an expert discourse analyst. Analyze the document using the provided framework and make exactly 1 tool call to record_evidence_quotes.

**EVIDENCE REQUIREMENTS:**
- Find specific textual evidence for each dimension
- Provide quotes with context and relevance scores
- Use the document_id provided: {document_id}
- Ensure all dimension names match the framework exactly

**FRAMEWORK:**
{framework_content}

**DOCUMENT:**
{document_content}

Make the record_evidence_quotes tool call now."""

        response = self.gateway.execute_call_with_tools(
            prompt=prompt,
            model="vertex_ai/gemini-2.5-flash",
            tools=tools,
            max_tokens=4000
        )
        
        # Handle tuple response format
        if isinstance(response, tuple):
            content, metadata = response
        else:
            content = response.get('content', '')
            metadata = response.get('metadata', {})
        
        # Extract tool call results
        if 'tool_calls' in metadata and metadata['tool_calls'] is not None:
            tool_calls = metadata['tool_calls']
            if tool_calls and len(tool_calls) > 0:
                tool_call = tool_calls[0]
                if tool_call.function.name == 'record_evidence_quotes':
                    args = json.loads(tool_call.function.arguments)
                    return args.get('evidence_quotes', [])
        
        return []
    
    def _calculate_derived_metrics(self, framework_path: Path, dimensional_scores: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate derived metrics using Flash Lite (THIN approach)."""
        
        # Load framework
        with open(framework_path, 'r') as f:
            content = f.read()
        
        yaml_match = re.search(r'```yaml\n(.*?)\n```', content, re.DOTALL)
        if not yaml_match:
            raise ValueError("No YAML found in framework file")
        
        framework_data = yaml.safe_load(yaml_match.group(1))
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
    """Test the hybrid analysis agent."""
    
    # Set up paths
    experiment_dir = Path("/Volumes/code/discernus/test_thin_approach")
    framework_path = experiment_dir / "framework" / "pdaf_v10.md"
    document_path = experiment_dir / "experiment" / "Trump_SOTU_2020.txt"
    
    # Test the hybrid agent
    print("=== Testing Hybrid Analysis Agent ===")
    print("Using Flash for tool calling (scores + evidence)")
    print("Using Flash Lite for derived metrics calculation")
    print()
    
    agent = HybridAnalysisAgent(experiment_dir=experiment_dir)
    
    results = agent.analyze_document(
        framework_path=framework_path,
        document_path=document_path,
        document_id="trump_sotu_2020"
    )
    
    # Save results
    with open(experiment_dir / "artifacts" / "hybrid_results.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to {experiment_dir / 'artifacts' / 'hybrid_results.json'}")
    print(f"Dimensional scores: {len(results.get('dimensional_scores', {}))}")
    print(f"Evidence quotes: {len(results.get('evidence_quotes', []))}")
    print(f"Derived metrics: {len(results.get('derived_metrics', {}).get('derived_metrics', {}))}")
    
    # Show sample results
    if results.get('dimensional_scores'):
        print(f"\nSample dimensional scores:")
        for key, value in list(results['dimensional_scores'].items())[:3]:
            print(f"  {key}: {value['raw_score']:.1f} (salience: {value['salience']:.1f})")
    
    if results.get('derived_metrics', {}).get('derived_metrics'):
        print(f"\nSample derived metrics:")
        for key, value in list(results['derived_metrics']['derived_metrics'].items())[:3]:
            print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
