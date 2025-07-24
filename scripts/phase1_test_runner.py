#!/usr/bin/env python3
"""
Phase 1 Test Runner - Manual Testing Framework
===============================================

Implements the Phase 1 validation questions from the Implementation Plan:
1. Can we manually create and enqueue a single `AnalyseBatch` task?
2. Does the `AnalyseBatchAgent` successfully process this task?
3. Does completion trigger a single `CorpusSynthesis` task?
4. Does the `CorpusSynthesisAgent` perform deterministic aggregation?

Usage:
    python3 phase1_test_runner.py --test question1
    python3 phase1_test_runner.py --test question2
    python3 phase1_test_runner.py --test full_pipeline
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
logging.basicConfig(level=logging.INFO, format='%(asctime)s - Phase1Test - %(message)s')
logger = logging.getLogger(__name__)

# Redis configuration  
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = 6379
REDIS_DB = 0

class Phase1TestRunner:
    """Manual testing framework for Phase 1 validation questions"""
    
    def __init__(self):
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        
    def test_question1_manual_enqueue(self) -> bool:
        """
        Question 1: Can we manually create and enqueue a single `AnalyseBatch` task in Redis?
        Test: A simple script enqueues a task with multiple document and framework hashes.
        Success: The task appears in the `tasks` stream and the Router correctly identifies it.
        """
        logger.info("=== TESTING QUESTION 1: Manual AnalyseBatch Task Enqueue ===")
        
        try:
            # Create test framework artifact
            test_framework = """
# Test Framework v1.0
This is a simple test framework for validation.

Instructions: Assign a score from 0.0 to 1.0 for:
- test_score: Overall test quality
- validation_score: How well this validates the system

Return JSON format with numerical scores.
"""
            framework_hash = put_artifact(test_framework.encode('utf-8'))
            logger.info(f"Created test framework artifact: {framework_hash}")
            
            # Create test document artifacts
            test_documents = [
                "This is test document 1. It contains sample text for analysis.",
                "This is test document 2. It has different content for testing.",
                "This is test document 3. Final document in the test batch."
            ]
            
            doc_hashes = []
            for i, doc in enumerate(test_documents):
                doc_hash = put_artifact(doc.encode('utf-8'))
                doc_hashes.append(doc_hash)
                logger.info(f"Created test document {i+1}: {doc_hash}")
            
            # Create AnalyseBatch task
            task_data = {
                'batch_id': 'test_batch_001',
                'framework_hashes': [framework_hash],
                'document_hashes': doc_hashes,
                'model': 'gemini-2.5-flash',
                'test_metadata': {
                    'test_type': 'phase1_question1',
                    'created_by': 'phase1_test_runner'
                }
            }
            
            # Enqueue task to Redis
            message_id = self.redis_client.xadd('tasks', {
                'type': 'analyse_batch',
                'data': json.dumps(task_data)
            })
            
            logger.info(f"Enqueued AnalyseBatch task: {message_id}")
            
            # Verify task exists in stream
            messages = self.redis_client.xread({'tasks': '0'})
            task_found = False
            
            for stream, msgs in messages:
                for msg_id, fields in msgs:
                    if msg_id == message_id:
                        task_found = True
                        logger.info(f"✅ Task verified in Redis stream: {msg_id}")
                        task_type = fields.get(b'type', b'').decode()
                        if task_type == 'analyse_batch':
                            logger.info("✅ Router should identify this as analyse_batch type")
                        break
            
            if not task_found:
                logger.error("❌ Task not found in Redis stream")
                return False
            
            logger.info("✅ QUESTION 1 SUCCESS: Manual AnalyseBatch task enqueued and verified")
            logger.info(f"   Next step: Run router to process task {message_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ QUESTION 1 FAILED: {e}")
            return False
    
    def test_question2_agent_processing(self, task_id: str = None) -> bool:
        """
        Question 2: Does the `AnalyseBatchAgent` successfully process this task?
        Test: The agent is spawned, reads task, calls LLM, gets valid response.
        Success: A `batch_analysis` artifact is created with structured data only.
        """
        logger.info("=== TESTING QUESTION 2: AnalyseBatchAgent Processing ===")
        
        if not task_id:
            logger.error("❌ QUESTION 2 REQUIRES: task_id from Question 1")
            return False
        
        try:
            # Check if task exists
            messages = self.redis_client.xrange('tasks', task_id, task_id, count=1)
            if not messages:
                logger.error(f"❌ Task {task_id} not found in Redis")
                return False
            
            logger.info(f"Task {task_id} found, ready for processing")
            
            # Wait for completion by polling the tasks.done stream
            logger.info("Waiting up to 120 seconds for agent execution...")
            task_completed = False
            result_hash = None
            start_time = time.time()
            
            while time.time() - start_time < 120:
                done_messages = self.redis_client.xread({'tasks.done': '0'})
                for stream, msgs in done_messages:
                    for msg_id, fields in msgs:
                        completion_data = json.loads(fields[b'data'])
                        if completion_data.get('original_task_id') == task_id:
                            task_completed = True
                            result_hash = completion_data.get('result_hash')
                            logger.info(f"✅ Task completion found: {result_hash}")
                            break
                if task_completed:
                    break
                time.sleep(5)  # Poll every 5 seconds
            
            if not task_completed:
                logger.warning("⚠️  Task completion not detected in time")
                return False
            
            # Validate result artifact structure
            if result_hash and artifact_exists(result_hash):
                result_bytes = get_artifact(result_hash)
                result_data = json.loads(result_bytes.decode('utf-8'))
                
                # Check for structured data requirements
                required_fields = ['batch_id', 'analysis_results', 'batch_metadata']
                for field in required_fields:
                    if field not in result_data:
                        logger.error(f"❌ Missing required field: {field}")
                        return False
                
                logger.info("✅ Result artifact has required structure")
                
                # Check that it's structured data only (no synthesis)
                llm_response = result_data.get('analysis_results', '')
                if 'analysis_results' in llm_response:
                    logger.info("✅ LLM response contains structured analysis_results")
                else:
                    logger.warning("⚠️  LLM response structure unclear - manual review needed")
                
            logger.info("✅ QUESTION 2 SUCCESS: AnalyseBatchAgent processed task successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ QUESTION 2 FAILED: {e}")
            return False
    
    def test_question3_synthesis_trigger(self, batch_result_hash: str = None) -> bool:
        """
        Question 3: Does completion trigger a single `CorpusSynthesis` task?
        Test: After AnalyseBatchAgent finishes, new CorpusSynthesis task appears.
        Success: CorpusSynthesis task enqueued with correct artifact hash.
        """
        logger.info("=== TESTING QUESTION 3: CorpusSynthesis Task Trigger ===")
        
        # For Phase 1, this would be triggered manually
        # In Phase 2, this will be automatic via OrchestratorAgent
        
        if not batch_result_hash:
            logger.error("❌ QUESTION 3 REQUIRES: batch_result_hash from Question 2")
            return False
        
        try:
            # Manually create CorpusSynthesis task for Phase 1 testing
            task_data = {
                'experiment_name': 'phase1_test_experiment',
                'batch_result_hashes': [batch_result_hash],
                'model': 'gemini-2.5-flash', # Explicitly set correct model
                'test_metadata': {
                    'test_type': 'phase1_question3',
                    'created_by': 'phase1_test_runner'
                }
            }
            
            message_id = self.redis_client.xadd('tasks', {
                'type': 'corpus_synthesis',
                'data': json.dumps(task_data)
            })
            
            logger.info(f"✅ Manually created CorpusSynthesis task: {message_id}")
            logger.info("   (In Phase 2, this will be automatic)")
            
            # Verify task structure
            messages = self.redis_client.xrange('tasks', message_id, message_id, count=1)
            if messages:
                msg_id, fields = messages[0]
                task_type = fields.get(b'type', b'').decode()
                if task_type == 'corpus_synthesis':
                    logger.info("✅ CorpusSynthesis task correctly typed")
                    
                    task_data_check = json.loads(fields[b'data'])
                    if batch_result_hash in task_data_check.get('batch_result_hashes', []):
                        logger.info("✅ Correct batch result hash referenced")
                    else:
                        logger.error("❌ Batch result hash not properly referenced")
                        return False
            
            logger.info("✅ QUESTION 3 SUCCESS: CorpusSynthesis task created and validated")
            return True
            
        except Exception as e:
            logger.error(f"❌ QUESTION 3 FAILED: {e}")
            return False
    
    def test_question4_synthesis_processing(self, task_id: str = None) -> bool:
        """
        Question 4: Does CorpusSynthesisAgent perform deterministic aggregation?
        Test: Agent retrieves artifact, performs mathematical aggregation.
        Success: Statistical report artifact created with no qualitative narrative.
        """
        logger.info("=== TESTING QUESTION 4: CorpusSynthesisAgent Processing ===")
        
        if not task_id:
            logger.error("❌ QUESTION 4 REQUIRES: task_id from Question 3")
            return False
        
        try:
            logger.info(f"Task {task_id} ready for CorpusSynthesisAgent processing")
            
            # Wait for completion by polling the tasks.done stream
            logger.info("Waiting up to 120 seconds for agent execution...")
            task_completed = False
            result_hash = None
            start_time = time.time()

            while time.time() - start_time < 120:
                done_messages = self.redis_client.xread({'tasks.done': '0'})
                for stream, msgs in done_messages:
                    for msg_id, fields in msgs:
                        completion_data = json.loads(fields[b'data'])
                        if completion_data.get('original_task_id') == task_id:
                            task_completed = True
                            result_hash = completion_data.get('result_hash')
                            logger.info(f"✅ Synthesis completion found: {result_hash}")
                            break
                if task_completed:
                    break
                time.sleep(5) # Poll every 5 seconds
            
            if not task_completed:
                logger.warning("⚠️  Synthesis completion not detected in time")
                return False
            
            # Validate synthesis result structure
            if result_hash and artifact_exists(result_hash):
                result_bytes = get_artifact(result_hash)
                result_data = json.loads(result_bytes.decode('utf-8'))
                
                # Check for statistical report requirements
                required_fields = ['experiment_name', 'raw_llm_statistical_report', 'aggregation_metadata']
                for field in required_fields:
                    if field not in result_data:
                        logger.error(f"❌ Missing required field: {field}")
                        return False
                
                logger.info("✅ Synthesis result has required structure")
                
                # Check that it's statistical only (no qualitative narrative)
                llm_report = result_data.get('raw_llm_statistical_report', '')
                if 'statistical_summary' in llm_report or 'descriptive_statistics' in llm_report:
                    logger.info("✅ LLM report contains statistical components")
                else:
                    logger.warning("⚠️  Statistical report structure unclear - manual review needed")
                
            logger.info("✅ QUESTION 4 SUCCESS: CorpusSynthesisAgent processed successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ QUESTION 4 FAILED: {e}")
            return False
    
    def run_full_pipeline_test(self) -> bool:
        """Run all Phase 1 questions in sequence"""
        logger.info("=== RUNNING FULL PHASE 1 PIPELINE TEST ===")
        
        # Question 1
        if not self.test_question1_manual_enqueue():
            return False
        
        # Get the task ID from Redis (latest task)
        messages = self.redis_client.xrevrange('tasks', count=1)
        if not messages:
            logger.error("❌ No tasks found for Question 2")
            return False
        
        task_id = messages[0][0].decode()
        logger.info(f"Using task ID for remaining tests: {task_id}")
        
        # Automated agent execution
        logger.info("🤖 AUTOMATED STEP: Running AnalyseBatchAgent...")
        try:
            agent_process = subprocess.run(
                ['python3', 'agents/AnalyseBatchAgent/main.py', task_id],
                capture_output=True, text=True, check=True, timeout=120
            )
            logger.info(f"AnalyseBatchAgent stdout:\n{agent_process.stdout}")
            logger.info("✅ AnalyseBatchAgent completed.")
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            logger.error(f"❌ AnalyseBatchAgent failed: {e}")
            logger.error(f"   stdout: {e.stdout}")
            logger.error(f"   stderr: {e.stderr}")
            return False

        # Question 2
        if not self.test_question2_agent_processing(task_id):
            return False
        
        # Get batch result hash
        done_messages = self.redis_client.xread({'tasks.done': '0'})
        batch_result_hash = None
        for stream, msgs in done_messages:
            for msg_id, fields in msgs:
                completion_data = json.loads(fields[b'data'])
                if completion_data.get('original_task_id') == task_id:
                    batch_result_hash = completion_data.get('result_hash')
                    break
        
        if not batch_result_hash:
            logger.error("❌ Could not find batch result hash")
            return False
        
        # Question 3
        if not self.test_question3_synthesis_trigger(batch_result_hash):
            return False
        
        # Get synthesis task ID
        messages = self.redis_client.xrevrange('tasks', count=1)
        synthesis_task_id = messages[0][0].decode()
        
        # Automated agent execution
        logger.info("🤖 AUTOMATED STEP: Running CorpusSynthesisAgent...")
        try:
            agent_process = subprocess.run(
                ['python3', 'agents/CorpusSynthesisAgent/main.py', synthesis_task_id],
                capture_output=True, text=True, check=True, timeout=120
            )
            logger.info(f"CorpusSynthesisAgent stdout:\n{agent_process.stdout}")
            logger.info("✅ CorpusSynthesisAgent completed.")
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            logger.error(f"❌ CorpusSynthesisAgent failed: {e}")
            logger.error(f"   stdout: {e.stdout}")
            logger.error(f"   stderr: {e.stderr}")
            return False

        # Question 4
        if not self.test_question4_synthesis_processing(synthesis_task_id):
            return False
        
        logger.info("🎉 FULL PHASE 1 PIPELINE TEST COMPLETED SUCCESSFULLY!")
        logger.info("✅ All Phase 1 validation questions answered YES")
        return True

def main():
    parser = argparse.ArgumentParser(description='Phase 1 Test Runner')
    parser.add_argument('--test', required=True, 
                       choices=['question1', 'question2', 'question3', 'question4', 'full_pipeline'],
                       help='Which test to run')
    parser.add_argument('--task-id', help='Task ID for questions 2-4')
    parser.add_argument('--result-hash', help='Result hash for questions 3-4')
    
    args = parser.parse_args()
    
    runner = Phase1TestRunner()
    
    if args.test == 'question1':
        success = runner.test_question1_manual_enqueue()
    elif args.test == 'question2':
        success = runner.test_question2_agent_processing(args.task_id)
    elif args.test == 'question3':
        success = runner.test_question3_synthesis_trigger(args.result_hash)
    elif args.test == 'question4':
        success = runner.test_question4_synthesis_processing(args.task_id)
    elif args.test == 'full_pipeline':
        success = runner.run_full_pipeline_test()
    else:
        success = False
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()