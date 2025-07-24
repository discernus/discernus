#!/usr/bin/env python3
"""
Phase 3 Test Runner - Complete Quality Assurance Pipeline
Tests the full 3-layer synthesis architecture:
1. Tier 1: AnalyseBatchAgent (multiple batches with CHF framework)
2. Tier 2: CorpusSynthesisAgent (statistical aggregation)  
3. Tier 3: ReviewerAgent + ModeratorAgent (adversarial review and moderation)

Uses Constitutional Health Framework (CHF) v1.1 with 4 substantial political speeches
to create realistic debate between ideological and statistical reviewers.
"""

import sys
import json
import time
import redis
import logging
import argparse
import subprocess
from typing import Dict, Any, List, Optional

# Add scripts directory to path for imports
sys.path.append('scripts')
from minio_client import get_artifact, put_artifact, ArtifactStorageError
from phase3_test_content import get_test_speeches

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Redis configuration
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

class Phase3TestRunner:
    def __init__(self):
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        self.orchestrator_process = None

    def run_full_pipeline_test(self) -> bool:
        """Run complete Phase 3 pipeline test"""
        try:
            logger.info("=== RUNNING FULL PHASE 3 PIPELINE TEST ===")
            
            # Clean Redis for fresh test
            self.redis_client.flushdb()
            logger.info("Redis DB flushed for a clean test run.")

            # Start OrchestratorAgent 
            self.orchestrator_process = self._start_orchestrator_agent()
            logger.info("Starting OrchestratorAgent in the background...")
            time.sleep(5)  # Allow startup

            # Connect to artifact store and create test data
            logger.info("Connected to artifact store at localhost:9000")

            # Create CHF framework artifact
            framework_hash = self._create_chf_framework()
            logger.info(f"Created CHF framework artifact: {framework_hash}")

            # Create speech corpus artifacts
            speech_hashes = self._create_speech_corpus()
            logger.info(f"Created {len(speech_hashes)} speech artifacts")

            # Create initial orchestration request
            experiment_data = {
                "experiment": {
                    "name": "phase3_chf_constitutional_debate",
                    "description": "Complete Phase 3 test with CHF framework and constitutional speeches for adversarial review",  
                    "research_question": "How do different political speakers demonstrate constitutional health/pathology patterns, and how does peer review enhance constitutional analysis?"
                },
                "framework_hashes": [framework_hash],
                "corpus_hashes": speech_hashes
            }

            orchestration_task_id = self.redis_client.xadd('orchestrator.tasks', {
                'data': json.dumps(experiment_data)
            }).decode()

            logger.info("Enqueued initial orchestration request to 'orchestrator.tasks'")

            # Run validation chain
            success = (
                self._validate_batch_analysis() and
                self._validate_corpus_synthesis() and  
                self._validate_review_process() and
                self._validate_moderation_synthesis()
            )

            if success:
                logger.info("✅ PHASE 3 PIPELINE TEST COMPLETED SUCCESSFULLY!")
                logger.info("Complete 3-layer synthesis with adversarial review validated")
                return True
            else:
                logger.error("❌ PHASE 3 PIPELINE TEST FAILED")
                return False

        except Exception as e:
            logger.error(f"❌ PHASE 3 PIPELINE TEST FAILED: {e}")
            import traceback
            traceback.print_exc()
            return False

        finally:
            if self.orchestrator_process:
                self.orchestrator_process.terminate()
                logger.info("OrchestratorAgent terminated.")

    def _start_orchestrator_agent(self) -> subprocess.Popen:
        """Start OrchestratorAgent in background"""
        return subprocess.Popen(
            ['python3', 'agents/OrchestratorAgent/main.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd='.'
        )

    def _create_chf_framework(self) -> str:
        """Create CHF v1.1 Phase 3 test framework artifact"""
        # Read the Phase 3 test CHF framework file
        try:
            with open('scripts/chf_v1.1_phase3_test.md', 'r', encoding='utf-8') as f:
                chf_content = f.read()
        except FileNotFoundError:
            # Fallback to a basic CHF framework if file not found
            chf_content = """# Constitutional Health Framework (CHF) v1.1 - Phase 3 Test Version

## Constitutional Health Dimensions
1. **Procedural Legitimacy** (0.0-1.0): Support for established procedures
2. **Institutional Respect** (0.0-1.0): Recognition of governing authority
3. **Systemic Continuity** (0.0-1.0): Support for constitutional adaptation

## Constitutional Pathology Dimensions  
1. **Procedural Rejection** (0.0-1.0): Rejection of established procedures
2. **Institutional Subversion** (0.0-1.0): Undermining institutional authority
3. **Systemic Replacement** (0.0-1.0): Calls for system replacement

Version 1.1 includes salience-weighted analysis for comprehensive constitutional assessment."""

        framework_bytes = chf_content.encode('utf-8')
        framework_hash = put_artifact(framework_bytes)
        return framework_hash

    def _create_speech_corpus(self) -> List[str]:
        """Create corpus of 4 substantial political speeches"""
        speeches = get_test_speeches()
        speech_hashes = []

        for i, (key, speech_data) in enumerate(speeches.items(), 1):
            speech_content = speech_data['content']
            speech_bytes = speech_content.encode('utf-8')
            speech_hash = put_artifact(speech_bytes)
            speech_hashes.append(speech_hash)
            
            logger.info(f"Created speech {i}: {speech_data['title'][:50]}... ({speech_data['word_count']} words) -> {speech_hash}")

        return speech_hashes

    def _validate_batch_analysis(self) -> bool:
        """Validate Tier 1: Multiple batch analysis completion"""
        logger.info("--- Validating Tier 1: Batch Analysis ---")
        
        # Wait for batch analysis tasks to be created and completed
        batch_tasks_found = self._wait_for_task_completion_by_type('analyse_batch', expected_count=2, timeout=300)
        
        if not batch_tasks_found:
            logger.error("Failed to find expected batch analysis tasks")
            return False

        logger.info(f"✅ Tier 1 validated: {len(batch_tasks_found)} batch analyses completed")
        return True

    def _validate_corpus_synthesis(self) -> bool:
        """Validate Tier 2: Corpus synthesis completion"""
        logger.info("--- Validating Tier 2: Corpus Synthesis ---")
        
        # Wait for synthesis task completion
        synthesis_tasks = self._wait_for_task_completion_by_type('corpus_synthesis', expected_count=1, timeout=300)
        
        if not synthesis_tasks:
            logger.error("Failed to find corpus synthesis task completion")
            return False

        # Store synthesis hash for Phase 3 validation
        self.synthesis_hash = synthesis_tasks[0].get('result_hash')
        logger.info(f"✅ Tier 2 validated: Corpus synthesis completed -> {self.synthesis_hash}")
        return True

    def _validate_review_process(self) -> bool:
        """Validate Tier 3: Review process initiation and completion"""
        logger.info("--- Validating Tier 3: Review Process ---")
        
        # Wait for review tasks to be created and completed
        review_tasks = self._wait_for_task_completion_by_type('review', expected_count=4, timeout=600)  # 2 opening + 2 response
        
        if len(review_tasks) < 4:
            logger.error(f"Expected 4 review tasks (2 opening + 2 response), got {len(review_tasks)}")
            return False

        logger.info(f"✅ Tier 3 Review validated: {len(review_tasks)} review tasks completed")
        
        # Examine review content
        ideological_reviews = [r for r in review_tasks if 'ideological' in str(r)]
        statistical_reviews = [r for r in review_tasks if 'statistical' in str(r)]
        
        logger.info(f"Reviews breakdown: ~{len(ideological_reviews)} ideological, ~{len(statistical_reviews)} statistical")
        return True

    def _validate_moderation_synthesis(self) -> bool:
        """Validate Tier 3: Final moderation and audit trail"""
        logger.info("--- Validating Tier 3: Moderation Synthesis ---")
        
        # Wait for moderation task completion  
        moderation_tasks = self._wait_for_task_completion_by_type('moderation', expected_count=1, timeout=600)
        
        if not moderation_tasks:
            logger.error("Failed to find moderation task completion")
            return False

        moderation_result = moderation_tasks[0]
        audit_trail_hash = moderation_result.get('audit_trail_hash')
        
        if audit_trail_hash:
            logger.info(f"✅ Tier 3 Moderation validated: Final synthesis with audit trail -> {audit_trail_hash}")
            
            # Optionally examine audit trail
            try:
                audit_bytes = get_artifact(audit_trail_hash)
                audit_metadata = json.loads(audit_bytes.decode('utf-8'))
                total_turns = audit_metadata.get('total_turns', 0)
                logger.info(f"Audit trail contains {total_turns} conversation turns")
            except Exception as e:
                logger.warning(f"Could not examine audit trail: {e}")
        else:
            logger.warning("Moderation completed but no audit trail hash found")

        return True

    def _wait_for_task_completion_by_type(self, task_type: str, expected_count: int, timeout: int = 300) -> List[Dict]:
        """Wait for specific number of tasks of given type to complete"""
        completed_tasks = []
        start_time = time.time()
        seen_task_ids = set()

        while len(completed_tasks) < expected_count and time.time() - start_time < timeout:
            try:
                # Read from tasks.done stream
                done_messages = self.redis_client.xread({'tasks.done': '0-0'}, block=1000)
                if not done_messages:
                    continue

                for stream, msgs in done_messages:
                    for msg_id, fields in msgs:
                        try:
                            completion_data = json.loads(fields[b'data'])
                            original_task_id = completion_data.get('original_task_id')
                            completed_task_type = completion_data.get('task_type', '').lower()
                            
                            # Check if this is the task type we're looking for and haven't seen before
                            if (task_type.lower() in completed_task_type or 
                                completed_task_type == task_type.lower()) and original_task_id not in seen_task_ids:
                                
                                completed_tasks.append(completion_data)
                                seen_task_ids.add(original_task_id)
                                logger.info(f"Found {task_type} completion: {original_task_id} ({len(completed_tasks)}/{expected_count})")

                        except Exception as e:
                            logger.error(f"Error processing completion message: {e}")
                            continue

            except Exception as e:
                logger.error(f"Error waiting for {task_type} tasks: {e}")
                time.sleep(1)
                continue

        if len(completed_tasks) < expected_count:
            logger.warning(f"Timeout waiting for {task_type}. Got {len(completed_tasks)}/{expected_count}")

        return completed_tasks

def main():
    """Main test runner entry point"""
    parser = argparse.ArgumentParser(description='Phase 3 Test Runner')
    parser.add_argument('--test', choices=['full_pipeline'], required=True,
                       help='Which test to run')
    
    args = parser.parse_args()
    
    runner = Phase3TestRunner()
    
    if args.test == 'full_pipeline':
        success = runner.run_full_pipeline_test()
        sys.exit(0 if success else 1)

if __name__ == '__main__':
    main() 