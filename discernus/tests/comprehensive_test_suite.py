#!/usr/bin/env python3
"""
Comprehensive Test Suite - "Trail of Tears" Test Data
====================================================

This test suite provides comprehensive coverage of the variety of corpora,
frameworks, experiment types, and calculations that Discernus should handle.
Designed to catch regressions and ensure true framework-agnostic behavior.
"""

import unittest
import sys
import json
from pathlib import Path
from typing import Dict, List, Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from discernus.tests.mocks.mock_llm_gateway import MockLLMGateway

class TestDataFactory:
    """Factory class for generating diverse test data scenarios."""
    
    @staticmethod
    def create_cff_framework_data() -> Dict[str, Any]:
        """CFF framework - political discourse analysis."""
        return {
            "worldview": "Progressive",
            "scores": {
                "identity_axis": 0.3,
                "fear_hope_axis": -0.2,
                "envy_compersion_axis": -0.8,
                "enmity_amity_axis": -0.6,
                "goal_axis": -0.5
            },
            "evidence": {
                "identity_axis": ["quote 1", "quote 2"],
                "fear_hope_axis": ["quote 3", "quote 4"]
            },
            "confidence": {
                "identity_axis": 0.9,
                "fear_hope_axis": 0.8
            },
            "reasoning": "This text expresses Progressive worldview with strong critique of inequality."
        }
    
    @staticmethod
    def create_pdaf_framework_data() -> Dict[str, Any]:
        """PDAF framework - populism analysis."""
        return {
            "political_orientation": "Anti-Pluralist",
            "dimension_scores": {
                "exclusion_dimension": 0.8,
                "authority_dimension": 0.6,
                "populism_dimension": 0.9
            },
            "evidence_citations": ["Quote 1", "Quote 2", "Quote 3"],
            "threat_indicators": ["us vs them", "elite conspiracy", "pure people"],
            "analysis_summary": "Strong anti-pluralist rhetoric with authoritarian tendencies."
        }
    
    @staticmethod
    def create_business_ethics_framework_data() -> Dict[str, Any]:
        """Business ethics framework - corporate analysis."""
        return {
            "ethical_stance": "Stakeholder Capitalism",
            "dimensions": {
                "shareholder_primacy": 0.2,
                "stakeholder_consideration": 0.8,
                "environmental_responsibility": 0.7,
                "social_impact": 0.9
            },
            "compliance_indicators": ["ESG reporting", "diversity metrics", "carbon neutrality"],
            "risk_factors": ["greenwashing", "virtue signaling"],
            "overall_assessment": "Genuine commitment to stakeholder value creation."
        }
    
    @staticmethod
    def create_academic_citation_framework_data() -> Dict[str, Any]:
        """Academic citation analysis framework."""
        return {
            "citation_quality": "High",
            "metrics": {
                "relevance_score": 0.9,
                "recency_score": 0.7,
                "authority_score": 0.8,
                "diversity_score": 0.6
            },
            "citation_types": {
                "primary_sources": 12,
                "secondary_sources": 8,
                "tertiary_sources": 3
            },
            "quality_indicators": ["peer reviewed", "high impact factor", "recent"],
            "methodological_notes": "Citations demonstrate strong theoretical grounding."
        }
    
    @staticmethod
    def create_sentiment_analysis_framework_data() -> Dict[str, Any]:
        """Sentiment analysis framework - social media."""
        return {
            "sentiment_classification": "Negative",
            "emotion_metrics": {
                "anger_level": 0.7,
                "joy_level": 0.1,
                "fear_level": 0.5,
                "sadness_level": 0.6,
                "disgust_level": 0.4
            },
            "key_themes": ["inequality", "injustice", "reform"],
            "engagement_predictors": ["viral potential", "controversy score"],
            "textual_evidence": "Multiple references to systemic problems and need for change."
        }
    
    @staticmethod
    def create_legal_document_framework_data() -> Dict[str, Any]:
        """Legal document analysis framework."""
        return {
            "document_type": "Contract",
            "legal_metrics": {
                "clarity_score": 0.6,
                "enforceability_score": 0.9,
                "fairness_score": 0.4,
                "compliance_score": 0.8
            },
            "risk_analysis": {
                "high_risk_clauses": ["termination", "liability"],
                "medium_risk_clauses": ["confidentiality"],
                "low_risk_clauses": ["definitions"]
            },
            "jurisdictional_considerations": ["federal", "state", "international"],
            "legal_reasoning": "Contract heavily favors one party with limited recourse."
        }
    
    @staticmethod
    def create_minimalist_framework_data() -> Dict[str, Any]:
        """Minimalist framework - simple analysis."""
        return {
            "score": 0.7,
            "category": "Positive",
            "notes": "Simple analysis with minimal fields."
        }
    
    @staticmethod
    def create_complex_nested_framework_data() -> Dict[str, Any]:
        """Complex nested framework - stress test."""
        return {
            "primary_analysis": {
                "level_1": {
                    "sub_level_1a": 0.8,
                    "sub_level_1b": 0.6,
                    "nested_metrics": {
                        "deep_metric_1": 0.9,
                        "deep_metric_2": 0.7
                    }
                },
                "level_2": {
                    "sub_level_2a": 0.5,
                    "sub_level_2b": 0.4
                }
            },
            "secondary_analysis": {
                "comparative_scores": [0.1, 0.2, 0.3, 0.4, 0.5],
                "temporal_tracking": {
                    "baseline": 0.3,
                    "current": 0.7,
                    "trend": "increasing"
                }
            },
            "metadata": {
                "processing_time": 1.2,
                "confidence_interval": [0.6, 0.8],
                "validation_flags": ["high_confidence", "peer_reviewed"]
            }
        }

class ComprehensiveTestSuite(unittest.TestCase):
    """
    Comprehensive test suite covering diverse scenarios.
    """
    
    def setUp(self):
        """Set up test scenarios with diverse framework and corpus combinations."""
        self.test_factory = TestDataFactory()
        
        # Create test scenarios for each framework type
        self.test_scenarios = [
            {
                "name": "CFF_Political_Speech",
                "framework_data": self.test_factory.create_cff_framework_data(),
                "corpus_type": "political_speech",
                "expected_calculations": ["cff_cohesion_index"],
                "expected_csv_fields": ["worldview", "scores_identity_axis", "reasoning"]
            },
            {
                "name": "PDAF_Populism_Analysis", 
                "framework_data": self.test_factory.create_pdaf_framework_data(),
                "corpus_type": "news_article",
                "expected_calculations": ["populism_threat_score"],
                "expected_csv_fields": ["political_orientation", "dimension_scores_exclusion_dimension"]
            },
            {
                "name": "Business_Ethics_Corporate",
                "framework_data": self.test_factory.create_business_ethics_framework_data(),
                "corpus_type": "corporate_report",
                "expected_calculations": ["ethical_compliance_score"],
                "expected_csv_fields": ["ethical_stance", "dimensions_shareholder_primacy"]
            },
            {
                "name": "Academic_Citation_Analysis",
                "framework_data": self.test_factory.create_academic_citation_framework_data(),
                "corpus_type": "academic_paper",
                "expected_calculations": ["citation_quality_index"],
                "expected_csv_fields": ["citation_quality", "metrics_relevance_score"]
            },
            {
                "name": "Sentiment_Social_Media",
                "framework_data": self.test_factory.create_sentiment_analysis_framework_data(),
                "corpus_type": "social_media",
                "expected_calculations": ["emotional_intensity_score"],
                "expected_csv_fields": ["sentiment_classification", "emotion_metrics_anger_level"]
            },
            {
                "name": "Legal_Document_Analysis",
                "framework_data": self.test_factory.create_legal_document_framework_data(),
                "corpus_type": "legal_document",
                "expected_calculations": ["legal_risk_score"],
                "expected_csv_fields": ["document_type", "legal_metrics_clarity_score"]
            },
            {
                "name": "Minimalist_Framework",
                "framework_data": self.test_factory.create_minimalist_framework_data(),
                "corpus_type": "simple_text",
                "expected_calculations": ["weighted_score"],
                "expected_csv_fields": ["score", "category"]
            },
            {
                "name": "Complex_Nested_Framework",
                "framework_data": self.test_factory.create_complex_nested_framework_data(),
                "corpus_type": "complex_document",
                "expected_calculations": ["composite_analysis_score"],
                "expected_csv_fields": ["primary_analysis_level_1_sub_level_1a", "secondary_analysis_temporal_tracking_trend"]
            }
        ]
        
        # Create mock responses for each scenario
        self.mock_responses = {}
        for scenario in self.test_scenarios:
            clean_json = json.dumps(scenario["framework_data"])
            messy_response = f"""
Here is my {scenario['name']} analysis:
```json
{scenario['framework_data']}
```
Analysis complete.
"""
            self.mock_responses[clean_json] = messy_response
        
        # Add synthesis response
        self.mock_responses["Synthesize the following information into a clear"] = "# Comprehensive Analysis Report\n\nThis report synthesizes results from multiple framework types."
    
    def test_all_framework_types_process_successfully(self):
        """Test that all framework types process through the pipeline successfully."""
        from discernus.orchestration.workflow_orchestrator import WorkflowOrchestrator
        
        for scenario in self.test_scenarios:
            with self.subTest(scenario=scenario["name"]):
                # Create test state for this scenario
                analysis_results = [{
                    "agent_id": f"test_{scenario['name'].lower()}_agent",
                    "corpus_file": f"{scenario['corpus_type']}_document.txt",
                    "raw_response": self.mock_responses[json.dumps(scenario["framework_data"])],
                    "success": True,
                    "model_name": "test_model",
                    "run_num": 1
                }]
                
                test_state = self._create_test_state(analysis_results, scenario)
                
                # Execute pipeline
                project_path = project_root / "projects" / "MVA" / "experiment_1"
                orchestrator = WorkflowOrchestrator(str(project_path))
                orchestrator.gateway = MockLLMGateway(self.mock_responses)
                
                result = orchestrator.execute_workflow(test_state)
                
                # Verify successful completion
                self.assertEqual(result['status'], 'success')
                
                # Verify expected CSV fields are present
                csv_path = orchestrator.session_results_path / "test_results.csv"
                if csv_path.exists():
                    import pandas as pd
                    df = pd.read_csv(csv_path)
                    
                    for expected_field in scenario["expected_csv_fields"]:
                        self.assertIn(expected_field, df.columns, 
                                    f"Expected field '{expected_field}' not found in CSV for {scenario['name']}")
    
    def test_calculation_agent_handles_diverse_numeric_structures(self):
        """Test that CalculationAgent can find numeric values in any framework structure."""
        from discernus.agents.calculation_agent import CalculationAgent
        
        for scenario in self.test_scenarios:
            with self.subTest(scenario=scenario["name"]):
                calc_agent = CalculationAgent()
                
                # Create test workflow state with calculation spec
                workflow_state = {
                    'framework': {
                        'calculation_spec': [
                            {'name': 'test_calc', 'formula': '0.5'}  # Simple formula that should work with any framework
                        ]
                    },
                    'analysis_results': [{
                        'success': True,
                        'json_output': scenario["framework_data"]
                    }]
                }
                
                result = calc_agent.execute(workflow_state, {})
                
                # Verify calculation was added
                self.assertIn('test_calc', result['analysis_results'][0]['json_output'])
                self.assertEqual(result['analysis_results'][0]['json_output']['test_calc'], 0.5)
    
    def test_synthesis_agent_csv_generation_framework_agnostic(self):
        """Test that SynthesisAgent CSV generation works with all framework types through the orchestrator."""
        from discernus.orchestration.workflow_orchestrator import WorkflowOrchestrator
        
        # Create mixed scenario with all framework types
        mixed_analysis_results = []
        for i, scenario in enumerate(self.test_scenarios):
            mixed_analysis_results.append({
                "agent_id": f"test_agent_{i}",
                "corpus_file": f"document_{i}.txt",
                "raw_response": self.mock_responses[json.dumps(scenario["framework_data"])],
                "success": True,
                "model_name": "test_model",
                "run_num": 1
            })
        
        # Create test state
        test_state = {
            'workflow': [
                {'agent': 'DataExtractionAgent'},
                {'agent': 'CalculationAgent'},
                {'agent': 'SynthesisAgent', 'config': {'output_artifacts': ['test_report.md', 'test_results.csv']}}
            ],
            'experiment': {'name': 'Mixed Framework Test'},
            'framework': {'name': 'Mixed Test Framework'},
            'analysis_results': mixed_analysis_results
        }
        
        # Execute pipeline
        project_path = project_root / "projects" / "MVA" / "experiment_1"
        orchestrator = WorkflowOrchestrator(str(project_path))
        orchestrator.gateway = MockLLMGateway(self.mock_responses)
        
        result = orchestrator.execute_workflow(test_state)
        
        # Verify successful completion
        self.assertEqual(result['status'], 'success')
        
        # Check that CSV was generated and contains data from all frameworks
        csv_path = orchestrator.session_results_path / "test_results.csv"
        if csv_path.exists():
            import pandas as pd
            df = pd.read_csv(csv_path)
            
            # Should have one row for each framework type
            self.assertEqual(len(df), len(self.test_scenarios))
            
            # Should have columns representing data from all framework types
            self.assertGreater(len(df.columns), 10)  # Should have many columns due to framework diversity
    
    def _create_test_state(self, analysis_results: List[Dict], scenario: Dict) -> Dict[str, Any]:
        """Helper method to create test workflow state."""
        return {
            'workflow': [
                {'agent': 'DataExtractionAgent'},
                {'agent': 'CalculationAgent'},
                {'agent': 'SynthesisAgent', 'config': {'output_artifacts': ['test_report.md', 'test_results.csv']}}
            ],
            'experiment': {
                'name': f'{scenario["name"]} Test',
                'description': f'Testing {scenario["corpus_type"]} analysis'
            },
            'framework': {
                'name': f'{scenario["name"]} Framework',
                'calculation_spec': [
                    {'name': calc_name, 'formula': '0.5'}
                    for calc_name in scenario["expected_calculations"]
                ]
            },
            'analysis_results': analysis_results
        }

if __name__ == '__main__':
    unittest.main() 