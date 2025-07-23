#!/usr/bin/env python3
"""
PlanExecutorAgent - Thin wrapper for executing orchestration plans
Reads Redis tasks, calls LLM to interpret raw plans, creates individual tasks.
"""

import redis
import json
import yaml
import sys
import os
import logging
import hashlib
import io
from typing import Dict, Any
from litellm import completion
from minio import Minio

# Add scripts directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from minio_client import get_artifact, put_artifact, ArtifactStorageError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - PlanExecutorAgent - %(message)s')
logger = logging.getLogger(__name__)

# Redis configuration
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = 6379
REDIS_DB = 0
CONSUMER_GROUP = 'discernus'

class PlanExecutorAgentError(Exception):
    """Agent-specific exceptions"""
    pass

class PlanExecutorAgent:
    """Thin agent for interpreting raw orchestration plans using external prompts"""
    
    def __init__(self):
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        self.prompt_template = self._load_prompt_template()
        
        # MinIO connection for artifact storage
        minio_host = os.getenv('MINIO_HOST', 'localhost')
        self.minio_client = Minio(
            f"{minio_host}:9000",
            access_key=os.getenv('MINIO_ACCESS_KEY', 'minioadmin'),
            secret_key=os.getenv('MINIO_SECRET_KEY', 'minioadmin'),
            secure=False
        )
        
    def _load_prompt_template(self) -> str:
        """Load external prompt template - NO PARSING, just string formatting"""
        try:
            prompt_path = os.path.join(os.path.dirname(__file__), 'prompt.yaml')
            with open(prompt_path, 'r') as f:
                prompt_data = yaml.safe_load(f)
            return prompt_data['template']
        except Exception as e:
            logger.error(f"Failed to load prompt template: {e}")
            raise PlanExecutorAgentError(f"Prompt loading failed: {e}")

    def execute_plan(self, task_id: str) -> bool:
        """Execute one plan interpretation task"""
        try:
            # Read the specific task from Redis
            messages = self.redis_client.xrange('tasks', task_id, task_id, count=1)
            if not messages:
                logger.error(f"Task not found: {task_id}")
                return False
                
            task_fields = messages[0][1]
            task_data = json.loads(task_fields[b'data'])
            
            plan_hash = task_data['plan_hash']
            experiment_name = task_data.get('experiment_name', 'unknown')
            
            logger.info(f"Processing plan execution for experiment: {experiment_name}")
            logger.info(f"Plan hash: {plan_hash[:12]}...")
            
            # Get the raw orchestration plan from MinIO
            logger.info("Retrieving raw orchestration plan...")
            raw_plan_data = get_artifact(plan_hash)
            plan_content = json.loads(raw_plan_data.decode('utf-8'))
            
            raw_llm_plan = plan_content['raw_llm_plan']
            framework_hash = plan_content['framework_hash']
            corpus_hashes = plan_content['corpus_hashes']
            
            logger.info(f"Retrieved plan with {len(raw_llm_plan)} characters")
            
            # Format prompt (THIN - minimal string substitution)  
            prompt_text = self.prompt_template.format(
                raw_plan=raw_llm_plan,
                framework_hash=framework_hash,
                corpus_hashes=json.dumps(corpus_hashes, indent=2)
            )
            
            # Call LLM (thin wrapper) with safety settings for political content
            logger.info("Calling LLM to interpret orchestration plan...")
            response = completion(
                model="gemini-2.5-flash",
                messages=[{"role": "user", "content": prompt_text}],
                temperature=0.0,
                safety_settings=[
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
                ]
            )
            
            # Get raw LLM response (THIN - no parsing, store as-is)
            llm_response = response.choices[0].message.content
            if not llm_response or llm_response.strip() == "":
                logger.error(f"LLM returned empty response for plan execution")
                return False
            
            logger.info(f"LLM interpreted plan into {len(llm_response)} character response")
            
            # Store raw LLM task interpretation (THIN - no parsing)
            task_list_hash = hashlib.sha256(llm_response.encode()).hexdigest()
            task_list_key = f"task_lists/{task_list_hash}"
            
            logger.info(f"Storing raw task list interpretation: {task_list_hash[:12]}...")
            self.minio_client.put_object(
                "discernus-artifacts",
                task_list_key,
                io.BytesIO(llm_response.encode()),
                length=len(llm_response.encode())
            )
            
            # Enqueue single task for downstream LLM agent to interpret
            message_id = self.redis_client.xadd('tasks', {
                'type': 'execute_task_list',
                'data': json.dumps({
                    'task_list_hash': task_list_hash,
                    'experiment_name': experiment_name,
                    'original_plan_hash': plan_hash
                })
            })
            
            logger.info(f"Enqueued task list execution: {message_id}")
            enqueued_count = 1
            
            # Signal completion to router
            completion_data = {
                'original_task_id': task_id,
                'result': 'success',
                'tasks_created': enqueued_count,
                'experiment_name': experiment_name
            }
            
            self.redis_client.xadd('tasks.done', {
                'original_task_id': task_id,
                'data': json.dumps(completion_data)
            })
            
            logger.info(f"Plan execution task completed: {task_id}")
            return True
            
        except Exception as e:
            logger.error(f"Plan execution failed: {e}")
            import traceback
            traceback.print_exc()
            return False

def main():
    """Main entry point for plan executor agent"""
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <task_id>")
        sys.exit(1)
        
    task_id = sys.argv[1]
    
    try:
        agent = PlanExecutorAgent()
        success = agent.execute_plan(task_id)
        sys.exit(0 if success else 1)
        
    except Exception as e:
        logger.error(f"Agent failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 