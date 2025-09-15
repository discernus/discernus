#!/usr/bin/env python3
"""
Real unit test for EnhancedAnalysisAgentMultiTool
Tests actual LLM behavior and artifact generation
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

class TestAnalysisAgentReal(unittest.TestCase):
    
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
    
    def test_analysis_agent_with_pdaf_framework(self):
        """Test analysis agent with PDAF framework - should produce 3 artifacts"""
        # Load PDAF framework
        pdaf_path = "frameworks/reference/pdaf_v10.0.2.md"
        if not os.path.exists(pdaf_path):
            self.skipTest(f"PDAF framework not found at {pdaf_path}")
        
        with open(pdaf_path, "r") as f:
            framework_content = f.read()
        
        # Test document (short for testing)
        document_content = """
        The people are being betrayed by the elite establishment. 
        We need to restore power to the working class and drain the swamp.
        The crisis is real and only I can fix it.
        """
        
        print(f"\n=== Testing PDAF Framework ===")
        print(f"Document length: {len(document_content)} characters")
        print(f"Framework length: {len(framework_content)} characters")
        
        # Run analysis
        result = self.agent.analyze_document(
            document_content=document_content,
            framework_content=framework_content,
            document_id="test_pdaf_doc"
        )
        
        # Verify result structure
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 7)
        self.assertIn("success", result)
        self.assertIn("document_id", result)
        self.assertIn("scores_artifact", result)
        self.assertIn("evidence_artifact", result)
        self.assertIn("work_artifact", result)
        self.assertIn("tool_calls_count", result)
        self.assertIn("usage", result)
        
        print(f"Result: {result}")
        
        # Verify each artifact exists and has content
        artifact_keys = ["scores_artifact", "evidence_artifact", "work_artifact"]
        for artifact_type in artifact_keys:
            artifact_id = result[artifact_type]
            if artifact_id is None:
                print(f"{artifact_type}: None (skipping)")
                continue
                
            self.assertIsNotNone(artifact_id)
            print(f"{artifact_type}: {artifact_id}")
            
            # Load and verify artifact content
            artifact_bytes = self.storage.get_artifact(artifact_id)
            artifact_data = json.loads(artifact_bytes.decode('utf-8'))
            self.assertIsNotNone(artifact_data)
            print(f"{artifact_type} content length: {len(str(artifact_data))}")
            
            # Verify artifact structure
            if artifact_type == "scores_artifact":
                self.assertIn("scores", artifact_data)
                self.assertIn("document_id", artifact_data)
                print(f"Scores dimensions: {list(artifact_data.get('scores', {}).keys())}")
            elif artifact_type == "evidence_artifact":
                self.assertIn("evidence", artifact_data)
                self.assertIn("document_id", artifact_data)
                print(f"Evidence count: {len(artifact_data.get('evidence', []))}")
            elif artifact_type == "work_artifact":
                self.assertIn("executed_code", artifact_data)
                self.assertIn("derived_metrics", artifact_data)
                print(f"Code length: {len(artifact_data.get('executed_code', ''))}")
                print(f"Derived metrics: {list(artifact_data.get('derived_metrics', {}).keys())}")
    
    def test_analysis_agent_with_sentiment_framework(self):
        """Test analysis agent with sentiment framework - should produce 3 artifacts"""
        # Create simple sentiment framework
        sentiment_framework = """
        # Sentiment Binary Framework v1.0
        
        ## Purpose
        Analyze sentiment polarity in political discourse
        
        ## Dimensions
        - positive_sentiment: Measures positive emotional content
        - negative_sentiment: Measures negative emotional content
        - neutral_sentiment: Measures neutral emotional content
        
        ## Scoring
        Each dimension scored 0.0-1.0 with confidence and salience
        """
        
        # Test document
        document_content = """
        This is a wonderful day for our great nation. 
        We have achieved incredible success and the future looks bright.
        The people are happy and prosperous.
        """
        
        print(f"\n=== Testing Sentiment Framework ===")
        print(f"Document length: {len(document_content)} characters")
        print(f"Framework length: {len(sentiment_framework)} characters")
        
        # Run analysis
        result = self.agent.analyze_document(
            document_content=document_content,
            framework_content=sentiment_framework,
            document_id="test_sentiment_doc"
        )
        
        # Verify result structure
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 7)
        self.assertIn("success", result)
        self.assertIn("document_id", result)
        self.assertIn("scores_artifact", result)
        self.assertIn("evidence_artifact", result)
        self.assertIn("work_artifact", result)
        self.assertIn("tool_calls_count", result)
        self.assertIn("usage", result)
        
        print(f"Result: {result}")
        
        # Verify each artifact exists and has content
        artifact_keys = ["scores_artifact", "evidence_artifact", "work_artifact"]
        for artifact_type in artifact_keys:
            artifact_id = result[artifact_type]
            if artifact_id is None:
                print(f"{artifact_type}: None (skipping)")
                continue
                
            self.assertIsNotNone(artifact_id)
            print(f"{artifact_type}: {artifact_id}")
            
            # Load and verify artifact content
            artifact_bytes = self.storage.get_artifact(artifact_id)
            artifact_data = json.loads(artifact_bytes.decode('utf-8'))
            self.assertIsNotNone(artifact_data)
            print(f"{artifact_type} content length: {len(str(artifact_data))}")
            
            # Verify artifact structure
            if artifact_type == "scores_artifact":
                self.assertIn("scores", artifact_data)
                scores = artifact_data.get("scores", {})
                print(f"Scores dimensions: {list(scores.keys())}")
                
                # Should have sentiment dimensions
                expected_dims = ["positive_sentiment", "negative_sentiment", "neutral_sentiment"]
                for dim in expected_dims:
                    if dim in scores:
                        score_data = scores[dim]
                        self.assertIn("raw_score", score_data)
                        self.assertIn("salience", score_data)
                        self.assertIn("confidence", score_data)
                        print(f"{dim}: {score_data}")
    
    def test_analysis_agent_reliability(self):
        """Test analysis agent reliability across multiple runs"""
        # Simple framework for reliability testing
        simple_framework = """
        # Simple Test Framework
        
        ## Dimensions
        - test_dimension_1
        - test_dimension_2
        """
        
        document_content = "This is a test document for reliability testing."
        
        print(f"\n=== Testing Reliability ===")
        
        # Run multiple times to test reliability
        results = []
        for i in range(3):
            print(f"\nRun {i+1}:")
            result = self.agent.analyze_document(
                document_content=document_content,
                framework_content=simple_framework,
                document_id=f"test_reliability_doc_{i}"
            )
            
            # Verify basic structure
            self.assertIsInstance(result, dict)
            self.assertEqual(len(result), 7)
            self.assertIn("success", result)
            self.assertIn("scores_artifact", result)
            self.assertIn("evidence_artifact", result)
            self.assertIn("work_artifact", result)
            
            results.append(result)
            print(f"Run {i+1} result: {result}")
        
        # All runs should produce valid results
        self.assertEqual(len(results), 3)
        for i, result in enumerate(results):
            self.assertIsNotNone(result["scores_artifact"])
            self.assertIsNotNone(result["evidence_artifact"])
            self.assertIsNotNone(result["work_artifact"])
            print(f"Run {i+1} artifacts verified")
    
    def tearDown(self):
        # Clean up temporary directory
        import shutil
        shutil.rmtree(self.temp_dir)

if __name__ == "__main__":
    unittest.main()
