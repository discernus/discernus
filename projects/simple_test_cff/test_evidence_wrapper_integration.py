#!/usr/bin/env python3
"""
Test script for EvidenceMatchingWrapper integration in simple_test_cff project.

This script demonstrates how our intelligent evidence wrapper can be used
to find evidence that supports statistical findings from real experiment data.
"""

import sys
import json
from pathlib import Path

# Add the main discernus package to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from discernus.core.evidence_matching_wrapper import EvidenceMatchingWrapper
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger

def test_evidence_wrapper_integration():
    """Test the EvidenceMatchingWrapper with real experiment data."""
    
    # Set up paths
    experiment_path = Path(__file__).parent
    shared_cache_path = experiment_path / "shared_cache"
    artifacts_path = shared_cache_path / "artifacts"
    
    print("🧪 Testing EvidenceMatchingWrapper Integration")
    print("=" * 50)
    print(f"Experiment path: {experiment_path}")
    print(f"Artifacts path: {artifacts_path}")
    print()
    
    # Initialize infrastructure
    security_boundary = ExperimentSecurityBoundary(experiment_path)
    artifact_storage = LocalArtifactStorage(
        security_boundary=security_boundary,
        run_folder=experiment_path / "runs" / "test_run"
    )
    audit_logger = AuditLogger(
        security_boundary=security_boundary,
        run_folder=experiment_path / "runs" / "test_run"
    )
    
    # Load artifact registry to get the correct hash values
    registry_path = artifacts_path / "artifact_registry.json"
    if not registry_path.exists():
        print("❌ Artifact registry not found. Cannot test wrapper.")
        return
    
    with open(registry_path, 'r') as f:
        artifact_registry = json.load(f)
    
    # Find evidence artifacts by looking for evidence_v6 type
    evidence_artifacts = []
    for artifact_hash, artifact_info in artifact_registry.items():
        if artifact_info.get('metadata', {}).get('artifact_type') == 'evidence_v6':
            evidence_artifacts.append(artifact_hash)
    
    print(f"📊 Found {len(evidence_artifacts)} evidence artifacts:")
    for artifact_hash in evidence_artifacts[:5]:  # Show first 5
        artifact_info = artifact_registry[artifact_hash]
        print(f"  - {artifact_hash[:8]}... -> {artifact_info['human_filename']}")
    if len(evidence_artifacts) > 5:
        print(f"  ... and {len(evidence_artifacts) - 5} more")
    print()
    
    if not evidence_artifacts:
        print("❌ No evidence artifacts found. Cannot test wrapper.")
        return
    
    # Initialize the EvidenceMatchingWrapper
    print("🧠 Initializing EvidenceMatchingWrapper...")
    evidence_wrapper = EvidenceMatchingWrapper(
        model="vertex_ai/gemini-2.5-pro",
        artifact_storage=artifact_storage,
        audit_logger=audit_logger
    )
    
    # Build the intelligent index
    print("🔨 Building intelligent evidence index...")
    success = evidence_wrapper.build_index(evidence_artifacts)
    
    if not success:
        print("❌ Failed to build evidence index")
        return
    
    # Get index status
    status = evidence_wrapper.get_index_status()
    print(f"✅ Index built successfully!")
    print(f"   - Evidence count: {status['evidence_count']}")
    print(f"   - Model: {status['model']}")
    print()
    
    # Test basic search functionality
    print("🔍 Testing basic evidence search...")
    test_queries = [
        "oligarchy",
        "democracy", 
        "political discourse",
        "civic engagement"
    ]
    
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        results = evidence_wrapper.search_evidence(query, limit=2)
        if results:
            for i, result in enumerate(results):
                print(f"  {i+1}. {result['quote_text'][:100]}...")
                print(f"     Source: {result['document_name']}")
                print(f"     Dimension: {result['dimension']}")
                print(f"     Confidence: {result['confidence']}")
        else:
            print("  No results found")
    
    # Test intelligent query generation
    print("\n🧠 Testing intelligent query generation...")
    statistical_findings = [
        "Strong correlation between oligarchy and political discourse patterns",
        "Evidence of democratic values in civic engagement responses"
    ]
    
    print("Statistical findings:")
    for finding in statistical_findings:
        print(f"  - {finding}")
    
    print("\nGenerating intelligent search queries...")
    queries = evidence_wrapper.generate_search_queries(statistical_findings, max_queries=3)
    
    print("Generated queries:")
    for i, query in enumerate(queries):
        print(f"  {i+1}. {query}")
    
    # Test auto-query evidence search
    print("\n🚀 Testing auto-query evidence search...")
    auto_results = evidence_wrapper.search_evidence_with_auto_queries(
        statistical_findings, 
        max_queries=3, 
        results_per_query=2
    )
    
    print(f"Auto-query search returned {len(auto_results)} evidence pieces:")
    for i, result in enumerate(auto_results[:3]):  # Show first 3
        print(f"  {i+1}. {result['quote_text'][:100]}...")
        print(f"     Source: {result['document_name']}")
        print(f"     Dimension: {result['dimension']}")
    
    # Test txtai compatibility
    print("\n🔌 Testing txtai compatibility...")
    txtai_results = evidence_wrapper.search("oligarchy", limit=3)
    print(f"txtai-compatible search returned {len(txtai_results)} results:")
    for doc_id, score in txtai_results:
        print(f"  Document {doc_id}: Score {score:.3f}")
    
    print("\n📚 Testing documents property...")
    documents = evidence_wrapper.documents
    print(f"Documents property contains {len(documents)} items")
    if documents:
        sample_doc = documents[0]
        print(f"Sample document structure: {list(sample_doc.keys())}")
        print(f"Sample text: {sample_doc['text'][:100]}...")
    
    print("\n🎉 EvidenceMatchingWrapper integration test completed successfully!")
    print("\nThis wrapper can now be used as a drop-in replacement for txtai indexes")
    print("in synthesis agents, providing intelligent evidence matching capabilities!")

if __name__ == "__main__":
    test_evidence_wrapper_integration()
