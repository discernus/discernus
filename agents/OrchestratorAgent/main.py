#!/usr/bin/env python3
"""
OrchestratorAgent - LLM-powered experiment orchestration
Receives orchestration requests, uses LLM to plan task queues, enqueues tasks.
"""

import redis
import json
import yaml
import sys
import os
import logging
import time
from typing import Dict, Any, List
from litellm import completion

# Add scripts directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from minio_client import put_artifact, get_artifact

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - OrchestratorAgent - %(message)s')
logger = logging.getLogger(__name__)

# Redis configuration
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = 6379
REDIS_DB = 0
CONSUMER_GROUP = 'discernus'
ORCHESTRATOR_STREAM = 'orchestrator.tasks'

class OrchestratorAgentError(Exception):
    """Agent-specific exceptions"""
    pass

class OrchestratorAgent:
    """LLM-powered orchestration agent"""
    
    def __init__(self):
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        self.prompt_template = self._load_prompt_template()
        
    def _load_prompt_template(self) -> str:
        """Load external prompt template - NO PARSING, just string formatting"""
        try:
            prompt_path = os.path.join(os.path.dirname(__file__), 'prompt.yaml')
            with open(prompt_path, 'r') as f:
                prompt_data = yaml.safe_load(f)
            return prompt_data['template']
        except Exception as e:
            logger.error(f"Failed to load prompt template: {e}")
            raise OrchestratorAgentError(f"Prompt loading failed: {e}")
    
    # Hardcoded 5-stage pipeline - prevents coordination variations (per Implementation Plan V3)
    STAGES = [
        ("pretest", "_enqueue_pretest_stage"),
        ("batch_analysis", "_enqueue_batch_analysis_stage"), 
        ("corpus_synthesis", "_enqueue_corpus_synthesis_stage"),
        ("review", "_enqueue_review_stage"),
        ("moderation", "_enqueue_moderation_stage"),
    ]

    def orchestrate_experiment(self, orchestration_data: Dict[str, Any], original_task_id: str) -> bool:
        """
        Orchestrates experiment using hardcoded 5-stage pipeline (Radical Simplification Mode).
        Fixed sequence: PreTest → BatchAnalysis → CorpusSynthesis → Review → Moderation
        """
        try:
            # Set run_id for Redis coordination
            self.run_id = original_task_id
            
            experiment = orchestration_data['experiment']
            framework_hashes = orchestration_data['framework_hashes']
            corpus_hashes = orchestration_data['corpus_hashes']
            experiment_name = experiment.get('name', 'unnamed')

            logger.info(f"Starting hardcoded 5-stage pipeline: {experiment_name} (run_id: {self.run_id})")

            # Execute each stage in fixed sequence
            state = {
                'experiment': experiment,
                'framework_hashes': framework_hashes,
                'corpus_hashes': corpus_hashes,
                'experiment_name': experiment_name
            }
            
            for stage_name, enqueue_method_name in self.STAGES:
                logger.info(f"Executing stage: {stage_name}")
                
                # Check cache first
                if self._is_stage_cached(stage_name, state):
                    logger.info(f"Stage {stage_name} found in cache, skipping")
                    continue
                
                # Get the enqueue method and execute it
                enqueue_method = getattr(self, enqueue_method_name)
                task_ids = enqueue_method(state)
                
                if not task_ids:
                    logger.error(f"Failed to enqueue tasks for stage: {stage_name}")
                    return False
                
                # Wait for completion (single task or multiple tasks)
                if isinstance(task_ids, list):
                    # Handle placeholder tasks (skip waiting)
                    if any("placeholder" in task_id for task_id in task_ids):
                        logger.info(f"Skipping placeholder tasks for stage: {stage_name}")
                        results = task_ids  # Use task_ids as placeholder results
                    else:
                        results = self._wait_for_all_tasks_completion(task_ids)
                    state[f"{stage_name}_results"] = results
                else:
                    # Handle placeholder tasks (skip waiting)
                    if "placeholder" in task_ids:
                        logger.info(f"Skipping placeholder task for stage: {stage_name}")
                        result = task_ids  # Use task_id as placeholder result
                    else:
                        result = self._wait_for_task_completion(task_ids)
                    state[f"{stage_name}_result"] = result
                
                logger.info(f"Stage {stage_name} completed successfully")

            logger.info("Hardcoded 5-stage pipeline completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Hardcoded pipeline failed: {e}", exc_info=True)
            return False

    def _is_stage_cached(self, stage_name: str, state: Dict[str, Any]) -> bool:
        """Check if stage results are already cached in Redis."""
        try:
            cache_key = f"stage:{self.run_id}:{stage_name}:status"
            return self.redis_client.get(cache_key) == b'done'
        except Exception as e:
            logger.warning(f"Cache check failed for stage {stage_name}: {e}")
            return False

    def _enqueue_pretest_stage(self, state: Dict[str, Any]) -> str:
        """Stage 1: PreTest - Variance estimation and run recommendation."""
        experiment_name = state['experiment_name']
        framework_hashes = state['framework_hashes']
        corpus_hashes = state['corpus_hashes']
        
        # Sample first 5 documents for pre-test
        sample_corpus = corpus_hashes[:5]
        
        task_data = {
            'experiment_name': f"{experiment_name}_pre_test",
            'framework_hashes': framework_hashes,
            'document_hashes': sample_corpus,
            'model': 'gemini-2.5-pro',
            'run_id': self.run_id
        }
        
        message_id = self.redis_client.xadd('tasks', {
            'type': 'pre_test',
            'data': json.dumps(task_data)
        })
        
        task_id = message_id.decode()
        logger.info(f"Enqueued PreTest stage: {task_id}")
        return task_id

    def _enqueue_batch_analysis_stage(self, state: Dict[str, Any]) -> List[str]:
        """Stage 2: BatchAnalysis - Multiple statistical runs of the same corpus."""
        framework_hashes = state['framework_hashes']
        corpus_hashes = state['corpus_hashes']
        
        # Get recommendation from pretest (default to 3 if not available)
        pretest_result = state.get('pretest_result', {})
        recommend_runs = 3  # Default fallback
        
        # Create multiple runs for statistical variance
        task_ids = []
        for run_num in range(recommend_runs):
            task_data = {
                'batch_id': f'run_{run_num+1}_of_{recommend_runs}',
                'framework_hashes': framework_hashes,
                'document_hashes': corpus_hashes,  # All documents in each run
                'model': 'gemini-2.5-pro',  # Standardized on Pro for reliability
                'run_number': run_num + 1,
                'total_runs': recommend_runs,
                'run_id': self.run_id
            }

            message_id = self.redis_client.xadd('tasks', {
                'type': 'analyse_batch',
                'data': json.dumps(task_data)
            })
            task_ids.append(message_id.decode())
            
        logger.info(f"Enqueued {len(task_ids)} BatchAnalysis tasks")
        return task_ids

    def _enqueue_corpus_synthesis_stage(self, state: Dict[str, Any]) -> str:
        """Stage 3: CorpusSynthesis - Statistical aggregation of all batch results."""
        experiment_name = state['experiment_name']
        framework_hashes = state['framework_hashes']
        batch_results = state.get('batch_analysis_results', [])
        
        synthesis_task_data = {
            "experiment_name": experiment_name,
            "batch_result_hashes": batch_results,
            "framework_hashes": framework_hashes,
            "model": "gemini-2.5-pro",  # Standardized on Pro for reliability
            "run_id": self.run_id
        }

        message_id = self.redis_client.xadd('tasks', {
            'type': 'corpus_synthesis',
            'data': json.dumps(synthesis_task_data)
        })
        
        task_id = message_id.decode()
        logger.info(f"Enqueued CorpusSynthesis stage: {task_id}")
        return task_id

    def _enqueue_review_stage(self, state: Dict[str, Any]) -> List[str]:
        """Stage 4: Review - Adversarial critique of synthesis report."""
        # TODO: Implement ReviewerAgent tasks (placeholder for Phase 3)
        logger.info("Review stage not yet implemented - skipping")
        return ["placeholder-review-task"]

    def _enqueue_moderation_stage(self, state: Dict[str, Any]) -> str:
        """Stage 5: Moderation - Final synthesis and reconciliation."""
        # TODO: Implement ModeratorAgent task (placeholder for Phase 3)
        logger.info("Moderation stage not yet implemented - skipping")
        return "placeholder-moderation-task"

    def _enqueue_pre_test_task(self, experiment_name: str, framework_hashes: List[str], corpus_hashes: List[str]) -> str:
        """Creates and enqueues a task for the PreTestAgent."""
        # For now, we sample the first 5 documents for the pre-test
        sample_corpus = corpus_hashes[:5]
        
        task_data = {
            'experiment_name': f"{experiment_name}_pre_test",
            'framework_hashes': framework_hashes,
            'document_hashes': sample_corpus,
            'model': 'gemini-2.5-pro',
            'run_id': self.run_id  # Add run_id for completion signaling
        }
        
        message_id = self.redis_client.xadd('tasks', {
            'type': 'pre_test',
            'data': json.dumps(task_data)
        })
        logger.info(f"Enqueued PreTest task: {message_id.decode()}")
        return message_id.decode()

    def _wait_for_task_completion(self, task_id: str, timeout: int = 300) -> Dict:
        """Waits for a single task completion using architect-specified Redis keys/lists pattern."""
        logger.info(f"Waiting for completion of task: {task_id}")
        
        # Check cache first - if status key exists and artifact present, skip
        status_key = f"task:{task_id}:status"
        if self.redis_client.get(status_key) == b'done':
            logger.info(f"Task {task_id} found in cache, retrieving result")
            # Get result hash from completion list (most recent entry for this run)
            completion_data = self._get_cached_result(task_id)
            if completion_data:
                return completion_data
        
        # Use architect-specified BRPOP pattern - no consumer groups, no races
        run_completion_key = f"run:{self.run_id}:done"
        logger.info(f"Blocking wait on completion list: {run_completion_key}")
        
        completed_task = self.redis_client.brpop(run_completion_key, timeout=timeout)
        if not completed_task:
            raise OrchestratorAgentError(f"Task {task_id} did not complete within {timeout} seconds")
            
        completed_task_id = completed_task[1].decode()
        logger.info(f"Task completed: {completed_task_id}")
        
        # Verify this is the task we were waiting for
        if completed_task_id != task_id:
            raise OrchestratorAgentError(f"Expected task {task_id}, but got {completed_task_id}")
        
        # Load result artifact
        return self._load_result_artifact(completed_task_id)

    def _get_cached_result(self, task_id: str) -> Dict:
        """Retrieve cached result for a completed task."""
        try:
            # Look for result hash in Redis (stored by agent completion)
            result_key = f"task:{task_id}:result_hash"
            result_hash = self.redis_client.get(result_key)
            if result_hash:
                result_bytes = get_artifact(result_hash.decode())
                return json.loads(result_bytes.decode('utf-8'))
            return None
        except Exception as e:
            logger.error(f"Error retrieving cached result for {task_id}: {e}")
            return None

    def _load_result_artifact(self, task_id: str) -> Dict:
        """Load result artifact for a completed task."""
        try:
            # Get result hash from Redis key set by agent
            result_key = f"task:{task_id}:result_hash"
            result_hash = self.redis_client.get(result_key)
            if not result_hash:
                raise OrchestratorAgentError(f"No result hash found for task {task_id}")
            
            result_bytes = get_artifact(result_hash.decode())
            return json.loads(result_bytes.decode('utf-8'))
        except Exception as e:
            logger.error(f"Error loading result artifact for {task_id}: {e}")
            raise OrchestratorAgentError(f"Failed to load result for task {task_id}: {e}")

    def _wait_for_all_tasks_completion(self, task_ids: List[str], timeout: int = 1800) -> List[str]:
        """Waits for multiple tasks to complete using architect-specified Redis keys/lists pattern."""
        logger.info(f"Waiting for {len(task_ids)} analysis tasks to complete...")
        completed_tasks = set()
        result_hashes = []
        start_time = time.time()
        run_completion_key = f"run:{self.run_id}:done"

        while len(completed_tasks) < len(task_ids):
            remaining_time = timeout - (time.time() - start_time)
            if remaining_time <= 0:
                raise OrchestratorAgentError(f"Timed out waiting for all analysis tasks. Completed {len(completed_tasks)} of {len(task_ids)}.")
            
            # Check cache first for any tasks that might already be done
            for task_id in task_ids:
                if task_id not in completed_tasks:
                    status_key = f"task:{task_id}:status"
                    if self.redis_client.get(status_key) == b'done':
                        logger.info(f"Task {task_id} found in cache ({len(completed_tasks)+1}/{len(task_ids)})")
                        result_hash = self.redis_client.get(f"task:{task_id}:result_hash")
                        if result_hash:
                            completed_tasks.add(task_id)
                            result_hashes.append(result_hash.decode())

            # If we still need to wait for tasks, use BRPOP
            if len(completed_tasks) < len(task_ids):
                completed_task = self.redis_client.brpop(run_completion_key, timeout=min(60, int(remaining_time)))
                if completed_task:
                    completed_task_id = completed_task[1].decode()
                    if completed_task_id in task_ids and completed_task_id not in completed_tasks:
                        logger.info(f"Analysis task {completed_task_id} completed ({len(completed_tasks)+1}/{len(task_ids)})")
                        result_hash = self.redis_client.get(f"task:{completed_task_id}:result_hash")
                        if result_hash:
                            completed_tasks.add(completed_task_id)
                            result_hashes.append(result_hash.decode())
        
        logger.info("All analysis tasks completed.")
        return result_hashes

    def _generate_analysis_plan(self, experiment: Dict, pre_test_result: Dict, framework_hashes: List[str], corpus_hashes: List[str]) -> str:
        """Calls the LLM to generate just the analysis part of the plan."""
        prompt_text = self.prompt_template.format(
            experiment=json.dumps(experiment, indent=2),
            pre_test_results=json.dumps(pre_test_result, indent=2),
            corpus_hashes=json.dumps(corpus_hashes, indent=2),
            framework_hashes=json.dumps(framework_hashes, indent=2),
            model_capabilities=json.dumps(self._get_model_capabilities(), indent=2),
            task_type_focus="'analyse_batch' tasks only" # New prompt parameter
        )

        logger.info("Calling LLM to generate batched ANALYSIS plan...")
        response = completion(
            model="gemini-2.5-pro",
            messages=[{"role": "user", "content": prompt_text}],
            temperature=0.0
        )

        plan_content = response.choices[0].message.content
        if not plan_content or plan_content.strip() == "":
            raise OrchestratorAgentError("LLM returned an empty analysis plan.")
        
        plan_hash = put_artifact(plan_content.strip().encode('utf-8'))
        logger.info(f"Stored analysis plan artifact: {plan_hash}")
        return plan_hash

    def _execute_plan(self, plan_hash: str, experiment_name: str, framework_hashes: List[str], corpus_hashes: List[str], pre_test_result: Dict = None) -> List[str]:
        """Executes a plan and returns the IDs of the tasks created."""
        logger.info(f"Executing plan from artifact: {plan_hash}")
        plan_bytes = get_artifact(plan_hash)
        plan_content = plan_bytes.decode('utf-8')

        # Extract recommend_runs from PreTest results
        recommend_runs = 3  # Default fallback
        if pre_test_result:
            # Try to extract recommend_runs from various possible formats
            if isinstance(pre_test_result, dict):
                # Direct key access
                recommend_runs = pre_test_result.get('recommend_runs', recommend_runs)
                
                # Check if it's in the raw LLM response text
                raw_response = pre_test_result.get('analysis_results', '')
                if not pre_test_result.get('recommend_runs') and raw_response:
                    # Parse the LLM response text for recommend_runs
                    import re
                    match = re.search(r'recommend_runs["\']?\s*:?\s*(\d+)', raw_response, re.IGNORECASE)
                    if match:
                        recommend_runs = int(match.group(1))
                        logger.info(f"Extracted recommend_runs={recommend_runs} from PreTest raw response")
                    else:
                        logger.warning(f"Could not extract recommend_runs from PreTest response, using default {recommend_runs}")
                        
            logger.info(f"PreTest recommended {recommend_runs} runs for statistical confidence")
        else:
            logger.warning("No PreTest result provided, using default 3 runs")

        # Create multiple runs of the SAME documents for statistical variance analysis
        logger.info(f"Creating {recommend_runs} statistical runs of identical document set...")
        task_ids = []
        
        for run_num in range(recommend_runs):
            task_data = {
                'batch_id': f'run_{run_num+1}_of_{recommend_runs}',
                'framework_hashes': framework_hashes,
                'document_hashes': corpus_hashes,  # ALL documents in each run
                'model': 'gemini-2.5-flash',
                'run_number': run_num + 1,
                'total_runs': recommend_runs,
                'run_id': self.run_id  # Add run_id for completion signaling
            }

            message_id = self.redis_client.xadd('tasks', {
                'type': 'analyse_batch',
                'data': json.dumps(task_data)
            })
            task_ids.append(message_id.decode())
            logger.info(f"Created run {run_num+1}/{recommend_runs} with {len(corpus_hashes)} documents")
        
        logger.info(f"Successfully created {len(task_ids)} statistical runs from plan {plan_hash}")
        return task_ids

    def _enqueue_synthesis_task(self, experiment_name: str, analysis_result_hashes: List[str], framework_hashes: List[str]):
        """Enqueues the final synthesis task."""
        synthesis_task_data = {
            "experiment_name": experiment_name,
            "batch_result_hashes": analysis_result_hashes,
            "framework_hashes": framework_hashes,
            "model": "gemini-2.5-flash",
            "run_id": self.run_id  # Add run_id for completion signaling
        }

        message_id = self.redis_client.xadd('tasks', {
            'type': 'corpus_synthesis',
            'data': json.dumps(synthesis_task_data)
        })
        logger.info(f"Enqueued final synthesis task: {message_id.decode()}")

    def _get_model_capabilities(self) -> Dict:
        """Returns a summary of available model capabilities."""
        # This can be expanded to read from a model registry in the future.
        return {
            "gemini-2.5-flash": {
                "context_window_tokens": 1000000,
                "use_case": "High-throughput, cost-effective analysis and synthesis"
            },
            "gemini-2.5-pro": {
                "context_window_tokens": 8000000,
                "use_case": "Complex reasoning, planning, and statistical interpretation"
            }
        }

    def listen_for_orchestration_requests(self):
        """Listen for orchestration requests on orchestrator.tasks stream"""
        logger.info("OrchestratorAgent listening for requests...")
        
        # Ensure the stream and consumer group exist
        try:
            self.redis_client.xgroup_create(ORCHESTRATOR_STREAM, CONSUMER_GROUP, id='0', mkstream=True)
            logger.info(f"Consumer group '{CONSUMER_GROUP}' created for stream '{ORCHESTRATOR_STREAM}'.")
        except redis.exceptions.ResponseError as e:
            if "consumer group name already exists" in str(e).lower():
                logger.info(f"Consumer group '{CONSUMER_GROUP}' already exists.")
            else:
                raise # Reraise other errors

        # Note: No longer creating 'waiters' consumer group - using Redis keys/lists pattern instead

        try:
            while True:
                # Read orchestration requests (blocking)
                messages = self.redis_client.xreadgroup(
                    CONSUMER_GROUP, 'orchestrator',
                    {'orchestrator.tasks': '>'},
                    count=1, block=0  # Block until message available
                )
                
                for stream, msgs in messages:
                    for msg_id, fields in msgs:
                        try:
                            orchestration_data = json.loads(fields[b'data'])
                            
                            # Process orchestration request
                            success = self.orchestrate_experiment(orchestration_data, msg_id.decode())
                            
                            if success:
                                logger.info(f"Orchestration request completed: {msg_id.decode()}")
                            else:
                                logger.error(f"Orchestration request failed: {msg_id.decode()}")
                            
                            # Acknowledge message
                            self.redis_client.xack('orchestrator.tasks', CONSUMER_GROUP, msg_id)
                            
                        except Exception as e:
                            logger.error(f"Error processing orchestration request: {e}")
                            continue
                            
        except KeyboardInterrupt:
            logger.info("OrchestratorAgent shutdown requested")
        except Exception as e:
            logger.error(f"Orchestrator listening error: {e}")
            raise

def main():
    """Agent entry point"""
    agent = OrchestratorAgent()
    
    try:
        # Start listening for orchestration requests
        agent.listen_for_orchestration_requests()
    except Exception as e:
        logger.error(f"OrchestratorAgent failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 