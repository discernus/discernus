#!/usr/bin/env python3
"""
Test script for IntelligentEvidenceRetrievalAgent evidence inventory functionality
"""

import sys
import os
from pathlib import Path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from discernus.agents.intelligent_evidence_retriever import IntelligentEvidenceRetrievalAgent
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.audit_logger import AuditLogger
from discernus.core.run_context import RunContext

def test_evidence_inventory():
    """Test evidence inventory functionality with real nano experiment data."""
    
    # Use existing nano experiment with real artifacts
    nano_dir = Path("/Volumes/code/discernus/projects/nano_test_experiment")
    nano_run_dir = nano_dir / "runs" / "20250920_223951"
    
    security = ExperimentSecurityBoundary(nano_dir)
    storage = LocalArtifactStorage(security, nano_run_dir)
    audit = AuditLogger(security, nano_run_dir)
    
    # Create agent
    agent = IntelligentEvidenceRetrievalAgent(security, storage, audit)
    
    # Create a mock RunContext with real artifact hashes from nano experiment
    # Get artifact hashes from the artifact registry
    artifacts_dir = nano_run_dir / "artifacts"
    artifact_hashes = []
    
    registry_file = artifacts_dir / "artifact_registry.json"
    if registry_file.exists():
        import json
        with open(registry_file, 'r') as f:
            registry = json.load(f)
        artifact_hashes = list(registry.keys())
        print(f"Loaded {len(artifact_hashes)} artifact hashes from registry")
    
    print(f"Found {len(artifact_hashes)} artifacts in nano experiment")
    
    # Create mock RunContext
    run_context = RunContext(
        experiment_id="nano_test_experiment",
        framework_path=nano_dir / "sentiment_binary_v1.md", 
        corpus_path=nano_dir / "corpus.md"
    )
    run_context.analysis_artifacts = artifact_hashes
    
    # Test evidence inventory
    print("\n=== Testing Evidence Inventory ===")
    evidence_count, evidence_size_mb = agent.count_evidence_artifacts(run_context)
    
    print(f"Evidence Count: {evidence_count}")
    print(f"Evidence Size: {evidence_size_mb:.3f} MB")
    
    # Test evidence details
    print("\n=== Testing Evidence Details ===")
    evidence_details = agent.get_evidence_artifact_details(run_context)
    
    for detail in evidence_details:
        print(f"Artifact {detail['hash'][:8]}...")
        print(f"  Size: {detail['size_bytes']} bytes")
        print(f"  Document: {detail['document_index']}")
        print(f"  Quotes: {detail['quote_count']}")
        print(f"  Model: {detail['model_used']}")
    
    total_quotes = sum(d['quote_count'] for d in evidence_details)
    print(f"\nTotal quotes across all evidence: {total_quotes}")
    
    # Verify we found evidence artifacts
    assert evidence_count > 0, "Should find evidence artifacts in nano experiment"
    assert evidence_size_mb > 0, "Evidence should have non-zero size"
    assert len(evidence_details) == evidence_count, "Details count should match evidence count"
    assert total_quotes > 0, "Should find quotes in evidence artifacts"
    
    print("\n✅ Evidence inventory test passed!")

if __name__ == "__main__":
    test_evidence_inventory()
