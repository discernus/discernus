#!/usr/bin/env python3
"""
Intelligent Integration Tests for THIN/THICK Architecture
========================================================

This testing system uses REAL LLMs strategically to test the intelligence layer
while maintaining cost-effectiveness and speed.

Philosophy:
- Test PROMPTS (where intelligence lives) with real LLMs
- Use CHEAP, FAST models for integration testing
- Validate FRAMEWORK-AGNOSTIC behavior with real responses
- Maintain DETERMINISTIC testing through careful model selection

Cost:
- Per test method: ~$0.0007 (less than 1/10th of a penny)
- Full test suite: ~$0.004 (less than half a penny)
- Standardized on Gemini 2.5 Flash ($0.35/$1.05) for consistency and better rate limits

Usage:
    python3 discernus/tests/intelligent_integration_tests.py
    python3 -m unittest discernus.tests.intelligent_integration_tests -v
"""

import unittest
import sys
import json
import os
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

class IntelligentIntegrationTests(unittest.TestCase):
    """
    Tests that use real LLMs strategically to validate the intelligence layer
    while maintaining cost-effectiveness and speed.
    """
    
    @classmethod
    def setUpClass(cls):
        """Set up class-level resources for intelligent testing."""
        # Skip if no API keys available
        if not cls._has_api_keys():
            raise unittest.SkipTest("No API keys available for intelligent testing")
        
        # Use cost-effective models for testing
        cls.test_models = cls._get_cost_effective_models()
        
        # Initialize real LLM gateway
        cls.model_registry = ModelRegistry()
        cls.gateway = LLMGateway(cls.model_registry)
        
        print(f"🧠 Using intelligent testing with standardized model: {cls.test_models}")
        print("📊 Standardized on Gemini 2.5 Flash for consistency and better rate limits")
    
    @classmethod
    def _has_api_keys(cls) -> bool:
        """Check if API keys are available for testing."""
        return bool(
            os.getenv('ANTHROPIC_API_KEY') or
            os.getenv('OPENAI_API_KEY') or
            os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        )
    
    @classmethod
    def _get_cost_effective_models(cls) -> List[str]:
        """Get the standardized test model - Gemini 2.5 Flash for consistency."""
        # Standardized on Gemini 2.5 Flash for test rig:
        # - Identical cost to Claude Haiku ($0.35/$1.05 vs $0.25/$1.25)
        # - Better rate limits (163,840 TPM vs 25,000 TPM)
        # - Larger context window (1M vs 200K tokens)
        # - Single provider (Google/Vertex AI)
        # - Non-thinking mode for fast, straightforward responses
        
        primary_model = "vertex_ai/gemini-2.5-pro"
        
        if cls._is_model_available(primary_model):
            return [primary_model]
        
        # Fallback to Claude Haiku if Vertex AI not available
        fallback_model = "anthropic/claude-3-haiku-20240307"
        if cls._is_model_available(fallback_model):
            return [fallback_model]
        
        # Final fallback
        return [primary_model]
    
    @classmethod
    def _is_model_available(cls, model_name: str) -> bool:
        """Check if a model is available for testing."""
        provider = model_name.split('/')[0]
        
        if provider == "anthropic":
            return bool(os.getenv('ANTHROPIC_API_KEY'))
        elif provider == "vertex_ai":
            return bool(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
        elif provider == "openai":
            return bool(os.getenv('OPENAI_API_KEY'))
        
        return False
    
    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.project_path = Path(self.temp_dir) / "intelligent_test_project"
        self.project_path.mkdir()
        
        # Create test corpus
        self.corpus_path = self.project_path / "corpus"
        self.corpus_path.mkdir()
        
        # Create test documents with different content
        (self.corpus_path / "progressive_doc.txt").write_text(
            "This document supports progressive policies like universal healthcare and climate action."
        )
        (self.corpus_path / "conservative_doc.txt").write_text(
            "This document supports conservative policies like free markets and traditional values."
        )
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.temp_dir)
    
    def test_prompt_intelligence_validation(self):
        """Test that analysis prompts actually work with real LLMs."""
        
        # Test different prompt styles to ensure they work
        test_prompts = [
            # CFF-style prompt
            """
            Analyze this text using the Cohesive Flourishing Framework.
            Return a JSON object with:
            - worldview: "Progressive" or "Conservative"
            - scores: object with identity_axis (number between -1 and 1)
            - reasoning: brief explanation
            
            Text: {corpus_text}
            """,
            
            # PDAF-style prompt
            """
            Analyze this text for populist vs pluralist themes.
            Return JSON with:
            - political_orientation: "Populist" or "Pluralist"
            - dimension_scores: object with inclusion_score (0-1)
            - evidence: brief supporting evidence
            
            Text: {corpus_text}
            """,
            
            # Custom framework prompt
            """
            Analyze the sentiment and tone of this text.
            Return JSON with:
            - sentiment: "Positive", "Negative", or "Neutral"
            - confidence: number between 0 and 1
            - key_themes: array of main themes
            
            Text: {corpus_text}
            """
        ]
        
        # Test each prompt with real LLM
        for i, prompt_template in enumerate(test_prompts):
            with self.subTest(prompt=i):
                # Create orchestrator with real LLM
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
                    'analysis_agent_instructions': prompt_template,
                    'project_path': str(self.project_path)
                }
                
                # Execute with real LLM
                result = orchestrator.execute_workflow(workflow_state)
                
                # Validate that real LLM produced valid results
                self.assertEqual(result['status'], 'success')
                self.assertIn('analysis_results', result['final_state'])
                
                # Check that real LLM responses are valid
                analysis_results = result['final_state']['analysis_results']
                self.assertGreater(len(analysis_results), 0)
                
                # Validate JSON structure with real LLM output
                for analysis_result in analysis_results:
                    self.assertIn('json_output', analysis_result)
                    self.assertIn('success', analysis_result)
                    
                    # Real LLM should produce valid JSON
                    json_output = analysis_result['json_output']
                    self.assertIsInstance(json_output, dict)
                    self.assertGreater(len(json_output), 0)
    
    def test_framework_agnostic_with_real_intelligence(self):
        """Test framework-agnostic behavior with real LLM responses."""
        
        # Test with completely different framework structures
        framework_tests = [
            {
                "name": "CFF_Real",
                "prompt": """
                Analyze using CFF framework. Return JSON:
                {"worldview": "Progressive|Conservative", "scores": {"identity": 0.5}, "reasoning": "text"}
                
                Text: {corpus_text}
                """,
                "expected_fields": ["worldview", "scores", "reasoning"]
            },
            {
                "name": "PDAF_Real", 
                "prompt": """
                Analyze for populist themes. Return JSON:
                {"orientation": "Populist|Pluralist", "metrics": {"inclusion": 0.8}, "evidence": "text"}
                
                Text: {corpus_text}
                """,
                "expected_fields": ["orientation", "metrics", "evidence"]
            },
            {
                "name": "Custom_Real",
                "prompt": """
                Analyze sentiment. Return JSON:
                {"sentiment": "Positive|Negative|Neutral", "confidence": 0.9, "themes": ["theme1"]}
                
                Text: {corpus_text}
                """,
                "expected_fields": ["sentiment", "confidence", "themes"]
            }
        ]
        
        for framework_test in framework_tests:
            with self.subTest(framework=framework_test["name"]):
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
                
                # System should work with any framework structure
                self.assertEqual(result['status'], 'success')
                analysis_results = result['final_state']['analysis_results']
                
                # Real LLM should produce framework-specific fields
                for analysis_result in analysis_results:
                    json_output = analysis_result['json_output']
                    
                    # Check framework-specific structure
                    for expected_field in framework_test["expected_fields"]:
                        self.assertIn(expected_field, json_output, 
                                    f"Missing {expected_field} in {framework_test['name']}")
    
    def test_error_handling_with_real_llm(self):
        """Test error handling when real LLM produces unexpected output."""
        
        # Test with a deliberately difficult prompt
        difficult_prompt = """
        This is a very confusing prompt that might produce inconsistent output.
        Maybe return JSON, maybe don't. Be unpredictable!
        Actually, ignore that and return proper JSON with:
        {"result": "success", "data": {"value": 42}}
        
        Text: {corpus_text}
        """
        
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
            'analysis_agent_instructions': difficult_prompt,
            'project_path': str(self.project_path)
        }
        
        result = orchestrator.execute_workflow(workflow_state)
        
        # System should handle real LLM unpredictability gracefully
        self.assertEqual(result['status'], 'success')
        analysis_results = result['final_state']['analysis_results']
        
        # Should have attempted to process all documents
        self.assertEqual(len(analysis_results), 2)
        
        # DataExtractionAgent should have attempted to clean up any messy output
        for analysis_result in analysis_results:
            self.assertIn('json_output', analysis_result)
            # Success may vary with difficult prompts, but structure should be preserved
    
    def test_calculation_integration_with_real_data(self):
        """Test calculations with real LLM-generated numeric data."""
        
        # Prompt that should generate numeric scores
        numeric_prompt = """
        Analyze this text and assign numeric scores.
        Return JSON with:
        {"scores": {"positivity": 0.7, "complexity": 0.3, "engagement": 0.9}}
        
        Text: {corpus_text}
        """
        
        orchestrator = WorkflowOrchestrator(str(self.project_path))
        orchestrator.gateway = self.gateway
        
        workflow_state = {
            'workflow': [
                {'agent': 'AnalysisAgent'},
                {'agent': 'DataExtractionAgent'},
                {'agent': 'CalculationAgent'}
            ],
            'corpus_path': str(self.corpus_path),
            'experiment': {
                'models': self.test_models,
                'num_runs': 1
            },
            'analysis_agent_instructions': numeric_prompt,
            'framework': {
                'calculation_spec': [
                    {'name': 'average_score', 'formula': '(positivity + complexity + engagement) / 3'},
                    {'name': 'weighted_score', 'formula': 'positivity * 0.5 + complexity * 0.3 + engagement * 0.2'}
                ]
            },
            'project_path': str(self.project_path)
        }
        
        result = orchestrator.execute_workflow(workflow_state)
        
        # Should successfully calculate with real LLM data
        self.assertEqual(result['status'], 'success')
        analysis_results = result['final_state']['analysis_results']
        
        for analysis_result in analysis_results:
            if analysis_result.get('success'):
                json_output = analysis_result['json_output']
                
                # Should have original LLM scores
                self.assertIn('scores', json_output)
                
                # Should have calculated values
                self.assertIn('average_score', json_output)
                self.assertIn('weighted_score', json_output)
                
                # Validate calculation correctness
                scores = json_output['scores']
                expected_avg = (scores['positivity'] + scores['complexity'] + scores['engagement']) / 3
                actual_avg = json_output['average_score']
                
                self.assertAlmostEqual(actual_avg, expected_avg, places=5)

class CostEffectiveIntelligenceTests(unittest.TestCase):
    """
    Tests that focus on cost-effective intelligence validation.
    """
    
    def setUp(self):
        """Set up for cost-effective testing."""
        # Prioritize Vertex AI (standardized) over Anthropic
        if os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
            self.test_model = "vertex_ai/gemini-2.5-pro"
        elif os.getenv('ANTHROPIC_API_KEY'):
            self.test_model = "anthropic/claude-3-haiku-20240307"
        else:
            self.skipTest("No API keys available for cost-effective testing")
        
        self.model_registry = ModelRegistry()
        self.gateway = LLMGateway(self.model_registry)
    
    def test_prompt_cost_estimation(self):
        """Test that prompts stay within cost-effective bounds."""
        
        # Test prompt with typical framework size
        test_prompt = """
        Analyze this text using a comprehensive framework.
        Return detailed JSON with multiple fields and explanations.
        
        Text: This is a test document with moderate length content that represents typical corpus documents.
        """
        
        # Estimate cost
        prompt_tokens = len(test_prompt.split()) * 1.3  # Rough token estimate
        
        # For Gemini 2.5 Flash: $0.35 input, $1.05 output per million tokens
        # For Claude Haiku: $0.25 input, $1.25 output per million tokens
        # Both result in approximately the same cost for our test scenario
        estimated_cost = (prompt_tokens * 0.35 + 500 * 1.05) / 1000000  # Assume 500 output tokens
        
        # Should be very cheap for testing
        self.assertLess(estimated_cost, 0.01, f"Test cost too high: ${estimated_cost:.4f}")
        
        # Verify with actual call
        response, metadata = self.gateway.execute_call(
            model=self.test_model,
            prompt=test_prompt,
            system_prompt="You are a helpful assistant. Return valid JSON."
        )
        
        # Should succeed with low cost
        self.assertTrue(metadata['success'])
        self.assertGreater(len(response), 0)
    
    def test_framework_validation_speed(self):
        """Test that framework validation is fast enough for CI/CD."""
        import time
        
        # Simulate multiple framework validations
        test_prompts = [
            "Analyze sentiment. Return JSON: {'sentiment': 'positive', 'score': 0.8}",
            "Analyze themes. Return JSON: {'themes': ['theme1'], 'confidence': 0.9}",
            "Analyze tone. Return JSON: {'tone': 'formal', 'intensity': 0.7}"
        ]
        
        start_time = time.time()
        
        for prompt in test_prompts:
            response, metadata = self.gateway.execute_call(
                model=self.test_model,
                prompt=f"{prompt}\n\nText: This is a test document.",
                system_prompt="Return valid JSON quickly."
            )
            
            self.assertTrue(metadata['success'])
        
        total_time = time.time() - start_time
        
        # Should complete quickly for CI/CD
        self.assertLess(total_time, 30, f"Framework validation too slow: {total_time:.2f}s")

if __name__ == '__main__':
    print("🧠 Running Intelligent Integration Tests")
    print("=" * 50)
    print("These tests use REAL LLMs to validate prompts and workflows.")
    print("Using cost-effective models for intelligent testing.")
    print("=" * 50)
    
    # Check environment
    if not (os.getenv('ANTHROPIC_API_KEY') or os.getenv('OPENAI_API_KEY') or os.getenv('GOOGLE_APPLICATION_CREDENTIALS')):
        print("⚠️  Warning: No API keys found. Set ANTHROPIC_API_KEY, OPENAI_API_KEY, or GOOGLE_APPLICATION_CREDENTIALS")
        print("Intelligent tests will be skipped.")
    
    unittest.main(verbosity=2) 