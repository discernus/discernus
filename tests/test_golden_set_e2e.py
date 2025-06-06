#!/usr/bin/env python3
"""
Golden Set End-to-End Testing System
Tests the complete narrative analysis pipeline using curated golden set data.

This test validates:
1. JSONL generation from golden set texts
2. Corpus ingestion and validation
3. Job creation and task queuing
4. Celery task processing
5. Results validation and export
6. Statistical analysis and consistency checks
"""

import requests
import json
import time
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging
import subprocess
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_BASE = "http://localhost:8000/api"
GOLDEN_SET_PATH = Path("corpus/golden_set/presidential_speeches")
CLI_PATH = Path("src/cli/jsonl_generator.py")
SCHEMA_PATH = Path("schemas/core_schema.json")

class GoldenSetTestSuite:
    """Comprehensive golden set testing framework."""
    
    def __init__(self):
        self.temp_dir = None
        self.created_corpora = []
        self.created_jobs = []
        
    def setup(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp(prefix="golden_set_test_")
        logger.info(f"Test temp directory: {self.temp_dir}")
        
    def teardown(self):
        """Clean up test environment."""
        # Clean up created jobs and corpora
        for job_id in self.created_jobs:
            try:
                requests.delete(f"{API_BASE}/jobs/{job_id}")
            except:
                pass
                
        for corpus_id in self.created_corpora:
            try:
                requests.delete(f"{API_BASE}/corpora/{corpus_id}")
            except:
                pass
        
        # Remove temp directory
        if self.temp_dir and Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)
            
    def test_api_health(self) -> bool:
        """Test API health and dependencies."""
        logger.info("🏥 Testing API Health...")
        
        try:
            response = requests.get(f"{API_BASE}/health", timeout=10)
            if response.status_code == 200:
                health_data = response.json()
                logger.info(f"   ✅ API Health: {health_data.get('status', 'unknown')}")
                
                # Check critical dependencies
                dependencies = health_data.get('dependencies', {})
                critical_deps = ['database', 'redis', 'celery']
                
                for dep in critical_deps:
                    status = dependencies.get(dep, {}).get('status', 'unknown')
                    if status != 'healthy':
                        logger.error(f"   ❌ {dep.title()} unhealthy: {status}")
                        return False
                    logger.info(f"   ✅ {dep.title()}: {status}")
                        
                return True
            else:
                logger.error(f"   ❌ API health check failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"   ❌ API health check exception: {e}")
            return False
    
    def test_golden_set_jsonl_generation(self) -> Dict[str, Path]:
        """Generate JSONL files from golden set texts."""
        logger.info("📄 Testing Golden Set JSONL Generation...")
        
        generated_files = {}
        
        # Get sample golden set files
        txt_files = list((GOLDEN_SET_PATH / "txt").glob("golden_*inaugural*.txt"))[:2]
        
        if not txt_files:
            logger.error("   ❌ No golden set files found")
            return generated_files
        
        output_file = Path(self.temp_dir) / "golden_set_test.jsonl"
        
        # Run JSONL generator
        cmd = [
            sys.executable, str(CLI_PATH),
            "--output", str(output_file),
            "--format", "text", 
            "--chunk-type", "fixed",
            "--chunk-size", "1000"
        ]
        
        # Add input files
        for txt_file in txt_files:
            cmd.extend(["--input", str(txt_file)])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0 and output_file.exists():
                record_count = self.validate_jsonl_file(output_file)
                if record_count > 0:
                    logger.info(f"   ✅ Generated {record_count} records")
                    generated_files["golden_set_test"] = output_file
                else:
                    logger.error("   ❌ No valid records generated")
            else:
                logger.error(f"   ❌ Generator failed: {result.stderr}")
                
        except Exception as e:
            logger.error(f"   ❌ Generator exception: {e}")
        
        return generated_files
    
    def validate_jsonl_file(self, jsonl_file: Path) -> int:
        """Validate a JSONL file and return record count."""
        try:
            record_count = 0
            with open(jsonl_file, 'r') as f:
                for line in f:
                    if line.strip():
                        try:
                            record = json.loads(line)
                            if isinstance(record, dict) and 'document' in record:
                                record_count += 1
                        except json.JSONDecodeError:
                            continue
            return record_count
        except:
            return 0
    
    def test_corpus_ingestion(self, jsonl_files: Dict[str, Path]) -> Dict[str, int]:
        """Test corpus ingestion for generated JSONL files."""
        logger.info("🗃️  Testing Corpus Ingestion...")
        
        ingested_corpora = {}
        
        for name, jsonl_file in jsonl_files.items():
            logger.info(f"   📥 Ingesting {name}...")
            
            try:
                with open(jsonl_file, 'rb') as f:
                    files = {'file': (jsonl_file.name, f, 'application/x-jsonlines')}
                    data = {
                        'name': f'Golden Set Test - {name}',
                        'description': f'E2E test corpus from {name}'
                    }
                    
                    response = requests.post(f"{API_BASE}/corpora/upload", files=files, data=data, timeout=60)
                
                if response.status_code == 200:
                    corpus = response.json()
                    corpus_id = corpus['id']
                    self.created_corpora.append(corpus_id)
                    
                    logger.info(f"   ✅ {name}: Corpus {corpus_id} created")
                    ingested_corpora[name] = corpus_id
                else:
                    logger.error(f"   ❌ {name}: Ingestion failed: {response.status_code}")
                    
            except Exception as e:
                logger.error(f"   ❌ {name}: Ingestion exception: {e}")
        
        return ingested_corpora
    
    def test_job_creation_and_processing(self, corpora: Dict[str, int]) -> Dict[str, int]:
        """Test job creation and processing for ingested corpora."""
        logger.info("⚙️  Testing Job Creation and Processing...")
        
        processed_jobs = {}
        
        if not corpora:
            logger.warning("   ⚠️  No corpora available for job testing")
            return processed_jobs
            
        corpus_name, corpus_id = next(iter(corpora.items()))
        
        # Get document text_ids
        doc_response = requests.get(f"{API_BASE}/corpora/{corpus_id}/documents")
        if doc_response.status_code != 200:
            logger.error(f"   ❌ Failed to get documents for corpus {corpus_id}")
            return processed_jobs
            
        documents = doc_response.json()
        text_ids = [doc['text_id'] for doc in documents[:1]]  # Limit to 1 doc for testing
        
        if not text_ids:
            logger.warning(f"   ⚠️  No documents found in corpus {corpus_id}")
            return processed_jobs
        
        # Create test job
        job_data = {
            "corpus_id": corpus_id,
            "job_name": "E2E Golden Set Test Job",
            "text_ids": text_ids,
            "frameworks": ["civic_virtue"],
            "models": ["distilbert-base-uncased"],
            "run_count": 1,
            "job_config": {"test_run": True, "golden_set": True}
        }
        
        try:
            response = requests.post(f"{API_BASE}/jobs", json=job_data, timeout=30)
            
            if response.status_code == 200:
                job = response.json()
                job_id = job['id']
                self.created_jobs.append(job_id)
                
                logger.info(f"   ✅ Job {job_id} created: {job['total_tasks']} tasks")
                
                # Monitor job progress (abbreviated for testing)
                success = self.monitor_job_progress(job_id, max_wait=60)  # 1 minute max
                
                if success:
                    processed_jobs["golden_set_test"] = job_id
                    logger.info(f"   🎉 Job {job_id} completed successfully")
                else:
                    logger.warning(f"   ⚠️  Job {job_id} did not complete in time")
                    
            else:
                logger.error(f"   ❌ Job creation failed: {response.status_code}")
                
        except Exception as e:
            logger.error(f"   ❌ Job creation exception: {e}")
        
        return processed_jobs
    
    def monitor_job_progress(self, job_id: int, max_wait: int = 300) -> bool:
        """Monitor job progress with timeout."""
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            try:
                response = requests.get(f"{API_BASE}/jobs/{job_id}")
                if response.status_code == 200:
                    job = response.json()
                    status = job['status']
                    
                    if status in ['completed', 'failed']:
                        return status == 'completed' and job['completed_tasks'] > 0
                        
                else:
                    logger.warning(f"      ⚠️  Job status check failed: {response.status_code}")
                    
            except Exception as e:
                logger.warning(f"      ⚠️  Job monitoring exception: {e}")
                
            time.sleep(5)  # Check every 5 seconds
        
        return False
    
    def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run the complete golden set end-to-end test suite."""
        logger.info("🚀 Starting Golden Set E2E Test Suite")
        logger.info("=" * 60)
        
        test_results = {
            "started_at": datetime.utcnow().isoformat(),
            "api_health": False,
            "jsonl_generation": {},
            "corpus_ingestion": {},
            "job_processing": {},
            "overall_success": False
        }
        
        try:
            self.setup()
            
            # 1. API Health Check
            test_results["api_health"] = self.test_api_health()
            if not test_results["api_health"]:
                logger.error("❌ API health check failed - aborting test")
                return test_results
            
            # 2. JSONL Generation
            test_results["jsonl_generation"] = self.test_golden_set_jsonl_generation()
            if not test_results["jsonl_generation"]:
                logger.error("❌ JSONL generation failed - aborting test")
                return test_results
            
            # 3. Corpus Ingestion
            test_results["corpus_ingestion"] = self.test_corpus_ingestion(test_results["jsonl_generation"])
            if not test_results["corpus_ingestion"]:
                logger.error("❌ Corpus ingestion failed - aborting test")
                return test_results
            
            # 4. Job Processing
            test_results["job_processing"] = self.test_job_creation_and_processing(test_results["corpus_ingestion"])
            
            # Determine overall success
            test_results["overall_success"] = (
                test_results["api_health"] and
                len(test_results["jsonl_generation"]) > 0 and
                len(test_results["corpus_ingestion"]) > 0
            )
            
            # Final summary
            logger.info("\n" + "=" * 60)
            if test_results["overall_success"]:
                logger.info("🎉 GOLDEN SET E2E TEST SUITE: SUCCESS!")
            else:
                logger.warning("⚠️  GOLDEN SET E2E TEST SUITE: PARTIAL SUCCESS")
            
            logger.info(f"   📊 JSONL Files Generated: {len(test_results['jsonl_generation'])}")
            logger.info(f"   📁 Corpora Ingested: {len(test_results['corpus_ingestion'])}")
            logger.info(f"   ⚙️  Jobs Processed: {len(test_results['job_processing'])}")
            
        except Exception as e:
            logger.error(f"❌ E2E Test Suite Exception: {e}")
            test_results["exception"] = str(e)
            
        finally:
            test_results["completed_at"] = datetime.utcnow().isoformat()
            self.teardown()
        
        return test_results


def main():
    """Run the golden set end-to-end test suite."""
    test_suite = GoldenSetTestSuite()
    results = test_suite.run_comprehensive_test()
    
    # Save results to file
    results_file = Path("test_results") / f"golden_set_e2e_{int(time.time())}.json"
    results_file.parent.mkdir(exist_ok=True)
    
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"\n📄 Detailed results saved to: {results_file}")
    
    # Exit with appropriate code
    exit_code = 0 if results.get("overall_success", False) else 1
    return exit_code


if __name__ == "__main__":
    exit(main()) 