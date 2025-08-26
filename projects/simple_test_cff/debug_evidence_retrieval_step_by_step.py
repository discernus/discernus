#!/usr/bin/env python3
"""
Step-by-step debug script to test evidence retrieval
"""

import sys
import os
import json
sys.path.insert(0, '/Volumes/code/discernus')

from discernus.core.evidence_matching_wrapper import EvidenceMatchingWrapper
from discernus.gateway.llm_gateway import LLMGateway

class MockLLMGateway:
    """Mock LLM gateway for testing"""
    def execute_call(self, model, prompt, **kwargs):
        return "mock response", {}

def test_step_by_step():
    """Test evidence retrieval step by step"""
    
    print("🔍 Step-by-Step Evidence Retrieval Debug")
    print("=" * 60)
    
    # Step 1: Create wrapper
    print("\n📋 Step 1: Creating EvidenceMatchingWrapper...")
    mock_llm = MockLLMGateway()
    wrapper = EvidenceMatchingWrapper(
        model="vertex_ai/gemini-2.5-flash",
        artifact_storage=None,
        audit_logger=None
    )
    print("✅ Wrapper created")
    
    # Step 2: Load evidence data directly
    print("\n📋 Step 2: Loading evidence data...")
    evidence_file = "shared_cache/artifacts/evidence_v6_124059af"
    with open(evidence_file, 'r') as f:
        evidence_data = json.load(f)
    
    evidence_pieces = evidence_data.get('evidence_data', [])
    print(f"✅ Loaded {len(evidence_pieces)} evidence pieces")
    
    # Step 3: Build index from data
    print("\n📋 Step 3: Building index from evidence data...")
    try:
        success = wrapper.build_index_from_data(evidence_pieces)
        if success:
            print("✅ Index built successfully!")
        else:
            print("❌ Index build failed!")
            return
    except Exception as e:
        print(f"❌ Index build failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 4: Test search_evidence method
    print("\n📋 Step 4: Testing search_evidence method...")
    query = "tribal dominance"
    print(f"Query: '{query}'")
    
    try:
        results = wrapper.search_evidence(query, limit=3)
        print(f"✅ search_evidence returned {len(results)} results")
        
        for i, result in enumerate(results):
            print(f"  Result {i+1}:")
            print(f"    Quote: {result.get('quote_text', 'No quote')[:100]}...")
            print(f"    Document: {result.get('document_name', 'Unknown')}")
            print(f"    Dimension: {result.get('dimension', 'Unknown')}")
            print(f"    Score: {result.get('relevance_score', 0.0)}")
    except Exception as e:
        print(f"❌ search_evidence failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Step 5: Test search method (compatibility)
    print("\n📋 Step 5: Testing search method (compatibility)...")
    try:
        search_results = wrapper.search(query, limit=3)
        print(f"✅ search returned {len(search_results)} results")
        print(f"  Type: {type(search_results)}")
        print(f"  Content: {search_results}")
    except Exception as e:
        print(f"❌ search failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Step 6: Test documents property
    print("\n📋 Step 6: Testing documents property...")
    try:
        documents = wrapper.documents
        print(f"✅ documents property returned {len(documents)} items")
        if documents:
            print(f"  First document keys: {list(documents[0].keys())}")
            print(f"  First document text: {documents[0].get('text', 'No text')[:100]}...")
    except Exception as e:
        print(f"❌ documents property failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_step_by_step()
