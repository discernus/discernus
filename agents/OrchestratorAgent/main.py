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
    
    def orchestrate_experiment(self, orchestration_data: Dict[str, Any], original_task_id: str) -> bool:
        """
        Orchestrates the full, dynamic, multi-step experiment pipeline.
        1. Triggers PreTestAgent to determine run count.
        2. Waits for PreTestAgent completion.
        3. Generates final batched execution plan.
        4. Hands off plan to ExecutionBridge.
        """
        try:
            experiment = orchestration_data['experiment']
            framework_hashes = orchestration_data['framework_hashes']
            corpus_hashes = orchestration_data['corpus_hashes']
            experiment_name = experiment.get('name', 'unnamed')

            logger.info(f"Orchestrating experiment: {experiment_name}")

            # 1. Enqueue PreTest task
            pre_test_task_id = self._enqueue_pre_test_task(experiment_name, framework_hashes, corpus_hashes)
            if not pre_test_task_id:
                return False

            # 2. Wait for PreTest completion
            pre_test_result = self._wait_for_task_completion(pre_test_task_id)
            if not pre_test_result:
                return False

            # 3. Generate and execute the analysis plan (fan-out)
            analysis_plan_hash = self._generate_analysis_plan(experiment, pre_test_result, framework_hashes, corpus_hashes)
            if not analysis_plan_hash:
                return False
            
            analysis_task_ids = self._execute_plan(analysis_plan_hash, experiment_name, framework_hashes, corpus_hashes, pre_test_result)
            if not analysis_task_ids:
                return False

            # 4. Wait for all analysis tasks to complete
            analysis_result_hashes = self._wait_for_all_tasks_completion(analysis_task_ids)
            if not analysis_result_hashes:
                return False
                
            # 5. Generate and execute the synthesis task (fan-in)
            self._enqueue_synthesis_task(experiment_name, analysis_result_hashes, framework_hashes)

            logger.info("Full orchestration complete: Fan-out/fan-in cycle finished.")
            return True
            
        except Exception as e:
            logger.error(f"Full orchestration failed: {e}", exc_info=True)
            return False

    def _enqueue_pre_test_task(self, experiment_name: str, framework_hashes: List[str], corpus_hashes: List[str]) -> str:
        """Creates and enqueues a task for the PreTestAgent."""
        # For now, we sample the first 5 documents for the pre-test
        sample_corpus = corpus_hashes[:5]
        
        task_data = {
            'experiment_name': f"{experiment_name}_pre_test",
            'framework_hashes': framework_hashes,
            'document_hashes': sample_corpus,
            'model': 'gemini-2.5-pro'
        }
        
        message_id = self.redis_client.xadd('tasks', {
            'type': 'pre_test',
            'data': json.dumps(task_data)
        })
        logger.info(f"Enqueued PreTest task: {message_id.decode()}")
        return message_id.decode()

    def _wait_for_task_completion(self, task_id: str, timeout: int = 300) -> Dict:
        """Waits for a single task to appear in the tasks.done stream."""
        logger.info(f"Waiting for completion of task: {task_id}")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            done_messages = self.redis_client.xread({'tasks.done': '0-0'}, block=1000)
            if not done_messages:
                continue
            for stream, msgs in done_messages:
                for msg_id, fields in msgs:
                    completion_data = json.loads(fields[b'data'])
                    if completion_data.get('original_task_id') == task_id:
                        logger.info(f"Task {task_id} completed.")
                        result_hash = completion_data.get('result_hash')
                        if not result_hash:
                            raise OrchestratorAgentError(f"Completion message for {task_id} is missing a result_hash.")
                        result_bytes = get_artifact(result_hash)
                        return json.loads(result_bytes.decode('utf-8'))
            time.sleep(1)
            
        raise OrchestratorAgentError(f"Timed out waiting for task {task_id}")

    def _wait_for_all_tasks_completion(self, task_ids: List[str], timeout: int = 1800) -> List[str]:
        """Waits for a list of tasks to complete and collects their result hashes."""
        logger.info(f"Waiting for {len(task_ids)} analysis tasks to complete...")
        completed_tasks = set()
        result_hashes = []
        start_time = time.time()

        while len(completed_tasks) < len(task_ids):
            if time.time() - start_time > timeout:
                raise OrchestratorAgentError(f"Timed out waiting for all analysis tasks. Completed {len(completed_tasks)} of {len(task_ids)}.")
            
            done_messages = self.redis_client.xread({'tasks.done': '0-0'}, block=1000)
            if not done_messages:
                continue
            
            for stream, msgs in done_messages:
                for msg_id, fields in msgs:
                    completion_data = json.loads(fields[b'data'])
                    original_task_id = completion_data.get('original_task_id')
                    
                    if original_task_id in task_ids and original_task_id not in completed_tasks:
                        logger.info(f"Analysis task {original_task_id} completed ({len(completed_tasks)+1}/{len(task_ids)}).")
                        result_hash = completion_data.get('result_hash')
                        if not result_hash:
                            logger.warning(f"Completion message for {original_task_id} is missing a result_hash.")
                            continue
                        
                        completed_tasks.add(original_task_id)
                        result_hashes.append(result_hash)
            
            time.sleep(2)
        
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
                'total_runs': recommend_runs
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
            "model": "gemini-2.5-flash"
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