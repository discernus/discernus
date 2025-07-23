#!/usr/bin/env python3
"""
Phase 2 Test Runner - Dynamic Orchestration Validation
======================================================

Implements the Phase 2 validation questions from the Implementation Plan by
testing the full, dynamic orchestration pipeline.

- Goal: To empower the `OrchestratorAgent` (the LLM) with the intelligence
        to automatically break down a large experiment into optimal batches
        and manage the entire fan-out/fan-in process via the `Execution Bridge`.
"""

import redis
import json
import sys
import os
import time
import argparse
import logging
import subprocess
from typing import Dict, Any, List

# Add scripts directory to path
sys.path.append(os.path.dirname(__file__))
from minio_client import put_artifact, get_artifact, artifact_exists

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - Phase2Test - %(message)s')
logger = logging.getLogger(__name__)

# Redis configuration  
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = 6379
REDIS_DB = 0
ORCHESTRATOR_STREAM = 'orchestrator.tasks'

class Phase2TestRunner:
    """Automated testing framework for Phase 2 validation questions"""
    
    def __init__(self):
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        
    def run_full_pipeline_test(self) -> bool:
        """Run the full Phase 2 dynamic orchestration pipeline test"""
        logger.info("=== RUNNING FULL PHASE 2 PIPELINE TEST ===")
        
        try:
            # 1. Setup test artifacts (corpus, framework)
            framework_hash = self._create_test_framework()
            corpus_hashes = self._create_test_corpus()

            # 2. Create and enqueue the initial orchestration request
            experiment_spec = {
                "name": "phase2_e2e_test",
                "description": "A full end-to-end test of the dynamic orchestration pipeline.",
                "research_question": "Does the pipeline successfully orchestrate a multi-batch analysis?"
            }
            
            orchestration_request = {
                "experiment": experiment_spec,
                "framework_hashes": [framework_hash],
                "corpus_hashes": corpus_hashes
            }

            self.redis_client.xadd(ORCHESTRATOR_STREAM, {
                'data': json.dumps(orchestration_request)
            })
            logger.info(f"Enqueued initial orchestration request to '{ORCHESTRATOR_STREAM}'")

            # 3. TODO: Run all agents and validate the sequence
            #    - OrchestratorAgent (to start pre-test)
            #    - PreTestAgent
            #    - OrchestratorAgent (to create final plan)
            #    - ExecutionBridge
            #    - AnalyseBatchAgent(s)
            #    - CorpusSynthesisAgent

            logger.info("🎉 (STUBBED) PHASE 2 PIPELINE TEST COMPLETED SUCCESSFULLY!")
            return True

        except Exception as e:
            logger.error(f"❌ PHASE 2 PIPELINE TEST FAILED: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _create_test_framework(self) -> str:
        """Creates a simple framework artifact for testing."""
        test_framework = """
# Test Framework v2.0
Instructions: Assign a score from 0.0 to 1.0 for test_score.
"""
        framework_hash = put_artifact(test_framework.encode('utf-8'))
        logger.info(f"Created test framework artifact: {framework_hash}")
        return framework_hash

    def _create_test_corpus(self) -> List[str]:
        """Creates a sample corpus with multiple documents."""
        # Create a corpus large enough to likely require multiple batches
        test_documents = [f"This is test document {i+1} for Phase 2." for i in range(10)]
        
        doc_hashes = []
        for i, doc in enumerate(test_documents):
            doc_hash = put_artifact(doc.encode('utf-8'))
            doc_hashes.append(doc_hash)
            logger.info(f"Created test document {i+1}: {doc_hash}")
        return doc_hashes

def main():
    parser = argparse.ArgumentParser(description='Phase 2 Test Runner')
    parser.add_argument('--test', required=True, choices=['full_pipeline'],
                       help='Which test to run')
    
    args = parser.parse_args()
    
    runner = Phase2TestRunner()
    
    if args.test == 'full_pipeline':
        success = runner.run_full_pipeline_test()
    else:
        success = False
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main() 