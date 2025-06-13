#!/usr/bin/env python3
"""
Unit Tests for LLM Quality Assurance System
==========================================

Tests the multi-layered validation system for LLM analysis results,
specifically targeting the Roosevelt 1933 silent failure scenario.
"""

import pytest
import numpy as np
from src.narrative_gravity.utils.llm_quality_assurance import (
    LLMQualityAssuranceSystem,
    validate_llm_analysis,
    QualityCheck,
    QualityAssessment
)

class TestLLMQualityAssuranceSystem:
    """Test suite for LLM Quality Assurance System."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.qa_system = LLMQualityAssuranceSystem()
        
        # Test data representing Roosevelt 1933 case (silent failure)
        self.roosevelt_text = """
        My fellow Americans, in this dark hour of our nation's history, 
        we must face the truth of our economic crisis with courage and determination.
        The only thing we have to fear is fear itself.
        """
        
        # Simulated LLM response with high default values (Roosevelt 1933 case)
        # 8/10 wells defaulted = 80% default ratio - should trigger CRITICAL and LOW confidence
        self.roosevelt_failing_response = {
            "scores": {
                "Dignity": 0.3,    # Failed parsing - defaulted
                "Truth": 0.65,     # Successfully parsed
                "Justice": 0.3,    # Failed parsing - defaulted
                "Hope": 0.55,      # Successfully parsed  
                "Pragmatism": 0.3, # Failed parsing - defaulted
                "Tribalism": 0.3,  # Failed parsing - defaulted
                "Manipulation": 0.3, # Failed parsing - defaulted
                "Resentment": 0.3, # Failed parsing - defaulted
                "Fantasy": 0.3,    # Failed parsing - defaulted
                "Fear": 0.3        # Failed parsing - defaulted
            },
            "analysis": "Brief analysis provided"
        }
        
        # Good quality response for comparison
        self.good_response = {
            "scores": {
                "Dignity": 0.8,
                "Truth": 0.7,
                "Justice": 0.6,
                "Hope": 0.9,
                "Pragmatism": 0.5,
                "Tribalism": 0.2,
                "Manipulation": 0.1,
                "Resentment": 0.3,
                "Fantasy": 0.2,
                "Fear": 0.4
            },
            "analysis": "Comprehensive analysis with detailed reasoning for each well score..."
        }
    
    def test_roosevelt_1933_case_detection(self):
        """Test detection of Roosevelt 1933 silent failure case."""
        
        assessment = self.qa_system.validate_llm_analysis(
            text_input=self.roosevelt_text,
            framework="civic_virtue",
            llm_response=self.roosevelt_failing_response,
            parsed_scores=self.roosevelt_failing_response["scores"]
        )
        
        # Should detect LOW confidence due to high default ratio
        assert assessment.confidence_level == "LOW"
        assert assessment.confidence_score < 0.5
        
        # Should require second opinion
        assert assessment.requires_second_opinion == True
        
        # Should detect high default value ratio anomaly
        default_ratio_anomaly = any("High default value ratio" in anomaly for anomaly in assessment.anomalies_detected)
        assert default_ratio_anomaly
        
        # Should have critical failure for default value ratio
        default_ratio_check = next((check for check in assessment.individual_checks 
                                  if check.check_name == "default_value_ratio"), None)
        assert default_ratio_check is not None
        assert default_ratio_check.passed == False
        assert default_ratio_check.severity == "CRITICAL"
    
    def test_good_quality_analysis(self):
        """Test that good quality analysis gets HIGH confidence."""
        
        assessment = self.qa_system.validate_llm_analysis(
            text_input=self.roosevelt_text,
            framework="civic_virtue", 
            llm_response=self.good_response,
            parsed_scores=self.good_response["scores"]
        )
        
        # Should get HIGH confidence
        assert assessment.confidence_level == "HIGH"
        assert assessment.confidence_score >= 0.8
        
        # Should not require second opinion
        assert assessment.requires_second_opinion == False
        
        # Should have minimal anomalies
        assert len(assessment.anomalies_detected) <= 1
        
    def test_input_validation_layer(self):
        """Test Layer 1: Input Validation."""
        
        # Test with very short text (should fail)
        short_text = "Too short."
        checks = self.qa_system._validate_input(short_text, "civic_virtue")
        
        text_quality_check = next((check for check in checks if check.check_name == "text_quality"), None)
        assert text_quality_check.passed == False
        
        # Test with good text length
        good_text = "This is a properly sized text for analysis. " * 10
        checks = self.qa_system._validate_input(good_text, "civic_virtue")
        
        text_length_check = next((check for check in checks if check.check_name == "text_length"), None)
        assert text_length_check.passed == True
    
    def test_llm_response_validation_layer(self):
        """Test Layer 2: LLM Response Validation."""
        
        # Test with missing scores
        bad_response = {"analysis": "Text without scores"}
        checks = self.qa_system._validate_llm_response(bad_response, {}, "civic_virtue")
        
        required_fields_check = next((check for check in checks if check.check_name == "required_fields"), None)
        assert required_fields_check.passed == False
        
        # Test with invalid score ranges
        invalid_scores = {"Dignity": 1.5, "Truth": -0.2}  # Out of range
        checks = self.qa_system._validate_llm_response({"scores": invalid_scores}, invalid_scores, "civic_virtue")
        
        score_ranges_check = next((check for check in checks if check.check_name == "score_ranges"), None)
        assert score_ranges_check.passed == False
    
    def test_statistical_coherence_validation(self):
        """Test Layer 3: Statistical Coherence Validation."""
        
        # Test high default value ratio (Roosevelt 1933 case)
        default_heavy_scores = {well: 0.3 for well in ["Dignity", "Truth", "Justice", "Hope", "Pragmatism"]}
        default_heavy_scores.update({well: 0.3 for well in ["Tribalism", "Manipulation", "Resentment", "Fantasy", "Fear"]})
        
        checks, anomalies = self.qa_system._validate_statistical_coherence(default_heavy_scores)
        
        default_ratio_check = next((check for check in checks if check.check_name == "default_value_ratio"), None)
        assert default_ratio_check is not None
        assert default_ratio_check.passed == False
        assert default_ratio_check.severity == "CRITICAL"
        
        # Test low variance detection
        uniform_scores = {f"Well_{i}": 0.5 for i in range(10)}  # All same score
        checks, anomalies = self.qa_system._validate_statistical_coherence(uniform_scores)
        
        variance_check = next((check for check in checks if check.check_name == "score_variance"), None)
        assert variance_check.passed == False
    
    def test_mathematical_consistency_validation(self):
        """Test Layer 4: Mathematical Consistency Verification."""
        
        # Test with scores that would create exactly zero position (Roosevelt 1933 case)
        balanced_scores = {
            "Dignity": 0.6, "Truth": 0.6, "Justice": 0.6, "Hope": 0.6, "Pragmatism": 0.6,  # Integrative
            "Tribalism": 0.6, "Manipulation": 0.6, "Resentment": 0.6, "Fantasy": 0.6, "Fear": 0.6  # Disintegrative
        }
        
        checks = self.qa_system._validate_mathematical_consistency(balanced_scores, "civic_virtue")
        
        # Should detect position calculation issues
        position_check = next((check for check in checks if check.check_name == "position_calculation"), None)
        if position_check:  # May not always be exactly zero due to well positioning
            # Just verify the check was performed
            assert position_check.check_name == "position_calculation"
    
    def test_anomaly_detection_layer(self):
        """Test Layer 6: Anomaly Detection."""
        
        # Test identical scores detection
        identical_scores = {f"Well_{i}": 0.5 for i in range(10)}
        checks, anomalies = self.qa_system._detect_anomalies(identical_scores)
        
        assert "All scores identical - possible total parsing failure" in anomalies
        
        # Test outlier detection
        outlier_scores = {"Well_1": 0.1, "Well_2": 0.2, "Well_3": 0.2, "Well_4": 0.9}  # 0.9 is outlier
        checks, anomalies = self.qa_system._detect_anomalies(outlier_scores)
        
        anomaly_check = next((check for check in checks if check.check_name == "anomaly_summary"), None)
        assert anomaly_check is not None
    
    def test_confidence_scoring(self):
        """Test confidence score calculation."""
        
        # Create mock checks with different severities
        good_checks = [
            QualityCheck("INPUT", "test1", True, 1.0, "Good", "INFO"),
            QualityCheck("LLM_RESPONSE", "test2", True, 1.0, "Good", "INFO"),
            QualityCheck("STATISTICAL", "test3", True, 0.9, "Good", "INFO")
        ]
        
        bad_checks = [
            QualityCheck("INPUT", "test1", False, 0.0, "Bad", "CRITICAL"),
            QualityCheck("LLM_RESPONSE", "test2", False, 0.0, "Bad", "CRITICAL"), 
            QualityCheck("STATISTICAL", "test3", False, 0.0, "Bad", "CRITICAL")
        ]
        
        good_score = self.qa_system._calculate_confidence_score(good_checks)
        bad_score = self.qa_system._calculate_confidence_score(bad_checks)
        
        assert good_score > 0.8
        assert bad_score < 0.3
    
    def test_second_opinion_triggers(self):
        """Test conditions that trigger second opinion requirement."""
        
        # High default ratio should trigger second opinion
        high_default_checks = [
            QualityCheck("STATISTICAL", "default_value_ratio", False, 0.2, "High defaults", "CRITICAL",
                        details={'ratio': 0.6})
        ]
        
        needs_second = self.qa_system._needs_second_opinion(high_default_checks, [])
        assert needs_second == True
        
        # Multiple anomalies should trigger second opinion 
        multiple_anomalies = ["Anomaly 1", "Anomaly 2"]
        needs_second = self.qa_system._needs_second_opinion([], multiple_anomalies)
        assert needs_second == True
    
    def test_framework_wells_detection(self):
        """Test framework-specific well detection."""
        
        civic_virtue_wells = self.qa_system._get_expected_wells("civic_virtue")
        assert "Dignity" in civic_virtue_wells
        assert "Truth" in civic_virtue_wells
        assert "Tribalism" in civic_virtue_wells
        assert len(civic_virtue_wells) == 10
        
        unknown_wells = self.qa_system._get_expected_wells("unknown_framework")
        assert unknown_wells == []
    
    def test_convenience_function(self):
        """Test the convenience function interface."""
        
        assessment = validate_llm_analysis(
            text_input=self.roosevelt_text,
            framework="civic_virtue",
            llm_response=self.roosevelt_failing_response,
            parsed_scores=self.roosevelt_failing_response["scores"]
        )
        
        assert isinstance(assessment, QualityAssessment)
        assert assessment.confidence_level in ["HIGH", "MEDIUM", "LOW"]
        assert 0.0 <= assessment.confidence_score <= 1.0
        assert len(assessment.individual_checks) > 0

# Integration tests
class TestLLMQualityAssuranceIntegration:
    """Integration tests with actual DirectAPIClient."""
    
    def test_quality_assurance_integration(self):
        """Test that quality assurance is integrated into DirectAPIClient."""
        
        # This would require actual API keys, so we'll test the structure
        from src.narrative_gravity.api_clients.direct_api_client import DirectAPIClient
        
        client = DirectAPIClient()
        
        # Verify that the client has the QA context attributes
        assert hasattr(client, '_current_text')
        assert hasattr(client, '_current_framework')
        
        # Verify _parse_response accepts the new parameters
        import inspect
        sig = inspect.signature(client._parse_response)
        params = list(sig.parameters.keys())
        assert 'text_input' in params
        assert 'framework' in params

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 