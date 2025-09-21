#!/usr/bin/env python3
"""
Test script for IntelligentEvidenceRetrievalAgent strategic planning functionality
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

def test_strategic_planning():
    """Test strategic planning functionality with real nano experiment data."""
    
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
    
    # Add mock metadata
    run_context.metadata = {
        "framework_name": "Sentiment Binary Framework v1.0",
        "corpus_documents": ["doc1.txt", "doc2.txt"]
    }
    
    print("=== Testing Strategic Planning ===")
    
    # Test evidence inventory first
    evidence_count, evidence_size_mb = agent.count_evidence_artifacts(run_context)
    print(f"Evidence Count: {evidence_count}")
    print(f"Evidence Size: {evidence_size_mb:.3f} MB")
    
    # Test fallback planning (should use single_pass for small corpus)
    print("\n=== Testing Fallback Planning ===")
    fallback_plan = agent.create_fallback_plan(evidence_count, evidence_size_mb)
    
    print(f"Strategy: {fallback_plan['strategy']}")
    print(f"Rationale: {fallback_plan['rationale']}")
    print(f"Execution Model: {fallback_plan['execution_model']}")
    print(f"Cost Estimate: {fallback_plan['cost_estimate']}")
    print(f"Total Estimated Quotes: {fallback_plan['estimated_total_quotes']}")
    
    print(f"\nIterations ({len(fallback_plan['iterations'])}):")
    for i, iteration in enumerate(fallback_plan['iterations']):
        print(f"  {i+1}. {iteration['iteration_name']}")
        print(f"     Focus: {iteration['focus_area']}")
        print(f"     Targets: {iteration['statistical_targets']}")
        print(f"     Expected Quotes: {iteration['expected_quotes']}")
        print(f"     Priority: {iteration['priority']}")
    
    # Verify fallback plan structure
    assert fallback_plan['strategy'] == 'single_pass', "Should use single_pass for small corpus"
    assert fallback_plan['execution_model'] == 'flash', "Should use Flash for small corpus"
    assert fallback_plan['cost_estimate'] == 'low', "Should be low cost for small corpus"
    assert len(fallback_plan['iterations']) == 1, "Should have single iteration for small corpus"
    
    # Test with larger corpus (mock)
    print("\n=== Testing Large Corpus Planning ===")
    large_plan = agent.create_fallback_plan(500, 4.0)  # Large corpus
    
    print(f"Large Corpus Strategy: {large_plan['strategy']}")
    print(f"Large Corpus Model: {large_plan['execution_model']}")
    print(f"Large Corpus Iterations: {len(large_plan['iterations'])}")
    
    assert large_plan['strategy'] == 'multi_iteration', "Should use multi_iteration for large corpus"
    assert large_plan['execution_model'] == 'pro', "Should use Pro for large corpus"
    assert len(large_plan['iterations']) >= 2, "Should have multiple iterations for large corpus"
    
    print("\n✅ Strategic planning test passed!")

if __name__ == "__main__":
    test_strategic_planning()
