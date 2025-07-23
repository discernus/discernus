#!/usr/bin/env python3
"""
CorpusSynthesisAgent - Deterministic Statistical Aggregation Agent
==================================================================

THIN Principle: LLM handles statistical reasoning and mathematical computation.
Software provides minimal Redis/MinIO coordination only.

Architecture: Layer 2 agent in deterministic 3-layer synthesis pipeline
- Input: Structured data from multiple AnalyseBatch results
- Process: Deterministic mathematical aggregation
- Output: Statistical report ONLY (no qualitative narrative)
- Model: Cost-optimized (claude-3-haiku) for computational tasks
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
logging.basicConfig(level=logging.INFO, format='%(asctime)s - CorpusSynthesisAgent - %(message)s')
logger = logging.getLogger(__name__)

# Redis configuration
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = 6379
REDIS_DB = 0
CONSUMER_GROUP = 'discernus'

class CorpusSynthesisAgentError(Exception):
    """Agent-specific exceptions"""
    pass

class CorpusSynthesisAgent:
    """
    Tier 2 agent for deterministic mathematical aggregation of batch analysis results.
    Produces STATISTICAL REPORTS ONLY - no qualitative interpretation.
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
            raise CorpusSynthesisAgentError(f"Prompt loading failed: {e}")
    
    def process_task(self, task_id: str) -> bool:
        """
        Process a single CorpusSynthesis task following Layer 2 principles:
        - Retrieve multiple batch analysis results
        - Perform deterministic mathematical aggregation
        - Output STATISTICAL REPORT ONLY (no interpretation)
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
            logger.info(f"Processing CorpusSynthesis task: {task_id}")
            
            # Validate required fields
            required_fields = ['experiment_name', 'batch_result_hashes']
            for field in required_fields:
                if field not in task_data:
                    raise CorpusSynthesisAgentError(f"Required field missing: {field}")
            
            experiment_name = task_data['experiment_name']
            batch_result_hashes = task_data['batch_result_hashes']
            model = task_data.get('model', 'claude-3-haiku')  # Cost-optimized for stats
            
            logger.info(f"Experiment '{experiment_name}': Aggregating {len(batch_result_hashes)} batch results")
            
            # Retrieve all batch analysis artifacts
            batch_analyses = []
            total_documents = 0
            total_frameworks = 0
            
            for i, batch_hash in enumerate(batch_result_hashes):
                # Strip sha256: prefix if present
                clean_hash = batch_hash[7:] if batch_hash.startswith('sha256:') else batch_hash
                batch_bytes = get_artifact(clean_hash)
                batch_data = json.loads(batch_bytes.decode('utf-8'))
                
                # Validate batch analysis structure
                if 'analysis_results' not in batch_data:
                    raise CorpusSynthesisAgentError(f"Invalid batch analysis structure in {clean_hash}")
                
                batch_analyses.append({
                    'batch_index': i + 1,
                    'batch_id': batch_data.get('batch_id', f'batch_{i+1}'),
                    'hash': clean_hash,
                    'data': batch_data
                })
                
                # Count documents and frameworks for validation
                if 'analysis_results' in batch_data:
                    total_documents += len(batch_data['analysis_results'])
                if 'batch_metadata' in batch_data:
                    frameworks_in_batch = batch_data['batch_metadata'].get('num_frameworks', 0)
                    if total_frameworks == 0:
                        total_frameworks = frameworks_in_batch
                    elif total_frameworks != frameworks_in_batch:
                        logger.warning(f"Framework count mismatch: expected {total_frameworks}, got {frameworks_in_batch}")
                
                logger.info(f"Retrieved batch {i+1}: {clean_hash[:12]}... ({len(batch_data['analysis_results'])} documents)")
            
            # Format prompt for statistical aggregation (THIN - minimal string substitution)
            prompt_text = self.prompt_template.format(
                experiment_name=experiment_name,
                batch_analyses=self._format_batch_analyses_for_prompt(batch_analyses),
                num_batches=len(batch_analyses),
                total_documents=total_documents,
                total_frameworks=total_frameworks
            )
            
            # Call LLM for statistical computation
            logger.info(f"Calling LLM ({model}) for corpus-level statistical aggregation...")
            response = completion(
                model=model,
                messages=[{"role": "user", "content": prompt_text}],
                temperature=0.0  # Deterministic for mathematical calculations
            )
            
            # Store result (THIN - no processing/parsing of LLM response)
            result_content = response.choices[0].message.content
            if not result_content or result_content.strip() == "":
                logger.error(f"LLM returned empty response for experiment {experiment_name}")
                return False
            
            # Create structured corpus synthesis artifact
            corpus_synthesis_artifact = {
                'experiment_name': experiment_name,
                'task_id': task_id,
                'model_used': model,
                'batch_result_hashes': batch_result_hashes,
                'synthesis_timestamp': self._get_timestamp(),
                'raw_llm_statistical_report': result_content,
                'aggregation_metadata': {
                    'num_batches_processed': len(batch_analyses),
                    'total_documents_analyzed': total_documents,
                    'total_frameworks_applied': total_frameworks,
                    'agent_version': 'CorpusSynthesisAgent_v1.0',
                    'statistical_approach': 'deterministic_mathematical_aggregation'
                }
            }
            
            result_hash = put_artifact(json.dumps(corpus_synthesis_artifact, indent=2).encode('utf-8'))
            logger.info(f"Corpus synthesis complete, statistical report stored: {result_hash}")
            
            # Signal completion to router
            completion_data = {
                'original_task_id': task_id,
                'experiment_name': experiment_name,
                'result_hash': result_hash,
                'status': 'completed',
                'task_type': 'CorpusSynthesis',
                'model_used': model,
                'next_layer': 'QualityAssurance'  # Indicate Layer 3 dependency
            }
            
            self.redis_client.xadd('tasks.done', {
                'original_task_id': task_id,
                'data': json.dumps(completion_data)
            })
            
            logger.info(f"CorpusSynthesis task completed: {task_id}")
            return True
            
        except ArtifactStorageError as e:
            logger.error(f"Artifact error processing task {task_id}: {e}")
            return False
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error in batch analysis: {e}")
            return False
        except Exception as e:
            logger.error(f"Error processing CorpusSynthesis task {task_id}: {e}")
            return False
    
    def _format_batch_analyses_for_prompt(self, batch_analyses: List[Dict]) -> str:
        """Format batch analyses for LLM prompt - structured data only"""
        formatted = []
        for batch in batch_analyses:
            batch_data = batch['data']
            formatted.append(f"=== BATCH {batch['batch_index']} (ID: {batch['batch_id']}) ===")
            formatted.append(f"Hash: {batch['hash']}")
            formatted.append(f"Analysis Results: {json.dumps(batch_data.get('analysis_results', []), indent=2)}")
            if 'batch_metadata' in batch_data:
                formatted.append(f"Batch Metadata: {json.dumps(batch_data['batch_metadata'], indent=2)}")
            formatted.append("")
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
    agent = CorpusSynthesisAgent()
    
    try:
        success = agent.process_task(task_id)
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"CorpusSynthesisAgent failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()