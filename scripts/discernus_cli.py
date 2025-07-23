#!/usr/bin/env python3
"""
Discernus PoC CLI - Experiment Orchestration
Simple CLI for running experiments using Redis Streams + MinIO architecture.
"""

import sys
import yaml
import redis
import json
import os
import hashlib
import time
import logging
from typing import Dict, Any
from minio_client import put_artifact, artifact_exists

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - CLI - %(message)s')
logger = logging.getLogger(__name__)

# Redis configuration
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

class DiscernusCLIError(Exception):
    """CLI-specific exceptions"""
    pass

class DiscernusCLI:
    """CLI for experiment orchestration"""
    
    def __init__(self):
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    
    def run_experiment(self, experiment_file: str, mode: str = 'dev'):
        """Run an experiment using the PoC architecture"""
        try:
            # Load experiment specification
            with open(experiment_file) as f:
                experiment = yaml.safe_load(f)
            
            logger.info(f"Running experiment: {experiment.get('name', 'unnamed')}")
            logger.info(f"Mode: {mode}")
            
            # Pre-hash all artifacts
            framework_hash = self._store_file_artifact(experiment['framework_file'])
            logger.info(f"Framework stored: {framework_hash[:12]}...")
            
            corpus_hashes = {}
            corpus_dir = experiment['corpus_dir']
            
            # Support binary file types for THIN testing
            supported_extensions = ['.txt', '.md', '.docx', '.pdf', '.doc', '.rtf']
            
            # If experiment specifies specific files, use those
            if 'corpus_files' in experiment:
                for filename in experiment['corpus_files']:
                    filepath = os.path.join(corpus_dir, filename)
                    if os.path.exists(filepath):
                        file_hash = self._store_file_artifact(filepath)
                        corpus_hashes[filename] = file_hash
                        logger.info(f"Binary corpus file stored: {filename} -> {file_hash[:12]}...")
                    else:
                        logger.warning(f"Specified corpus file not found: {filename}")
            else:
                # Auto-discover files with supported extensions
                for filename in os.listdir(corpus_dir):
                    if any(filename.endswith(ext) for ext in supported_extensions):
                        filepath = os.path.join(corpus_dir, filename)
                        file_hash = self._store_file_artifact(filepath)
                        corpus_hashes[filename] = file_hash
                        logger.info(f"Corpus file stored: {filename} -> {file_hash[:12]}...")
            
            logger.info(f"Total corpus files: {len(corpus_hashes)}")
            
            # Check cache - predict if all results exist
            if self._check_experiment_cache(framework_hash, corpus_hashes, experiment):
                print(f"✅ Cache hit - experiment already complete!")
                return
            
            # Cost estimation (if live mode)
            if mode == 'live':
                estimated_cost = self._estimate_cost(corpus_hashes, experiment.get('model', 'gpt-4o-mini'))
                budget_cap = experiment.get('budget_cap', 10.0)
                
                print(f"Estimated cost: ${estimated_cost:.2f} (cap ${budget_cap:.2f})")
                response = input("Continue? [y/N]: ")
                if response.lower() != 'y':
                    print("Aborted by user")
                    return
            else:
                print(f"🚀 Dev mode - auto-continuing")
            
            # Create orchestration request
            orchestration_data = {
                'experiment': experiment,
                'framework_hash': framework_hash,
                'corpus_hashes': corpus_hashes
            }
            
            # Queue orchestration request
            message_id = self.redis_client.xadd('orchestrator.tasks', {
                'data': json.dumps(orchestration_data)
            })
            
            run_id = experiment.get('name', f"run_{int(time.time())}")
            print(f"🚀 Experiment queued - run ID: {run_id}")
            print(f"Orchestration request: {message_id}")
            
            # Set run status for pause/resume
            self.redis_client.set(f'run:{run_id}:status', 'RUNNING')
            
        except Exception as e:
            logger.error(f"Failed to run experiment: {e}")
            raise DiscernusCLIError(f"Experiment execution failed: {e}")
    
    def _store_file_artifact(self, filepath: str) -> str:
        """Store file content and return hash - THIN: always binary"""
        try:
            from minio_client import put_file
            return put_file(filepath)
        except Exception as e:
            logger.error(f"Failed to store file {filepath}: {e}")
            raise DiscernusCLIError(f"File storage failed: {e}")
    
    def _check_experiment_cache(self, framework_hash: str, corpus_hashes: Dict[str, str], experiment: Dict[str, Any]) -> bool:
        """Check if experiment results already exist (predictive caching)"""
        try:
            # This is a simplified cache check - in practice you'd predict result hashes
            # For now, we'll assume cache miss (real caching would be more sophisticated)
            return False
        except Exception as e:
            logger.error(f"Cache check failed: {e}")
            return False
    
    def _estimate_cost(self, corpus_hashes: Dict[str, str], model: str) -> float:
        """Estimate experiment cost based on corpus size and model"""
        try:
            # Simplified cost estimation - would use actual LiteLLM pricing in practice
            estimated_tokens_per_file = 2000  # Framework + chunk + response
            total_files = len(corpus_hashes)
            
            # Model pricing (simplified)
            pricing = {
                'gpt-4o-mini': 0.00015,  # per 1K tokens
                'gpt-4o': 0.005,
                'claude-3.5-sonnet': 0.003
            }
            
            price_per_1k = pricing.get(model, 0.002)
            estimated_cost = (estimated_tokens_per_file * total_files * price_per_1k) / 1000
            
            return estimated_cost
            
        except Exception as e:
            logger.error(f"Cost estimation failed: {e}")
            return 0.0
    
    def pause_experiment(self, run_id: str):
        """Pause a running experiment"""
        try:
            self.redis_client.set(f'run:{run_id}:status', 'PAUSED')
            print(f"⏸️  Paused {run_id}")
        except Exception as e:
            logger.error(f"Failed to pause experiment: {e}")
            raise DiscernusCLIError(f"Pause failed: {e}")
    
    def resume_experiment(self, run_id: str):
        """Resume a paused experiment"""
        try:
            self.redis_client.set(f'run:{run_id}:status', 'RUNNING')
            print(f"▶️  Resumed {run_id}")
        except Exception as e:
            logger.error(f"Failed to resume experiment: {e}")
            raise DiscernusCLIError(f"Resume failed: {e}")
    
    def list_runs(self):
        """List experiment runs"""
        try:
            keys = self.redis_client.keys('run:*:status')
            if not keys:
                print("No experiment runs found")
                return
                
            print("Experiment Runs:")
            for key in keys:
                run_id = key.decode().split(':')[1]
                status = self.redis_client.get(key).decode()
                print(f"  {run_id}: {status}")
                
        except Exception as e:
            logger.error(f"Failed to list runs: {e}")
            raise DiscernusCLIError(f"List runs failed: {e}")

def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  discernus_cli.py run <experiment.yaml> [--mode live|dev]")
        print("  discernus_cli.py pause <run_id>")
        print("  discernus_cli.py resume <run_id>")
        print("  discernus_cli.py list")
        sys.exit(1)
    
    command = sys.argv[1]
    cli = DiscernusCLI()
    
    try:
        if command == 'run' and len(sys.argv) >= 3:
            experiment_file = sys.argv[2]
            mode = 'dev'
            
            # Check for mode flag
            if len(sys.argv) >= 4 and sys.argv[3].startswith('--mode'):
                if '=' in sys.argv[3]:
                    mode = sys.argv[3].split('=')[1]
                elif len(sys.argv) >= 5:
                    mode = sys.argv[4]
                    
            cli.run_experiment(experiment_file, mode)
            
        elif command == 'pause' and len(sys.argv) >= 3:
            run_id = sys.argv[2]
            cli.pause_experiment(run_id)
            
        elif command == 'resume' and len(sys.argv) >= 3:
            run_id = sys.argv[2]
            cli.resume_experiment(run_id)
            
        elif command == 'list':
            cli.list_runs()
            
        else:
            print("Invalid command or missing arguments")
            sys.exit(1)
            
    except DiscernusCLIError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 