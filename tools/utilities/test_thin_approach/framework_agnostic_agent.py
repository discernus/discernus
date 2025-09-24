#!/usr/bin/env python3
"""
Framework-Agnostic Tool Calling Agent

This agent reads tool calling schemas from frameworks and makes sequential tool calls
for dimensional scoring, evidence gathering, and computational work.
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


class FrameworkAgnosticToolCallingAgent:
    """Framework-agnostic agent that uses tool calling schemas from frameworks."""
    
    def __init__(self, experiment_dir: Path, model_name: str = "vertex_ai/gemini-2.5-flash"):
        self.experiment_dir = experiment_dir
        self.model_name = model_name
        
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
        """Analyze document using framework's tool calling schema."""
        
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
        
        # Step 1: Dimensional Scoring
        print("Step 1: Making dimensional scoring call...")
        scores_result = self._make_scoring_call(framework_content, document_content, document_id, tools)
        results['dimensional_scores'] = scores_result
        
        # Step 2: Evidence Gathering
        print("Step 2: Making evidence gathering call...")
        evidence_result = self._make_evidence_call(framework_content, document_content, document_id, tools)
        results['evidence_quotes'] = evidence_result
        
        # Step 3: Computational Work
        print("Step 3: Making computational work call...")
        work_result = self._make_work_call(framework_content, document_content, document_id, tools)
        results['computational_work'] = work_result
        
        return results
    
    def _make_scoring_call(self, framework_content: str, document_content: str, document_id: str, tools: List[Dict]) -> Dict[str, Any]:
        """Make tool call for dimensional scoring."""
        
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
            model=self.model_name,
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
        """Make tool call for evidence gathering."""
        
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
            model=self.model_name,
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
                if tool_call.function.name == 'record_evidence_quotes':
                    args = json.loads(tool_call.function.arguments)
                    print(f"DEBUG: Parsed args: {args}")
                    return args.get('evidence_quotes', [])
        else:
            print("DEBUG: No tool_calls in metadata or tool_calls is None")
        
        return []
    
    def _make_work_call(self, framework_content: str, document_content: str, document_id: str, tools: List[Dict]) -> Dict[str, Any]:
        """Make tool call for computational work."""
        
        prompt = f"""You are an expert discourse analyst. Analyze the document using the provided framework and make exactly 1 tool call to record_computational_work.

**COMPUTATIONAL REQUIREMENTS:**
- Generate Python code to calculate all derived metrics
- Provide statistical analysis and insights
- Use the document_id provided: {document_id}
- Ensure all metric names match the framework exactly

**FRAMEWORK:**
{framework_content}

**DOCUMENT:**
{document_content}

Make the record_computational_work tool call now."""

        response = self.gateway.execute_call_with_tools(
            prompt=prompt,
            model=self.model_name,
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
                if tool_call.function.name == 'record_computational_work':
                    args = json.loads(tool_call.function.arguments)
                    print(f"DEBUG: Parsed args: {args}")
                    return args.get('computational_work', {})
        else:
            print("DEBUG: No tool_calls in metadata or tool_calls is None")
        
        return {}


def main():
    """Test the framework-agnostic tool calling agent."""
    
    # Set up paths
    experiment_dir = Path("/Volumes/code/discernus/test_tool_calling_prototype")
    framework_path = experiment_dir / "framework" / "pdaf_v10.md"
    document_path = experiment_dir / "experiment" / "Trump_SOTU_2020.txt"
    
    # Test with Flash
    print("=== Testing with Gemini 2.5 Flash ===")
    agent_flash = FrameworkAgnosticToolCallingAgent(
        experiment_dir=experiment_dir,
        model_name="vertex_ai/gemini-2.5-flash"
    )
    
    results_flash = agent_flash.analyze_document(
        framework_path=framework_path,
        document_path=document_path,
        document_id="trump_sotu_2020"
    )
    
    # Save results
    with open(experiment_dir / "artifacts" / "results_flash.json", 'w') as f:
        json.dump(results_flash, f, indent=2)
    
    print(f"Flash results saved to {experiment_dir / 'artifacts' / 'results_flash.json'}")
    print(f"Dimensional scores: {len(results_flash.get('dimensional_scores', {}))}")
    print(f"Evidence quotes: {len(results_flash.get('evidence_quotes', []))}")
    print(f"Computational work keys: {list(results_flash.get('computational_work', {}).keys())}")
    
    # Test with Pro
    print("\n=== Testing with Gemini 2.5 Pro ===")
    agent_pro = FrameworkAgnosticToolCallingAgent(
        experiment_dir=experiment_dir,
        model_name="vertex_ai/gemini-2.5-pro"
    )
    
    results_pro = agent_pro.analyze_document(
        framework_path=framework_path,
        document_path=document_path,
        document_id="trump_sotu_2020"
    )
    
    # Save results
    with open(experiment_dir / "artifacts" / "results_pro.json", 'w') as f:
        json.dump(results_pro, f, indent=2)
    
    print(f"Pro results saved to {experiment_dir / 'artifacts' / 'results_pro.json'}")
    print(f"Dimensional scores: {len(results_pro.get('dimensional_scores', {}))}")
    print(f"Evidence quotes: {len(results_pro.get('evidence_quotes', []))}")
    print(f"Computational work keys: {list(results_pro.get('computational_work', {}).keys())}")


if __name__ == "__main__":
    main()
