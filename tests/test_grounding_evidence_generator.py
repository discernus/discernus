#!/usr/bin/env python3
"""
Test Grounding Evidence Generator - THIN Implementation

Tests the automatic grounding evidence generation for numerical scores.
"""

import json
import tempfile
import os
from unittest.mock import Mock, patch

from discernus.agents.score_grounding.grounding_evidence_generator import (
    GroundingEvidenceGenerator,
    GroundingEvidenceRequest,
    GroundingEvidence
)


def test_grounding_evidence_generator_initialization():
    """Test that the grounding evidence generator initializes correctly."""
    generator = GroundingEvidenceGenerator()
    assert generator.model == "vertex_ai/gemini-2.5-flash-lite"
    assert generator.agent_name == "GroundingEvidenceGenerator"
    print("✅ Grounding evidence generator initialization test passed")


def test_grounding_evidence_request_creation():
    """Test that grounding evidence requests can be created correctly."""
    analysis_scores = {
        "populism_score": 0.85,
        "pluralism_score": 0.45,
        "cohesion_score": 0.72
    }
    
    evidence_data = b'{"evidence": [{"text": "test evidence", "confidence": 0.8}]}'
    framework_spec = "# Test Framework\n## Analysis Dimensions\n- populism_pluralism_axis"
    
    request = GroundingEvidenceRequest(
        analysis_scores=analysis_scores,
        evidence_data=evidence_data,
        framework_spec=framework_spec,
        document_name="test_document.txt",
        min_confidence_threshold=0.6
    )
    
    assert request.analysis_scores == analysis_scores
    assert request.evidence_data == evidence_data
    assert request.framework_spec == framework_spec
    assert request.document_name == "test_document.txt"
    assert request.min_confidence_threshold == 0.6
    print("✅ Grounding evidence request creation test passed")


def test_grounding_evidence_structure():
    """Test that grounding evidence structures are created correctly."""
    grounding_evidence = GroundingEvidence(
        document_id="test_document.txt",
        dimension="populism_pluralism_axis",
        score=0.85,
        score_confidence=0.8,
        grounding_evidence={
            "primary_quote": "people that have been forgotten",
            "context": "My economic plan is about investing in places and people that have been forgotten",
            "evidence_confidence": 0.8,
            "reasoning": "Direct populist appeal targeting economic inequality",
            "validation_type": "direct_textual_support"
        },
        evidence_hash="abc123def456",
        generation_timestamp="2025-01-01T12:00:00Z"
    )
    
    assert grounding_evidence.document_id == "test_document.txt"
    assert grounding_evidence.dimension == "populism_pluralism_axis"
    assert grounding_evidence.score == 0.85
    assert grounding_evidence.score_confidence == 0.8
    assert grounding_evidence.evidence_hash == "abc123def456"
    assert "primary_quote" in grounding_evidence.grounding_evidence
    print("✅ Grounding evidence structure test passed")


def test_extract_numerical_scores():
    """Test extraction of numerical scores from analysis results."""
    generator = GroundingEvidenceGenerator()
    
    # Test simple numerical scores
    analysis_scores = {
        "populism_score": 0.85,
        "pluralism_score": 0.45,
        "cohesion_score": 0.72
    }
    
    numerical_scores = generator._extract_numerical_scores(analysis_scores)
    assert numerical_scores["populism_score"] == 0.85
    assert numerical_scores["pluralism_score"] == 0.45
    assert numerical_scores["cohesion_score"] == 0.72
    assert len(numerical_scores) == 3
    
    # Test nested numerical scores
    nested_scores = {
        "descriptive_stats": {
            "mean_populism": 0.75,
            "std_populism": 0.15
        },
        "correlation_matrix": {
            "populism_pluralism": -0.82
        }
    }
    
    numerical_scores = generator._extract_numerical_scores(nested_scores)
    assert numerical_scores["descriptive_stats_mean_populism"] == 0.75
    assert numerical_scores["descriptive_stats_std_populism"] == 0.15
    assert numerical_scores["correlation_matrix_populism_pluralism"] == -0.82
    assert len(numerical_scores) == 3
    
    print("✅ Numerical score extraction test passed")


def test_evidence_hash_creation():
    """Test evidence hash creation for verification."""
    generator = GroundingEvidenceGenerator()
    
    evidence_text = "people that have been forgotten"
    document_name = "test_document.txt"
    dimension = "populism_pluralism_axis"
    
    evidence_hash = generator._create_evidence_hash(evidence_text, document_name, dimension)
    
    # Hash should be 12 characters long
    assert len(evidence_hash) == 12
    assert isinstance(evidence_hash, str)
    
    # Same inputs should produce same hash
    hash2 = generator._create_evidence_hash(evidence_text, document_name, dimension)
    assert evidence_hash == hash2
    
    # Different inputs should produce different hash
    hash3 = generator._create_evidence_hash("different text", document_name, dimension)
    assert evidence_hash != hash3
    
    print("✅ Evidence hash creation test passed")


def test_grounding_summary_generation():
    """Test grounding summary generation."""
    generator = GroundingEvidenceGenerator()
    
    # Create sample grounding evidence
    grounding_evidence_list = [
        GroundingEvidence(
            document_id="test_document.txt",
            dimension="populism_pluralism_axis",
            score=0.85,
            score_confidence=0.8,
            grounding_evidence={
                "primary_quote": "test quote",
                "evidence_confidence": 0.8,
                "reasoning": "test reasoning"
            },
            evidence_hash="abc123def456",
            generation_timestamp="2025-01-01T12:00:00Z"
        ),
        GroundingEvidence(
            document_id="test_document.txt",
            dimension="cohesion_axis",
            score=0.72,
            score_confidence=0.7,
            grounding_evidence={
                "primary_quote": "another quote",
                "evidence_confidence": 0.9,
                "reasoning": "another reasoning"
            },
            evidence_hash="def456ghi789",
            generation_timestamp="2025-01-01T12:00:00Z"
        )
    ]
    
    total_scores = 3
    generation_time = 2.5
    
    summary = generator._generate_grounding_summary(grounding_evidence_list, total_scores, generation_time)
    
    assert summary["total_scores"] == 3
    assert summary["grounded_scores"] == 2
    assert summary["coverage_percentage"] == (2/3) * 100
    assert summary["generation_time_seconds"] == 2.5
    assert summary["average_evidence_confidence"] == (0.8 + 0.9) / 2
    assert summary["high_confidence_evidence"] == 2  # Both >= 0.8
    
    print("✅ Grounding summary generation test passed")


@patch('discernus.agents.score_grounding.grounding_evidence_generator.LLMGateway')
def test_grounding_evidence_generation_mock(mock_llm_gateway):
    """Test grounding evidence generation with mocked LLM."""
    # Mock LLM response
    mock_response = json.dumps([
        {
            "document_id": "test_document.txt",
            "dimension": "populism_pluralism_axis",
            "score": 0.85,
            "score_confidence": 0.8,
            "grounding_evidence": {
                "primary_quote": "people that have been forgotten",
                "context": "My economic plan is about investing in places and people that have been forgotten",
                "evidence_confidence": 0.8,
                "reasoning": "Direct populist appeal targeting economic inequality",
                "validation_type": "direct_textual_support"
            }
        }
    ])
    
    mock_llm_gateway.return_value.execute_call.return_value = (mock_response, {})
    
    generator = GroundingEvidenceGenerator()
    
    # Create test request
    request = GroundingEvidenceRequest(
        analysis_scores={"populism_score": 0.85},
        evidence_data=b'{"evidence": [{"text": "test evidence", "confidence": 0.8}]}',
        framework_spec="# Test Framework",
        document_name="test_document.txt"
    )
    
    # Generate grounding evidence
    response = generator.generate_grounding_evidence(request)
    
    assert response.success
    assert len(response.grounding_evidence) == 1
    assert response.grounding_evidence[0].document_id == "test_document.txt"
    assert response.grounding_evidence[0].dimension == "populism_pluralism_axis"
    assert response.grounding_evidence[0].score == 0.85
    
    print("✅ Grounding evidence generation mock test passed")


def run_all_tests():
    """Run all grounding evidence generator tests."""
    print("🧪 Running Grounding Evidence Generator Tests...")
    
    test_grounding_evidence_generator_initialization()
    test_grounding_evidence_request_creation()
    test_grounding_evidence_structure()
    test_extract_numerical_scores()
    test_evidence_hash_creation()
    test_grounding_summary_generation()
    
    # Mock test (requires patching)
    test_grounding_evidence_generation_mock()
    
    print("✅ All grounding evidence generator tests passed!")


if __name__ == "__main__":
    run_all_tests() 