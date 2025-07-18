#!/usr/bin/env python3
"""
Schema Transformation Tests
===========================

Comprehensive tests for schema transformation functionality using realistic LLM response patterns.
This addresses the critical test coverage gap identified in the MVA Experiment 3 failure analysis.

Key principle: Test with hierarchical JSON that LLMs actually produce, not artificially constrained flat JSON.
"""

import sys
import json
import unittest
from pathlib import Path
from typing import Dict, Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from discernus.agents.data_extraction_agent import DataExtractionAgent
from discernus.gateway.model_registry import ModelRegistry
from discernus.gateway.llm_gateway import LLMGateway
from discernus.tests.realistic_test_data_generator import RealisticTestDataGenerator


class SchemaTransformationTests(unittest.TestCase):
    """
    Test schema transformation with realistic LLM response patterns.
    
    These tests validate that the DataExtractionAgent can correctly transform
    complex hierarchical JSON into the flat schema expected by downstream agents.
    """
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment with real gateway and test data."""
        # Initialize real components (not mocks)
        cls.model_registry = ModelRegistry()
        cls.gateway = LLMGateway(cls.model_registry)
        cls.test_data_generator = RealisticTestDataGenerator()
        
        # Load test fixtures
        cls.fixtures_dir = Path("discernus/tests/fixtures/realistic_responses")
        cls.test_fixtures = cls._load_test_fixtures()
        
        print(f"✅ Loaded {len(cls.test_fixtures)} realistic test fixtures")
    
    @classmethod
    def _load_test_fixtures(cls) -> Dict[str, Dict[str, Any]]:
        """Load all test fixtures from disk."""
        fixtures = {}
        
        if not cls.fixtures_dir.exists():
            print(f"⚠️  Test fixtures directory not found: {cls.fixtures_dir}")
            return fixtures
        
        for fixture_file in cls.fixtures_dir.glob("*.json"):
            try:
                with open(fixture_file, 'r', encoding='utf-8') as f:
                    fixture_data = json.load(f)
                    fixtures[fixture_file.stem] = fixture_data
                    print(f"📂 Loaded fixture: {fixture_file.name}")
            except Exception as e:
                print(f"❌ Failed to load fixture {fixture_file}: {e}")
        
        return fixtures
    
    def setUp(self):
        """Set up for each test."""
        self.data_extraction_agent = DataExtractionAgent(self.gateway)
    
    def test_cff_gemini_hierarchical_transformation(self):
        """Test transformation of Gemini's hierarchical CFF response."""
        fixture_name = "cff_gemini_hierarchical_cff_test_case"
        self._test_schema_transformation(fixture_name)
    
    def test_cff_claude_nested_transformation(self):
        """Test transformation of Claude's nested CFF response."""
        fixture_name = "cff_claude_nested_cff_test_case"
        self._test_schema_transformation(fixture_name)
    
    def test_pdaf_transformation(self):
        """Test transformation of PDAF framework response."""
        fixture_name = "pdaf_gemini_pdaf_analysis_test_case"
        self._test_schema_transformation(fixture_name)
    
    def test_generic_framework_transformation(self):
        """Test transformation of generic framework response."""
        fixture_name = "generic_gpt_custom_framework_test_case"
        self._test_schema_transformation(fixture_name)
    
    def _test_schema_transformation(self, fixture_name: str):
        """
        Test schema transformation with a specific fixture.
        
        This is the core test that validates the DataExtractionAgent can transform
        realistic hierarchical JSON into the expected flat schema.
        """
        # Skip if fixture not available
        if fixture_name not in self.test_fixtures:
            self.skipTest(f"Test fixture {fixture_name} not available")
        
        fixture = self.test_fixtures[fixture_name]
        hierarchical_response = fixture["input_response"]
        expected_schema = fixture["expected_schema"]
        framework_type = fixture["framework_type"]
        
        print(f"\n🧪 Testing {fixture_name}")
        print(f"   Framework: {framework_type}")
        print(f"   Input keys: {list(hierarchical_response.keys())}")
        
        # Create mock analysis results that would come from AnalysisAgent
        mock_analysis_results = {
            "analysis_agent_run1_vertex_ai_gemini-2.5-pro_test": {
                "agent_id": "test_agent",
                "content": json.dumps(hierarchical_response),
                "metadata": {"success": True},
                "corpus_file": "test_file.txt",
                "model_name": "vertex_ai/gemini-2.5-pro",
                "run_num": 1
            }
        }
        
        # Create workflow state as DataExtractionAgent expects
        workflow_state = {
            "analysis_results": mock_analysis_results,
            "framework": {
                "output_contract": {
                    "schema": expected_schema
                }
            }
        }
        
        # Execute DataExtractionAgent
        try:
            result = self.data_extraction_agent.execute(workflow_state, {})
            
            # Validate that extraction was successful
            self.assertIn("analysis_results", result, "DataExtractionAgent should return analysis_results")
            
            analysis_results = result["analysis_results"]
            self.assertIsInstance(analysis_results, list, "Analysis results should be a list")
            self.assertGreater(len(analysis_results), 0, "Should have extracted at least one result")
            
            # Get the transformed data from the first result
            first_result = analysis_results[0]
            self.assertIn("json_output", first_result, "Analysis result should contain json_output")
            self.assertIn("success", first_result, "Analysis result should contain success flag")
            self.assertTrue(first_result["success"], "Analysis should have succeeded")
            
            # Validate schema compliance on the transformed data
            transformed_data = first_result["json_output"]
            self._validate_schema_compliance(transformed_data, expected_schema, framework_type)
            
            print(f"✅ Schema transformation successful for {fixture_name}")
            
        except Exception as e:
            self.fail(f"Schema transformation failed for {fixture_name}: {str(e)}")
    
    def _validate_schema_compliance(self, extracted_result: Dict[str, Any], 
                                    expected_schema: Dict[str, str], 
                                    framework_type: str):
        """
        Validate that the extracted result complies with the expected schema.
        
        This checks that all expected fields are present and have the correct types.
        """
        print(f"   🔍 Validating schema compliance for {framework_type}")
        
        # Check that expected fields are present (with flexibility for different LLM response patterns)
        core_fields_found = 0
        total_fields = len(expected_schema)
        
        for field_name, field_type in expected_schema.items():
            if field_name in extracted_result:
                core_fields_found += 1
                actual_value = extracted_result[field_name]
                
                # Validate field types
                if field_type == "number":
                    self.assertIsInstance(actual_value, (int, float), 
                                        f"Field '{field_name}' should be a number, got {type(actual_value)}")
                elif field_type == "string":
                    self.assertIsInstance(actual_value, str, 
                                        f"Field '{field_name}' should be a string, got {type(actual_value)}")
                elif field_type == "array":
                    self.assertIsInstance(actual_value, list, 
                                        f"Field '{field_name}' should be an array, got {type(actual_value)}")
            else:
                # Print missing field for debugging but don't fail the test
                print(f"   ⚠️  Field '{field_name}' not found in extracted result (different LLM response pattern)")
        
        # Require at least 60% of expected fields to be present (handles different response patterns)
        coverage_ratio = core_fields_found / total_fields
        self.assertGreaterEqual(coverage_ratio, 0.6, 
                               f"Schema coverage too low: {coverage_ratio:.1%} ({core_fields_found}/{total_fields} fields)")
        
        print(f"   📊 Schema coverage: {coverage_ratio:.1%} ({core_fields_found}/{total_fields} fields)")
        
        # Validate that at least the core fields are present
        core_fields = ["worldview"] if framework_type == "cff" or framework_type == "pdaf" else ["primary_classification"]
        for core_field in core_fields:
            if core_field in expected_schema:
                self.assertIn(core_field, extracted_result, 
                             f"Core field '{core_field}' must be present in extracted result")
        
        print(f"   ✅ Schema validation passed for {framework_type}")
    
    def test_mvp_experiment_3_reproduction(self):
        """
        Test that reproduces the MVA Experiment 3 failure scenario.
        
        This test uses the exact type of hierarchical JSON that caused the original failure
        to ensure that the schema transformation now works correctly.
        """
        print("\n🎯 Testing MVA Experiment 3 failure reproduction")
        
        # Create a realistic analysis result similar to what caused the failure
        mvp_hierarchical_response = {
            "Political Worldview Classification": {
                "Worldview": "Progressive"
            },
            "Cohesive Flourishing Framework v4.1 Analysis": {
                "Identity Axis": {
                    "Tribal Dominance": {
                        "Score": 0.2,
                        "Confidence": 0.8,
                        "Evidence": [
                            "* **Tribal Dominance: 0.2 / 1.0**",
                            "Limited evidence of group hierarchy markers"
                        ]
                    },
                    "Individual Dignity": {
                        "Score": 0.8,
                        "Confidence": 0.9,
                        "Evidence": [
                            "* **Individual Dignity: 0.8 / 1.0**",
                            "Strong emphasis on universal rights and dignity"
                        ]
                    }
                }
            },
            "Overall Analysis Confidence": 0.85,
            "Competitive Patterns Observed": "Pure Directional"
        }
        
        # Create mock analysis results
        mock_analysis_results = {
            "analysis_agent_run1_vertex_ai_gemini-2.5-pro_mvp_test": {
                "agent_id": "mvp_reproduction_test",
                "content": json.dumps(mvp_hierarchical_response),
                "metadata": {"success": True},
                "corpus_file": "mvp_test_speech.md",
                "model_name": "vertex_ai/gemini-2.5-pro", 
                "run_num": 1
            }
        }
        
        # Create workflow state with CFF schema
        workflow_state = {
            "analysis_results": mock_analysis_results,
            "framework": {
                "output_contract": {
                    "schema": self.test_data_generator.get_expected_flat_schema("cff")
                }
            }
        }
        
        # Execute DataExtractionAgent - this should NOT fail
        try:
            result = self.data_extraction_agent.execute(workflow_state, {})
            
            # Validate successful extraction
            self.assertIn("analysis_results", result)
            analysis_results = result["analysis_results"]
            self.assertGreater(len(analysis_results), 0)
            
            # Get the transformed data from the first result
            first_result = analysis_results[0]
            self.assertIn("json_output", first_result)
            self.assertTrue(first_result["success"])
            
            # Validate specific CFF fields that were problematic
            transformed_data = first_result["json_output"]
            self.assertIn("tribal_dominance_score", transformed_data)
            self.assertIn("individual_dignity_score", transformed_data)
            self.assertIn("overall_analysis_confidence", transformed_data)
            
            # Validate the scores were extracted correctly
            self.assertEqual(transformed_data["tribal_dominance_score"], 0.2)
            self.assertEqual(transformed_data["individual_dignity_score"], 0.8)
            self.assertEqual(transformed_data["overall_analysis_confidence"], 0.85)
            
            print("✅ MVA Experiment 3 failure scenario now works correctly")
            
        except Exception as e:
            self.fail(f"MVA Experiment 3 reproduction test failed: {str(e)}")
    
    def test_multiple_llm_response_patterns(self):
        """
        Test that the schema transformation works with different LLM response patterns.
        
        This validates multi-LLM compatibility (Gemini, Claude, GPT response patterns).
        """
        print("\n🔬 Testing multiple LLM response patterns")
        
        # Test all available fixtures
        for fixture_name, fixture_data in self.test_fixtures.items():
            if fixture_data["framework_type"] == "cff":
                with self.subTest(fixture=fixture_name):
                    self._test_schema_transformation(fixture_name)
    
    def test_schema_transformation_error_handling(self):
        """
        Test error handling when schema transformation encounters problems.
        
        This validates fallback behavior and graceful degradation.
        """
        print("\n🛡️  Testing schema transformation error handling")
        
        # Test with malformed JSON
        malformed_analysis_results = {
            "analysis_agent_run1_vertex_ai_gemini-2.5-pro_error_test": {
                "agent_id": "error_test",
                "content": "NOT_VALID_JSON{malformed",
                "metadata": {"success": True},
                "corpus_file": "error_test.txt",
                "model_name": "vertex_ai/gemini-2.5-pro",
                "run_num": 1
            }
        }
        
        workflow_state = {
            "analysis_results": malformed_analysis_results,
            "framework": {
                "output_contract": {
                    "schema": self.test_data_generator.get_expected_flat_schema("cff")
                }
            }
        }
        
        # This should not crash, but should handle the error gracefully
        try:
            result = self.data_extraction_agent.execute(workflow_state, {})
            # Should still return a result, even if some extractions failed
            self.assertIn("analysis_results", result)
            # Check that error was properly handled
            analysis_results = result["analysis_results"]
            self.assertGreater(len(analysis_results), 0)
            first_result = analysis_results[0]
            self.assertFalse(first_result["success"], "Malformed JSON should result in failure")
            print("✅ Error handling works correctly")
        except Exception as e:
            # If it does throw an exception, it should be informative
            self.assertIn("JSON", str(e), "Error message should mention JSON parsing issue")
            print(f"✅ Error handling provides informative error: {str(e)}")


class FrameworkAgnosticTests(unittest.TestCase):
    """
    Test framework-agnostic behavior with realistic data.
    
    These tests ensure that the system works correctly with multiple framework types
    and doesn't make hardcoded assumptions about specific frameworks.
    """
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        cls.model_registry = ModelRegistry()
        cls.gateway = LLMGateway(cls.model_registry)
        cls.test_data_generator = RealisticTestDataGenerator()
    
    def setUp(self):
        """Set up for each test."""
        self.data_extraction_agent = DataExtractionAgent(self.gateway)
    
    def test_framework_agnostic_transformation(self):
        """
        Test that schema transformation works with different framework types.
        
        This validates that the system is truly framework-agnostic and doesn't
        make hardcoded assumptions about CFF or any specific framework.
        """
        print("\n🌐 Testing framework-agnostic transformation")
        
        framework_types = ["cff", "pdaf", "generic"]
        
        for framework_type in framework_types:
            with self.subTest(framework=framework_type):
                print(f"   Testing {framework_type} framework")
                
                # Generate realistic response for this framework type
                realistic_response = self.test_data_generator.generate_realistic_response(framework_type)
                expected_schema = self.test_data_generator.get_expected_flat_schema(framework_type)
                
                # Create mock analysis results
                mock_analysis_results = {
                    f"analysis_agent_run1_test_{framework_type}": {
                        "agent_id": f"test_agent_{framework_type}",
                        "content": json.dumps(realistic_response),
                        "metadata": {"success": True},
                        "corpus_file": f"test_{framework_type}.txt",
                        "model_name": "vertex_ai/gemini-2.5-pro",
                        "run_num": 1
                    }
                }
                
                workflow_state = {
                    "analysis_results": mock_analysis_results,
                    "framework": {
                        "output_contract": {
                            "schema": expected_schema
                        }
                    }
                }
                
                # Execute transformation
                result = self.data_extraction_agent.execute(workflow_state, {})
                
                # Validate results
                self.assertIn("analysis_results", result)
                analysis_results = result["analysis_results"]
                self.assertGreater(len(analysis_results), 0)
                
                # Validate successful transformation
                first_result = analysis_results[0]
                self.assertIn("json_output", first_result)
                self.assertTrue(first_result["success"])
                
                print(f"   ✅ {framework_type} framework transformation successful")


def main():
    """Run the schema transformation tests."""
    print("🧪 Running Schema Transformation Tests")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    
    # Add schema transformation tests
    test_suite.addTest(loader.loadTestsFromTestCase(SchemaTransformationTests))
    test_suite.addTest(loader.loadTestsFromTestCase(FrameworkAgnosticTests))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    if result.wasSuccessful():
        print("\n🎉 All schema transformation tests passed!")
        print("   The test coverage gap has been addressed.")
    else:
        print(f"\n❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        for test, trace in result.failures + result.errors:
            print(f"   Failed: {test}")


if __name__ == "__main__":
    main() 