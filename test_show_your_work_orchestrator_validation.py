#!/usr/bin/env python3
"""
Test Show Your Work Orchestrator with mock components
====================================================

This test validates the ShowYourWorkOrchestrator architecture using mock agents
to ensure the workflow management works correctly before integration testing.
"""

import json
import tempfile
from pathlib import Path
from typing import Dict, Any, List

from discernus.core.show_your_work_orchestrator import ShowYourWorkOrchestrator


class MockEnhancedAnalysisAgent:
    """Mock Enhanced Analysis Agent for testing"""
    
    def __init__(self, security, audit, storage):
        self.security = security
        self.audit = audit
        self.storage = storage
    
    def analyze_document(self, framework_content: str, document_content: str, 
                        document_name: str, model: str) -> Dict[str, Any]:
        """Mock document analysis"""
        
        # Create mock analysis data
        analysis_data = {
            "document_id": f"doc_{hash(document_name) % 10000}",
            "document_name": document_name,
            "dimensional_scores": {
                "populism": {"raw_score": 0.8, "salience": 0.9, "confidence": 0.85},
                "authoritarianism": {"raw_score": 0.7, "salience": 0.8, "confidence": 0.9}
            },
            "derived_metrics": {
                "overall_intensity": 0.75,
                "rhetorical_complexity": 0.15
            },
            "evidence": [
                {
                    "dimension": "populism",
                    "quote_text": "The people are being betrayed by the elite",
                    "confidence": 0.9,
                    "context_type": "direct_statement"
                }
            ]
        }
        
        work_data = {
            "executed_code": "import numpy as np; scores = [0.8, 0.7]; overall_intensity = np.mean(scores)",
            "execution_output": "Overall intensity: 0.75"
        }
        
        # Store artifacts
        analysis_artifact_id = self.storage.put_artifact(
            json.dumps(analysis_data).encode('utf-8'),
            {"artifact_type": "analysis", "document_name": document_name}
        )
        
        work_artifact_id = self.storage.put_artifact(
            json.dumps(work_data).encode('utf-8'),
            {"artifact_type": "work", "document_name": document_name}
        )
        
        return {
            "success": True,
            "artifacts": [analysis_artifact_id, work_artifact_id]
        }


class MockVerificationAgent:
    """Mock Verification Agent for testing"""
    
    def __init__(self, security, audit, storage):
        self.security = security
        self.audit = audit
        self.storage = storage
    
    def verify_analysis(self, analysis_artifact_id: str, work_artifact_id: str, model: str = None) -> Dict[str, Any]:
        """Mock verification"""
        
        attestation_data = {
            "document_id": "test_doc",
            "success": True,
            "verifier_model": model or "mock_verifier",
            "reasoning": "Mock verification successful"
        }
        
        attestation_artifact_id = self.storage.put_artifact(
            json.dumps(attestation_data).encode('utf-8'),
            {"artifact_type": "attestation"}
        )
        
        return {
            "success": True,
            "attestation_artifact": attestation_artifact_id
        }


class MockStatisticalAgent:
    """Mock Statistical Planning Execution Agent for testing"""
    
    def __init__(self, security, audit, storage):
        self.security = security
        self.audit = audit
        self.storage = storage
    
    def execute_statistical_analysis(self, analysis_artifacts: List[str], model: str) -> Dict[str, Any]:
        """Mock statistical analysis"""
        
        statistics_data = {
            "anova_results": {"F_statistic": 15.2, "p_value": 0.001},
            "correlation_matrix": {"populism_authoritarianism": 0.75}
        }
        
        work_data = {
            "executed_code": "import scipy.stats; f_stat, p_val = scipy.stats.f_oneway(data)",
            "execution_output": "ANOVA F-statistic: 15.2, p-value: 0.001"
        }
        
        csv_data = "dimension,mean,std\npopulism,0.75,0.15\nauthoritarianism,0.70,0.18"
        
        # Store artifacts
        statistics_artifact_id = self.storage.put_artifact(
            json.dumps(statistics_data).encode('utf-8'),
            {"artifact_type": "statistics"}
        )
        
        work_artifact_id = self.storage.put_artifact(
            json.dumps(work_data).encode('utf-8'),
            {"artifact_type": "statistical_work"}
        )
        
        csv_artifact_id = self.storage.put_artifact(
            csv_data.encode('utf-8'),
            {"artifact_type": "statistical_csv"}
        )
        
        return {
            "success": True,
            "artifacts": [statistics_artifact_id, work_artifact_id, csv_artifact_id]
        }


class MockStatisticalVerificationAgent:
    """Mock Statistical Verification Agent for testing"""
    
    def __init__(self, security, audit, storage):
        self.security = security
        self.audit = audit
        self.storage = storage
    
    def verify_statistical_analysis(self, statistics_artifact_id: str, work_artifact_id: str, 
                                   csv_artifact_id: str, model: str = None) -> Dict[str, Any]:
        """Mock statistical verification"""
        
        attestation_data = {
            "success": True,
            "verifier_model": model or "mock_statistical_verifier",
            "reasoning": "Mock statistical verification successful"
        }
        
        attestation_artifact_id = self.storage.put_artifact(
            json.dumps(attestation_data).encode('utf-8'),
            {"artifact_type": "statistical_attestation"}
        )
        
        return {
            "success": True,
            "attestation_artifact": attestation_artifact_id
        }


class MockEvidenceCSVModule:
    """Mock Evidence CSV Export Module for testing"""
    
    def __init__(self, storage):
        self.storage = storage
    
    def generate_evidence_csv(self, analysis_artifacts: List[str]) -> Dict[str, Any]:
        """Mock evidence CSV generation"""
        
        csv_data = "document_id,document_name,dimension,quote_text,confidence\n"
        csv_data += "doc_1,test1.txt,populism,The people are betrayed,0.9\n"
        csv_data += "doc_2,test2.txt,authoritarianism,We need strong leadership,0.8\n"
        
        csv_artifact_id = self.storage.put_artifact(
            csv_data.encode('utf-8'),
            {"artifact_type": "evidence_csv"}
        )
        
        return {
            "success": True,
            "artifacts": [csv_artifact_id]
        }


def test_show_your_work_orchestrator_validation():
    """Test ShowYourWorkOrchestrator with mock components"""
    
    print("🧪 Testing Show Your Work Orchestrator Architecture")
    print("=" * 60)
    
    # Setup test environment
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create experiment structure
        experiment_dir = temp_path / "test_experiment"
        experiment_dir.mkdir()
        (experiment_dir / "logs").mkdir()
        (experiment_dir / "experiment.md").write_text("# Test Experiment")
        
        # Create test framework
        framework_path = experiment_dir / "framework.md"
        framework_path.write_text("""
# Test Framework

## Dimensions
- populism: Rhetorical appeals to the people vs. elite
- authoritarianism: Support for strong, centralized authority

## Analysis Instructions
Analyze each document for these dimensions on a 0.0-1.0 scale.
""")
        
        # Create test corpus
        corpus_dir = experiment_dir / "corpus"
        corpus_dir.mkdir()
        (corpus_dir / "doc1.txt").write_text("The people are being betrayed by the elite establishment.")
        (corpus_dir / "doc2.txt").write_text("We need strong leadership to restore order.")
        
        # Initialize orchestrator with mock agents
        orchestrator = ShowYourWorkOrchestrator(
            experiment_path=experiment_dir,
            enable_verification=True,
            enable_caching=True
        )
        
        # Replace agents with mocks
        orchestrator.analysis_agent = MockEnhancedAnalysisAgent(
            orchestrator.security, orchestrator.audit, orchestrator.storage
        )
        orchestrator.verification_agent = MockVerificationAgent(
            orchestrator.security, orchestrator.audit, orchestrator.storage
        )
        orchestrator.statistical_agent = MockStatisticalAgent(
            orchestrator.security, orchestrator.audit, orchestrator.storage
        )
        orchestrator.statistical_verification_agent = MockStatisticalVerificationAgent(
            orchestrator.security, orchestrator.audit, orchestrator.storage
        )
        orchestrator.evidence_csv_module = MockEvidenceCSVModule(orchestrator.storage)
        
        print(f"✅ Initialized ShowYourWorkOrchestrator with mock agents")
        
        # Execute experiment
        try:
            results = orchestrator.execute_experiment(
                framework_path=framework_path,
                corpus_path=corpus_dir,
                analysis_model="vertex_ai/gemini-2.5-flash",
                statistical_model="vertex_ai/gemini-2.5-pro"
            )
            
            print(f"✅ Experiment executed successfully")
            print(f"   Success: {results['success']}")
            print(f"   Duration: {results['duration_seconds']:.2f} seconds")
            print(f"   Analysis artifacts: {len(results['artifacts']['analysis_artifacts'])}")
            print(f"   Statistical artifacts: {len(results['artifacts']['statistical_artifacts'])}")
            print(f"   Evidence artifacts: {len(results['artifacts']['evidence_artifacts'])}")
            
            # Test experiment status
            status = orchestrator.get_experiment_status()
            print(f"✅ Experiment status: {status.get('status', 'unknown')}")
            
            # Test resume functionality
            resume_info = orchestrator.resume_experiment()
            print(f"✅ Resume info: {resume_info.get('status', 'unknown')}")
            
            print(f"\n🎉 ShowYourWorkOrchestrator validation PASSED")
            return True
            
        except Exception as e:
            print(f"❌ Experiment execution failed: {e}")
            import traceback
            traceback.print_exc()
            return False


def test_orchestrator_failure_handling():
    """Test orchestrator failure handling"""
    
    print("\n🧪 Testing Orchestrator Failure Handling")
    print("=" * 50)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create experiment structure
        experiment_dir = temp_path / "test_experiment"
        experiment_dir.mkdir()
        (experiment_dir / "logs").mkdir()
        (experiment_dir / "experiment.md").write_text("# Test Experiment")
        
        # Create test framework
        framework_path = experiment_dir / "framework.md"
        framework_path.write_text("# Test Framework")
        
        # Create test corpus
        corpus_dir = experiment_dir / "corpus"
        corpus_dir.mkdir()
        (corpus_dir / "doc1.txt").write_text("Test document")
        
        # Initialize orchestrator
        orchestrator = ShowYourWorkOrchestrator(experiment_path=experiment_dir)
        
        # Test with non-existent framework
        try:
            results = orchestrator.execute_experiment(
                framework_path=Path("nonexistent.md"),
                corpus_path=corpus_dir
            )
            
            if not results["success"]:
                print(f"✅ Failure handling working: {results['failure_type']}")
                return True
            else:
                print(f"❌ Expected failure but got success")
                return False
                
        except Exception as e:
            print(f"❌ Unexpected exception: {e}")
            return False


if __name__ == "__main__":
    print("🚀 Starting Show Your Work Orchestrator Validation Tests")
    print("=" * 70)
    
    success1 = test_show_your_work_orchestrator_validation()
    success2 = test_orchestrator_failure_handling()
    
    if success1 and success2:
        print(f"\n🎉 ALL TESTS PASSED - ShowYourWorkOrchestrator is ready!")
    else:
        print(f"\n❌ SOME TESTS FAILED - Check implementation")
