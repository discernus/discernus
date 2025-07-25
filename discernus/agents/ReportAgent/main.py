#!/usr/bin/env python3
"""
ReportAgent - Human-Readable Report Generation Agent
====================================================

THIN Principle: LLM handles all report formatting and narrative synthesis.
Software provides minimal coordination for final output generation.

Alpha System Component: Generates human-readable markdown reports from
synthesis results for researchers and stakeholders.

Architecture: Final-stage agent that converts structured synthesis data
into accessible, well-formatted research reports.
"""

import json
import sys
import os
from typing import Dict, Any
from litellm import completion

# Import BaseAgent infrastructure
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'core'))
from base_agent import BaseAgent, BaseAgentError, main_agent_entry_point

# Add scripts directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))
from minio_client import get_artifact, put_artifact, ArtifactStorageError

class ReportAgentError(BaseAgentError):
    """Agent-specific exceptions"""
    pass

class ReportAgent(BaseAgent):
    """
    Final-stage agent for human-readable report generation.
    Converts structured synthesis results into accessible research reports.
    """
    
    def __init__(self):
        super().__init__('ReportAgent')
    
    def process_task(self, task_id: str) -> bool:
        """
        Process a report generation task:
        - Retrieve synthesis results and experiment metadata
        - Generate human-readable markdown report
        - Store final report for researchers
        """
        try:
            # Get the specific message by ID from Redis stream
            messages = self.redis_client.xrange('tasks', task_id, task_id, count=1)
            
            if not messages:
                self._log_error(f"Task not found: {task_id}")
                return False
                
            # Extract task data
            msg_id, fields = messages[0]
            task_data = json.loads(fields[b'data'])
            self._log_info(f"Processing report generation task: {task_id}")
            
            # Validate required fields
            required_fields = ['synthesis_hash', 'experiment_name']
            for field in required_fields:
                if field not in task_data:
                    raise ReportAgentError(f"Required field missing: {field}")
            
            synthesis_hash = task_data['synthesis_hash']
            experiment_name = task_data['experiment_name']
            model = task_data.get('model', 'vertex_ai/gemini-2.5-pro')
            
            self._log_info(f"Generating report for experiment: {experiment_name}")
            
            # Capture prompt DNA for provenance if run_folder provided
            if 'run_folder' in task_data:
                try:
                    prompt_hash = self.capture_prompt_dna(task_data['run_folder'])
                    self._log_info(f"Captured prompt DNA for run: {prompt_hash}")
                except Exception as e:
                    self._log_warning(f"Prompt DNA capture failed: {e}")
            
            # Strip sha256: prefix if present
            if synthesis_hash.startswith('sha256:'):
                synthesis_hash = synthesis_hash[7:]
            
            self._log_info(f"Retrieving synthesis results: {synthesis_hash[:12]}...")
            
            # Retrieve synthesis artifact
            synthesis_bytes = get_artifact(synthesis_hash)
            
            # THIN: Let LLM handle format detection and parsing
            try:
                synthesis_text = synthesis_bytes.decode('utf-8')
            except UnicodeDecodeError:
                synthesis_text = synthesis_bytes.decode('utf-8', errors='ignore')
            
            # Get additional context if available
            experiment_metadata = task_data.get('experiment_metadata', {})
            framework_name = experiment_metadata.get('framework_name', 'Unknown Framework')
            corpus_info = experiment_metadata.get('corpus_info', {})
            
            # Format prompt for report generation
            prompt_text = self.prompt_template.format(
                experiment_name=experiment_name,
                framework_name=framework_name,
                synthesis_results=synthesis_text,
                corpus_info=json.dumps(corpus_info, indent=2) if corpus_info else "No corpus information available"
            )
            
            # Call LLM for report generation
            self._log_info(f"Calling LLM ({model}) for report generation...")
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
            
            # Store result
            result_content = response.choices[0].message.content
            if not result_content or result_content.strip() == "":
                self._log_error(f"LLM returned empty response for report generation")
                return False
            
            # Create final report artifact with metadata
            report_artifact = {
                'final_report': result_content,
                'report_metadata': {
                    'experiment_name': experiment_name,
                    'framework_name': framework_name,
                    'synthesis_hash': synthesis_hash,
                    'model_used': model,
                    'agent_version': 'ReportAgent_v1.0_BaseAgent',
                    'prompt_dna': getattr(self, 'prompt_hash', 'unknown'),
                    'corpus_info': corpus_info
                }
            }
            
            result_hash = put_artifact(json.dumps(report_artifact, indent=2).encode('utf-8'))
            self._log_info(f"Report generation complete, final report stored: {result_hash}")
            
            # Also store the markdown report separately for easy access
            markdown_hash = put_artifact(result_content.encode('utf-8'))
            self._log_info(f"Markdown report stored separately: {markdown_hash}")
            
            # Signal completion using standardized pattern
            # Set status key with expiration
            self.redis_client.set(f"task:{task_id}:status", "done", ex=86400)
            
            # Store result hashes for easy retrieval
            self.redis_client.set(f"task:{task_id}:result_hash", result_hash, ex=86400)
            self.redis_client.set(f"task:{task_id}:markdown_hash", markdown_hash, ex=86400)
            
            # Signal completion to orchestrator
            run_id = task_data.get('run_id', task_id)
            self.redis_client.lpush(f"run:{run_id}:done", task_id)
            
            self._log_info(f"Report generation task completed: {task_id} (signaled to run:{run_id}:done)")
            return True
            
        except ArtifactStorageError as e:
            self._log_error(f"Artifact error processing task {task_id}: {e}")
            return False
        except Exception as e:
            self._log_error(f"Error processing report generation task {task_id}: {e}")
            return False

def main():
    """Agent entry point using BaseAgent infrastructure"""
    main_agent_entry_point(ReportAgent, 'ReportAgent')

if __name__ == '__main__':
    main() 