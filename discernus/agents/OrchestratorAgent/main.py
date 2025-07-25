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
import hashlib
from typing import Dict, Any, List
from litellm import completion

# Add scripts directory to path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
scripts_path = os.path.join(project_root, 'scripts')
sys.path.insert(0, scripts_path)
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
    
    # Alpha System Specification Section 4.2: Required 3-agent pipeline
    # CLI handles VALIDATION and RUN SETUP, orchestrator handles the agent stages
    STAGES = [
        ("batch_analysis", "_enqueue_batch_analysis_stage"), 
        ("synthesis", "_enqueue_synthesis_stage"),
        ("report_generation", "_enqueue_report_generation_stage"),
    ]

    def orchestrate_experiment(self, orchestration_data: Dict[str, Any], original_task_id: str) -> bool:
        """
        Orchestrates experiment using Alpha System Specification Section 4.2 pipeline.
        Fixed sequence: BatchAnalysis → Synthesis → ReportGeneration
        """
        completed_stages = []
        
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
                    completed_stages.append(stage_name)
                    continue
                
                # Get the enqueue method and execute it
                enqueue_method = getattr(self, enqueue_method_name)
                task_ids = enqueue_method(state)
                
                if not task_ids:
                    logger.error(f"Failed to enqueue tasks for stage: {stage_name}")
                    self._export_partial_manifest(completed_stages, "ENQUEUE_FAILED")
                    return False
                
                # Wait for completion with timeout handling
                try:
                    if isinstance(task_ids, list):
                        if not task_ids:
                            logger.error(f"No tasks returned for stage: {stage_name}")
                            self._export_partial_manifest(completed_stages, "NO_TASKS")
                            return False
                        results = self._wait_for_all_tasks_completion(task_ids, timeout=300)
                        state[f"{stage_name}_results"] = results
                    else:
                        if not task_ids:
                            logger.error(f"No task returned for stage: {stage_name}")
                            self._export_partial_manifest(completed_stages, "NO_TASK")
                            return False
                        result = self._wait_for_task_completion(task_ids, timeout=300)
                        # Store both the full result and extract the result hash for next stage
                        state[f"{stage_name}_result"] = result
                        # Extract result hash from Redis key for passing to next stage
                        result_key = f"task:{task_ids}:result_hash"
                        result_hash = self.redis_client.get(result_key)
                        if result_hash:
                            state[f"{stage_name}_result"]['result_hash'] = result_hash.decode()
                        
                    completed_stages.append(stage_name)
                    logger.info(f"Stage {stage_name} completed successfully")
                    
                except Exception as e:
                    if "timeout" in str(e).lower():
                        logger.error(f"Stage {stage_name} timed out: {e}")
                        self._export_partial_manifest(completed_stages, "ERROR_TIMEOUT")
                        return False
                    else:
                        logger.error(f"Stage {stage_name} failed: {e}")
                        self._export_partial_manifest(completed_stages, "ERROR_FAILED")
                        return False

            logger.info("Hardcoded 5-stage pipeline completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Hardcoded pipeline failed: {e}", exc_info=True)
            self._export_partial_manifest(completed_stages, "ERROR_EXCEPTION")
            return False

    def _generate_cache_key(self, stage_name: str, state: Dict[str, Any], run_index: int = 0) -> str:
        """Generate SHA-256 cache key per Implementation Plan V4 specification"""
        try:
            # Get document and framework hashes
            doc_hashes = sorted(state.get('corpus_hashes', []))
            framework_hashes = sorted(state.get('framework_hashes', []))
            
            # Create prompt hash (simplified for now - could be actual prompt content hash)
            prompt_hash = f"{stage_name}_{self.run_id}"
            
            # Combine all components for cache key
            cache_components = doc_hashes + framework_hashes + [prompt_hash, str(run_index)]
            cache_string = "|".join(cache_components)
            
            # Generate SHA-256 hash
            cache_key = hashlib.sha256(cache_string.encode('utf-8')).hexdigest()
            return f"stage:{self.run_id}:{stage_name}:{cache_key}"
            
        except Exception as e:
            logger.warning(f"Cache key generation failed: {e}, using fallback")
            return f"stage:{self.run_id}:{stage_name}:fallback"

    def _is_stage_cached(self, stage_name: str, state: Dict[str, Any]) -> bool:
        """Check if stage results are already cached using proper cache key."""
        try:
            cache_key = self._generate_cache_key(stage_name, state)
            status_key = f"{cache_key}:status"
            return self.redis_client.get(status_key) == b'done'
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
            'type': 'pre_test',  # Include type in task data for router
            'experiment_name': f"{experiment_name}_pre_test",
            'framework_hashes': framework_hashes,
            'document_hashes': sample_corpus,
            'model': 'gemini-2.5-pro',
            'run_id': self.run_id
        }
        
        # Use LPUSH to task list instead of XADD to stream (per architecture spec 4.2)
        self.redis_client.lpush('tasks', json.dumps(task_data))
        
        # Generate deterministic task ID for tracking
        task_id = f"{self.run_id}_pretest"
        logger.info(f"Enqueued PreTest stage: {task_id}")
        return task_id

    def _enqueue_batch_analysis_stage(self, state: Dict[str, Any]) -> str:
        """Stage 1: BatchAnalysis - Single batch analysis of entire corpus per Alpha System Spec."""
        framework_hashes = state['framework_hashes']
        corpus_hashes = state['corpus_hashes']
        experiment_name = state['experiment_name']
        
        # Single batch analysis (Alpha System processes single-batch corpus sizes)
        task_data = {
            'batch_id': f"{experiment_name}_single_batch",  # Required by AnalyseBatchAgent
            'experiment_name': experiment_name,
            'framework_hashes': framework_hashes,
            'document_hashes': corpus_hashes,  # All documents in single batch
            'model': 'vertex_ai/gemini-2.5-pro',  # Standardized on Pro for reliability
            'run_id': self.run_id
        }

        # Use 'analyse_batch' task type to route to AnalyseBatchAgent per router configuration
        # Router generates task ID as: {run_id}_{task_type}
        task_id = f"{self.run_id}_analyse_batch"
        self.redis_client.lpush('tasks', json.dumps({
            'type': 'analyse_batch',
            **task_data
        }))
            
        logger.info(f"Enqueued BatchAnalysis stage: {task_id}")
        return task_id

    def _enqueue_synthesis_stage(self, state: Dict[str, Any]) -> str:
        """Stage 2: Synthesis - Statistical aggregation of all batch results per Alpha System Spec."""
        experiment_name = state['experiment_name']
        framework_hashes = state['framework_hashes']
        # Fix: Use singular "batch_analysis_result" to match completion handler
        batch_result = state.get('batch_analysis_result', {})
        batch_results = [batch_result.get('result_hash')] if batch_result.get('result_hash') else []
        
        synthesis_task_data = {
            "experiment_name": experiment_name,
            "analysis_hashes": batch_results,  # Match SynthesisAgent expected field
            "framework_hash": framework_hashes[0] if framework_hashes else "",  # SynthesisAgent expects singular
            "model": "vertex_ai/gemini-2.5-pro",  # Match LiteLLM format
            "run_id": self.run_id
        }

        # Use 'synthesis' task type to route to SynthesisAgent per router configuration
        # Router generates task ID as: {run_id}_{task_type}
        task_id = f"{self.run_id}_synthesis"
        self.redis_client.lpush('tasks', json.dumps({
            'type': 'synthesis',
            **synthesis_task_data
        }))
        
        logger.info(f"Enqueued Synthesis stage: {task_id}")
        return task_id

    def _enqueue_report_generation_stage(self, state: Dict[str, Any]) -> str:
        """Stage 3: Report Generation - Human-readable final report per Alpha System Spec."""
        experiment_name = state['experiment_name']
        framework_hashes = state['framework_hashes']
        # Fix: Use singular "synthesis_result" to match completion handler
        synthesis_result = state.get('synthesis_result', {})
        synthesis_hash = synthesis_result.get('result_hash') if synthesis_result else None
        
        report_task_data = {
            "experiment_name": experiment_name,
            "synthesis_hash": synthesis_hash,
            "framework_hashes": framework_hashes,
            "model": "gemini-2.5-pro",  # Standardized on Pro for reliability
            "run_id": self.run_id
        }

        # Use 'report' task type to route to ReportAgent per router configuration
        # Router generates task ID as: {run_id}_{task_type}
        task_id = f"{self.run_id}_report"
        self.redis_client.lpush('tasks', json.dumps({
            'type': 'report',
            **report_task_data
        }))
        
        logger.info(f"Enqueued Report Generation stage: {task_id}")
        return task_id

    def _enqueue_review_stage(self, state: Dict[str, Any]) -> List[str]:
        """Stage 4: Review - Adversarial critique of synthesis report."""
        synthesis_result = state.get('corpus_synthesis_result')
        if not synthesis_result:
            logger.error("No synthesis result available for review stage")
            return []
        
        # Create two review tasks: ideological and statistical
        review_tasks = []
        
        # Ideological review task
        ideological_task_data = {
            'review_type': 'ideological',
            'ideology': 'progressive',  # Default ideology
            'synthesis_hash': synthesis_result,
            'model': 'gemini-2.5-pro',
            'run_id': self.run_id
        }
        
        ideological_message_id = self.redis_client.xadd('tasks', {
            'type': 'review',
            'data': json.dumps(ideological_task_data)
        })
        review_tasks.append(ideological_message_id.decode())
        
        # Statistical review task  
        statistical_task_data = {
            'review_type': 'statistical',
            'synthesis_hash': synthesis_result,
            'model': 'gemini-2.5-pro',
            'run_id': self.run_id
        }
        
        statistical_message_id = self.redis_client.xadd('tasks', {
            'type': 'review', 
            'data': json.dumps(statistical_task_data)
        })
        review_tasks.append(statistical_message_id.decode())
        
        logger.info(f"Enqueued {len(review_tasks)} review tasks")
        return review_tasks

    def _enqueue_moderation_stage(self, state: Dict[str, Any]) -> str:
        """Stage 5: Moderation - Final synthesis and reconciliation."""
        synthesis_result = state.get('corpus_synthesis_result')
        review_results = state.get('review_results', [])
        experiment_name = state['experiment_name']
        
        if not synthesis_result:
            logger.error("No synthesis result available for moderation stage")
            return ""
        
        moderation_task_data = {
            'synthesis_hash': synthesis_result,
            'review_hashes': review_results,
            'experiment_name': experiment_name,
            'model': 'gemini-2.5-pro',
            'run_id': self.run_id
        }
        
        message_id = self.redis_client.xadd('tasks', {
            'type': 'moderation',
            'data': json.dumps(moderation_task_data)
        })
        
        task_id = message_id.decode()
        logger.info(f"Enqueued moderation task: {task_id}")
        return task_id

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
                'model': 'gemini-2.5-pro',
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
            "model": "gemini-2.5-pro",
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
            "gemini-2.5-pro": {
                "context_window_tokens": 8000000,
                "use_case": "Complex reasoning, planning, statistical interpretation, and reliable multi-framework analysis"
            }
        }

    def _export_partial_manifest(self, completed_stages: List[str], error_status: str) -> None:
        """Export partial manifest when pipeline fails or times out"""
        try:
            partial_manifest = {
                "run_id": self.run_id,
                "completed_stages": completed_stages,
                "total_stages": len(self.STAGES),
                "run_status": error_status,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "resume_from": completed_stages[-1] if completed_stages else "pretest"
            }
            
            # Store partial manifest in Redis for potential resume
            manifest_key = f"partial_manifest:{self.run_id}"
            self.redis_client.setex(manifest_key, 86400, json.dumps(partial_manifest))  # 24 hour expiry
            
            logger.info(f"Partial manifest exported: {error_status}, completed {len(completed_stages)}/{len(self.STAGES)} stages")
            
        except Exception as e:
            logger.error(f"Failed to export partial manifest: {e}")

    def listen_for_orchestration_requests(self):
        """Listen for orchestration requests on orchestrator.tasks list (per architecture spec 4.2)"""
        logger.info("OrchestratorAgent listening for requests...")
        
        # No stream setup needed - using simple Redis lists per architecture spec
        # Architecture 4.2: "Legacy consumer‑group races are eliminated. Completion signalling uses Redis keys/lists"
        
        try:
            while True:
                # Use BRPOP on orchestrator.tasks list (blocking, deterministic, no consumer groups)
                result = self.redis_client.brpop('orchestrator.tasks', timeout=0)
                
                if result:
                    list_name, data = result
                    task_id = None
                    
                    try:
                        orchestration_data = json.loads(data)
                        task_id = orchestration_data.get('task_id', 'unknown')
                        
                        # Process orchestration request
                        success = self.orchestrate_experiment(orchestration_data, task_id)
                        
                        if success:
                            logger.info(f"Orchestration request completed: {task_id}")
                        else:
                            logger.error(f"Orchestration request failed: {task_id}")
                            
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