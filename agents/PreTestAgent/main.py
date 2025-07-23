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

            # 1. Get corpus sample and frameworks from task_data
            required_fields = ['experiment_name', 'framework_hashes', 'document_hashes', 'model']
            for field in required_fields:
                if field not in task_data:
                    raise PreTestAgentError(f"Required field missing: {field}")

            experiment_name = task_data['experiment_name']
            framework_hashes = task_data['framework_hashes']
            document_hashes = task_data['document_hashes']
            model = task_data.get('model', 'gemini-2.5-pro') # Pro for complex statistical reasoning

            logger.info(f"Pre-test for '{experiment_name}': sampling {len(document_hashes)} documents with {len(framework_hashes)} frameworks.")

            # Retrieve frameworks
            frameworks = self._get_artifacts_by_hash(framework_hashes, "framework")
            
            # Retrieve document sample
            documents = self._get_artifacts_by_hash(document_hashes, "document")

            # 2. Format prompt with sample data
            prompt_text = self.prompt_template.format(
                frameworks=self._format_artifacts_for_prompt(frameworks, "FRAMEWORK"),
                documents=self._format_artifacts_for_prompt(documents, "DOCUMENT SAMPLE")
            )

            # 3. Call LLM to perform variance analysis
            logger.info(f"Calling LLM ({model}) for pre-test variance analysis...")
            response = completion(
                model=model,
                messages=[{"role": "user", "content": prompt_text}],
                temperature=0.0
            )

            result_content = response.choices[0].message.content
            if not result_content or result_content.strip() == "":
                raise PreTestAgentError(f"LLM returned empty response for pre-test {task_id}")

            # 4. Store result artifact with `recommend_runs`
            try:
                llm_response_data = json.loads(result_content)
            except json.JSONDecodeError:
                raise PreTestAgentError(f"Failed to parse LLM JSON response for pre-test {task_id}")

            pretest_artifact = {
                'experiment_name': experiment_name,
                'task_id': task_id,
                'model_used': model,
                'recommendation': llm_response_data,
                'pretest_metadata': {
                    'num_frameworks_sampled': len(frameworks),
                    'num_documents_sampled': len(documents),
                    'agent_version': 'PreTestAgent_v1.0'
                }
            }

            result_hash = put_artifact(json.dumps(pretest_artifact, indent=2).encode('utf-8'))
            logger.info(f"Pre-test analysis complete, result stored: {result_hash}")

            # 5. Signal completion
            completion_data = {
                'original_task_id': task_id,
                'experiment_name': experiment_name,
                'result_hash': result_hash,
                'status': 'completed',
                'task_type': 'PreTest',
                'model_used': model
            }
            
            self.redis_client.xadd('tasks.done', {
                'original_task_id': task_id,
                'data': json.dumps(completion_data)
            })

            logger.info(f"PreTest task completed: {task_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error processing PreTest task {task_id}: {e}")
            return False

    def _get_artifacts_by_hash(self, hashes: List[str], artifact_type: str) -> List[Dict]:
        """Retrieve and decode a list of artifacts from storage."""
        artifacts = []
        for i, artifact_hash in enumerate(hashes):
            clean_hash = artifact_hash[7:] if artifact_hash.startswith('sha256:') else artifact_hash
            artifact_bytes = get_artifact(clean_hash)
            
            content, encoding = self._decode_artifact(artifact_bytes)
            
            artifacts.append({
                'index': i + 1,
                'hash': clean_hash,
                'content': content,
                'encoding': encoding
            })
            logger.info(f"Retrieved {artifact_type} {i+1} ({encoding}): {clean_hash[:12]}...")
        return artifacts

    def _decode_artifact(self, artifact_bytes: bytes) -> (str, str):
        """Applies the Text-First Fallback Principle."""
        try:
            return artifact_bytes.decode('utf-8'), 'text'
        except UnicodeDecodeError:
            return base64.b64encode(artifact_bytes).decode('utf-8'), 'base64'

    def _format_artifacts_for_prompt(self, artifacts: List[Dict], header: str) -> str:
        """Format a list of artifacts for the LLM prompt."""
        formatted = []
        for artifact in artifacts:
            formatted.append(f"=== {header} {artifact['index']} (encoding: {artifact['encoding']}) ===\n{artifact['content']}\n")
        return "\n".join(formatted)

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