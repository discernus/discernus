#!/usr/bin/env python3
"""
PreTestAgent - Variance Estimation Agent
========================================

THIN Principle: LLM handles statistical reasoning for variance estimation.
Software provides minimal coordination and data routing.

Architecture: A specialized agent called by the OrchestratorAgent before
the main analysis plan is generated.

- Input: A sample of a corpus and a set of frameworks.
- Process: Performs a small number of analysis runs on the sample to estimate
           scoring variance across documents.
- Output: A recommendation for the optimal number of runs (`recommend_runs`)
          needed to achieve statistical confidence.
"""

import redis
import json
import yaml
import sys
import os
import logging
from typing import Dict, Any, List
from litellm import completion
import base64

# Add scripts directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from minio_client import get_artifact, put_artifact, ArtifactStorageError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - PreTestAgent - %(message)s')
logger = logging.getLogger(__name__)

# Redis configuration
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = 6379
REDIS_DB = 0

class PreTestAgentError(Exception):
    """Agent-specific exceptions"""
    pass

class PreTestAgent:
    """
    Tier 1 agent for estimating variance and recommending run count.
    """
    
    def __init__(self):
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        self.prompt_template = self._load_prompt_template()
        
    def _load_prompt_template(self) -> str:
        """Load external prompt template."""
        try:
            prompt_path = os.path.join(os.path.dirname(__file__), 'prompt.yaml')
            with open(prompt_path, 'r') as f:
                prompt_data = yaml.safe_load(f)
            return prompt_data['template']
        except Exception as e:
            logger.error(f"Failed to load prompt template: {e}")
            raise PreTestAgentError(f"Prompt loading failed: {e}")
    
    def process_task(self, task_id: str) -> bool:
        """
        Process a single PreTest task.
        """
        try:
            messages = self.redis_client.xrange('tasks', task_id, task_id, count=1)
            
            if not messages:
                logger.error(f"Task not found: {task_id}")
                return False
                
            msg_id, fields = messages[0]
            task_data = json.loads(fields[b'data'])
            logger.info(f"Processing PreTest task: {task_id}")
            
            # TODO: Implement the full pre-test logic
            # 1. Get corpus sample and frameworks from task_data
            # 2. Format prompt with sample data
            # 3. Call LLM to perform variance analysis
            # 4. Store result artifact with `recommend_runs`
            # 5. Signal completion
            
            logger.info(f"PreTest task completed (stub): {task_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error processing PreTest task {task_id}: {e}")
            return False

def main():
    """Agent entry point"""
    if len(sys.argv) != 2:
        print("Usage: main.py <task_id>")
        sys.exit(1)
    
    task_id = sys.argv[1]
    agent = PreTestAgent()
    
    try:
        success = agent.process_task(task_id)
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"PreTestAgent failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 