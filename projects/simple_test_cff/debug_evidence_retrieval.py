#!/usr/bin/env python3
"""
Debug script to test evidence retrieval from our EvidenceMatchingWrapper
"""

import sys
import os
import json
sys.path.insert(0, '/Volumes/code/discernus')

from discernus.core.evidence_matching_wrapper import EvidenceMatchingWrapper
from discernus.gateway.llm_gateway import LLMGateway
from discernus.core.audit_logger import AuditLogger

class MockLLMGateway:
    """Mock LLM gateway for testing"""
    def execute_call(self, model, prompt, **kwargs):
        return "mock response", {}

def test_evidence_retrieval():
    """Test evidence retrieval directly"""
    
    print("🔍 Testing EvidenceMatchingWrapper...")
    
    # Check what evidence artifacts are available
    experiment_path = "/Volumes/code/discernus/projects/simple_test_cff"
    artifacts_dir = f"{experiment_path}/shared_cache/artifacts"
    
    print("\n📁 Available evidence artifacts:")
    evidence_hashes = []
    for filename in os.listdir(artifacts_dir):
        if filename.startswith("evidence_v6_"):
            evidence_hashes.append(filename)
            print(f"  - {filename}")
    
    if not evidence_hashes:
        print("❌ No evidence artifacts found!")
        return
    
    # Read one evidence artifact directly
    evidence_file = f"{artifacts_dir}/{evidence_hashes[0]}"
    print(f"\n📖 Reading evidence file: {evidence_file}")
    
    try:
        with open(evidence_file, 'r') as f:
            evidence_data = json.load(f)
        
        print(f"✅ Evidence file loaded successfully!")
        print(f"   - Total evidence pieces: {evidence_data.get('evidence_metadata', {}).get('total_evidence_pieces', 0)}")
        print(f"   - First evidence piece: {evidence_data.get('evidence_data', [{}])[0].get('quote_text', 'No quote')[:100]}...")
        
        # Test wrapper with mock components
        print(f"\n🔧 Testing wrapper with mock components...")
        
        mock_llm = MockLLMGateway()
        audit_logger = None  # Skip for now
        
        wrapper = EvidenceMatchingWrapper(
            model="vertex_ai/gemini-2.5-flash",
            artifact_storage=None,  # Skip for testing
            audit_logger=audit_logger
        )
        
        # Test building index with the evidence data
        print("Building index...")
        wrapper.evidence_data = evidence_data.get('evidence_data', [])
        wrapper.evidence_metadata = evidence_data.get('evidence_metadata', {})
        
        # Test search
        print("\n🔍 Testing search...")
        results = wrapper.search_evidence("tribal dominance", limit=3)
        print(f"Search returned {len(results)} results")
        
        for i, result in enumerate(results):
            print(f"\nResult {i+1}:")
            print(f"  Quote: {result.get('quote_text', 'No quote')[:100]}...")
            print(f"  Document: {result.get('document_name', 'Unknown')}")
            print(f"  Dimension: {result.get('dimension', 'Unknown')}")
            print(f"  Score: {result.get('relevance_score', 0.0)}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_evidence_retrieval()
