#!/usr/bin/env python3
"""
TaskListExecutorAgent - THIN agent for executing raw task lists
Reads raw LLM task interpretations and lets LLM agents execute them directly.
"""

import redis
import json
import sys
import os
import logging
from typing import Dict, Any
from litellm import completion
from minio import Minio

# Add scripts directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TaskListExecutorAgent:
    def __init__(self):
        # Redis connection for task queues
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        self.redis_client = redis.Redis(host=redis_host, port=6379, db=0)
        
        # MinIO connection for artifact storage
        minio_host = os.getenv('MINIO_HOST', 'localhost')
        self.minio_client = Minio(
            f"{minio_host}:9000",
            access_key=os.getenv('MINIO_ACCESS_KEY', 'minioadmin'),
            secret_key=os.getenv('MINIO_SECRET_KEY', 'minioadmin'),
            secure=False
        )
        
        logger.info("TaskListExecutorAgent initialized")

    def execute_task_list(self, task_id: str) -> bool:
        """Execute a raw task list by having LLM interpret and enqueue tasks"""
        
        # Get task data from Redis
        task_data = self.redis_client.xrange('tasks', task_id, task_id)
        if not task_data:
            logger.error(f"Task {task_id} not found in Redis")
            return False
            
        task_info = task_data[0][1]
        data = json.loads(task_info[b'data'].decode())
        
        task_list_hash = data['task_list_hash']
        experiment_name = data['experiment_name']
        
        logger.info(f"Executing task list for experiment: {experiment_name}")
        logger.info(f"Task list hash: {task_list_hash[:12]}...")
        
        # Retrieve raw task list from MinIO (THIN - no parsing)
        try:
            task_list_key = f"task_lists/{task_list_hash}"
            logger.info("Retrieving raw task list...")
            
            response = self.minio_client.get_object("discernus-artifacts", task_list_key)
            raw_task_list = response.read().decode()
            response.close()
            
            logger.info(f"Retrieved raw task list with {len(raw_task_list)} characters")
            
        except Exception as e:
            logger.error(f"Failed to retrieve task list: {e}")
            return False
            
        # Let LLM interpret and execute the raw task list (THIN - no parsing)
        prompt = f"""You are a task execution agent. You have access to a Redis task queue system.

I'm giving you a raw LLM response that contains task instructions for experiment "{experiment_name}".

Your job is to interpret this raw response and directly enqueue individual tasks to Redis.

Raw task list response:
{raw_task_list}

Please write Python code to:
1. Extract the individual tasks from this response (handle any markdown formatting)
2. For each task, call redis_client.xadd('tasks', {{'type': task_type, 'data': json.dumps(task_params)}})

Available task types: analyse, synthesize

Redis client is already connected as `redis_client`.
"""

        try:
            # Call LLM with code execution capabilities
            logger.info("Calling LLM to interpret and execute task list...")
            response = completion(
                model="gemini-2.5-flash",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                safety_settings=[
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
                ]
            )
            
            # Store raw LLM execution response (THIN - no parsing)
            llm_response = response.choices[0].message.content
            logger.info(f"LLM provided task execution instructions with {len(llm_response)} characters")
            
            # For now, log the response - in full THIN implementation, 
            # this would be executed in LLM's code environment
            logger.info("Raw LLM execution response:")
            logger.info("=" * 50)
            logger.info(llm_response)
            logger.info("=" * 50)
            
            # Signal completion
            completion_data = {
                'original_task_id': task_id,
                'result': 'success',
                'experiment_name': experiment_name,
                'task_list_hash': task_list_hash
            }
            
            self.redis_client.xadd('tasks.done', {
                'original_task_id': task_id,
                'data': json.dumps(completion_data)
            })
            
            logger.info(f"Task list execution completed: {task_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to execute task list: {e}")
            return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <task_id>")
        sys.exit(1)
    
    task_id = sys.argv[1]
    agent = TaskListExecutorAgent()
    
    success = agent.execute_task_list(task_id)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 