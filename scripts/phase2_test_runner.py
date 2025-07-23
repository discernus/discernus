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
        
        # Start a set to track all tasks we expect to see completed
        all_tasks = set()

        try:
            # 1. Start OrchestratorAgent in the background
            logger.info("Starting OrchestratorAgent in the background...")
            orchestrator_process = subprocess.Popen(
                ['python3', 'agents/OrchestratorAgent/main.py'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            time.sleep(5) # Give it a moment to initialize

            # 2. Setup test artifacts and enqueue the initial request
            framework_hash = self._create_test_framework()
            corpus_hashes = self._create_test_corpus()
            self._enqueue_orchestration_request(framework_hash, corpus_hashes)

            # 3. Wait for and execute the PreTest task
            logger.info("--- Validating Step 1: PreTest Orchestration ---")
            pre_test_task_id = self._wait_for_task_type('pre_test', timeout=60)
            all_tasks.add(pre_test_task_id)
            self._run_agent_script('PreTestAgent', 'agents/PreTestAgent/main.py', pre_test_task_id)

            # 4. Wait for and execute the Plan Execution task
            logger.info("--- Validating Step 2: Final Plan Generation ---")
            plan_execution_task_id = self._wait_for_task_type('execute_plan', timeout=60)
            all_tasks.add(plan_execution_task_id)
            plan_hash = self._get_plan_hash_from_task(plan_execution_task_id)
            self._run_agent_script('ExecutionBridge', 'scripts/execution_bridge.py', plan_hash)
            
            # 5. Discover and execute all analysis and synthesis tasks
            logger.info("--- Validating Step 3: Batched Analysis & Synthesis ---")
            time.sleep(5) # Allow bridge to enqueue tasks
            
            analysis_tasks = self._discover_tasks_by_type('analyse_batch')
            synthesis_tasks = self._discover_tasks_by_type('corpus_synthesis')
            
            if not analysis_tasks:
                raise Exception("Validation failed: No 'analyse_batch' tasks were created by the ExecutionBridge.")
            if len(synthesis_tasks) != 1:
                raise Exception(f"Validation failed: Expected 1 'corpus_synthesis' task, but found {len(synthesis_tasks)}.")

            all_tasks.update(analysis_tasks)
            all_tasks.update(synthesis_tasks)
            
            # Execute analysis tasks in parallel
            for task_id in analysis_tasks:
                self._run_agent_script('AnalyseBatchAgent', 'agents/AnalyseBatchAgent/main.py', task_id)
            
            # Execute synthesis task
            self._run_agent_script('CorpusSynthesisAgent', 'agents/CorpusSynthesisAgent/main.py', synthesis_tasks[0])
            
            # 6. Final validation
            logger.info("--- Final Validation ---")
            self._wait_for_all_tasks_to_complete(all_tasks, timeout=300)

            logger.info("🎉 FULL PHASE 2 PIPELINE TEST COMPLETED SUCCESSFULLY!")
            return True

        except Exception as e:
            logger.error(f"❌ PHASE 2 PIPELINE TEST FAILED: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            # Cleanup
            if 'orchestrator_process' in locals() and orchestrator_process.poll() is None:
                orchestrator_process.terminate()
                orchestrator_process.wait()
                logger.info("OrchestratorAgent terminated.")

    def _enqueue_orchestration_request(self, framework_hash: str, corpus_hashes: List[str]):
        """Creates and enqueues the initial orchestration request."""
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

    def _wait_for_task_type(self, task_type: str, timeout: int = 60) -> str:
        """Polls the 'tasks' stream for a task of a specific type."""
        logger.info(f"Waiting for task of type '{task_type}'...")
        start_time = time.time()
        while time.time() - start_time < timeout:
            messages = self.redis_client.xread({'tasks': '0'})
            for stream, msgs in messages:
                for msg_id, fields in msgs:
                    if fields.get(b'type', b'').decode() == task_type:
                        task_id = msg_id.decode()
                        logger.info(f"Found '{task_type}' task: {task_id}")
                        return task_id
            time.sleep(2)
        raise TimeoutError(f"Timed out waiting for '{task_type}' task.")

    def _get_plan_hash_from_task(self, task_id: str) -> str:
        """Retrieves the plan_hash from an execute_plan task."""
        messages = self.redis_client.xrange('tasks', task_id, task_id)
        if not messages:
            raise ValueError(f"Task {task_id} not found.")
        task_data = json.loads(messages[0][1][b'data'])
        return task_data['plan_hash']

    def _discover_tasks_by_type(self, task_type: str) -> List[str]:
        """Finds all tasks of a specific type in the stream."""
        task_ids = []
        messages = self.redis_client.xread({'tasks': '0'})
        for stream, msgs in messages:
            for msg_id, fields in msgs:
                if fields.get(b'type', b'').decode() == task_type:
                    task_ids.append(msg_id.decode())
        logger.info(f"Discovered {len(task_ids)} tasks of type '{task_type}'.")
        return task_ids

    def _run_agent_script(self, agent_name: str, script_path: str, script_arg: str):
        """Runs an agent script as a subprocess and waits for it to complete."""
        logger.info(f"Running {agent_name} for task/arg: {script_arg}...")
        try:
            process = subprocess.run(
                ['python3', script_path, script_arg],
                capture_output=True, text=True, check=True, timeout=180
            )
            logger.info(f"{agent_name} completed successfully.")
            if process.stdout:
                logger.debug(f"{agent_name} stdout:\n{process.stdout}")
            if process.stderr:
                logger.warning(f"{agent_name} stderr:\n{process.stderr}")
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ {agent_name} failed!")
            logger.error(f"   stdout: {e.stdout}")
            logger.error(f"   stderr: {e.stderr}")
            raise

    def _wait_for_all_tasks_to_complete(self, task_ids: set, timeout: int = 300):
        """Checks the tasks.done stream until all expected tasks are complete."""
        logger.info(f"Waiting for {len(task_ids)} tasks to complete...")
        completed_tasks = set()
        start_time = time.time()
        while time.time() - start_time < timeout:
            done_messages = self.redis_client.xread({'tasks.done': '0'})
            for _, msgs in done_messages:
                for _, fields in msgs:
                    data = json.loads(fields[b'data'])
                    completed_tasks.add(data['original_task_id'])
            
            if task_ids.issubset(completed_tasks):
                logger.info("✅ All expected tasks have completed.")
                return
            
            time.sleep(5)
        
        missing_tasks = task_ids - completed_tasks
        raise TimeoutError(f"Timed out waiting for all tasks to complete. Missing: {missing_tasks}")

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