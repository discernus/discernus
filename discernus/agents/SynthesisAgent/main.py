#!/usr/bin/env python3
"""
SynthesisAgent - Thin wrapper for synthesis of multiple analysis results
Reads Redis tasks, retrieves multiple analysis results, calls LLM with framework + analyses, stores final report.
"""

import json
import sys
import os
from typing import Dict, Any, List
from litellm import completion

# Import BaseAgent infrastructure
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'core'))
from base_agent import BaseAgent, BaseAgentError, main_agent_entry_point

from discernus.storage import get_artifact, put_artifact, ArtifactStorageError

class SynthesisAgentError(BaseAgentError):
    """Agent-specific exceptions"""
    pass

class SynthesisAgent(BaseAgent):
    """Thin agent for synthesis of multiple analysis results"""
    
    def __init__(self, agent_name: str = 'SynthesisAgent'):
        super().__init__(agent_name)
    
    def process_task(self, task_id: str) -> bool:
        """Process a single synthesis task - THIN implementation"""
        try:
            # Retrieve task data from Redis key (per architecture spec 4.2 - lists not streams)
            task_data_key = f"task:{task_id}:data"
            task_data_raw = self.redis_client.get(task_data_key)
            
            if not task_data_raw:
                self._log_error(f"Task data not found: {task_data_key}")
                return False
                
            # Extract task data
            task_data = json.loads(task_data_raw)
            self._log_info(f"Processing synthesis task: {task_id}")
            
            # Get artifacts (no parsing - just retrieval)
            analysis_hashes = task_data['analysis_hashes']
            framework_hash = task_data['framework_hash']
            model = task_data.get('model', 'vertex_ai/gemini-2.5-pro')  # Use Pro for synthesis by default
            
            # Capture prompt DNA for provenance if run_folder provided
            if 'run_folder' in task_data:
                try:
                    prompt_hash = self.capture_prompt_dna(task_data['run_folder'])
                    self._log_info(f"Captured prompt DNA for run: {prompt_hash}")
                except Exception as e:
                    self._log_warning(f"Prompt DNA capture failed: {e}")
            
            # Strip sha256: prefix if present (orchestrator adds it, MinIO expects raw hash)
            if framework_hash.startswith('sha256:'):
                framework_hash = framework_hash[7:]
            
            clean_analysis_hashes = []
            for ah in analysis_hashes:
                if ah.startswith('sha256:'):
                    clean_analysis_hashes.append(ah[7:])
                else:
                    clean_analysis_hashes.append(ah)
            
            self._log_info(f"Retrieving framework: {framework_hash[:12]}...")
            self._log_info(f"Retrieving {len(clean_analysis_hashes)} analysis results...")
            
            # THIN: Get raw bytes, let LLM handle format detection
            framework_bytes = get_artifact(framework_hash)
            
            # Get all analysis results
            analysis_results = []
            for i, analysis_hash in enumerate(clean_analysis_hashes):
                self._log_info(f"Retrieving analysis {i+1}/{len(clean_analysis_hashes)}: {analysis_hash[:12]}...")
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
            
            # Call LLM (thin wrapper) with safety settings for political content
            self._log_info(f"Calling LLM ({model}) for synthesis of {len(analysis_results)} analyses...")
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
            
            # Store result (THIN - no processing/parsing)
            result_content = response.choices[0].message.content
            if not result_content or result_content.strip() == "":
                self._log_error(f"LLM returned empty response for synthesis task")
                return False
            
            # Create enhanced synthesis artifact with metadata
            synthesis_artifact = {
                'synthesis_result': result_content,
                'synthesis_metadata': {
                    'model_used': model,
                    'analysis_hashes': analysis_hashes,
                    'framework_hash': framework_hash,
                    'agent_version': 'SynthesisAgent_v2.0_BaseAgent',
                    'prompt_dna': getattr(self, 'prompt_hash', 'unknown'),
                    'analysis_count': len(analysis_results)
                }
            }
            
            result_hash = put_artifact(json.dumps(synthesis_artifact, indent=2).encode('utf-8'))
            self._log_info(f"Synthesis complete, final report stored: {result_hash}")
            
            # Signal completion using standardized pattern
            # Set status key with expiration
            self.redis_client.set(f"task:{task_id}:status", "done", ex=86400)
            
            # Store result hash for easy retrieval
            self.redis_client.set(f"task:{task_id}:result_hash", result_hash, ex=86400)
            
            # Signal completion to orchestrator
            run_id = task_data.get('run_id', task_id)
            self.redis_client.lpush(f"run:{run_id}:done", task_id)
            
            self._log_info(f"Synthesis task completed: {task_id} (signaled to run:{run_id}:done)")
            return True
            
        except ArtifactStorageError as e:
            self._log_error(f"Artifact error processing task {task_id}: {e}")
            return False
        except Exception as e:
            self._log_error(f"Error processing task {task_id}: {e}")
            return False

def main():
    """Agent entry point using BaseAgent infrastructure"""
    main_agent_entry_point(SynthesisAgent, 'SynthesisAgent')

if __name__ == '__main__':
    main() 