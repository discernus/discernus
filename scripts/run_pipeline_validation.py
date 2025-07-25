#!/usr/bin/env python3
"""
Pipeline Validation Script - Execute 3-Stage Pipeline
===================================================

Executes the pipeline validation experiment using the Redis-based coordination
system as specified in Implementation Plan V4. This script creates the initial
orchestration task and waits for completion.

Pipeline: PreTest → BatchAnalysis → CorpusSynthesis (stops after Stage 3)
"""

import redis
import json
import yaml
import sys
import os
import time
import hashlib
from pathlib import Path
from typing import Dict, Any, List

# Add scripts directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__)))
from minio_client import put_artifact, get_artifact

# Configure logging
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - PipelineValidation - %(message)s')
logger = logging.getLogger(__name__)

# Redis configuration
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = 6379
REDIS_DB = 0

class PipelineValidationRunner:
    """
    Executes the 3-stage pipeline validation experiment.
    """
    
    def __init__(self):
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        self.project_path = Path("projects/pipeline_validation")
        
    def run_validation_experiment(self) -> Dict[str, Any]:
        """
        Execute the pipeline validation experiment.
        """
        logger.info("Starting Pipeline Validation Experiment")
        
        try:
            # 1. Load experiment configuration
            experiment_config = self._load_experiment_config()
            logger.info(f"Loaded experiment: {experiment_config['name']}")
            
            # 2. Prepare framework and corpus artifacts
            framework_hashes = self._prepare_framework_artifacts(experiment_config)
            corpus_hashes = self._prepare_corpus_artifacts(experiment_config)
            
            logger.info(f"Framework artifacts: {len(framework_hashes)} files")
            logger.info(f"Corpus artifacts: {len(corpus_hashes)} files")
            
            # 3. Create orchestration task
            orchestration_data = {
                'experiment': experiment_config,
                'framework_hashes': framework_hashes,
                'corpus_hashes': corpus_hashes,
                'pipeline_mode': '3_stage_validation'  # Stop after CorpusSynthesis
            }
            
            task_id = self._create_orchestration_task(orchestration_data)
            logger.info(f"Created orchestration task: {task_id}")
            
            # 4. Wait for completion and collect results
            results = self._wait_for_pipeline_completion(task_id)
            
            logger.info("Pipeline validation experiment completed successfully")
            return results
            
        except Exception as e:
            logger.error(f"Pipeline validation failed: {e}")
            raise
    
    def _load_experiment_config(self) -> Dict[str, Any]:
        """Load experiment configuration from experiment.md"""
        experiment_file = self.project_path / "experiment.md"
        
        if not experiment_file.exists():
            raise FileNotFoundError(f"Experiment file not found: {experiment_file}")
        
        with open(experiment_file, 'r') as f:
            content = f.read()
            
        # Parse YAML content
        experiment_config = yaml.safe_load(content)
        return experiment_config
    
    def _prepare_framework_artifacts(self, experiment_config: Dict[str, Any]) -> List[str]:
        """Prepare framework artifacts and store in MinIO"""
        framework_hashes = []
        
        for framework_spec in experiment_config.get('frameworks', []):
            framework_id = framework_spec['id']
            framework_file = self.project_path / framework_id
            
            if not framework_file.exists():
                raise FileNotFoundError(f"Framework file not found: {framework_file}")
            
            # Read framework content
            with open(framework_file, 'r') as f:
                framework_content = f.read()
            
            # Store in MinIO and get hash
            framework_hash = put_artifact(framework_content.encode('utf-8'))
            framework_hashes.append(framework_hash)
            
            logger.info(f"Stored framework {framework_id} as {framework_hash}")
        
        return framework_hashes
    
    def _prepare_corpus_artifacts(self, experiment_config: Dict[str, Any]) -> List[str]:
        """Prepare corpus artifacts and store in MinIO"""
        corpus_hashes = []
        corpus_path = self.project_path / experiment_config.get('corpus_path', 'corpus')
        
        if not corpus_path.exists():
            raise FileNotFoundError(f"Corpus directory not found: {corpus_path}")
        
        # Process all files in corpus directory
        for corpus_file in corpus_path.glob('*.md'):
            with open(corpus_file, 'r') as f:
                corpus_content = f.read()
            
            # Store in MinIO and get hash
            corpus_hash = put_artifact(corpus_content.encode('utf-8'))
            corpus_hashes.append(corpus_hash)
            
            logger.info(f"Stored corpus file {corpus_file.name} as {corpus_hash}")
        
        return corpus_hashes
    
    def _create_orchestration_task(self, orchestration_data: Dict[str, Any]) -> str:
        """Create orchestration task in Redis stream"""
        
        task_data = {
            'type': 'orchestrate',
            'data': json.dumps(orchestration_data),
            'timestamp': time.time()
        }
        
        message_id = self.redis_client.xadd('orchestrator.tasks', task_data)
        return message_id.decode()
    
    def _wait_for_pipeline_completion(self, task_id: str, timeout: int = 3600) -> Dict[str, Any]:
        """Wait for pipeline completion and collect results"""
        
        logger.info(f"Waiting for pipeline completion (timeout: {timeout}s)")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            # Check if there are completion signals or artifacts
            # For now, we'll use a simple polling approach
            
            # Check Redis streams for completion
            try:
                # Look for task completion in tasks.done stream
                messages = self.redis_client.xrevrange('tasks.done', count=10)
                
                for msg_id, fields in messages:
                    msg_data = json.loads(fields[b'data'])
                    if 'corpus_synthesis' in str(msg_data):  # Stage 3 completion
                        logger.info("Detected CorpusSynthesis completion - pipeline finished")
                        return self._collect_pipeline_results()
                
            except Exception as e:
                logger.debug(f"Error checking completion: {e}")
            
            time.sleep(5)  # Poll every 5 seconds
        
        raise TimeoutError(f"Pipeline did not complete within {timeout} seconds")
    
    def _collect_pipeline_results(self) -> Dict[str, Any]:
        """Collect and return pipeline execution results"""
        
        results = {
            'status': 'completed',
            'stages_executed': ['PreTest', 'BatchAnalysis', 'CorpusSynthesis'],
            'completion_time': time.time(),
            'pipeline_mode': '3_stage_validation'
        }
        
        # Check Redis streams for stage results
        try:
            # Get recent task completions
            done_messages = self.redis_client.xrevrange('tasks.done', count=20)
            stage_results = []
            
            for msg_id, fields in done_messages:
                try:
                    result_data = json.loads(fields[b'data'])
                    stage_results.append({
                        'message_id': msg_id.decode(),
                        'data': result_data
                    })
                except json.JSONDecodeError:
                    continue
            
            results['stage_results'] = stage_results
            
        except Exception as e:
            logger.warning(f"Could not collect detailed stage results: {e}")
        
        return results

def main():
    """Main execution function"""
    
    runner = PipelineValidationRunner()
    
    try:
        results = runner.run_validation_experiment()
        
        print("\n" + "="*80)
        print("🎯 PIPELINE VALIDATION RESULTS")
        print("="*80)
        print(f"Status: {results['status']}")  
        print(f"Stages Executed: {', '.join(results['stages_executed'])}")
        print(f"Pipeline Mode: {results['pipeline_mode']}")
        print(f"Completion Time: {time.ctime(results['completion_time'])}")
        
        if 'stage_results' in results:
            print(f"Stage Results Collected: {len(results['stage_results'])} messages")
        
        print("\n✅ 3-Stage Pipeline Validation Completed Successfully!")
        print("="*80)
        
        # Save results to file
        results_file = Path("projects/pipeline_validation/validation_results.json")
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"📁 Results saved to: {results_file}")
        
    except Exception as e:
        print(f"\n❌ Pipeline validation failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 