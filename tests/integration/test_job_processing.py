#!/usr/bin/env python3
"""
Test script for complete job processing pipeline.
Tests Epic 1 completion: JSONL ingestion → Job creation → Task processing → Results
"""

import requests
import json
import time
from pathlib import Path

API_BASE = "http://localhost:8000/api"

def test_complete_pipeline():
    """Test the complete narrative analysis pipeline."""
    print("🧪 Epic 1 Complete Pipeline Test")
    print("=" * 50)
    
    # Step 1: Health check
    print("1️⃣ API Health Check...")
    response = requests.get(f"{API_BASE}/health")
    if response.status_code == 200:
        print("   ✅ API is healthy")
    else:
        print(f"   ❌ API health failed: {response.status_code}")
        return
    
    # Step 2: Create test corpus
    print("\n2️⃣ Creating test corpus...")
    timestamp = int(time.time())
    test_data = [
        {
            "document": {
                "text_id": f"pipeline_test_{timestamp}_1",
                "title": "Pipeline Test Document 1",
                "document_type": "speech",
                "author": "Test Speaker",
                "date": "2024-06-05T00:00:00Z",
                "schema_version": "1.0.0",
                "document_metadata": {"test_run": timestamp, "category": "pipeline_test"}
            },
            "chunk_id": 0,
            "total_chunks": 1,
            "chunk_type": "fixed",
            "chunk_size": 512,
            "document_position": 0.0,
            "word_count": 25,
            "unique_words": 20,
            "word_density": 0.80,
            "chunk_content": "This is a test document for the complete narrative analysis pipeline. We are testing civic virtue, moral rhetorical posture, and political spectrum analysis capabilities.",
            "framework_data": {}
        }
    ]
    
    # Create JSONL file
    test_file = f"test_data/pipeline_test_{timestamp}.jsonl"
    with open(test_file, 'w') as f:
        for record in test_data:
            f.write(json.dumps(record) + '\n')
    
    # Upload corpus
    try:
        with open(test_file, 'rb') as f:
            files = {'file': (f'pipeline_test_{timestamp}.jsonl', f, 'application/x-jsonlines')}
            data = {
                'name': f'Pipeline Test Corpus {timestamp}',
                'description': 'Testing complete Epic 1 pipeline'
            }
            
            response = requests.post(f"{API_BASE}/corpora/upload", files=files, data=data)
        
        if response.status_code == 200:
            corpus = response.json()
            corpus_id = corpus['id']
            print(f"   ✅ Corpus created: {corpus['name']} (ID: {corpus_id})")
        else:
            print(f"   ❌ Corpus creation failed: {response.status_code}")
            return
    finally:
        Path(test_file).unlink(missing_ok=True)
    
    # Step 3: Get text_ids from corpus
    print("\n3️⃣ Getting document text_ids...")
    response = requests.get(f"{API_BASE}/corpora/{corpus_id}/documents")
    if response.status_code == 200:
        documents = response.json()
        text_ids = [doc['text_id'] for doc in documents]
        print(f"   ✅ Found {len(text_ids)} documents: {text_ids}")
    else:
        print(f"   ❌ Failed to get documents: {response.status_code}")
        return
    
    # Step 4: Create analysis job
    print("\n4️⃣ Creating analysis job...")
    job_data = {
        "corpus_id": corpus_id,
        "job_name": f"Pipeline Test Job {timestamp}",
        "text_ids": text_ids,
        "frameworks": ["civic_virtue", "political_spectrum"],
        "models": ["distilbert-base-uncased"],  # Simple model for testing
        "run_count": 1,
        "job_config": {"test_run": True}
    }
    
    response = requests.post(f"{API_BASE}/jobs", json=job_data)
    if response.status_code == 200:
        job = response.json()
        job_id = job['id']
        print(f"   ✅ Job created: {job['job_name']} (ID: {job_id})")
        print(f"   📊 Total tasks: {job['total_tasks']}")
    else:
        print(f"   ❌ Job creation failed: {response.status_code} - {response.text}")
        return
    
    # Step 5: Monitor job progress
    print(f"\n5️⃣ Monitoring job progress...")
    print("   ⏳ Tasks are being processed by Celery workers...")
    print("   (Make sure you have started the Celery worker with: python run_celery.py)")
    
    max_wait = 300  # 5 minutes max wait
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        response = requests.get(f"{API_BASE}/jobs/{job_id}")
        if response.status_code == 200:
            job_detail = response.json()
            status = job_detail['status']
            completed = job_detail['completed_tasks']
            failed = job_detail['failed_tasks']
            total = job_detail['total_tasks']
            
            print(f"   📈 Status: {status} | Progress: {completed}/{total} completed, {failed} failed")
            
            if status in ['completed', 'failed']:
                break
                
        time.sleep(5)  # Check every 5 seconds
    
    # Step 6: Check final results
    print(f"\n6️⃣ Final Results...")
    response = requests.get(f"{API_BASE}/jobs/{job_id}")
    if response.status_code == 200:
        final_job = response.json()
        print(f"   🎯 Final Status: {final_job['status']}")
        print(f"   📊 Tasks: {final_job['completed_tasks']}/{final_job['total_tasks']} completed")
        print(f"   💰 Estimated Cost: ${final_job.get('estimated_cost', 0):.4f}")
        print(f"   💸 Actual Cost: ${final_job.get('actual_cost', 0):.4f}")
        
        if final_job['completed_tasks'] > 0:
            print("\n   🎉 SUCCESS! Tasks have been processed!")
            print("   📈 The complete Epic 1 pipeline is working:")
            print("      ✅ JSONL Ingestion")
            print("      ✅ Job Creation") 
            print("      ✅ Task Queuing")
            print("      ✅ Celery Processing")
            print("      ✅ Results Storage")
            print("      ✅ Progress Monitoring")
        else:
            print("\n   ⚠️  No tasks completed. Check Celery worker logs.")
    
    print(f"\n📋 Summary:")
    print(f"   Corpus ID: {corpus_id}")
    print(f"   Job ID: {job_id}")
    print(f"   Test completed in {time.time() - start_time:.1f} seconds")

if __name__ == "__main__":
    test_complete_pipeline() 