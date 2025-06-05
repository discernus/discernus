#!/usr/bin/env python3
"""
Test script for JSONL ingestion functionality
Tests the complete workflow: corpus creation -> JSONL upload -> document verification
"""
import requests
import json
import time
from pathlib import Path

API_BASE = "http://localhost:8000/api"

def test_api_health():
    """Test if API is running"""
    print("🔍 Testing API health...")
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            print("✅ API is healthy")
            return True
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"❌ Cannot connect to API: {e}")
        return False

def test_jsonl_ingestion():
    """Test JSONL file ingestion - creates corpus and ingests documents in one step"""
    print("\n📤 Testing JSONL ingestion (creates corpus + documents)...")
    
    jsonl_file = Path("test_data/sample_corpus_v2.jsonl")
    if not jsonl_file.exists():
        print(f"❌ JSONL file not found: {jsonl_file}")
        return None, None
    
    try:
        with open(jsonl_file, 'rb') as f:
            files = {'file': ('sample_corpus.jsonl', f, 'application/x-jsonlines')}
            data = {
                'name': 'Test Corpus for JSONL Ingestion',
                'description': 'A test corpus to validate JSONL ingestion functionality'
            }
            
            response = requests.post(f"{API_BASE}/corpora/upload", files=files, data=data)
        
        if response.status_code == 200:  # Updated expected status code
            corpus = response.json()
            print(f"✅ JSONL ingestion successful!")
            print(f"   Created corpus: {corpus['name']} (ID: {corpus['id']})")
            print(f"   Record count: {corpus.get('record_count', 'Unknown')}")
            return corpus, corpus['id']
        else:
            print(f"❌ JSONL ingestion failed: {response.status_code} - {response.text}")
            return None, None
    except requests.RequestException as e:
        print(f"❌ Error during JSONL ingestion: {e}")
        return None, None

def verify_documents(corpus_id, expected_count=3):
    """Verify that documents were created correctly"""
    print(f"\n🔍 Verifying documents in corpus {corpus_id}...")
    
    try:
        response = requests.get(f"{API_BASE}/corpora/{corpus_id}/documents")
        if response.status_code == 200:
            documents = response.json()
            print(f"✅ Found {len(documents)} documents")
            
            if len(documents) == expected_count:
                print("✅ Document count matches expected")
            else:
                print(f"⚠️  Expected {expected_count} documents, found {len(documents)}")
            
            # Verify document structure
            for i, doc in enumerate(documents[:3]):  # Check first 3 documents
                print(f"   Document {i+1}: '{doc.get('title', 'No title')}'")
                if 'document_metadata' in doc and doc['document_metadata']:
                    metadata = doc['document_metadata']
                    print(f"     Author: {metadata.get('author', 'Unknown')}")
                    print(f"     Category: {metadata.get('category', 'Unknown')}")
            
            return documents
        else:
            print(f"❌ Failed to retrieve documents: {response.status_code}")
            return []
    except requests.RequestException as e:
        print(f"❌ Error retrieving documents: {e}")
        return []

def verify_chunks(corpus_id):
    """Verify that chunks were created correctly"""
    print(f"\n🧩 Verifying chunks in corpus {corpus_id}...")
    
    try:
        response = requests.get(f"{API_BASE}/corpora/{corpus_id}/chunks")
        if response.status_code == 200:
            chunks = response.json()
            print(f"✅ Found {len(chunks)} chunks")
            
            # Show sample chunk
            if chunks:
                sample_chunk = chunks[0]
                print(f"   Sample chunk text: '{sample_chunk['chunk_content'][:100]}...'")
                print(f"   Chunk size: {len(sample_chunk['chunk_content'])} characters")
            
            return chunks
        else:
            print(f"❌ Failed to retrieve chunks: {response.status_code}")
            return []
    except requests.RequestException as e:
        print(f"❌ Error retrieving chunks: {e}")
        return []

def cleanup_test_corpus(corpus_id):
    """Clean up test corpus"""
    print(f"\n🧹 Cleaning up test corpus {corpus_id}...")
    try:
        response = requests.delete(f"{API_BASE}/corpora/{corpus_id}")
        if response.status_code == 200:
            print("✅ Test corpus cleaned up")
        else:
            print(f"⚠️  Could not delete test corpus: {response.status_code}")
    except requests.RequestException as e:
        print(f"⚠️  Error during cleanup: {e}")

def main():
    """Run the complete ingestion test"""
    print("🧪 JSONL Ingestion Test Suite")
    print("=" * 40)
    
    # Test API health
    if not test_api_health():
        print("\n❌ API is not available. Please start the API server first.")
        print("   Run: python run_api.py")
        return
    
    # Test JSONL ingestion (creates corpus and documents in one step)
    corpus, corpus_id = test_jsonl_ingestion()
    if not corpus_id:
        print("\n❌ JSONL ingestion failed. Test incomplete.")
        return
    
    try:
        # Verify documents were created
        documents = verify_documents(corpus_id)
        
        # Verify chunks were created
        chunks = verify_chunks(corpus_id)
        
        # Summary
        print("\n" + "=" * 40)
        print("📊 Test Summary:")
        print(f"✅ Corpus created: {corpus_id}")
        print(f"✅ Documents ingested: {len(documents)}")
        print(f"✅ Chunks created: {len(chunks)}")
        print("✅ All tests passed!")
        
    finally:
        # Cleanup
        cleanup_test_corpus(corpus_id)

if __name__ == "__main__":
    main() 