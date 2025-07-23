#!/usr/bin/env python3
"""
AnalyseChunkAgent - Thin wrapper for text analysis
Reads Redis tasks, calls LLM with framework + chunk, stores results.
"""

import redis
import json
import yaml
import sys
import os
import logging
from typing import Dict, Any
from litellm import completion

# Add scripts directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from minio_client import get_artifact, put_artifact, ArtifactStorageError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - AnalyseChunkAgent - %(message)s')
logger = logging.getLogger(__name__)

# Redis configuration
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
CONSUMER_GROUP = 'discernus'

class AnalyseChunkAgentError(Exception):
    """Agent-specific exceptions"""
    pass

class AnalyseChunkAgent:
    """Thin agent for chunk analysis using external prompts"""
    
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
            raise AnalyseChunkAgentError(f"Prompt loading failed: {e}")
    
    def process_task(self, task_id: str) -> bool:
        """Process a single analysis task - THIN implementation"""
        try:
            # Get task from Redis stream
            messages = self.redis_client.xread({'tasks': task_id}, count=1)
            
            if not messages:
                logger.error(f"Task not found: {task_id}")
                return False
                
            # Extract task data
            stream, msgs = messages[0]
            msg_id, fields = msgs[0]
            
            task_data = json.loads(fields[b'data'])
            logger.info(f"Processing task: {task_id}")
            
            # Get artifacts (no parsing - just retrieval)
            chunk_hash = task_data['chunk_hash']
            framework_hash = task_data['framework_hash']
            model = task_data.get('model', 'gpt-4o-mini')
            
            logger.info(f"Retrieving artifacts: chunk={chunk_hash[:12]}..., framework={framework_hash[:12]}...")
            
            chunk_text = get_artifact(chunk_hash)
            framework_text = get_artifact(framework_hash)
            
            # Format prompt (THIN - just string substitution)
            prompt_text = self.prompt_template.format(
                framework=framework_text,
                chunk=chunk_text
            )
            
            # Call LLM (thin wrapper)
            logger.info(f"Calling LLM ({model}) for analysis...")
            response = completion(
                model=model,
                messages=[{"role": "user", "content": prompt_text}],
                temperature=0.0
            )
            
            # Store result (no processing/parsing)
            result_content = response.choices[0].message.content
            result_hash = put_artifact(result_content)
            
            logger.info(f"Analysis complete, result stored: {result_hash}")
            
            # Signal completion to router
            completion_data = {
                'original_task_id': task_id,
                'result_hash': result_hash,
                'status': 'completed',
                'model_used': model,
                'chunk_hash': chunk_hash,
                'framework_hash': framework_hash
            }
            
            self.redis_client.xadd('tasks.done', {
                'original_task_id': task_id,
                'data': json.dumps(completion_data)
            })
            
            logger.info(f"Task completed: {task_id}")
            return True
            
        except ArtifactStorageError as e:
            logger.error(f"Artifact error processing task {task_id}: {e}")
            return False
        except Exception as e:
            logger.error(f"Error processing task {task_id}: {e}")
            return False

def main():
    """Agent entry point"""
    if len(sys.argv) != 2:
        print("Usage: main.py <task_id>")
        sys.exit(1)
    
    task_id = sys.argv[1]
    agent = AnalyseChunkAgent()
    
    try:
        success = agent.process_task(task_id)
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"Agent failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 