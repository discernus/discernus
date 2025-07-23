#!/usr/bin/env python3
"""
SynthesisAgent - Thin wrapper for synthesis of multiple analysis results
Reads Redis tasks, retrieves multiple analysis results, calls LLM with framework + analyses, stores final report.
"""

import redis
import json
import yaml
import sys
import os
import logging
from typing import Dict, Any, List
from litellm import completion

# Add scripts directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from minio_client import get_artifact, put_artifact, ArtifactStorageError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - SynthesisAgent - %(message)s')
logger = logging.getLogger(__name__)

# Redis configuration
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
CONSUMER_GROUP = 'discernus'

class SynthesisAgentError(Exception):
    """Agent-specific exceptions"""
    pass

class SynthesisAgent:
    """Thin agent for synthesis of multiple analysis results"""
    
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
            raise SynthesisAgentError(f"Prompt loading failed: {e}")
    
    def process_task(self, task_id: str) -> bool:
        """Process a single synthesis task - THIN implementation"""
        try:
            # Get the specific message by ID from Redis stream
            messages = self.redis_client.xrange('tasks', task_id, task_id, count=1)
            
            if not messages:
                logger.error(f"Task not found: {task_id}")
                return False
                
            # Extract task data
            msg_id, fields = messages[0]
            task_data = json.loads(fields[b'data'])
            logger.info(f"Processing synthesis task: {task_id}")
            
            # Get artifacts (no parsing - just retrieval)
            analysis_hashes = task_data['analysis_hashes']
            framework_hash = task_data['framework_hash']
            model = task_data.get('model', 'gemini-2.5-flash')
            
            # Strip sha256: prefix if present (orchestrator adds it, MinIO expects raw hash)
            if framework_hash.startswith('sha256:'):
                framework_hash = framework_hash[7:]
            
            clean_analysis_hashes = []
            for ah in analysis_hashes:
                if ah.startswith('sha256:'):
                    clean_analysis_hashes.append(ah[7:])
                else:
                    clean_analysis_hashes.append(ah)
            
            logger.info(f"Retrieving framework: {framework_hash[:12]}...")
            logger.info(f"Retrieving {len(clean_analysis_hashes)} analysis results...")
            
            # THIN: Get raw bytes, let LLM handle format detection
            framework_bytes = get_artifact(framework_hash)
            
            # Get all analysis results
            analysis_results = []
            for i, analysis_hash in enumerate(clean_analysis_hashes):
                logger.info(f"Retrieving analysis {i+1}/{len(clean_analysis_hashes)}: {analysis_hash[:12]}...")
                analysis_bytes = get_artifact(analysis_hash)
                
                # THIN: Pass raw bytes to LLM - no preprocessing/parsing
                # For PoC, decode for text-based prompting
                try:
                    analysis_text = analysis_bytes.decode('utf-8')
                    analysis_results.append(analysis_text)
                except UnicodeDecodeError:
                    analysis_text = analysis_bytes.decode('utf-8', errors='ignore')
                    analysis_results.append(f"[BINARY ANALYSIS: {len(analysis_bytes)} bytes - would be passed directly to multimodal LLM]")
            
            # THIN: Pass framework raw bytes to LLM - no preprocessing/parsing  
            try:
                framework_text = framework_bytes.decode('utf-8')
            except UnicodeDecodeError:
                framework_text = framework_bytes.decode('utf-8', errors='ignore')
            
            # Format prompt (THIN - minimal string substitution)
            combined_analyses = "\n\n".join([f"ANALYSIS {i+1}:\n{result}" for i, result in enumerate(analysis_results)])
            
            prompt_text = self.prompt_template.format(
                framework=framework_text,
                analyses=combined_analyses,
                analysis_count=len(analysis_results)
            )
            
            # Call LLM (thin wrapper)
            logger.info(f"Calling LLM ({model}) for synthesis of {len(analysis_results)} analyses...")
            response = completion(
                model=model,
                messages=[{"role": "user", "content": prompt_text}],
                temperature=0.0
            )
            
            # Store result (THIN - no processing/parsing)
            result_content = response.choices[0].message.content
            result_hash = put_artifact(result_content.encode('utf-8'))
            
            logger.info(f"Synthesis complete, final report stored: {result_hash}")
            
            # Signal completion to router
            completion_data = {
                'original_task_id': task_id,
                'result_hash': result_hash,
                'status': 'completed',
                'model_used': model,
                'analysis_hashes': analysis_hashes,
                'framework_hash': framework_hash,
                'type': 'synthesis_report'
            }
            
            self.redis_client.xadd('tasks.done', {
                'original_task_id': task_id,
                'data': json.dumps(completion_data)
            })
            
            logger.info(f"Synthesis task completed: {task_id}")
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
    agent = SynthesisAgent()
    
    try:
        success = agent.process_task(task_id)
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"Agent failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 