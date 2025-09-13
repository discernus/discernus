#!/usr/bin/env python3
"""
Test VerificationAgent with mock LLM responses
==============================================

This test validates the VerificationAgent architecture using mock LLM responses
to ensure the tool-calling flow works correctly before integration testing.
"""

import json
import tempfile
from pathlib import Path
from typing import Dict, Any, List

from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.agents.verification_agent.agent import VerificationAgent


class MockEnhancedLLMGateway:
    """Mock LLM Gateway that returns predictable tool calls for testing"""
    
    def __init__(self, model_registry):
        self.model_registry = model_registry
    
    def execute_call_with_tools(self, model: str, prompt: str, system_prompt: str, 
                               tools: List[Dict], context: str = None) -> tuple:
        """Mock LLM call that returns a verification tool call"""
        
        # Simulate successful verification
        mock_tool_call = {
            "function": {
                "name": "record_attestation",
                "arguments": json.dumps({
                    "document_id": "test_doc_123",
                    "success": True,
                    "verifier_model": model,
                    "verifier_model_version": "1.0.0",
                    "reasoning": "Code re-execution successful. All calculations verified as mathematically correct. Derived metrics calculations match expected results within acceptable precision. No logical errors or methodological issues found.",
                    "executed_code_digest_sha256": "abc123def456",
                    "analysis_digest_sha256": "def456ghi789",
                    "re_execution_output": "Verification successful - results match claimed output"
                })
            }
        }
        
        return "Mock verification response", {
            "success": True,
            "tool_calls": [mock_tool_call],
            "usage": {"input_tokens": 1000, "output_tokens": 200}
        }


def test_verification_agent_validation():
    """Test VerificationAgent with mock LLM responses"""
    
    print("🧪 Testing VerificationAgent Architecture")
    print("=" * 50)
    
    # Setup test environment
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create experiment structure
        experiment_dir = temp_path / "test_experiment"
        experiment_dir.mkdir()
        (experiment_dir / "logs").mkdir()
        (experiment_dir / "experiment.md").write_text("# Test Experiment")
        
        # Initialize components
        security_boundary = ExperimentSecurityBoundary(experiment_path=experiment_dir)
        audit_logger = AuditLogger(security_boundary, experiment_dir)
        run_folder = experiment_dir / "run_001"
        run_folder.mkdir()
        artifact_storage = LocalArtifactStorage(security_boundary, run_folder)
        
        # Create test artifacts
        analysis_data = {
            "document_id": "test_doc_123",
            "dimensional_scores": {
                "populism": {"raw_score": 0.8, "salience": 0.9, "confidence": 0.85},
                "authoritarianism": {"raw_score": 0.7, "salience": 0.8, "confidence": 0.9}
            },
            "derived_metrics": {
                "overall_intensity": 0.75,
                "rhetorical_complexity": 0.15
            }
        }
        
        work_data = {
            "executed_code": """
import numpy as np
scores = [0.8, 0.7]
overall_intensity = np.mean(scores)
rhetorical_complexity = np.std(scores)
print(f"Overall intensity: {overall_intensity}")
print(f"Rhetorical complexity: {rhetorical_complexity}")
""",
            "execution_output": "Overall intensity: 0.75\nRhetorical complexity: 0.05"
        }
        
        # Store test artifacts
        analysis_artifact_id = artifact_storage.put_artifact(
            json.dumps(analysis_data).encode('utf-8'),
            {"artifact_type": "analysis", "document_id": "test_doc_123"}
        )
        
        work_artifact_id = artifact_storage.put_artifact(
            json.dumps(work_data).encode('utf-8'),
            {"artifact_type": "work", "document_id": "test_doc_123"}
        )
        
        print(f"✅ Created test artifacts:")
        print(f"   Analysis: {analysis_artifact_id}")
        print(f"   Work: {work_artifact_id}")
        
        # Initialize VerificationAgent with mock gateway
        verification_agent = VerificationAgent(security_boundary, audit_logger, artifact_storage)
        verification_agent.llm_gateway = MockEnhancedLLMGateway(None)
        
        print(f"✅ Initialized VerificationAgent")
        
        # Test verification
        try:
            result = verification_agent.verify_analysis(
                analysis_artifact_id=analysis_artifact_id,
                work_artifact_id=work_artifact_id,
                model="openrouter/deepseek/deepseek-prover-v2"
            )
            
            print(f"✅ Verification completed successfully")
            print(f"   Document ID: {result['document_id']}")
            print(f"   Success: {result['success']}")
            print(f"   Attestation Artifact: {result['attestation_artifact']}")
            print(f"   Reasoning: {result['reasoning'][:100]}...")
            
            # Verify attestation artifact was created
            attestation_data = artifact_storage.get_artifact(result['attestation_artifact'])
            attestation_content = json.loads(attestation_data.decode('utf-8'))
            
            print(f"✅ Attestation artifact verified:")
            print(f"   Success: {attestation_content['success']}")
            print(f"   Verifier Model: {attestation_content['verifier_model']}")
            print(f"   Timestamp: {attestation_content['timestamp']}")
            
            # Test model selection
            selected_model = verification_agent._select_verifier_model()
            print(f"✅ Model selection working: {selected_model}")
            
            print(f"\n🎉 VerificationAgent validation PASSED")
            return True
            
        except Exception as e:
            print(f"❌ Verification failed: {e}")
            import traceback
            traceback.print_exc()
            return False


def test_verification_agent_failure_case():
    """Test VerificationAgent with a failure scenario"""
    
    print("\n🧪 Testing VerificationAgent Failure Case")
    print("=" * 50)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create experiment structure
        experiment_dir = temp_path / "test_experiment"
        experiment_dir.mkdir()
        (experiment_dir / "logs").mkdir()
        (experiment_dir / "experiment.md").write_text("# Test Experiment")
        
        # Initialize components
        security_boundary = ExperimentSecurityBoundary(experiment_path=experiment_dir)
        audit_logger = AuditLogger(security_boundary, experiment_dir)
        run_folder = experiment_dir / "run_001"
        run_folder.mkdir()
        artifact_storage = LocalArtifactStorage(security_boundary, run_folder)
        
        # Create test artifacts with incorrect calculations
        analysis_data = {
            "document_id": "test_doc_456",
            "dimensional_scores": {
                "populism": {"raw_score": 0.8, "salience": 0.9, "confidence": 0.85}
            },
            "derived_metrics": {
                "overall_intensity": 0.9  # This should be 0.8, not 0.9
            }
        }
        
        work_data = {
            "executed_code": """
import numpy as np
scores = [0.8]
overall_intensity = np.mean(scores)
print(f"Overall intensity: {overall_intensity}")
""",
            "execution_output": "Overall intensity: 0.8"  # Correct output
        }
        
        # Store test artifacts
        analysis_artifact_id = artifact_storage.put_artifact(
            json.dumps(analysis_data).encode('utf-8'),
            {"artifact_type": "analysis", "document_id": "test_doc_456"}
        )
        
        work_artifact_id = artifact_storage.put_artifact(
            json.dumps(work_data).encode('utf-8'),
            {"artifact_type": "work", "document_id": "test_doc_456"}
        )
        
        # Mock gateway that detects the error
        class MockFailureLLMGateway:
            def execute_call_with_tools(self, model, prompt, system_prompt, tools, context=None):
                mock_tool_call = {
                    "function": {
                        "name": "record_attestation",
                        "arguments": json.dumps({
                            "document_id": "test_doc_456",
                            "success": False,
                            "verifier_model": model,
                            "verifier_model_version": "1.0.0",
                            "reasoning": "VERIFICATION FAILED: Analysis claims overall_intensity=0.9 but code execution produces 0.8. Mathematical inconsistency detected.",
                            "executed_code_digest_sha256": "abc123def456",
                            "analysis_digest_sha256": "def456ghi789",
                            "re_execution_output": "Overall intensity: 0.8"
                        })
                    }
                }
                
                return "Mock verification response", {
                    "success": True,
                    "tool_calls": [mock_tool_call],
                    "usage": {"input_tokens": 1000, "output_tokens": 200}
                }
        
        # Initialize VerificationAgent with failure mock
        verification_agent = VerificationAgent(security_boundary, audit_logger, artifact_storage)
        verification_agent.llm_gateway = MockFailureLLMGateway()
        
        try:
            result = verification_agent.verify_analysis(
                analysis_artifact_id=analysis_artifact_id,
                work_artifact_id=work_artifact_id,
                model="openrouter/deepseek/deepseek-prover-v2"
            )
            
            print(f"✅ Failure case verification completed")
            print(f"   Document ID: {result['document_id']}")
            print(f"   Success: {result['success']} (should be False)")
            print(f"   Reasoning: {result['reasoning']}")
            
            if not result['success']:
                print(f"🎉 Failure case correctly detected - verification PASSED")
                return True
            else:
                print(f"❌ Failure case not detected - verification FAILED")
                return False
                
        except Exception as e:
            print(f"❌ Failure case test failed: {e}")
            import traceback
            traceback.print_exc()
            return False


if __name__ == "__main__":
    print("🚀 Starting VerificationAgent Validation Tests")
    print("=" * 60)
    
    success1 = test_verification_agent_validation()
    success2 = test_verification_agent_failure_case()
    
    if success1 and success2:
        print(f"\n🎉 ALL TESTS PASSED - VerificationAgent is ready!")
    else:
        print(f"\n❌ SOME TESTS FAILED - Check implementation")
