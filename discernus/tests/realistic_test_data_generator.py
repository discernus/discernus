#!/usr/bin/env python3
"""
Realistic Test Data Generator
============================

This module generates realistic test data based on actual LLM response patterns
to address the test coverage gap identified in the MVA Experiment 3 failure.

Key principle: Test what LLMs actually produce, not what we wish they would produce.
"""

import json
from typing import Dict, Any, List, Optional
from pathlib import Path


class RealisticTestDataGenerator:
    """
    Generates realistic test data based on actual LLM response patterns.
    
    This addresses the critical test coverage gap where our tests were using
    artificially constrained LLM responses instead of realistic hierarchical JSON.
    """
    
    def __init__(self):
        self.cff_v4_1_patterns = self._load_cff_v4_1_patterns()
        self.pdaf_patterns = self._load_pdaf_patterns()
        self.generic_patterns = self._load_generic_patterns()
    
    def _load_cff_v4_1_patterns(self) -> List[Dict[str, Any]]:
        """Load realistic CFF v4.1 response patterns based on actual LLM output."""
        return [
            {
                "name": "gemini_hierarchical_cff",
                "description": "Typical Gemini response to CFF v4.1 framework",
                "response": {
                    "Political Worldview Classification": {
                        "Worldview": "Progressive"
                    },
                    "Cohesive Flourishing Framework v4.1 Analysis": {
                        "Identity Axis": {
                            "Tribal Dominance": {
                                "Score": 0.1,
                                "Confidence": 0.8,
                                "Evidence": [
                                    "The speaker consistently uses inclusive language",
                                    "No evidence of group hierarchy or supremacy claims"
                                ]
                            },
                            "Individual Dignity": {
                                "Score": 0.9,
                                "Confidence": 0.9,
                                "Evidence": [
                                    "Emphasis on 'universal rights' and 'inherent dignity'",
                                    "Consistent use of equality language throughout"
                                ]
                            }
                        },
                        "Fear-Hope Axis": {
                            "Fear": {
                                "Score": 0.3,
                                "Confidence": 0.7,
                                "Evidence": [
                                    "References to 'challenges' and 'obstacles'",
                                    "Some urgency markers present"
                                ]
                            },
                            "Hope": {
                                "Score": 0.8,
                                "Confidence": 0.8,
                                "Evidence": [
                                    "Strong opportunity language: 'bright future', 'breakthrough'",
                                    "Progress emphasis throughout the speech"
                                ]
                            }
                        },
                        "Envy-Compersion Axis": {
                            "Envy": {
                                "Score": 0.2,
                                "Confidence": 0.6,
                                "Evidence": [
                                    "Mild critique of 'privileged elite' mentioned once",
                                    "No significant success dismissal patterns"
                                ]
                            },
                            "Compersion": {
                                "Score": 0.7,
                                "Confidence": 0.8,
                                "Evidence": [
                                    "Celebrates achievements of coalition partners",
                                    "Recognition of hard work and merit"
                                ]
                            }
                        },
                        "Enmity-Amity Axis": {
                            "Enmity": {
                                "Score": 0.1,
                                "Confidence": 0.9,
                                "Evidence": [
                                    "No hostile language toward people",
                                    "Critique focused on systems, not individuals"
                                ]
                            },
                            "Amity": {
                                "Score": 0.9,
                                "Confidence": 0.9,
                                "Evidence": [
                                    "Extensive use of friendship and partnership language",
                                    "Unity expressions: 'together', 'united', 'connected'"
                                ]
                            }
                        },
                        "Goal Axis": {
                            "Fragmentative Goals": {
                                "Score": 0.0,
                                "Confidence": 0.9,
                                "Evidence": [
                                    "No dominance seeking language",
                                    "No zero-sum competition rhetoric"
                                ]
                            },
                            "Cohesive Goals": {
                                "Score": 1.0,
                                "Confidence": 0.9,
                                "Evidence": [
                                    "Service orientation: 'help', 'support', 'aid'",
                                    "Unity building: 'bring together', 'connect', 'include'"
                                ]
                            }
                        }
                    },
                    "Overall Analysis Confidence": 0.8,
                    "Competitive Patterns Observed": "Pure Directional"
                }
            },
            {
                "name": "claude_nested_cff",
                "description": "Claude's typical response structure for CFF analysis",
                "response": {
                    "framework_analysis": {
                        "worldview_classification": "Conservative",
                        "cff_scoring": {
                            "identity_dimension": {
                                "tribal_dominance": {
                                    "score": 0.6,
                                    "confidence": 0.7,
                                    "supporting_evidence": [
                                        "Appeals to traditional values and established order",
                                        "In-group references to 'real Americans' and 'our people'"
                                    ]
                                },
                                "individual_dignity": {
                                    "score": 0.4,
                                    "confidence": 0.6,
                                    "supporting_evidence": [
                                        "Some universal principles mentioned",
                                        "Focus on individual responsibility"
                                    ]
                                }
                            },
                            "emotional_dimensions": {
                                "fear_markers": {
                                    "score": 0.7,
                                    "confidence": 0.8,
                                    "evidence": [
                                        "Crisis language: 'under attack', 'existential threat'",
                                        "Urgency markers: 'running out of time'"
                                    ]
                                },
                                "hope_markers": {
                                    "score": 0.5,
                                    "confidence": 0.6,
                                    "evidence": [
                                        "Some opportunity language present",
                                        "References to restoration and renewal"
                                    ]
                                }
                            },
                            "social_dimensions": {
                                "envy_patterns": 0.3,
                                "compersion_patterns": 0.4,
                                "enmity_patterns": 0.2,
                                "amity_patterns": 0.6
                            },
                            "goal_orientation": {
                                "fragmentative_goals": 0.3,
                                "cohesive_goals": 0.7
                            }
                        }
                    },
                    "analysis_metadata": {
                        "overall_confidence": 0.7,
                        "competitive_pattern": "Strategic Balance",
                        "framework_version": "CFF v4.1"
                    }
                }
            }
        ]
    
    def _load_pdaf_patterns(self) -> List[Dict[str, Any]]:
        """Load realistic PDAF response patterns."""
        return [
            {
                "name": "gemini_pdaf_analysis",
                "description": "Typical Gemini response to PDAF framework",
                "response": {
                    "Political Discourse Analysis Framework Results": {
                        "Worldview Classification": "Progressive",
                        "Discourse Categories": {
                            "Populist Elements": {
                                "People vs Elite": {
                                    "score": 0.8,
                                    "evidence": [
                                        "Clear distinction between 'working families' and 'billionaire class'",
                                        "Consistent framing of ordinary people against powerful interests"
                                    ]
                                },
                                "Moral Outrage": {
                                    "score": 0.6,
                                    "evidence": [
                                        "Expressions of anger at system unfairness",
                                        "Calls for justice and accountability"
                                    ]
                                }
                            },
                            "Democratic Elements": {
                                "Pluralism": {
                                    "score": 0.7,
                                    "evidence": [
                                        "Recognition of multiple valid perspectives",
                                        "Emphasis on coalition building"
                                    ]
                                },
                                "Institutional Respect": {
                                    "score": 0.5,
                                    "evidence": [
                                        "Mixed references to democratic institutions",
                                        "Some critique of current system functioning"
                                    ]
                                }
                            }
                        },
                        "Rhetorical Strategies": {
                            "Emotional Appeals": 0.8,
                            "Logical Arguments": 0.6,
                            "Credibility Markers": 0.7
                        }
                    },
                    "Analysis Confidence": 0.8,
                    "Framework Version": "PDAF v1.1"
                }
            }
        ]
    
    def _load_generic_patterns(self) -> List[Dict[str, Any]]:
        """Load generic response patterns for framework-agnostic testing."""
        return [
            {
                "name": "gpt_custom_framework",
                "description": "GPT response to custom framework",
                "response": {
                    "Analysis Results": {
                        "Primary Classification": "Category A",
                        "Detailed Scoring": {
                            "dimension_1": {
                                "sub_dimension_a": 0.7,
                                "sub_dimension_b": 0.3,
                                "confidence": 0.8
                            },
                            "dimension_2": {
                                "sub_dimension_c": 0.5,
                                "sub_dimension_d": 0.6,
                                "confidence": 0.7
                            }
                        },
                        "Supporting Evidence": {
                            "key_quotes": [
                                "Evidence supporting the analysis",
                                "Additional supporting quote"
                            ],
                            "reasoning": "Detailed explanation of the analysis"
                        }
                    },
                    "Metadata": {
                        "confidence_score": 0.75,
                        "analysis_approach": "systematic",
                        "framework_compliance": "high"
                    }
                }
            }
        ]
    
    def generate_realistic_response(self, framework_type: str, pattern_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a realistic LLM response for testing.
        
        Args:
            framework_type: Type of framework ("cff", "pdaf", "generic")
            pattern_name: Specific pattern to use (optional)
            
        Returns:
            Realistic hierarchical JSON response
        """
        if framework_type == "cff":
            patterns = self.cff_v4_1_patterns
        elif framework_type == "pdaf":
            patterns = self.pdaf_patterns
        elif framework_type == "generic":
            patterns = self.generic_patterns
        else:
            raise ValueError(f"Unknown framework type: {framework_type}")
        
        if pattern_name:
            pattern = next((p for p in patterns if p["name"] == pattern_name), None)
            if not pattern:
                raise ValueError(f"Pattern '{pattern_name}' not found in {framework_type} patterns")
        else:
            pattern = patterns[0]  # Use first pattern as default
        
        return pattern["response"]
    
    def get_expected_flat_schema(self, framework_type: str) -> Dict[str, str]:
        """
        Get the expected flat schema for a framework type.
        
        This represents what the DataExtractionAgent should produce
        after transforming the hierarchical JSON.
        """
        if framework_type == "cff":
            return {
                "worldview": "string",
                "tribal_dominance_score": "number",
                "tribal_dominance_confidence": "number",
                "tribal_dominance_evidence": "array",
                "individual_dignity_score": "number",
                "individual_dignity_confidence": "number",
                "individual_dignity_evidence": "array",
                "fear_score": "number",
                "fear_confidence": "number",
                "fear_evidence": "array",
                "hope_score": "number",
                "hope_confidence": "number",
                "hope_evidence": "array",
                "envy_score": "number",
                "envy_confidence": "number",
                "envy_evidence": "array",
                "compersion_score": "number",
                "compersion_confidence": "number",
                "compersion_evidence": "array",
                "enmity_score": "number",
                "enmity_confidence": "number",
                "enmity_evidence": "array",
                "amity_score": "number",
                "amity_confidence": "number",
                "amity_evidence": "array",
                "fragmentative_goal_score": "number",
                "fragmentative_goal_confidence": "number",
                "fragmentative_goal_evidence": "array",
                "cohesive_goal_score": "number",
                "cohesive_goal_confidence": "number",
                "cohesive_goal_evidence": "array",
                "overall_analysis_confidence": "number",
                "competitive_patterns_observed": "string"
            }
        elif framework_type == "pdaf":
            return {
                "worldview": "string",
                "people_vs_elite_score": "number",
                "people_vs_elite_evidence": "array",
                "moral_outrage_score": "number",
                "moral_outrage_evidence": "array",
                "pluralism_score": "number",
                "pluralism_evidence": "array",
                "institutional_respect_score": "number",
                "institutional_respect_evidence": "array",
                "emotional_appeals": "number",
                "logical_arguments": "number",
                "credibility_markers": "number",
                "analysis_confidence": "number",
                "framework_version": "string"
            }
        else:
            return {
                "primary_classification": "string",
                "dimension_1_a": "number",
                "dimension_1_b": "number",
                "dimension_2_c": "number",
                "dimension_2_d": "number",
                "confidence_score": "number",
                "key_quotes": "array",
                "reasoning": "string"
            }
    
    def create_test_case(self, framework_type: str, pattern_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a complete test case with realistic input and expected output.
        
        Returns:
            Dictionary containing:
            - input_response: Realistic hierarchical JSON
            - expected_schema: Expected flat schema
            - test_description: Human-readable description
        """
        realistic_response = self.generate_realistic_response(framework_type, pattern_name)
        expected_schema = self.get_expected_flat_schema(framework_type)
        
        return {
            "input_response": realistic_response,
            "expected_schema": expected_schema,
            "test_description": f"Test {framework_type} schema transformation with realistic {pattern_name or 'default'} pattern",
            "framework_type": framework_type,
            "pattern_name": pattern_name
        }
    
    def save_test_fixtures(self, output_dir: Path):
        """Save test fixtures to disk for use in test suites."""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate test cases for each framework type
        frameworks = ["cff", "pdaf", "generic"]
        
        for framework_type in frameworks:
            patterns = getattr(self, f"{framework_type}_v4_1_patterns" if framework_type == "cff" else f"{framework_type}_patterns")
            
            for pattern in patterns:
                test_case = self.create_test_case(framework_type, pattern["name"])
                
                filename = f"{framework_type}_{pattern['name']}_test_case.json"
                filepath = output_dir / filename
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(test_case, f, indent=2, ensure_ascii=False)
                
                print(f"✅ Saved test fixture: {filepath}")


def main():
    """Generate realistic test data fixtures."""
    generator = RealisticTestDataGenerator()
    
    # Create test fixtures directory
    fixtures_dir = Path("discernus/tests/fixtures/realistic_responses")
    
    print("🔬 Generating realistic test data fixtures...")
    generator.save_test_fixtures(fixtures_dir)
    print(f"✅ Test fixtures saved to: {fixtures_dir}")


if __name__ == "__main__":
    main() 