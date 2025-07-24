#!/usr/bin/env python3
"""
AnalyseBatchAgent - Multi-Document Batch Analysis Agent
=======================================================

THIN Principle: LLM handles all framework interpretation and multi-document analysis.
Software provides minimal Redis/MinIO coordination only.

Based on empirical validation:
- Gemini 2.5 Flash successfully processed 9 speeches + complex CAF framework
- Context window: Up to 341 speeches per batch (empirically validated)
- Output: STRUCTURED DATA ONLY - no qualitative synthesis
- Architecture: Layer 1 agent in deterministic 3-layer synthesis pipeline
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
logging.basicConfig(level=logging.INFO, format='%(asctime)s - AnalyseBatchAgent - %(message)s')
logger = logging.getLogger(__name__)

# Redis configuration
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = 6379
REDIS_DB = 0
CONSUMER_GROUP = 'discernus'

class AnalyseBatchAgentError(Exception):
    """Agent-specific exceptions"""
    pass

class AnalyseBatchAgent:
    """
    Tier 1 agent for multi-document, multi-framework batch analysis.
    Produces STRUCTURED DATA ONLY - no qualitative synthesis.
    """
    
    def __init__(self):
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        self.prompt_template = self._load_prompt_template()
        
    def _load_prompt_template(self) -> str:
        """Load external prompt template - THIN approach"""
        try:
            prompt_path = os.path.join(os.path.dirname(__file__), 'prompt.yaml')
            with open(prompt_path, 'r') as f:
                prompt_data = yaml.safe_load(f)
            return prompt_data['template']
        except Exception as e:
            logger.error(f"Failed to load prompt template: {e}")
            raise AnalyseBatchAgentError(f"Prompt loading failed: {e}")
    
    def process_task(self, task_id: str) -> bool:
        """
        Process a single AnalyseBatch task following Layer 1 principles:
        - Retrieve multiple documents and frameworks
        - Apply frameworks to all documents in single LLM call
        - Output STRUCTURED DATA ONLY (no synthesis)
        """
        try:
            # Get the specific message by ID from Redis stream
            messages = self.redis_client.xrange('tasks', task_id, task_id, count=1)
            
            if not messages:
                logger.error(f"Task not found: {task_id}")
                return False
                
            # Extract task data
            msg_id, fields = messages[0]
            task_data = json.loads(fields[b'data'])
            logger.info(f"Processing AnalyseBatch task: {task_id}")
            
            # Validate required fields
            required_fields = ['batch_id', 'framework_hashes', 'document_hashes', 'model']
            for field in required_fields:
                if field not in task_data:
                    raise AnalyseBatchAgentError(f"Required field missing: {field}")
            
            batch_id = task_data['batch_id']
            framework_hashes = task_data['framework_hashes']
            document_hashes = task_data['document_hashes']
            model = task_data.get('model', 'gemini-2.5-pro')
            
            logger.info(f"Batch {batch_id}: Processing {len(document_hashes)} documents with {len(framework_hashes)} frameworks")
            
            # Retrieve framework artifacts
            frameworks = []
            for i, framework_hash in enumerate(framework_hashes):
                # Strip sha256: prefix if present
                clean_hash = framework_hash[7:] if framework_hash.startswith('sha256:') else framework_hash
                framework_bytes = get_artifact(clean_hash)
                # Binary-First Principle: Frameworks also as base64
                framework_content = base64.b64encode(framework_bytes).decode('utf-8')
                frameworks.append({
                    'index': i + 1,
                    'hash': clean_hash,
                    'content': framework_content
                })
                logger.info(f"Retrieved framework {i+1}: {clean_hash[:12]}...")
            
            # Retrieve document artifacts  
            documents = []
            for i, doc_hash in enumerate(document_hashes):
                # Strip sha256: prefix if present
                clean_hash = doc_hash[7:] if doc_hash.startswith('sha256:') else doc_hash
                doc_bytes = get_artifact(clean_hash)
                
                # Binary-First Principle: All content as base64, LLM handles decoding
                doc_content = base64.b64encode(doc_bytes).decode('utf-8')
                doc_encoding = 'base64'
                logger.info(f"Retrieved and encoded document {i+1} as base64: {clean_hash[:12]}... ({len(doc_bytes)} bytes)")

                documents.append({
                    'index': i + 1,
                    'hash': clean_hash,
                    'content': doc_content,
                    'encoding': doc_encoding,
                    'size_bytes': len(doc_bytes)
                })

            # Format prompt for batch analysis (THIN - minimal string substitution)
            prompt_text = self.prompt_template.format(
                batch_id=batch_id,
                frameworks=self._format_frameworks_for_prompt(frameworks),
                documents=self._format_documents_for_prompt(documents),
                num_frameworks=len(frameworks),
                num_documents=len(documents)
            )
            
            # Call LLM with safety settings for political content
            logger.info(f"Calling LLM ({model}) for batch analysis...")
            response = completion(
                model=model,
                messages=[{"role": "user", "content": prompt_text}],
                temperature=0.0,
                safety_settings=[
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
                ]
            )
            
            # Store result - let the LLM return natural mixed content
            result_content = response.choices[0].message.content
            if not result_content or result_content.strip() == "":
                logger.error(f"LLM returned empty response for batch {batch_id}")
                return False
            
            # Create structured artifact with the LLM's natural response
            # The LLM can return mixed markdown/JSON/text - downstream agents handle this naturally
            batch_artifact = {
                'batch_id': batch_id,
                'experiment_name': task_data.get('experiment_name', 'unknown'),
                'model_used': model,
                'analysis_results': result_content,  # Raw LLM response
                'batch_metadata': {
                    'num_frameworks': len(frameworks),
                    'num_documents': len(documents),
                    'framework_hashes': framework_hashes,
                    'document_hashes': document_hashes,
                    'agent_version': 'AnalyseBatchAgent_v1.0'
                }
            }
            
            result_hash = put_artifact(json.dumps(batch_artifact, indent=2).encode('utf-8'))
            logger.info(f"Batch analysis complete, result stored: {result_hash}")
            
            # Signal completion using architect-specified Redis keys/lists pattern
            # Set status key with expiration
            self.redis_client.set(f"task:{task_id}:status", "done", ex=86400)
            
            # Store result hash for easy retrieval
            self.redis_client.set(f"task:{task_id}:result_hash", result_hash, ex=86400)
            
            # Signal completion to orchestrator
            run_id = task_data.get('run_id', task_id)
            self.redis_client.lpush(f"run:{run_id}:done", task_id)
            
            logger.info(f"AnalyseBatch task completed: {task_id} (signaled to run:{run_id}:done)")
            return True
            
        except ArtifactStorageError as e:
            logger.error(f"Artifact error processing task {task_id}: {e}")
            return False
        except Exception as e:
            logger.error(f"Error processing AnalyseBatch task {task_id}: {e}")
            return False
    
    def _format_frameworks_for_prompt(self, frameworks: List[Dict]) -> str:
        """Format frameworks for LLM prompt"""
        formatted = []
        for framework in frameworks:
            formatted.append(f"=== FRAMEWORK {framework['index']} (base64 encoded) ===\n{framework['content']}\n")
        return "\n".join(formatted)
    
    def _format_documents_for_prompt(self, documents: List[Dict]) -> str:
        """Format documents for LLM prompt"""
        formatted = []
        for document in documents:
            formatted.append(f"=== DOCUMENT {document['index']} (base64 encoded) ===\n{document['content']}\n")
        return "\n".join(formatted)
    
    def _get_timestamp(self) -> str:
        """Get ISO timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()

def main():
    """Agent entry point"""
    if len(sys.argv) != 2:
        print("Usage: main.py <task_id>")
        sys.exit(1)
    
    task_id = sys.argv[1]
    agent = AnalyseBatchAgent()
    
    try:
        success = agent.process_task(task_id)
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"AnalyseBatchAgent failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()