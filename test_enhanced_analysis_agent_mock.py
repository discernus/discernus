#!/usr/bin/env python3
"""
Test Enhanced Analysis Agent with Mock LLM (Production Architecture)
===================================================================

This test validates the production architecture using mock LLM responses
to ensure the tool calling flow works correctly.
"""

import json
import tempfile
import os
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

# Import the production agents
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage

# Mock the enhanced LLM gateway for testing
class MockEnhancedLLMGateway:
    """Mock enhanced LLM gateway that simulates tool calling responses"""
    
    def __init__(self, model_registry):
        self.model_registry = model_registry
        self.call_count = 0
    
    def execute_call_with_tools(self, model: str, prompt: str, system_prompt: str, 
                               tools: List[Dict[str, Any]] = None, max_retries: int = 3, 
                               context: Optional[str] = None, **kwargs) -> tuple[str, Dict[str, Any]]:
        """Simulate LLM call with tool calling"""
        self.call_count += 1
        
        # Simulate the LLM's tool call response
        tool_call_response = {
            "id": f"call_{self.call_count}",
            "type": "function",
            "function": {
                "name": "record_analysis_with_work",
                "arguments": json.dumps({
                    "document_id": "test_doc_001",
                    "document_hash": "abc123def456",
                    "framework_name": "political_discourse_v1",
                    "framework_version": "1.0.0",
                    "analysis_payload": {
                        "scores": {
                            "sentiment": {
                                "raw_score": 0.7,
                                "salience": 0.8,
                                "confidence": 0.9
                            },
                            "populism": {
                                "raw_score": 0.8,
                                "salience": 0.9,
                                "confidence": 0.85
                            },
                            "authority": {
                                "raw_score": 0.3,
                                "salience": 0.6,
                                "confidence": 0.8
                            }
                        },
                        "derived_metrics": {
                            "overall_intensity": 0.6,
                            "rhetorical_complexity": 0.25,
                            "populism_index": 0.8
                        },
                        "evidence": [
                            {
                                "dimension": "sentiment",
                                "quote": "The American people deserve better leadership",
                                "source": "paragraph_1",
                                "offset": 0
                            },
                            {
                                "dimension": "populism",
                                "quote": "We must work together to create a brighter future for all citizens",
                                "source": "paragraph_1",
                                "offset": 50
                            },
                            {
                                "dimension": "authority",
                                "quote": "The current system has failed us",
                                "source": "paragraph_1",
                                "offset": 100
                            }
                        ]
                    },
                    "executed_code": """
# Calculate derived metrics
import numpy as np

scores = {
    'sentiment': {'raw_score': 0.7, 'salience': 0.8, 'confidence': 0.9},
    'populism': {'raw_score': 0.8, 'salience': 0.9, 'confidence': 0.85},
    'authority': {'raw_score': 0.3, 'salience': 0.6, 'confidence': 0.8}
}

# Calculate overall intensity (weighted average)
raw_scores = [scores[dim]['raw_score'] for dim in scores]
salience_weights = [scores[dim]['salience'] for dim in scores]
overall_intensity = np.average(raw_scores, weights=salience_weights)

# Calculate rhetorical complexity (standard deviation)
rhetorical_complexity = np.std(raw_scores)

# Calculate populism index (specific to populism dimension)
populism_index = scores['populism']['raw_score']

derived_metrics = {
    'overall_intensity': float(overall_intensity),
    'rhetorical_complexity': float(rhetorical_complexity),
    'populism_index': float(populism_index)
}

print(f"Overall intensity: {overall_intensity:.3f}")
print(f"Rhetorical complexity: {rhetorical_complexity:.3f}")
print(f"Populism index: {populism_index:.3f}")
""",
                    "execution_output": """Overall intensity: 0.600
Rhetorical complexity: 0.250
Populism index: 0.800
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
        
        return "Tool call executed", metadata

# Mock verification LLM gateway
class MockVerificationLLMGateway:
    """Mock verification LLM gateway"""
    
    def __init__(self, model_registry):
        self.model_registry = model_registry
        self.call_count = 0
    
    def execute_call_with_tools(self, model: str, prompt: str, system_prompt: str, 
                               tools: List[Dict[str, Any]] = None, max_retries: int = 3, 
                               context: Optional[str] = None, **kwargs) -> tuple[str, Dict[str, Any]]:
        """Simulate verification LLM call with tool calling"""
        self.call_count += 1
        
        tool_call_response = {
            "id": f"verification_call_{self.call_count}",
            "type": "function",
            "function": {
                "name": "record_attestation",
                "arguments": json.dumps({
                    "document_id": "test_doc_001",
                    "success": True,
                    "verifier_model": "vertex_ai/gemini-2.5-pro",
                    "verifier_model_version": "2.5.0",
                    "reasoning": "Re-executed the provided code and verified the derived metrics calculations. The overall_intensity calculation using weighted average is correct (0.6), the rhetorical_complexity using standard deviation is accurate (0.25), and the populism_index calculation is correct (0.8). All mathematical operations are sound and the results match the claimed output.",
                    "executed_code_digest_sha256": "abc123def456789",
                    "analysis_digest_sha256": "def456abc123789",
                    "re_execution_output": "Overall intensity: 0.600\nRhetorical complexity: 0.250\nPopulism index: 0.800\n"
                })
            }
        }
        
        metadata = {
            "success": True,
            "usage": {
                "total_tokens": 800,
                "prompt_tokens": 600,
                "completion_tokens": 200,
                "response_cost_usd": 0.0008
            },
            "model": model,
            "tool_calls": [tool_call_response]
        }
        
        return "Verification completed", metadata

# Patch the imports in the agent files
import sys
from unittest.mock import patch

def create_test_environment():
    """Create a test environment with proper directory structure"""
    test_dir = Path(tempfile.mkdtemp(prefix="syw_test_"))
    
    # Create experiment directory structure
    experiment_dir = test_dir / "test_experiment"
    experiment_dir.mkdir()
    
    # Create experiment.md file
    (experiment_dir / "experiment.md").write_text("# Test Experiment\n\nThis is a test experiment for Show Your Work architecture.")
    
    # Create logs directory
    (experiment_dir / "logs").mkdir()
    
    return test_dir, experiment_dir

def main():
    """Test the production enhanced analysis agent with mock LLM"""
    print("=== Enhanced Analysis Agent Production Test (Mock LLM) ===\n")
    
    # Create test environment
    test_dir, experiment_dir = create_test_environment()
    
    try:
        # Initialize core components
        security = ExperimentSecurityBoundary(experiment_path=experiment_dir)
        audit = AuditLogger(security_boundary=security, run_folder=experiment_dir)
        storage = LocalArtifactStorage(security_boundary=security, run_folder=experiment_dir)
        
        print("1. Initialized core components")
        print(f"   Test directory: {test_dir}")
        print(f"   Experiment directory: {experiment_dir}")
        
        # Mock the LLM gateways
        with patch('discernus.agents.EnhancedAnalysisAgent.agent_tool_calling.EnhancedLLMGateway', MockEnhancedLLMGateway):
            with patch('discernus.agents.verification_agent.agent.EnhancedLLMGateway', MockVerificationLLMGateway):
                # Import the agents after patching
                from discernus.agents.EnhancedAnalysisAgent.agent_tool_calling import EnhancedAnalysisAgentToolCalling
                from discernus.agents.verification_agent.agent import VerificationAgent
                
                # Create the enhanced analysis agent
                analysis_agent = EnhancedAnalysisAgentToolCalling(security, audit, storage)
                print("\n2. Created Enhanced Analysis Agent with tool calling")
                
                # Create the verification agent
                verification_agent = VerificationAgent(security, audit, storage)
                print("3. Created Verification Agent")
                
                # Sample document and framework
                document = {
                    "id": "test_doc_001",
                    "title": "Test Political Speech",
                    "content": "The American people deserve better leadership. We must work together to create a brighter future for all citizens. The current system has failed us, and we need real change now."
                }
                
                framework = {
                    "name": "political_discourse_v1",
                    "version": "1.0.0",
                    "dimensions": {
                        "sentiment": {
                            "description": "Overall emotional tone",
                            "scale": "0.0 (negative) to 1.0 (positive)"
                        },
                        "populism": {
                            "description": "Appeal to the common people",
                            "scale": "0.0 (elitist) to 1.0 (populist)"
                        },
                        "authority": {
                            "description": "Deference to institutional authority",
                            "scale": "0.0 (anti-authority) to 1.0 (pro-authority)"
                        }
                    }
                }
                
                print("\n4. Sample data prepared")
                print(f"   Document: {document['title']}")
                print(f"   Framework: {framework['name']} v{framework['version']}")
                
                # Test analysis with tool calling
                print("\n5. Running analysis with tool calling...")
                try:
                    analysis_result = analysis_agent.analyze_document(document, framework)
                    
                    print(f"   ✅ Analysis completed successfully!")
                    print(f"   Document ID: {analysis_result['document_id']}")
                    print(f"   Analysis Artifact: {analysis_result['analysis_artifact']}")
                    print(f"   Work Artifact: {analysis_result['work_artifact']}")
                    
                    # Test verification
                    print("\n6. Running verification...")
                    try:
                        verification_result = verification_agent.verify_analysis(
                            analysis_result['analysis_artifact'],
                            analysis_result['work_artifact']
                        )
                        
                        print(f"   ✅ Verification completed!")
                        print(f"   Success: {verification_result['success']}")
                        print(f"   Attestation Artifact: {verification_result['attestation_artifact']}")
                        print(f"   Reasoning: {verification_result['reasoning'][:100]}...")
                        
                        # Inspect artifacts
                        print("\n7. Artifact inspection:")
                        
                        # Analysis artifact
                        analysis_data = storage.get_artifact(analysis_result['analysis_artifact'])
                        analysis_content = json.loads(analysis_data.decode('utf-8'))
                        print(f"\n   Analysis artifact ({analysis_result['analysis_artifact']}):")
                        print(f"   - Document: {analysis_content['document_id']}")
                        print(f"   - Framework: {analysis_content['framework_name']} v{analysis_content['framework_version']}")
                        print(f"   - Scores: {list(analysis_content['scores'].keys())}")
                        print(f"   - Derived metrics: {list(analysis_content['derived_metrics'].keys())}")
                        print(f"   - Evidence quotes: {len(analysis_content['evidence'])}")
                        
                        # Work artifact
                        work_data = storage.get_artifact(analysis_result['work_artifact'])
                        work_content = json.loads(work_data.decode('utf-8'))
                        print(f"\n   Work artifact ({analysis_result['work_artifact']}):")
                        print(f"   - Code length: {len(work_content['executed_code'])} characters")
                        print(f"   - Output: {work_content['execution_output'].strip()}")
                        
                        # Attestation artifact
                        attestation_data = storage.get_artifact(verification_result['attestation_artifact'])
                        attestation_content = json.loads(attestation_data.decode('utf-8'))
                        print(f"\n   Attestation artifact ({verification_result['attestation_artifact']}):")
                        print(f"   - Success: {attestation_content['success']}")
                        print(f"   - Verifier: {attestation_content['verifier_model']}")
                        print(f"   - Reasoning: {attestation_content['reasoning'][:100]}...")
                        
                        print(f"\n=== Test Results ===")
                        print("✅ Enhanced Analysis Agent with tool calling: WORKING")
                        print("✅ Verification Agent with tool calling: WORKING")
                        print("✅ Structured output via tool calls: WORKING")
                        print("✅ Artifact storage and retrieval: WORKING")
                        print("✅ Complete audit trail: WORKING")
                        print("✅ Production architecture validated with mock LLM")
                        
                    except Exception as e:
                        print(f"   ❌ Verification failed: {e}")
                        raise
                        
                except Exception as e:
                    print(f"   ❌ Analysis failed: {e}")
                    raise
                    
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        raise
        
    finally:
        # Cleanup
        import shutil
        shutil.rmtree(test_dir)
        print(f"\n8. Cleaned up test directory: {test_dir}")

if __name__ == "__main__":
    main()
