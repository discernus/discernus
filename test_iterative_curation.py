#!/usr/bin/env python3
"""
Test script for iterative evidence curation functionality
"""

import sys
import os
import json
from pathlib import Path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from discernus.agents.intelligent_evidence_retriever import IntelligentEvidenceRetrievalAgent
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.audit_logger import AuditLogger
from discernus.core.run_context import RunContext

def test_iterative_curation():
    """Test iterative evidence curation with real nano experiment data."""
    
    # Use existing nano experiment with real artifacts
    nano_dir = Path("/Volumes/code/discernus/projects/nano_test_experiment")
    nano_run_dir = nano_dir / "runs" / "20250920_223951"
    
    security = ExperimentSecurityBoundary(nano_dir)
    storage = LocalArtifactStorage(security, nano_run_dir)
    audit = AuditLogger(security, nano_run_dir)
    
    # Create agent
    agent = IntelligentEvidenceRetrievalAgent(security, storage, audit)
    
    # Create mock RunContext with real data
    artifacts_dir = nano_run_dir / "artifacts"
    registry_file = artifacts_dir / "artifact_registry.json"
    
    with open(registry_file, 'r') as f:
        registry = json.load(f)
    artifact_hashes = list(registry.keys())
    
    # Create RunContext with mock statistical results
    run_context = RunContext(
        experiment_id="nano_test_experiment",
        framework_path=nano_dir / "sentiment_binary_v1.md", 
        corpus_path=nano_dir / "corpus.md"
    )
    run_context.analysis_artifacts = artifact_hashes
    
    # Add mock statistical results
    run_context.statistical_results = {
        "correlations": {
            "positive_negative_sentiment": -1.0
        },
        "descriptive_stats": {
            "positive_sentiment": {"mean": 0.5, "std": 0.707},
            "negative_sentiment": {"mean": 0.5, "std": 0.707}
        },
        "significant_findings": [
            "Perfect negative correlation between positive and negative sentiment",
            "Binary sentiment classification working as expected"
        ]
    }
    
    print("=== Testing Iterative Evidence Curation ===")
    
    # Test evidence selection for iteration
    print("\n1. Testing evidence selection:")
    evidence_count, evidence_size_mb = agent.count_evidence_artifacts(run_context)
    print(f"Total evidence artifacts: {evidence_count}")
    
    # Create mock iteration
    mock_iteration = {
        "iteration_name": "test_sentiment_analysis",
        "focus_area": "sentiment_correlation_patterns",
        "statistical_targets": ["negative_correlation", "binary_classification"],
        "evidence_subset": "all_evidence",
        "curation_instructions": "Find quotes that demonstrate clear positive or negative sentiment",
        "expected_quotes": 5,
        "priority": "high"
    }
    
    # Test evidence selection
    evidence_artifacts = agent._get_evidence_for_iteration(run_context, mock_iteration)
    print(f"Selected evidence artifacts: {len(evidence_artifacts)}")
    
    for i, artifact in enumerate(evidence_artifacts):
        print(f"  {i+1}. Document {artifact['document_index']}: {len(artifact['evidence_content'])} chars")
    
    # Test prompt creation
    print("\n2. Testing curation prompt creation:")
    curation_prompt = agent._create_curation_prompt(run_context, mock_iteration, evidence_artifacts)
    print(f"Prompt length: {len(curation_prompt)} characters")
    print("Prompt preview:")
    print(curation_prompt[:500] + "...")
    
    # Test quote parsing with mock response
    print("\n3. Testing quote parsing:")
    mock_response = '''
Document 0:
"This is a very positive statement about the future."
Statistical relevance: Supports positive sentiment classification
Strength rating: 4

Document 1:
"I feel terrible about this situation and everything is wrong."
Statistical relevance: Supports negative sentiment classification  
Strength rating: 5
'''
    
    parsed_quotes = agent._parse_curated_quotes(mock_response, mock_iteration)
    print(f"Parsed {len(parsed_quotes)} quotes:")
    
    for i, quote in enumerate(parsed_quotes):
        print(f"  {i+1}. Doc {quote.get('document_index', 'unknown')}: {quote.get('quote_text', 'N/A')[:50]}...")
        print(f"     Strength: {quote.get('strength_rating', 'N/A')}, Focus: {quote.get('iteration_focus', 'N/A')}")
    
    # Test artifact storage
    print("\n4. Testing artifact storage:")
    mock_results = {
        "quotes": parsed_quotes,
        "focus_area": mock_iteration['focus_area'],
        "evidence_processed": len(evidence_artifacts),
        "model_used": "gemini-2.5-flash"
    }
    
    artifact_hash = agent.store_curated_artifact(mock_results, mock_iteration['focus_area'])
    print(f"Stored curated artifact: {artifact_hash}")
    
    # Verify stored artifact
    stored_bytes = storage.get_artifact(artifact_hash)
    stored_data = json.loads(stored_bytes.decode('utf-8'))
    print(f"Verified storage: {stored_data['agent_name']}, {len(stored_data['curated_evidence']['quotes'])} quotes")
    
    print("\n✅ Iterative evidence curation tests passed!")
    print("🎯 Ready for real LLM curation execution!")

if __name__ == "__main__":
    test_iterative_curation()
