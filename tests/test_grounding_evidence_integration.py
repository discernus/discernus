#!/usr/bin/env python3
"""
Test Grounding Evidence Integration - THIN Implementation

Tests the integration of grounding evidence generation with the synthesis pipeline.
"""

import json
import tempfile
import os
from unittest.mock import Mock, patch

from discernus.agents.thin_synthesis.orchestration.pipeline import (
    ProductionThinSynthesisPipeline,
    ProductionPipelineRequest
)
from discernus.agents.score_grounding.grounding_evidence_generator import (
    GroundingEvidenceGenerator
)


def test_pipeline_initialization_with_grounding():
    """Test that the pipeline initializes correctly with grounding evidence generator."""
    # Mock dependencies
    mock_artifact_client = Mock()
    mock_audit_logger = Mock()
    
    # Initialize pipeline
    pipeline = ProductionThinSynthesisPipeline(
        artifact_client=mock_artifact_client,
        audit_logger=mock_audit_logger,
        model="vertex_ai/gemini-2.5-flash-lite"
    )
    
    # Check that grounding evidence generator is initialized
    assert hasattr(pipeline, 'grounding_evidence_generator')
    assert isinstance(pipeline.grounding_evidence_generator, GroundingEvidenceGenerator)
    assert pipeline.grounding_evidence_generator.model == "vertex_ai/gemini-2.5-flash-lite"
    
    print("✅ Pipeline initialization with grounding evidence test passed")


def test_grounding_evidence_request_structure():
    """Test that grounding evidence requests are structured correctly."""
    from discernus.agents.score_grounding.grounding_evidence_generator import GroundingEvidenceRequest
    
    # Create sample request
    request = GroundingEvidenceRequest(
        analysis_scores={"populism_score": 0.85, "pluralism_score": 0.45},
        evidence_data=b'{"evidence": [{"text": "test", "confidence": 0.8}]}',
        framework_spec="# Test Framework",
        document_name="test_document.txt",
        min_confidence_threshold=0.6
    )
    
    # Validate structure
    assert request.analysis_scores["populism_score"] == 0.85
    assert request.evidence_data == b'{"evidence": [{"text": "test", "confidence": 0.8}]}'
    assert request.framework_spec == "# Test Framework"
    assert request.document_name == "test_document.txt"
    assert request.min_confidence_threshold == 0.6
    
    print("✅ Grounding evidence request structure test passed")


def test_pipeline_request_with_grounding():
    """Test that pipeline requests can include grounding evidence context."""
    request = ProductionPipelineRequest(
        framework_spec="# Test Framework",
        scores_artifact_hash="abc123def456",
        evidence_artifact_hash="def456ghi789",
        experiment_context="Document: test_document.txt, Framework: CFF v7.3",
        max_evidence_per_finding=3,
        min_confidence_threshold=0.7,
        interpretation_focus="comprehensive",
        framework_hash="framework_hash_123",
        corpus_hash="corpus_hash_456",
        framework_name="CFF v7.3",
        corpus_manifest={"documents": ["test_document.txt"]}
    )
    
    # Validate request structure
    assert request.framework_spec == "# Test Framework"
    assert request.scores_artifact_hash == "abc123def456"
    assert request.evidence_artifact_hash == "def456ghi789"
    assert "test_document.txt" in request.experiment_context
    assert request.max_evidence_per_finding == 3
    assert request.min_confidence_threshold == 0.7
    assert request.framework_name == "CFF v7.3"
    
    print("✅ Pipeline request with grounding context test passed")


@patch('discernus.agents.thin_synthesis.orchestration.pipeline.LLMGateway')
def test_grounding_evidence_stage_integration(mock_llm_gateway):
    """Test that the grounding evidence stage integrates correctly with the pipeline."""
    # Mock LLM responses for different stages
    mock_llm_gateway.return_value.execute_call.return_value = (
        '{"analysis_plan": {"stages": ["descriptive_stats", "correlations"]}}', {}
    )
    
    # Mock artifact client
    mock_artifact_client = Mock()
    mock_artifact_client.get_artifact.return_value = b'{"scores": [{"populism_score": 0.85}]}'
    mock_artifact_client.put_artifact.return_value = "artifact_hash_123"
    mock_artifact_client.artifact_exists.return_value = False
    
    # Mock audit logger
    mock_audit_logger = Mock()
    
    # Initialize pipeline
    pipeline = ProductionThinSynthesisPipeline(
        artifact_client=mock_artifact_client,
        audit_logger=mock_audit_logger,
        model="vertex_ai/gemini-2.5-flash-lite"
    )
    
    # Create pipeline request
    request = ProductionPipelineRequest(
        framework_spec="# Test Framework\n## Analysis Dimensions\n- populism_pluralism_axis",
        scores_artifact_hash="scores_hash_123",
        evidence_artifact_hash="evidence_hash_456",
        experiment_context="Document: test_document.txt",
        framework_name="CFF v7.3"
    )
    
    # Test that pipeline can be initialized with grounding evidence generator
    assert hasattr(pipeline, 'grounding_evidence_generator')
    assert pipeline.grounding_evidence_generator is not None
    
    print("✅ Grounding evidence stage integration test passed")


def test_grounding_evidence_response_serialization():
    """Test that grounding evidence responses can be serialized correctly."""
    from discernus.agents.score_grounding.grounding_evidence_generator import (
        GroundingEvidenceResponse,
        GroundingEvidence
    )
    
    # Create sample grounding evidence
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
    
    # Create response
    response = GroundingEvidenceResponse(
        grounding_evidence=[grounding_evidence],
        generation_summary={
            "total_scores": 1,
            "grounded_scores": 1,
            "coverage_percentage": 100.0,
            "generation_time_seconds": 2.5,
            "average_evidence_confidence": 0.8,
            "high_confidence_evidence": 1
        },
        success=True
    )
    
    # Test serialization
    serialized = response.to_json_serializable()
    
    assert serialized["success"] == True
    assert len(serialized["grounding_evidence"]) == 1
    assert serialized["grounding_evidence"][0]["document_id"] == "test_document.txt"
    assert serialized["grounding_evidence"][0]["dimension"] == "populism_pluralism_axis"
    assert serialized["grounding_evidence"][0]["score"] == 0.85
    assert serialized["generation_summary"]["coverage_percentage"] == 100.0
    
    # Test JSON serialization
    json_str = json.dumps(serialized)
    assert "test_document.txt" in json_str
    assert "populism_pluralism_axis" in json_str
    assert "0.85" in json_str
    
    print("✅ Grounding evidence response serialization test passed")


def run_all_integration_tests():
    """Run all grounding evidence integration tests."""
    print("🧪 Running Grounding Evidence Integration Tests...")
    
    test_pipeline_initialization_with_grounding()
    test_grounding_evidence_request_structure()
    test_pipeline_request_with_grounding()
    test_grounding_evidence_response_serialization()
    
    print("✅ All grounding evidence integration tests passed!")


if __name__ == "__main__":
    run_all_integration_tests() 