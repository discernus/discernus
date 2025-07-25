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

import json
import sys
import os
from typing import Dict, Any, List
from litellm import completion
import base64

# Import BaseAgent infrastructure
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'core'))
from base_agent import BaseAgent, BaseAgentError, main_agent_entry_point

from discernus.storage import get_artifact, put_artifact, ArtifactStorageError

class AnalyseBatchAgentError(BaseAgentError):
    """Agent-specific exceptions"""
    pass

class AnalyseBatchAgent(BaseAgent):
    """
    Tier 1 agent for multi-document, multi-framework batch analysis.
    Produces STRUCTURED DATA ONLY - no qualitative synthesis.
    """
    
    def __init__(self, agent_name: str = 'AnalyseBatchAgent'):
        super().__init__(agent_name)
    
    def process_task(self, task_id: str) -> bool:
        """
        Process a single AnalyseBatch task following Layer 1 principles:
        - Retrieve multiple documents and frameworks
        - Apply frameworks to all documents in single LLM call
        - Output STRUCTURED DATA ONLY (no synthesis)
        """
        try:
            # Retrieve task data from Redis key (per architecture spec 4.2 - lists not streams)
            task_data_key = f"task:{task_id}:data"
            task_data_raw = self.redis_client.get(task_data_key)
            
            if not task_data_raw:
                self._log_error(f"Task data not found: {task_data_key}")
                return False
                
            # Extract task data
            task_data = json.loads(task_data_raw)
            self._log_info(f"Processing AnalyseBatch task: {task_id}")
            
            # Validate required fields
            required_fields = ['batch_id', 'framework_hashes', 'document_hashes', 'model']
            for field in required_fields:
                if field not in task_data:
                    raise AnalyseBatchAgentError(f"Required field missing: {field}")
            
            batch_id = task_data['batch_id']
            framework_hashes = task_data['framework_hashes']
            document_hashes = task_data['document_hashes']
            model = task_data.get('model', 'vertex_ai/gemini-2.5-pro')
            
            self._log_info(f"Batch {batch_id}: Processing {len(document_hashes)} documents with {len(framework_hashes)} frameworks")
            
            # Capture prompt DNA for provenance if run_folder provided
            if 'run_folder' in task_data:
                try:
                    prompt_hash = self.capture_prompt_dna(task_data['run_folder'])
                    self._log_info(f"Captured prompt DNA for run: {prompt_hash}")
                except Exception as e:
                    self._log_warning(f"Prompt DNA capture failed: {e}")
            
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
                self._log_info(f"Retrieved framework {i+1}: {clean_hash[:12]}...")
            
            # Retrieve document artifacts  
            documents = []
            for i, doc_hash in enumerate(document_hashes):
                # Strip sha256: prefix if present
                clean_hash = doc_hash[7:] if doc_hash.startswith('sha256:') else doc_hash
                doc_bytes = get_artifact(clean_hash)
                
                # Binary-First Principle: All content as base64, LLM handles decoding
                doc_content = base64.b64encode(doc_bytes).decode('utf-8')
                doc_encoding = 'base64'
                self._log_info(f"Retrieved and encoded document {i+1} as base64: {clean_hash[:12]}... ({len(doc_bytes)} bytes)")

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
            self._log_info(f"Calling LLM ({model}) for batch analysis...")
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
                self._log_error(f"LLM returned empty response for batch {batch_id}")
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
                    'agent_version': 'AnalyseBatchAgent_v2.0_BaseAgent',
                    'prompt_dna': getattr(self, 'prompt_hash', 'unknown')
                }
            }
            
            result_hash = put_artifact(json.dumps(batch_artifact, indent=2).encode('utf-8'))
            self._log_info(f"Batch analysis complete, result stored: {result_hash}")
            
            # Signal completion using architect-specified Redis keys/lists pattern
            # Set status key with expiration
            self.redis_client.set(f"task:{task_id}:status", "done", ex=86400)
            
            # Store result hash for easy retrieval
            self.redis_client.set(f"task:{task_id}:result_hash", result_hash, ex=86400)
            
            # Signal completion to orchestrator
            run_id = task_data.get('run_id', task_id)
            self.redis_client.lpush(f"run:{run_id}:done", task_id)
            
            self._log_info(f"AnalyseBatch task completed: {task_id} (signaled to run:{run_id}:done)")
            return True
            
        except ArtifactStorageError as e:
            self._log_error(f"Artifact error processing task {task_id}: {e}")
            return False
        except Exception as e:
            self._log_error(f"Error processing AnalyseBatch task {task_id}: {e}")
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

def main():
    """Agent entry point using BaseAgent infrastructure"""
    main_agent_entry_point(AnalyseBatchAgent, 'AnalyseBatchAgent')

if __name__ == '__main__':
    main()