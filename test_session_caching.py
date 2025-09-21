#!/usr/bin/env python3
"""
Test script for session caching functionality
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

def test_session_caching():
    """Test session caching with ALL evidence loaded."""
    
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
    
    # Create RunContext
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
        }
    }
    
    print("=== Testing Session Caching Architecture ===")
    
    # Test 1: Create cached session with ALL evidence
    print("\n1. Creating cached session with ALL evidence:")
    cache_session = agent.create_cached_session(run_context)
    
    print(f"Session Evidence Count: {cache_session['total_evidence_count']}")
    print(f"Session Evidence Chars: {cache_session['total_evidence_chars']:,}")
    print(f"Session Created: {cache_session['session_created']}")
    
    # Verify all evidence is loaded
    evidence_artifacts = cache_session['evidence_artifacts']
    print(f"\nEvidence artifacts in session:")
    for i, artifact in enumerate(evidence_artifacts):
        doc_index = artifact['document_index']
        content_len = len(artifact['evidence_content'])
        print(f"  {i+1}. Document {doc_index}: {content_len} chars")
    
    # Test 2: Create cached curation prompt
    print("\n2. Testing cached curation prompt (with ALL evidence):")
    
    mock_iteration = {
        "iteration_name": "comprehensive_sentiment_analysis",
        "focus_area": "sentiment_correlation_patterns",
        "statistical_targets": ["negative_correlation", "binary_classification"],
        "curation_instructions": "Find quotes demonstrating clear sentiment patterns across ALL documents",
        "expected_quotes": 10,
        "priority": "high"
    }
    
    cached_prompt = agent._create_cached_curation_prompt(cache_session, mock_iteration)
    
    print(f"Cached prompt length: {len(cached_prompt):,} characters")
    print("Cached prompt preview:")
    print(cached_prompt[:800] + "...")
    
    # Verify ALL evidence is included (no 10-artifact limit)
    evidence_sections = cached_prompt.count("--- DOCUMENT")
    print(f"\nEvidence sections in prompt: {evidence_sections}")
    print(f"Expected (all evidence): {cache_session['total_evidence_count']}")
    
    assert evidence_sections == cache_session['total_evidence_count'], \
        f"Should include ALL evidence, not just {evidence_sections}"
    
    # Test 3: Compare with direct execution (limited evidence)
    print("\n3. Comparing cached vs direct execution approaches:")
    
    # Direct execution (old approach with limits)
    direct_evidence = agent._get_evidence_for_iteration(run_context, mock_iteration)
    direct_prompt = agent._create_curation_prompt(run_context, mock_iteration, direct_evidence)
    
    print(f"Direct prompt length: {len(direct_prompt):,} characters")
    print(f"Direct evidence count: {len(direct_evidence)}")
    
    print(f"\nCached approach:")
    print(f"  - Evidence: ALL {cache_session['total_evidence_count']} artifacts")
    print(f"  - Characters: {cache_session['total_evidence_chars']:,}")
    print(f"  - Model: Gemini 2.5 Pro with session caching")
    
    print(f"\nDirect approach:")
    print(f"  - Evidence: {len(direct_evidence)} artifacts (limited)")
    print(f"  - Characters: {sum(len(a['evidence_content']) for a in direct_evidence):,}")
    print(f"  - Model: Gemini 2.5 Flash with direct calls")
    
    # Test 4: Verify session context structure
    print("\n4. Verifying session context structure:")
    required_keys = ['evidence_artifacts', 'total_evidence_count', 'total_evidence_chars', 
                    'statistical_context', 'experiment_metadata', 'session_created']
    
    for key in required_keys:
        assert key in cache_session, f"Missing required key: {key}"
        print(f"  ✓ {key}: {type(cache_session[key]).__name__}")
    
    print("\n✅ Session caching architecture tests passed!")
    print("🎯 Ready for Pro model execution with ALL evidence context!")

if __name__ == "__main__":
    test_session_caching()
