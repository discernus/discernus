#!/usr/bin/env python3
"""
Execution Bridge - THIN Orchestration Plan Executor
===================================================

THIN Principle: This script is a non-intelligent, deterministic executor.
It translates a natural language plan from an LLM (the OrchestratorAgent)
into a series of concrete tasks in a Redis stream. It does not make decisions.

- Input: A structured plan artifact containing a natural language plan.
- Process: Parses the plan and creates Redis tasks for each step.
- Output: A series of tasks in the 'tasks' Redis stream.
"""

import redis
import json
import sys
import os
import logging
import re
from typing import Dict, Any, List

# Add scripts directory to path for imports
sys.path.append(os.path.dirname(__file__))
from minio_client import get_artifact

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - ExecutionBridge - %(message)s')
logger = logging.getLogger(__name__)

# Redis configuration
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = 6379
REDIS_DB = 0

class ExecutionBridgeError(Exception):
    """Bridge-specific exceptions"""
    pass

class ExecutionBridge:
    """
    Translates an OrchestratorAgent's plan into Redis tasks.
    """
    
    def __init__(self):
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        
    def execute_plan(self, plan_hash: str) -> bool:
        """
        Parses a plan artifact and enqueues tasks in Redis.
        """
        try:
            logger.info(f"Executing plan from artifact: {plan_hash}")
            
            # 1. Retrieve the plan artifact
            clean_hash = plan_hash[7:] if plan_hash.startswith('sha256:') else plan_hash
            plan_bytes = get_artifact(clean_hash)
            
            # 2. Parse the plan content
            try:
                plan_data = json.loads(plan_bytes.decode('utf-8'))
            except json.JSONDecodeError as e:
                raise ExecutionBridgeError(f"Failed to parse plan artifact {clean_hash}: {e}")

            # 3. Validate plan structure
            if 'tasks' not in plan_data or not isinstance(plan_data['tasks'], list):
                raise ExecutionBridgeError("Plan artifact is missing a valid 'tasks' list.")
            
            tasks_to_create = plan_data['tasks']
            experiment_name = plan_data.get('experiment_name', 'untitled_experiment')
            logger.info(f"Plan for experiment '{experiment_name}' contains {len(tasks_to_create)} tasks to be enqueued.")

            # 4. Iterate through the plan and enqueue each task
            enqueued_count = 0
            for i, task in enumerate(tasks_to_create):
                task_type = task.get('type')
                task_data = task.get('data')

                if not task_type or not task_data:
                    logger.warning(f"Skipping malformed task at index {i} in plan {clean_hash}")
                    continue

                message_id = self.redis_client.xadd('tasks', {
                    'type': task_type,
                    'data': json.dumps(task_data)
                })
                logger.info(f"Enqueued task {i+1}/{len(tasks_to_create)}: type='{task_type}', id={message_id}")
                enqueued_count += 1
            
            logger.info(f"Successfully enqueued {enqueued_count} tasks from plan {clean_hash}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to execute plan {plan_hash}: {e}")
            return False

def main():
    """Script entry point"""
    if len(sys.argv) != 2:
        print("Usage: execution_bridge.py <plan_hash>")
        sys.exit(1)
    
    plan_hash = sys.argv[1]
    bridge = ExecutionBridge()
    
    success = bridge.execute_plan(plan_hash)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main() 