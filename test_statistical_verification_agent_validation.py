#!/usr/bin/env python3
"""
Test Statistical Verification Agent with mock LLM responses
===========================================================

This test validates the Statistical Verification Agent architecture using mock LLM responses
to ensure the tool-calling flow works correctly before integration testing.
"""

import json
import tempfile
from pathlib import Path
from typing import Dict, Any, List

from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.agents.statistical_verification.agent import StatisticalVerificationAgent


class MockEnhancedLLMGateway:
    """Mock LLM Gateway that returns predictable tool calls for testing"""
    
    def __init__(self, model_registry):
        self.model_registry = model_registry
    
    def execute_call_with_tools(self, model: str, prompt: str, system_prompt: str, 
                               tools: List[Dict], context: str = None) -> tuple:
        """Mock LLM call that returns a statistical verification tool call"""
        
        # Simulate successful statistical verification
        mock_tool_call = {
            "function": {
                "name": "record_statistical_attestation",
                "arguments": json.dumps({
                    "success": True,
                    "verifier_model": model,
                    "verifier_model_version": "1.0.0",
                    "reasoning": "Statistical verification successful. All calculations verified as mathematically correct. ANOVA F-statistics, correlation coefficients, and Cronbach's alpha values match expected results within acceptable precision. CSV data generation is correct and properly formatted. No statistical methodology issues found.",
                    "executed_code_digest_sha256": "stat123abc456",
                    "statistics_digest_sha256": "stats456def789",
                    "re_execution_output": "Statistical verification successful - all results match claimed output"
                })
            }
        }
        
        return "Mock statistical verification response", {
            "success": True,
            "tool_calls": [mock_tool_call],
            "usage": {"input_tokens": 1500, "output_tokens": 300}
        }


def test_statistical_verification_agent_validation():
    """Test Statistical Verification Agent with mock LLM responses"""
    
    print("🧪 Testing Statistical Verification Agent Architecture")
    print("=" * 60)
    
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
        
        # Create test statistical artifacts
        statistics_data = {
            "anova_results": {
                "F_statistic": 15.2,
                "p_value": 0.001,
                "df_between": 2,
                "df_within": 27
            },
            "correlation_matrix": {
                "populism_authoritarianism": 0.75,
                "populism_nationalism": 0.68
            },
            "reliability_analysis": {
                "cronbach_alpha": 0.89,
                "n_items": 5
            }
        }
        
        work_data = {
            "executed_code": """
import pandas as pd
import numpy as np
from scipy import stats

# Simulate ANOVA calculation
data = np.random.normal(0.5, 0.2, 30)
groups = np.repeat([0, 1, 2], 10)
f_stat, p_val = stats.f_oneway(data[groups==0], data[groups==1], data[groups==2])

# Simulate correlation
corr_matrix = np.corrcoef([0.8, 0.7, 0.6], [0.75, 0.65, 0.55])

# Simulate Cronbach's alpha
alpha = 0.89

print(f"ANOVA F-statistic: {f_stat:.1f}")
print(f"ANOVA p-value: {p_val:.3f}")
print(f"Correlation: {corr_matrix[0,1]:.2f}")
print(f"Cronbach's alpha: {alpha:.2f}")
""",
            "execution_output": "ANOVA F-statistic: 15.2\nANOVA p-value: 0.001\nCorrelation: 0.75\nCronbach's alpha: 0.89"
        }
        
        csv_data = """dimension,mean,std,count
populism,0.75,0.15,30
authoritarianism,0.68,0.18,30
nationalism,0.72,0.16,30"""
        
        # Store test artifacts
        statistics_artifact_id = artifact_storage.put_artifact(
            json.dumps(statistics_data).encode('utf-8'),
            {"artifact_type": "statistics", "analysis_type": "batch"}
        )
        
        work_artifact_id = artifact_storage.put_artifact(
            json.dumps(work_data).encode('utf-8'),
            {"artifact_type": "statistical_work", "analysis_type": "batch"}
        )
        
        csv_artifact_id = artifact_storage.put_artifact(
            csv_data.encode('utf-8'),
            {"artifact_type": "statistical_csv", "analysis_type": "batch"}
        )
        
        print(f"✅ Created test statistical artifacts:")
        print(f"   Statistics: {statistics_artifact_id}")
        print(f"   Work: {work_artifact_id}")
        print(f"   CSV: {csv_artifact_id}")
        
        # Initialize Statistical Verification Agent with mock gateway
        verification_agent = StatisticalVerificationAgent(security_boundary, audit_logger, artifact_storage)
        verification_agent.llm_gateway = MockEnhancedLLMGateway(None)
        
        print(f"✅ Initialized Statistical Verification Agent")
        
        # Test verification
        try:
            result = verification_agent.verify_statistical_analysis(
                statistics_artifact_id=statistics_artifact_id,
                work_artifact_id=work_artifact_id,
                csv_artifact_id=csv_artifact_id,
                model="openrouter/deepseek/deepseek-prover-v2"
            )
            
            print(f"✅ Statistical verification completed successfully")
            print(f"   Success: {result['success']}")
            print(f"   Attestation Artifact: {result['attestation_artifact']}")
            print(f"   Reasoning: {result['reasoning'][:100]}...")
            
            # Verify attestation artifact was created
            attestation_data = artifact_storage.get_artifact(result['attestation_artifact'])
            attestation_content = json.loads(attestation_data.decode('utf-8'))
            
            print(f"✅ Statistical attestation artifact verified:")
            print(f"   Success: {attestation_content['success']}")
            print(f"   Verifier Model: {attestation_content['verifier_model']}")
            print(f"   Timestamp: {attestation_content['timestamp']}")
            
            # Test model selection
            selected_model = verification_agent._select_verifier_model()
            print(f"✅ Model selection working: {selected_model}")
            
            print(f"\n🎉 Statistical Verification Agent validation PASSED")
            return True
            
        except Exception as e:
            print(f"❌ Statistical verification failed: {e}")
            import traceback
            traceback.print_exc()
            return False


def test_statistical_verification_agent_failure_case():
    """Test Statistical Verification Agent with a failure scenario"""
    
    print("\n🧪 Testing Statistical Verification Agent Failure Case")
    print("=" * 60)
    
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
        
        # Create test artifacts with incorrect statistical calculations
        statistics_data = {
            "anova_results": {
                "F_statistic": 25.0,  # This should be 15.2
                "p_value": 0.001,
                "df_between": 2,
                "df_within": 27
            }
        }
        
        work_data = {
            "executed_code": """
import numpy as np
from scipy import stats

# Simulate ANOVA calculation
data = np.random.normal(0.5, 0.2, 30)
groups = np.repeat([0, 1, 2], 10)
f_stat, p_val = stats.f_oneway(data[groups==0], data[groups==1], data[groups==2])

print(f"ANOVA F-statistic: {f_stat:.1f}")
""",
            "execution_output": "ANOVA F-statistic: 15.2"  # Correct output
        }
        
        csv_data = """dimension,mean,std,count
populism,0.75,0.15,30"""
        
        # Store test artifacts
        statistics_artifact_id = artifact_storage.put_artifact(
            json.dumps(statistics_data).encode('utf-8'),
            {"artifact_type": "statistics", "analysis_type": "batch"}
        )
        
        work_artifact_id = artifact_storage.put_artifact(
            json.dumps(work_data).encode('utf-8'),
            {"artifact_type": "statistical_work", "analysis_type": "batch"}
        )
        
        csv_artifact_id = artifact_storage.put_artifact(
            csv_data.encode('utf-8'),
            {"artifact_type": "statistical_csv", "analysis_type": "batch"}
        )
        
        # Mock gateway that detects the statistical error
        class MockFailureLLMGateway:
            def execute_call_with_tools(self, model, prompt, system_prompt, tools, context=None):
                mock_tool_call = {
                    "function": {
                        "name": "record_statistical_attestation",
                        "arguments": json.dumps({
                            "success": False,
                            "verifier_model": model,
                            "verifier_model_version": "1.0.0",
                            "reasoning": "STATISTICAL VERIFICATION FAILED: Analysis claims F-statistic=25.0 but code execution produces 15.2. Statistical calculation inconsistency detected. This invalidates the ANOVA results.",
                            "executed_code_digest_sha256": "stat123abc456",
                            "statistics_digest_sha256": "stats456def789",
                            "re_execution_output": "ANOVA F-statistic: 15.2"
                        })
                    }
                }
                
                return "Mock statistical verification response", {
                    "success": True,
                    "tool_calls": [mock_tool_call],
                    "usage": {"input_tokens": 1500, "output_tokens": 300}
                }
        
        # Initialize Statistical Verification Agent with failure mock
        verification_agent = StatisticalVerificationAgent(security_boundary, audit_logger, artifact_storage)
        verification_agent.llm_gateway = MockFailureLLMGateway()
        
        try:
            result = verification_agent.verify_statistical_analysis(
                statistics_artifact_id=statistics_artifact_id,
                work_artifact_id=work_artifact_id,
                csv_artifact_id=csv_artifact_id,
                model="openrouter/deepseek/deepseek-prover-v2"
            )
            
            print(f"✅ Statistical failure case verification completed")
            print(f"   Success: {result['success']} (should be False)")
            print(f"   Reasoning: {result['reasoning']}")
            
            if not result['success']:
                print(f"🎉 Statistical failure case correctly detected - verification PASSED")
                return True
            else:
                print(f"❌ Statistical failure case not detected - verification FAILED")
                return False
                
        except Exception as e:
            print(f"❌ Statistical failure case test failed: {e}")
            import traceback
            traceback.print_exc()
            return False


if __name__ == "__main__":
    print("🚀 Starting Statistical Verification Agent Validation Tests")
    print("=" * 70)
    
    success1 = test_statistical_verification_agent_validation()
    success2 = test_statistical_verification_agent_failure_case()
    
    if success1 and success2:
        print(f"\n🎉 ALL TESTS PASSED - Statistical Verification Agent is ready!")
    else:
        print(f"\n❌ SOME TESTS FAILED - Check implementation")
