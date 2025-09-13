#!/usr/bin/env python3
"""
Prototype: Enhanced Analysis Agent with Tool Calling
===================================================

This prototype demonstrates the new "Show Your Work" architecture using
structured output via tool calling instead of text parsing.
"""

import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional
import tempfile
import os

# Mock the core dependencies for the prototype
class MockSecurityBoundary:
    def get_boundary_info(self):
        return {"experiment_id": "test_experiment", "run_id": "test_run"}

class MockAuditLogger:
    def __init__(self):
        self.session_id = "test_session"
        self.events = []
    
    def log_agent_event(self, agent_name: str, event_type: str, data: Dict[str, Any]):
        self.events.append({
            "agent": agent_name,
            "event": event_type,
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        print(f"[AUDIT] {agent_name}: {event_type} - {data}")
    
    def log_llm_interaction(self, model: str, prompt: str, response: str, 
                          agent_name: str, interaction_type: str, metadata: Dict[str, Any]):
        self.events.append({
            "agent": agent_name,
            "event": "llm_interaction",
            "model": model,
            "interaction_type": interaction_type,
            "metadata": metadata,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        print(f"[AUDIT] LLM Call: {model} - {interaction_type}")

class MockArtifactStorage:
    def __init__(self):
        self.artifacts = {}
    
    def put_artifact(self, content: bytes, metadata: Dict[str, Any]) -> str:
        content_hash = hashlib.sha256(content).hexdigest()
        self.artifacts[content_hash] = {
            "content": content,
            "metadata": metadata
        }
        return content_hash
    
    def get_artifact(self, artifact_id: str) -> Dict[str, Any]:
        return self.artifacts.get(artifact_id, {})

class MockLLMGateway:
    """Mock LLM Gateway that simulates tool calling responses"""
    
    def __init__(self):
        self.call_count = 0
    
    def execute_call_with_tools(self, model: str, prompt: str, system_prompt: str, 
                               tools: List[Dict[str, Any]]) -> tuple[str, Dict[str, Any]]:
        """Simulate LLM call with tool calling"""
        self.call_count += 1
        
        # Simulate the LLM's tool call response
        # In reality, this would be the actual LLM response
        tool_call_response = {
            "id": f"call_{self.call_count}",
            "type": "function",
            "function": {
                "name": "record_analysis_with_work",
                "arguments": json.dumps({
                    "document_id": "doc_001",
                    "document_hash": "abc123def456",
                    "framework_name": "test_framework",
                    "framework_version": "1.0.0",
                    "analysis_payload": {
                        "scores": {
                            "sentiment": {
                                "raw_score": 0.8,
                                "salience": 0.9,
                                "confidence": 0.95
                            },
                            "populism": {
                                "raw_score": 0.6,
                                "salience": 0.7,
                                "confidence": 0.85
                            }
                        },
                        "derived_metrics": {
                            "overall_intensity": 0.7,
                            "rhetorical_complexity": 0.65
                        },
                        "evidence": [
                            {
                                "dimension": "sentiment",
                                "quote": "This is a great example of positive sentiment",
                                "source": "paragraph_2",
                                "offset": 45
                            },
                            {
                                "dimension": "populism",
                                "quote": "The people deserve better representation",
                                "source": "paragraph_5",
                                "offset": 120
                            }
                        ]
                    },
                    "executed_code": """
# Calculate derived metrics
import numpy as np

scores = {
    'sentiment': {'raw_score': 0.8, 'salience': 0.9, 'confidence': 0.95},
    'populism': {'raw_score': 0.6, 'salience': 0.7, 'confidence': 0.85}
}

# Calculate overall intensity (weighted average)
raw_scores = [scores[dim]['raw_score'] for dim in scores]
salience_weights = [scores[dim]['salience'] for dim in scores]
overall_intensity = np.average(raw_scores, weights=salience_weights)

# Calculate rhetorical complexity (standard deviation)
rhetorical_complexity = np.std(raw_scores)

derived_metrics = {
    'overall_intensity': float(overall_intensity),
    'rhetorical_complexity': float(rhetorical_complexity)
}

print(f"Overall intensity: {overall_intensity:.3f}")
print(f"Rhetorical complexity: {rhetorical_complexity:.3f}")
""",
                    "execution_output": """Overall intensity: 0.700
Rhetorical complexity: 0.100
"""
                })
            }
        }
        
        # Simulate metadata
        metadata = {
            "success": True,
            "usage": {
                "total_tokens": 1500,
                "prompt_tokens": 1200,
                "completion_tokens": 300,
                "response_cost_usd": 0.0015
            },
            "model": model,
            "tool_calls": [tool_call_response]
        }
        
        return json.dumps(tool_call_response), metadata

class EnhancedAnalysisAgentToolCalling:
    """Prototype of Enhanced Analysis Agent using tool calling"""
    
    def __init__(self, security_boundary, audit_logger, artifact_storage):
        self.security = security_boundary
        self.audit = audit_logger
        self.storage = artifact_storage
        self.agent_name = "EnhancedAnalysisAgentToolCalling"
        self.llm_gateway = MockLLMGateway()
        
        self.audit.log_agent_event(self.agent_name, "initialization", {
            "capabilities": ["tool_calling", "derived_metrics", "structured_output"]
        })
    
    def analyze_document(self, document: Dict[str, Any], framework: Dict[str, Any], 
                        model: str = "vertex_ai/gemini-2.5-flash") -> Dict[str, Any]:
        """Analyze a single document using tool calling approach"""
        
        # Create analysis prompt
        prompt = self._create_analysis_prompt(document, framework)
        
        # Define the tool schema
        tools = [{
            "type": "function",
            "function": {
                "name": "record_analysis_with_work",
                "description": "Record analysis results with computational work",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "document_id": {"type": "string"},
                        "document_hash": {"type": "string"},
                        "framework_name": {"type": "string"},
                        "framework_version": {"type": "string"},
                        "analysis_payload": {
                            "type": "object",
                            "properties": {
                                "scores": {
                                    "type": "object",
                                    "additionalProperties": {
                                        "type": "object",
                                        "properties": {
                                            "raw_score": {"type": "number"},
                                            "salience": {"type": "number"},
                                            "confidence": {"type": "number"}
                                        }
                                    }
                                },
                                "derived_metrics": {
                                    "type": "object",
                                    "additionalProperties": {"type": "number"}
                                },
                                "evidence": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "dimension": {"type": "string"},
                                            "quote": {"type": "string"},
                                            "source": {"type": "string"},
                                            "offset": {"type": "integer"}
                                        }
                                    }
                                }
                            },
                            "required": ["scores", "derived_metrics"]
                        },
                        "executed_code": {"type": "string"},
                        "execution_output": {"type": "string"}
                    },
                    "required": ["document_id", "document_hash", "analysis_payload", 
                                "executed_code", "execution_output"]
                }
            }
        }]
        
        # Execute LLM call with tools
        system_prompt = "You are an expert discourse analyst. Analyze the document using the framework and call the record_analysis_with_work tool with your results and the code you executed."
        
        self.audit.log_agent_event(self.agent_name, "llm_call_start", {
            "model": model,
            "document_id": document.get("id", "unknown")
        })
        
        response_content, metadata = self.llm_gateway.execute_call_with_tools(
            model=model,
            prompt=prompt,
            system_prompt=system_prompt,
            tools=tools
        )
        
        # Parse the tool call response
        tool_call_data = json.loads(response_content)
        function_args = json.loads(tool_call_data["function"]["arguments"])
        
        # Save artifacts using the structured data (no parsing needed!)
        analysis_artifact = self._save_analysis_artifact(function_args)
        work_artifact = self._save_work_artifact(function_args)
        
        self.audit.log_agent_event(self.agent_name, "analysis_complete", {
            "document_id": function_args["document_id"],
            "analysis_artifact": analysis_artifact,
            "work_artifact": work_artifact
        })
        
        return {
            "document_id": function_args["document_id"],
            "analysis_artifact": analysis_artifact,
            "work_artifact": work_artifact,
            "metadata": metadata
        }
    
    def _create_analysis_prompt(self, document: Dict[str, Any], framework: Dict[str, Any]) -> str:
        """Create the analysis prompt for the LLM"""
        return f"""
Analyze the following document using the provided framework.

DOCUMENT:
Title: {document.get('title', 'Untitled')}
Content: {document.get('content', '')}

FRAMEWORK:
{json.dumps(framework, indent=2)}

INSTRUCTIONS:
1. Score each dimension in the framework (0.0-1.0 scale)
2. Calculate derived metrics using Python code
3. Provide specific evidence quotes
4. Call the record_analysis_with_work tool with your results

Execute your analysis code internally and provide both the results and the code in the tool call.
"""
    
    def _save_analysis_artifact(self, function_args: Dict[str, Any]) -> str:
        """Save the analysis results as a clean artifact"""
        analysis_data = {
            "document_id": function_args["document_id"],
            "document_hash": function_args["document_hash"],
            "framework_name": function_args["framework_name"],
            "framework_version": function_args["framework_version"],
            "scores": function_args["analysis_payload"]["scores"],
            "derived_metrics": function_args["analysis_payload"]["derived_metrics"],
            "evidence": function_args["analysis_payload"]["evidence"],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        content = json.dumps(analysis_data, indent=2).encode('utf-8')
        return self.storage.put_artifact(content, {
            "artifact_type": "analysis",
            "document_id": function_args["document_id"],
            "framework": function_args["framework_name"]
        })
    
    def _save_work_artifact(self, function_args: Dict[str, Any]) -> str:
        """Save the computational work as a separate artifact"""
        work_data = {
            "document_id": function_args["document_id"],
            "executed_code": function_args["executed_code"],
            "execution_output": function_args["execution_output"],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        content = json.dumps(work_data, indent=2).encode('utf-8')
        return self.storage.put_artifact(content, {
            "artifact_type": "work",
            "document_id": function_args["document_id"],
            "framework": function_args["framework_name"]
        })

def main():
    """Demonstrate the tool calling prototype"""
    print("=== Enhanced Analysis Agent Tool Calling Prototype ===\n")
    
    # Initialize mock dependencies
    security = MockSecurityBoundary()
    audit = MockAuditLogger()
    storage = MockArtifactStorage()
    
    # Create the agent
    agent = EnhancedAnalysisAgentToolCalling(security, audit, storage)
    
    # Sample document and framework
    document = {
        "id": "doc_001",
        "title": "Sample Political Speech",
        "content": "This is a great example of positive sentiment. The people deserve better representation and we must work together for change."
    }
    
    framework = {
        "name": "test_framework",
        "version": "1.0.0",
        "dimensions": {
            "sentiment": {
                "description": "Overall emotional tone",
                "scale": "0.0 (negative) to 1.0 (positive)"
            },
            "populism": {
                "description": "Appeal to the common people",
                "scale": "0.0 (elitist) to 1.0 (populist)"
            }
        }
    }
    
    print("1. Analyzing document with tool calling...")
    result = agent.analyze_document(document, framework)
    
    print(f"\n2. Analysis complete!")
    print(f"   Document ID: {result['document_id']}")
    print(f"   Analysis Artifact: {result['analysis_artifact']}")
    print(f"   Work Artifact: {result['work_artifact']}")
    
    print(f"\n3. Artifacts stored:")
    analysis_data = storage.get_artifact(result['analysis_artifact'])
    work_data = storage.get_artifact(result['work_artifact'])
    
    print(f"\n   Analysis artifact content:")
    print(json.dumps(json.loads(analysis_data['content']), indent=2))
    
    print(f"\n   Work artifact content:")
    print(json.dumps(json.loads(work_data['content']), indent=2))
    
    print(f"\n4. Audit log:")
    for event in audit.events:
        print(f"   {event['timestamp']}: {event['agent']} - {event['event']}")
    
    print(f"\n=== Key Benefits Demonstrated ===")
    print("✅ No string parsing - structured data from tool calls")
    print("✅ Clean artifact separation - analysis.json and work.json")
    print("✅ Derived metrics calculated by LLM internally")
    print("✅ Complete audit trail of all operations")
    print("✅ Fail-fast capability (verification can be added)")

if __name__ == "__main__":
    main()
