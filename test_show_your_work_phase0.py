#!/usr/bin/env python3
"""
Show Your Work Phase 0 Validation Test
=====================================

Tests the EnhancedAnalysisAgentMultiTool without parsing LLM output.
Validates that the agent correctly saves three artifacts to disk:
1. analysis_scores.json - Dimensional scores with confidence/salience
2. evidence_quotes.json - Evidence quotes and reasoning  
3. computational_work.json - Derived metrics and code execution

This test validates the core principle: structured output via tool calling
eliminates parsing brittleness by saving artifacts directly to disk.
"""

import unittest
import tempfile
import os
import json
import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

from discernus.agents.EnhancedAnalysisAgent.agent_multi_tool import EnhancedAnalysisAgentMultiTool
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway
from discernus.gateway.model_registry import ModelRegistry


class TestShowYourWorkPhase0(unittest.TestCase):
    """
    Phase 0 Validation: EnhancedAnalysisAgentMultiTool with tool calling
    
    Validates the core "Show Your Work" principle:
    - LLM uses structured tool calls (no parsing needed)
    - Three artifacts saved to disk with correct structure
    - Artifacts contain the data we expect based on tool schemas
    """
    
    def setUp(self):
        # Create temporary experiment directory
        self.temp_dir = tempfile.mkdtemp()
        self.experiment_path = os.path.join(self.temp_dir, "experiment.md")
        with open(self.experiment_path, "w") as f:
            f.write("# Test Experiment\n")
        
        # Create real dependencies
        from pathlib import Path
        self.security = ExperimentSecurityBoundary(Path(self.temp_dir))
        self.run_folder = Path(self.temp_dir) / "run_001"
        self.run_folder.mkdir(exist_ok=True)
        self.audit = AuditLogger(self.security, self.run_folder)
        self.storage = LocalArtifactStorage(self.security, self.run_folder)
        self.llm_gateway = EnhancedLLMGateway(ModelRegistry())
        
        # Create agent
        self.agent = EnhancedAnalysisAgentMultiTool(
            security_boundary=self.security,
            audit_logger=self.audit,
            storage=self.storage,
            llm_gateway=self.llm_gateway
        )
    
    def test_pdaf_framework_artifacts(self):
        """Test with PDAF framework - validate three artifacts are saved correctly"""
        # Load PDAF framework
        pdaf_path = "frameworks/reference/pdaf_v10.0.2.md"
        if not os.path.exists(pdaf_path):
            self.skipTest(f"PDAF framework not found at {pdaf_path}")
        
        with open(pdaf_path, "r") as f:
            framework_content = f.read()
        
        # Test document (real political content)
        document_content = """
        The people are being betrayed by the elite establishment. 
        We need to restore power to the working class and drain the swamp.
        The crisis is real and only I can fix it. The media won't tell you the truth.
        We must take back our country from the corrupt politicians.
        """
        
        print(f"\n=== Testing PDAF Framework with Tool Calling ===")
        print(f"Document length: {len(document_content)} characters")
        print(f"Framework length: {len(framework_content)} characters")
        
        # Run analysis - this should save three artifacts to disk
        result = self.agent.analyze_document(
            document_content=document_content,
            framework_content=framework_content,
            document_id="test_pdaf_doc"
        )
        
        # Validate result structure (not parsing LLM output)
        self.assertIsInstance(result, dict)
        self.assertIn("success", result)
        self.assertTrue(result["success"], "Analysis should succeed")
        self.assertIn("scores_artifact", result)
        self.assertIn("evidence_artifact", result)
        self.assertIn("work_artifact", result)
        
        print(f"Analysis result: {result}")
        
        # Validate artifacts exist on disk
        scores_artifact_id = result["scores_artifact"]
        evidence_artifact_id = result["evidence_artifact"]
        work_artifact_id = result["work_artifact"]
        
        self.assertIsNotNone(scores_artifact_id, "Scores artifact should be created")
        self.assertIsNotNone(evidence_artifact_id, "Evidence artifact should be created")
        self.assertIsNotNone(work_artifact_id, "Work artifact should be created")
        
        # Load and validate artifacts from disk
        self._validate_analysis_scores_artifact(scores_artifact_id)
        self._validate_evidence_quotes_artifact(evidence_artifact_id)
        self._validate_computational_work_artifact(work_artifact_id)
        
        print("✅ All three artifacts validated successfully")
    
    def test_simple_framework_artifacts(self):
        """Test with simple framework - validate artifact structure"""
        # Create simple framework
        simple_framework = """
        # Simple Test Framework v1.0
        
        ## Purpose
        Test framework for validation
        
        ## Dimensions
        - test_dimension_1: Measures first test dimension
        - test_dimension_2: Measures second test dimension
        
        ## Scoring
        Each dimension scored 0.0-1.0 with confidence and salience
        """
        
        document_content = "This is a test document for framework validation."
        
        print(f"\n=== Testing Simple Framework with Tool Calling ===")
        print(f"Document length: {len(document_content)} characters")
        print(f"Framework length: {len(simple_framework)} characters")
        
        # Run analysis
        result = self.agent.analyze_document(
            document_content=document_content,
            framework_content=simple_framework,
            document_id="test_simple_doc"
        )
        
        # Validate basic success
        self.assertTrue(result["success"], "Analysis should succeed")
        
        # Validate artifacts exist
        scores_artifact_id = result["scores_artifact"]
        evidence_artifact_id = result["evidence_artifact"]
        work_artifact_id = result["work_artifact"]
        
        self.assertIsNotNone(scores_artifact_id)
        self.assertIsNotNone(evidence_artifact_id)
        self.assertIsNotNone(work_artifact_id)
        
        # Validate artifact structure
        self._validate_analysis_scores_artifact(scores_artifact_id)
        self._validate_evidence_quotes_artifact(evidence_artifact_id)
        self._validate_computational_work_artifact(work_artifact_id)
        
        print("✅ Simple framework artifacts validated successfully")
    
    def _validate_analysis_scores_artifact(self, artifact_id: str):
        """Validate analysis_scores.json artifact structure"""
        print(f"  📊 Validating analysis_scores artifact: {artifact_id}")
        
        # Load artifact from disk
        artifact_bytes = self.storage.get_artifact(artifact_id)
        artifact_data = json.loads(artifact_bytes.decode('utf-8'))
        
        # Validate required fields
        self.assertIn("document_id", artifact_data)
        self.assertIn("framework_name", artifact_data)
        self.assertIn("framework_version", artifact_data)
        self.assertIn("scores", artifact_data)
        
        # Validate scores structure
        scores = artifact_data["scores"]
        self.assertIsInstance(scores, dict)
        self.assertGreater(len(scores), 0, "Should have at least one dimension scored")
        
        # Validate each dimension has required fields
        for dim_name, dim_data in scores.items():
            self.assertIsInstance(dim_data, dict)
            self.assertIn("raw_score", dim_data)
            self.assertIn("salience", dim_data)
            self.assertIn("confidence", dim_data)
            
            # Validate score ranges
            self.assertGreaterEqual(dim_data["raw_score"], 0.0)
            self.assertLessEqual(dim_data["raw_score"], 1.0)
            self.assertGreaterEqual(dim_data["salience"], 0.0)
            self.assertLessEqual(dim_data["salience"], 1.0)
            self.assertGreaterEqual(dim_data["confidence"], 0.0)
            self.assertLessEqual(dim_data["confidence"], 1.0)
        
        print(f"    ✅ {len(scores)} dimensions scored correctly")
    
    def _validate_evidence_quotes_artifact(self, artifact_id: str):
        """Validate evidence_quotes.json artifact structure"""
        print(f"  📝 Validating evidence_quotes artifact: {artifact_id}")
        
        # Load artifact from disk
        artifact_bytes = self.storage.get_artifact(artifact_id)
        artifact_data = json.loads(artifact_bytes.decode('utf-8'))
        
        # Validate required fields
        self.assertIn("document_id", artifact_data)
        self.assertIn("evidence", artifact_data)
        
        # Validate evidence structure
        evidence = artifact_data["evidence"]
        self.assertIsInstance(evidence, list)
        self.assertGreater(len(evidence), 0, "Should have at least one evidence quote")
        
        # Validate each evidence entry
        for i, evidence_entry in enumerate(evidence):
            self.assertIsInstance(evidence_entry, dict)
            self.assertIn("dimension", evidence_entry)
            self.assertIn("quote", evidence_entry)
            self.assertIn("reasoning", evidence_entry)
            
            # Validate content
            self.assertIsInstance(evidence_entry["dimension"], str)
            self.assertIsInstance(evidence_entry["quote"], str)
            self.assertIsInstance(evidence_entry["reasoning"], str)
            self.assertGreater(len(evidence_entry["quote"]), 0, "Quote should not be empty")
            self.assertGreater(len(evidence_entry["reasoning"]), 0, "Reasoning should not be empty")
        
        print(f"    ✅ {len(evidence)} evidence quotes provided")
    
    def _validate_computational_work_artifact(self, artifact_id: str):
        """Validate computational_work.json artifact structure"""
        print(f"  🔧 Validating computational_work artifact: {artifact_id}")
        
        # Load artifact from disk
        artifact_bytes = self.storage.get_artifact(artifact_id)
        artifact_data = json.loads(artifact_bytes.decode('utf-8'))
        
        # Validate required fields
        self.assertIn("document_id", artifact_data)
        self.assertIn("executed_code", artifact_data)
        self.assertIn("execution_output", artifact_data)
        self.assertIn("derived_metrics", artifact_data)
        
        # Validate code execution
        executed_code = artifact_data["executed_code"]
        execution_output = artifact_data["execution_output"]
        derived_metrics = artifact_data["derived_metrics"]
        
        self.assertIsInstance(executed_code, str)
        self.assertIsInstance(execution_output, str)
        self.assertIsInstance(derived_metrics, dict)
        
        # Validate code contains Python syntax patterns
        self.assertTrue(
            any(keyword in executed_code for keyword in ["import", "def", "if", "for", "print", "=", "sum(", "len("]),
            "Code should contain Python syntax patterns"
        )
        
        # Validate derived metrics (may be empty if no calculations were performed)
        if len(derived_metrics) > 0:
            for metric_name, metric_value in derived_metrics.items():
                self.assertIsInstance(metric_value, (int, float), f"Metric {metric_name} should be numeric")
        
        # Validate execution output exists
        self.assertGreater(len(execution_output), 0, "Execution output should not be empty")
        
        print(f"    ✅ {len(derived_metrics)} derived metrics calculated")
        print(f"    ✅ Code length: {len(executed_code)} characters")
    
    def tearDown(self):
        # Clean up temporary directory
        import shutil
        shutil.rmtree(self.temp_dir)


if __name__ == "__main__":
    print("🧪 Show Your Work Phase 0 Validation Test")
    print("=" * 50)
    print("Testing: EnhancedAnalysisAgentMultiTool with tool calling")
    print("Principle: Structured output via tool calls eliminates parsing")
    print("Validation: Three artifacts saved to disk with correct structure")
    print("=" * 50)
    
    unittest.main(verbosity=2)
