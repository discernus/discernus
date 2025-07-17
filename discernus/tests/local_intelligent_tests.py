#!/usr/bin/env python3
"""
Local Intelligent Tests using Ollama
====================================

This testing system uses LOCAL Ollama models for intelligence validation.
Trade-off: FREE but SLOW. Good for development without API costs.

Philosophy:
- Use LOCAL models for cost-free intelligent testing
- Validate PROMPTS with real (local) LLMs
- Slower but perfect for development and CI/CD in budget-conscious environments
- Deterministic with temperature=0

Requirements:
- Ollama installed locally
- Models downloaded: ollama pull mistral

Usage:
    python3 discernus/tests/local_intelligent_tests.py
    python3 -m unittest discernus.tests.local_intelligent_tests -v
"""

import unittest
import sys
import json
import subprocess
import time
from pathlib import Path
from typing import Dict, Any, List
import tempfile
import shutil

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from discernus.orchestration.workflow_orchestrator import WorkflowOrchestrator
from discernus.gateway.model_registry import ModelRegistry
from discernus.gateway.llm_gateway import LLMGateway

class LocalIntelligentTests(unittest.TestCase):
    """
    Tests using local Ollama models for intelligence validation.
    FREE but SLOW - perfect for development.
    """
    
    @classmethod
    def setUpClass(cls):
        """Set up class-level resources for local intelligent testing."""
        # Check if Ollama is available
        if not cls._is_ollama_available():
            raise unittest.SkipTest("Ollama not available for local intelligent testing")
        
        # Use local models for testing
        cls.test_models = ["ollama/mistral"]
        
        # Initialize real LLM gateway
        cls.model_registry = ModelRegistry()
        cls.gateway = LLMGateway(cls.model_registry)
        
        print(f"🏠 Using local intelligent testing with models: {cls.test_models}")
        print("⚠️  Note: Local models are FREE but SLOW. Please be patient.")
    
    @classmethod
    def _is_ollama_available(cls) -> bool:
        """Check if Ollama is available and has required models."""
        try:
            # Check if ollama command exists
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=10)
            
            # Check if mistral model is available
            if result.returncode == 0 and 'mistral' in result.stdout:
                return True
            
            print("⚠️  Ollama available but mistral model not found. Run: ollama pull mistral")
            return False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("⚠️  Ollama not available. Install from https://ollama.ai")
            return False
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir) / "local_test_project"
        self.project_path.mkdir()
        
        # Create test corpus
        self.corpus_path = self.project_path / "corpus"
        self.corpus_path.mkdir()
        
        # Create test documents
        (self.corpus_path / "progressive_doc.txt").write_text(
            "This document discusses progressive policies like universal healthcare and climate action."
        )
        (self.corpus_path / "conservative_doc.txt").write_text(
            "This document discusses conservative policies like free markets and traditional values."
        )
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    def test_local_prompt_validation(self):
        """Test that prompts work with local LLMs (slow but free)."""
        
        # Simple prompt for local model
        test_prompt = """
        Analyze this text briefly.
        Return JSON with:
        - sentiment: "positive", "negative", or "neutral"
        - key_theme: one main theme as a string
        
        Text: {corpus_text}
        """
        
        print("\n⏳ Testing local prompt validation (may take 30-60 seconds)...")
        start_time = time.time()
        
        orchestrator = WorkflowOrchestrator(str(self.project_path))
        orchestrator.gateway = self.gateway
        
        workflow_state = {
            'workflow': [
                {'agent': 'AnalysisAgent'},
                {'agent': 'DataExtractionAgent'}
            ],
            'corpus_path': str(self.corpus_path),
            'experiment': {
                'models': self.test_models,
                'num_runs': 1
            },
            'analysis_agent_instructions': test_prompt,
            'project_path': str(self.project_path)
        }
        
        result = orchestrator.execute_workflow(workflow_state)
        
        elapsed_time = time.time() - start_time
        print(f"✅ Local validation completed in {elapsed_time:.1f}s")
        
        # Validate that local LLM produced valid results
        self.assertEqual(result['status'], 'success')
        self.assertIn('analysis_results', result['final_state'])
        
        analysis_results = result['final_state']['analysis_results']
        self.assertGreater(len(analysis_results), 0)
        
        # Check local LLM output structure
        for analysis_result in analysis_results:
            self.assertIn('json_output', analysis_result)
            if analysis_result.get('success'):
                json_output = analysis_result['json_output']
                self.assertIsInstance(json_output, dict)
                
                # Local model should produce expected fields
                self.assertIn('sentiment', json_output)
                self.assertIn('key_theme', json_output)
    
    def test_local_framework_agnostic_behavior(self):
        """Test framework-agnostic behavior with local models."""
        
        # Test different framework structures
        framework_tests = [
            {
                "name": "Simple_Sentiment",
                "prompt": """
                Analyze sentiment. Return JSON:
                {"sentiment": "positive|negative|neutral", "score": 0.7}
                
                Text: {corpus_text}
                """,
                "expected_fields": ["sentiment", "score"]
            },
            {
                "name": "Simple_Themes",
                "prompt": """
                Find main themes. Return JSON:
                {"themes": ["theme1", "theme2"], "confidence": 0.8}
                
                Text: {corpus_text}
                """,
                "expected_fields": ["themes", "confidence"]
            }
        ]
        
        for framework_test in framework_tests:
            with self.subTest(framework=framework_test["name"]):
                print(f"\n⏳ Testing {framework_test['name']} (may take 30-60 seconds)...")
                
                orchestrator = WorkflowOrchestrator(str(self.project_path))
                orchestrator.gateway = self.gateway
                
                workflow_state = {
                    'workflow': [
                        {'agent': 'AnalysisAgent'},
                        {'agent': 'DataExtractionAgent'}
                    ],
                    'corpus_path': str(self.corpus_path),
                    'experiment': {
                        'models': self.test_models,
                        'num_runs': 1
                    },
                    'analysis_agent_instructions': framework_test["prompt"],
                    'project_path': str(self.project_path)
                }
                
                result = orchestrator.execute_workflow(workflow_state)
                
                self.assertEqual(result['status'], 'success')
                analysis_results = result['final_state']['analysis_results']
                
                # Local LLM should handle different frameworks
                for analysis_result in analysis_results:
                    if analysis_result.get('success'):
                        json_output = analysis_result['json_output']
                        
                        # Check framework-specific fields
                        for expected_field in framework_test["expected_fields"]:
                            self.assertIn(expected_field, json_output,
                                        f"Missing {expected_field} in {framework_test['name']}")
    
    def test_local_model_robustness(self):
        """Test local model handling of edge cases."""
        
        # Test with minimal prompt
        minimal_prompt = """
        Analyze this text. Return JSON: {"result": "done"}
        
        Text: {corpus_text}
        """
        
        print("\n⏳ Testing local model robustness...")
        
        orchestrator = WorkflowOrchestrator(str(self.project_path))
        orchestrator.gateway = self.gateway
        
        workflow_state = {
            'workflow': [
                {'agent': 'AnalysisAgent'},
                {'agent': 'DataExtractionAgent'}
            ],
            'corpus_path': str(self.corpus_path),
            'experiment': {
                'models': self.test_models,
                'num_runs': 1
            },
            'analysis_agent_instructions': minimal_prompt,
            'project_path': str(self.project_path)
        }
        
        result = orchestrator.execute_workflow(workflow_state)
        
        # Should handle minimal prompts gracefully
        self.assertEqual(result['status'], 'success')
        analysis_results = result['final_state']['analysis_results']
        
        # Should process both documents
        self.assertEqual(len(analysis_results), 2)
        
        for analysis_result in analysis_results:
            self.assertIn('json_output', analysis_result)
            # May not always succeed with minimal prompts, but should not crash

class LocalModelPerformanceTests(unittest.TestCase):
    """
    Tests focused on local model performance and limitations.
    """
    
    def setUp(self):
        """Set up for local performance testing."""
        if not self._is_ollama_available():
            self.skipTest("Ollama not available for performance testing")
        
        self.model_registry = ModelRegistry()
        self.gateway = LLMGateway(self.model_registry)
        self.test_model = "ollama/mistral"
    
    def _is_ollama_available(self) -> bool:
        """Check if Ollama is available."""
        try:
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=10)
            return result.returncode == 0 and 'mistral' in result.stdout
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def test_local_model_timeout_handling(self):
        """Test that local models handle timeouts appropriately."""
        
        # Test with reasonable timeout
        simple_prompt = """
        Analyze this text briefly.
        Return JSON: {"analysis": "brief analysis"}
        
        Text: This is a test document.
        """
        
        print("\n⏳ Testing local model timeout handling...")
        start_time = time.time()
        
        response, metadata = self.gateway.execute_call(
            model=self.test_model,
            prompt=simple_prompt,
            system_prompt="Be concise."
        )
        
        elapsed_time = time.time() - start_time
        print(f"✅ Local model response time: {elapsed_time:.1f}s")
        
        # Should complete within reasonable time
        self.assertLess(elapsed_time, 120, f"Local model too slow: {elapsed_time:.1f}s")
        
        # Should produce valid response
        self.assertTrue(metadata['success'])
        self.assertGreater(len(response), 0)
    
    def test_local_model_resource_usage(self):
        """Test local model resource usage patterns."""
        
        # Test multiple quick calls
        test_prompts = [
            "Analyze sentiment. Return JSON: {'sentiment': 'positive'}",
            "Find themes. Return JSON: {'themes': ['theme1']}",
            "Rate complexity. Return JSON: {'complexity': 0.5}"
        ]
        
        print("\n⏳ Testing local model resource usage...")
        total_start = time.time()
        
        for i, prompt in enumerate(test_prompts):
            start_time = time.time()
            
            response, metadata = self.gateway.execute_call(
                model=self.test_model,
                prompt=f"{prompt}\n\nText: Test document {i+1}.",
                system_prompt="Be brief."
            )
            
            elapsed_time = time.time() - start_time
            print(f"  Call {i+1}: {elapsed_time:.1f}s")
            
            # Each call should succeed
            self.assertTrue(metadata['success'])
        
        total_time = time.time() - total_start
        print(f"✅ Total local testing time: {total_time:.1f}s")
        
        # Should complete all calls within reasonable time
        self.assertLess(total_time, 300, f"Local model batch too slow: {total_time:.1f}s")

if __name__ == '__main__':
    print("🏠 Running Local Intelligent Tests")
    print("=" * 50)
    print("These tests use LOCAL Ollama models for intelligence validation.")
    print("FREE but SLOW - perfect for development without API costs.")
    print("=" * 50)
    
    # Check Ollama availability
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Ollama available")
            if 'mistral' in result.stdout:
                print("✅ Mistral model available")
            else:
                print("⚠️  Mistral model not found. Run: ollama pull mistral")
        else:
            print("❌ Ollama not responding properly")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Ollama not installed. Install from https://ollama.ai")
    
    unittest.main(verbosity=2) 