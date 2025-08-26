#!/usr/bin/env python3
"""
Direct test of EvidenceMatchingWrapper with evidence files.

This script bypasses the artifact storage complexity and directly reads
evidence files to test our wrapper's core functionality.
"""

import sys
import json
from pathlib import Path

# Add the main discernus package to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from discernus.core.evidence_matching_wrapper import EvidenceMatchingWrapper

def test_evidence_wrapper_direct():
    """Test the EvidenceMatchingWrapper by directly reading evidence files."""
    
    # Set up paths
    experiment_path = Path(__file__).parent
    artifacts_path = experiment_path / "shared_cache" / "artifacts"
    
    print("🧪 Testing EvidenceMatchingWrapper Direct Integration")
    print("=" * 55)
    print(f"Experiment path: {experiment_path}")
    print(f"Artifacts path: {artifacts_path}")
    print()
    
    # Load artifact registry to find evidence files
    registry_path = artifacts_path / "artifact_registry.json"
    if not registry_path.exists():
        print("❌ Artifact registry not found. Cannot test wrapper.")
        return
    
    with open(registry_path, 'r') as f:
        artifact_registry = json.load(f)
    
    # Find evidence artifacts
    evidence_files = []
    for artifact_hash, artifact_info in artifact_registry.items():
        if artifact_info.get('metadata', {}).get('artifact_type') == 'evidence_v6':
            evidence_file = artifacts_path / artifact_info['artifact_path']
            if evidence_file.exists():
                evidence_files.append((artifact_hash, evidence_file))
    
    print(f"📊 Found {len(evidence_files)} evidence files:")
    for artifact_hash, evidence_file in evidence_files[:5]:
        print(f"  - {artifact_hash[:8]}... -> {evidence_file.name}")
    if len(evidence_files) > 5:
        print(f"  ... and {len(evidence_files) - 5} more")
    print()
    
    if not evidence_files:
        print("❌ No evidence files found. Cannot test wrapper.")
        return
    
    # Create a mock artifact storage interface
    class MockArtifactStorage:
        def __init__(self, evidence_files):
            self.evidence_files = evidence_files
        
        def get_artifact(self, artifact_hash: str, quiet: bool = False):
            """Mock get_artifact that reads from files."""
            for hash_val, file_path in self.evidence_files:
                if hash_val == artifact_hash:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            return f.read().encode('utf-8')
                    except Exception as e:
                        if not quiet:
                            print(f"Failed to read {file_path}: {e}")
                        return None
            return None
    
    # Initialize mock storage and wrapper
    mock_storage = MockArtifactStorage(evidence_files)
    
    print("🧠 Initializing EvidenceMatchingWrapper with mock storage...")
    evidence_wrapper = EvidenceMatchingWrapper(
        model="vertex_ai/gemini-2.5-pro",
        artifact_storage=mock_storage,
        audit_logger=None
    )
    
    # Build the intelligent index using the artifact hashes
    artifact_hashes = [hash_val for hash_val, _ in evidence_files]
    print("🔨 Building intelligent evidence index...")
    success = evidence_wrapper.build_index(artifact_hashes)
    
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
    
    print("\n🎉 EvidenceMatchingWrapper direct integration test completed successfully!")
    print("\nThis wrapper can now be used as a drop-in replacement for txtai indexes")
    print("in synthesis agents, providing intelligent evidence matching capabilities!")

if __name__ == "__main__":
    test_evidence_wrapper_direct()
