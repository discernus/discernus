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
            model = task_data.get('model', 'gemini-2.5-flash')
            
            logger.info(f"Batch {batch_id}: Processing {len(document_hashes)} documents with {len(framework_hashes)} frameworks")
            
            # Retrieve framework artifacts
            frameworks = []
            for i, framework_hash in enumerate(framework_hashes):
                # Strip sha256: prefix if present
                clean_hash = framework_hash[7:] if framework_hash.startswith('sha256:') else framework_hash
                framework_bytes = get_artifact(clean_hash)
                framework_text = framework_bytes.decode('utf-8')
                frameworks.append({
                    'index': i + 1,
                    'hash': clean_hash,
                    'content': framework_text
                })
                logger.info(f"Retrieved framework {i+1}: {clean_hash[:12]}...")
            
            # Retrieve document artifacts  
            documents = []
            for i, doc_hash in enumerate(document_hashes):
                # Strip sha256: prefix if present
                clean_hash = doc_hash[7:] if doc_hash.startswith('sha256:') else doc_hash
                doc_bytes = get_artifact(clean_hash)
                
                # Provisional: Text-First Fallback Principle
                try:
                    # Attempt to decode as text first for efficiency
                    doc_content = doc_bytes.decode('utf-8')
                    doc_encoding = 'text'
                    logger.info(f"Retrieved document {i+1} as text: {clean_hash[:12]}... ({len(doc_bytes)} bytes)")
                except UnicodeDecodeError:
                    # Fallback to base64 for binary files
                    doc_content = base64.b64encode(doc_bytes).decode('utf-8')
                    doc_encoding = 'base64'
                    logger.info(f"Retrieved and encoded document {i+1} as binary: {clean_hash[:12]}... ({len(doc_bytes)} bytes)")

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
            
            # Store result, parsing the LLM's response to create the explicit contract
            result_content = response.choices[0].message.content
            if not result_content or result_content.strip() == "":
                logger.error(f"LLM returned empty response for batch {batch_id}")
                return False
            
            # THICK Anti-Pattern Fix: The agent that receives the LLM response is
            # responsible for parsing it and creating the clean, structured artifact.
            # This prevents downstream agents from having to make assumptions.
            try:
                # The LLM is instructed to return a JSON object as a string.
                # We parse it here to create the final structured data.
                llm_response_data = json.loads(result_content)
                analysis_results = llm_response_data.get('analysis_results', [])
            except json.JSONDecodeError:
                logger.error(f"Failed to parse LLM JSON response for batch {batch_id}")
                # As a fallback, store the raw response for debugging
                analysis_results = {"error": "Failed to parse LLM response", "raw_response": result_content}

            # Create structured batch analysis artifact
            batch_analysis_artifact = {
                'batch_id': batch_id,
                'task_id': task_id,
                'model_used': model,
                'framework_hashes': framework_hashes,
                'document_hashes': document_hashes,
                'analysis_timestamp': self._get_timestamp(),
                'analysis_results': analysis_results, # Explicit, structured data
                'raw_llm_response': result_content, # Retained for debugging
                'batch_metadata': {
                    'num_frameworks': len(frameworks),
                    'num_documents': len(documents),
                    'total_document_bytes': sum(doc['size_bytes'] for doc in documents),
                    'agent_version': 'AnalyseBatchAgent_v1.0'
                }
            }
            
            result_hash = put_artifact(json.dumps(batch_analysis_artifact, indent=2).encode('utf-8'))
            logger.info(f"Batch analysis complete, result stored: {result_hash}")
            
            # Signal completion to router
            completion_data = {
                'original_task_id': task_id,
                'batch_id': batch_id,
                'result_hash': result_hash,
                'status': 'completed',
                'task_type': 'AnalyseBatch',
                'model_used': model,
                'next_layer': 'CorpusSynthesis'  # Indicate Layer 2 dependency
            }
            
            self.redis_client.xadd('tasks.done', {
                'original_task_id': task_id,
                'data': json.dumps(completion_data)
            })
            
            logger.info(f"AnalyseBatch task completed: {task_id}")
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
            formatted.append(f"=== FRAMEWORK {framework['index']} ===\n{framework['content']}\n")
        return "\n".join(formatted)
    
    def _format_documents_for_prompt(self, documents: List[Dict]) -> str:
        """Format documents for LLM prompt"""
        formatted = []
        for document in documents:
            formatted.append(f"=== DOCUMENT {document['index']} (encoding: {document['encoding']}) ===\n{document['content']}\n")
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