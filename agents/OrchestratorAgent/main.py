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

            # 3. Generate final execution plan
            plan_hash = self._generate_final_plan(experiment, pre_test_result, framework_hashes, corpus_hashes)
            if not plan_hash:
                return False

            # 4. Enqueue plan execution task for the bridge
            self._enqueue_plan_for_execution(plan_hash, experiment_name)
            
            logger.info("Full orchestration complete: Plan generated and enqueued for execution.")
            return True
            
        except Exception as e:
            logger.error(f"Full orchestration failed: {e}")
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
        """Waits for a specific task to appear in the tasks.done stream."""
        logger.info(f"Waiting for completion of task: {task_id}")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            done_messages = self.redis_client.xread({'tasks.done': '0'})
            for stream, msgs in done_messages:
                for msg_id, fields in msgs:
                    completion_data = json.loads(fields[b'data'])
                    if completion_data.get('original_task_id') == task_id:
                        logger.info(f"Task {task_id} completed.")
                        result_hash = completion_data.get('result_hash')
                        result_bytes = get_artifact(result_hash)
                        return json.loads(result_bytes.decode('utf-8'))
            time.sleep(5)
            
        raise OrchestratorAgentError(f"Timed out waiting for task {task_id}")

    def _generate_final_plan(self, experiment: Dict, pre_test_result: Dict, framework_hashes: List[str], corpus_hashes: List[str]) -> str:
        """Calls the LLM with all necessary context to generate the final execution plan."""
        prompt_text = self.prompt_template.format(
            experiment=json.dumps(experiment, indent=2),
            pre_test_results=json.dumps(pre_test_result, indent=2),
            corpus_hashes=json.dumps(corpus_hashes, indent=2),
            framework_hashes=json.dumps(framework_hashes, indent=2),
            model_capabilities=json.dumps(self._get_model_capabilities(), indent=2)
        )

        logger.info("Calling LLM to generate final, batched execution plan...")
        response = completion(
            model="gemini-2.5-pro", # Use Pro for sophisticated planning
            messages=[{"role": "user", "content": prompt_text}],
            temperature=0.0
        )

        plan_content = response.choices[0].message.content
        if not plan_content or plan_content.strip() == "":
            raise OrchestratorAgentError("LLM returned an empty plan.")
        
        # The LLM should return a JSON object with the plan.
        # We store this directly. The ExecutionBridge will parse the 'tasks' key.
        plan_hash = put_artifact(plan_content.encode('utf-8'))
        logger.info(f"Stored final execution plan artifact: {plan_hash}")
        return plan_hash

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

    def _enqueue_plan_for_execution(self, plan_hash: str, experiment_name: str):
        """Enqueues a task for the ExecutionBridge."""
        message_id = self.redis_client.xadd('tasks', {
            'type': 'execute_plan',
            'data': json.dumps({
                'plan_hash': plan_hash,
                'experiment_name': experiment_name
            })
        })
        logger.info(f"Enqueued plan execution task for bridge: {message_id.decode()}")

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