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
from typing import Dict, Any, List
from pathlib import Path
from minio_client import put_artifact, artifact_exists

# Import PEL cleanup functionality
from cleanup_redis_pel import cleanup_pending_tasks

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

class ArtifactManifestWriter:
    """Manages artifact manifests for experiment runs"""
    
    def __init__(self, run_id: str):
        self.run_id = run_id
        self.manifest_dir = Path(f'runs/{run_id}')
        self.manifest_file = self.manifest_dir / 'manifest.json'
        self.artifacts = []
        
        # Create runs directory
        self.manifest_dir.mkdir(parents=True, exist_ok=True)
        
    def add_artifact(self, sha256: str, uri: str, task_type: str, 
                    parent_sha256: str = None, prompt_hash: str = None, 
                    original_filename: str = None, mime_type: str = None):
        """Add artifact to manifest"""
        artifact_entry = {
            'sha256': sha256,
            'uri': uri,
            'parent_sha256': parent_sha256,
            'task_type': task_type,
            'timestamp': time.time(),
            'prompt_hash': prompt_hash,
            'original_filename': original_filename,
            'mime_type': mime_type
        }
        self.artifacts.append(artifact_entry)
        
        # Write manifest immediately for fault tolerance
        self._write_manifest()
        
    def _write_manifest(self):
        """Write manifest to JSON file"""
        manifest_data = {
            'run_id': self.run_id,
            'created': time.time(),
            'total_artifacts': len(self.artifacts),
            'artifacts': self.artifacts
        }
        
        with open(self.manifest_file, 'w') as f:
            json.dump(manifest_data, f, indent=2)
            
    def generate_markdown_summary(self) -> str:
        """Generate human-readable Markdown summary from JSON manifest"""
        md_content = f"""# Experiment Run Manifest: {self.run_id}

**Generated**: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}  
**Total Artifacts**: {len(self.artifacts)}

## Artifact Overview

| SHA256 (12 chars) | Task Type | Original Filename | Timestamp |
|-------------------|-----------|-------------------|-----------|
"""
        
        for artifact in self.artifacts:
            sha256_short = artifact['sha256'][:12] + '...'
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(artifact['timestamp']))
            filename = artifact.get('original_filename', 'N/A')
            task_type = artifact['task_type']
            
            md_content += f"| `{sha256_short}` | {task_type} | {filename} | {timestamp} |\n"
            
        md_content += f"""
## Provenance Chain

This manifest provides complete artifact traceability for academic reproducibility:

- **Content-Addressable Storage**: All artifacts stored by SHA256 hash
- **Parent Relationships**: `parent_sha256` tracks derivation chains
- **Task Classification**: `task_type` identifies processing stage
- **Temporal Ordering**: `timestamp` provides execution chronology

## File Reconstruction

Original files can be reconstructed from MinIO storage:

```bash"""

        for artifact in self.artifacts:
            if artifact.get('original_filename'):
                md_content += f"\n# Retrieve {artifact['original_filename']}\n"
                md_content += f"python3 scripts/minio_client.py get {artifact['sha256']} {artifact['original_filename']}"
                
        md_content += "\n```\n"
        
        # Write markdown summary
        md_file = self.manifest_dir / 'manifest.md'
        with open(md_file, 'w') as f:
            f.write(md_content)
            
        return md_content

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
            
            run_id = experiment.get('name', f"run_{int(time.time())}")
            logger.info(f"Running experiment: {experiment.get('name', 'unnamed')} (run_id: {run_id})")
            logger.info(f"Mode: {mode}")
            
            # Initialize artifact manifest
            manifest = ArtifactManifestWriter(run_id)
            
            # Pre-hash all artifacts with manifest tracking
            framework_hash = self._store_file_artifact(experiment['framework_file'])
            manifest.add_artifact(
                sha256=framework_hash,
                uri=f"minio://discernus-artifacts/{framework_hash}",
                task_type='framework',
                original_filename=os.path.basename(experiment['framework_file']),
                mime_type='text/markdown'
            )
            logger.info(f"Framework stored: {framework_hash[:12]}...")
            
            corpus_hashes = {}
            corpus_dir = experiment['corpus_dir']
            
            # If experiment specifies specific files, use those
            if 'corpus_files' in experiment:
                for filename in experiment['corpus_files']:
                    filepath = os.path.join(corpus_dir, filename)
                    if os.path.exists(filepath):
                        file_hash = self._store_file_artifact(filepath)
                        corpus_hashes[filename] = file_hash
                        
                        # Add to manifest
                        manifest.add_artifact(
                            sha256=file_hash,
                            uri=f"minio://discernus-artifacts/{file_hash}",
                            task_type='corpus',
                            original_filename=filename,
                            mime_type=self._get_mime_type(filename)
                        )
                        logger.info(f"Binary corpus file stored: {filename} -> {file_hash[:12]}...")
                    else:
                        logger.warning(f"Specified corpus file not found: {filename}")
            else:
                # Auto-discover files (remove file extension filtering per your feedback)
                for filename in os.listdir(corpus_dir):
                    filepath = os.path.join(corpus_dir, filename)
                    if os.path.isfile(filepath):  # Store ANY file type
                        file_hash = self._store_file_artifact(filepath)
                        corpus_hashes[filename] = file_hash
                        
                        # Add to manifest
                        manifest.add_artifact(
                            sha256=file_hash,
                            uri=f"minio://discernus-artifacts/{file_hash}",
                            task_type='corpus',
                            original_filename=filename,
                            mime_type=self._get_mime_type(filename)
                        )
                        logger.info(f"Corpus file stored: {filename} -> {file_hash[:12]}...")
            
            logger.info(f"Total corpus files: {len(corpus_hashes)}")
            
            # Generate manifest summary
            manifest.generate_markdown_summary()
            print(f"📋 Artifact manifest created: {manifest.manifest_file}")
            
            # Check cache - predict if all results exist
            if self._check_experiment_cache(framework_hash, corpus_hashes, experiment):
                print(f"✅ Cache hit - experiment already complete!")
                return
            
            # Cost estimation and budget guard (if live mode)
            if mode == 'live':
                logger.info("Live mode: Performing cost estimation and budget validation...")
                
                estimated_cost = self._estimate_cost(corpus_hashes, experiment.get('model', 'gemini-2.5-flash'))
                budget_cap = experiment.get('budget_cap', 10.0)
                
                # Enhanced cost guard with validation
                print(f"\n💰 COST ESTIMATION (Live Mode)")
                print(f"  Model: {experiment.get('model', 'gemini-2.5-flash')}")
                print(f"  Corpus files: {len(corpus_hashes)}")
                print(f"  Estimated cost: ${estimated_cost:.4f}")
                print(f"  Budget cap: ${budget_cap:.2f}")
                
                # Budget validation
                if estimated_cost > budget_cap:
                    print(f"\n❌ COST GUARD BLOCKED")
                    print(f"   Estimated cost (${estimated_cost:.4f}) exceeds budget cap (${budget_cap:.2f})")
                    print(f"   Increase budget_cap in experiment file or switch to dev mode")
                    raise DiscernusCLIError(f"Cost estimate ${estimated_cost:.4f} exceeds budget cap ${budget_cap:.2f}")
                
                # User confirmation
                cost_percentage = (estimated_cost / budget_cap) * 100
                print(f"  Budget utilization: {cost_percentage:.1f}%")
                print(f"\n🚨 Live mode will incur real costs!")
                response = input("Continue with live LLM calls? [y/N]: ")
                if response.lower() != 'y':
                    print("Aborted by user")
                    return
                    
                print(f"✅ Cost guard passed - proceeding with live mode")
            else:
                print(f"🚀 Dev mode - bypassing cost guard")
                logger.info("Dev mode: Skipping cost estimation and budget validation")
            
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
            
            print(f"🚀 Experiment queued - run ID: {run_id}")
            print(f"Orchestration request: {message_id}")
            
            # Set run status for pause/resume
            self.redis_client.set(f'run:{run_id}:status', 'RUNNING')
            
        except Exception as e:
            logger.error(f"Failed to run experiment: {e}")
            raise DiscernusCLIError(f"Experiment execution failed: {e}")
    def run_from_manifest(self, manifest_file: str):
        """Resume or replay an experiment exactly from a manifest JSON file."""
        print(f"Replaying experiment from manifest: {manifest_file}")
        # TODO: Implement re-queuing of tasks based on manifest for full replay
        # For now, simply display artifact summary
        try:
            import json
            from pathlib import Path
            manifest_path = Path(manifest_file)
            data = json.loads(manifest_path.read_text())
            print(json.dumps(data, indent=2))
        except Exception as e:
            print(f"Failed to load manifest: {e}")
    
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
        """Estimate experiment cost using real LiteLLM cost APIs - THIN approach"""
        try:
            # Import LiteLLM for real cost calculation
            import litellm
            from litellm.cost_calculator import completion_cost
            
            # Get framework and corpus sizes for realistic token estimation
            total_cost = 0.0
            
            # Rough estimation: Get actual model pricing from LiteLLM
            try:
                # Get model cost info from LiteLLM's cost map
                cost_info = litellm.model_cost.get(model, {})
                input_cost_per_token = cost_info.get('input_cost_per_token', 0.0001)  # Fallback
                output_cost_per_token = cost_info.get('output_cost_per_token', 0.0002)  # Fallback
                
                if not cost_info:
                    logger.warning(f"Cost info not found for {model}, using fallback estimates")
                
            except Exception as e:
                logger.warning(f"Failed to get LiteLLM cost info: {e}, using fallback")
                input_cost_per_token = 0.0001  # Conservative fallback
                output_cost_per_token = 0.0002
            
            # Estimate tokens per file (framework + document + response)
            estimated_input_tokens_per_file = 3000   # Framework (1500) + Document (1500) 
            estimated_output_tokens_per_file = 800   # Structured analysis response
            
            total_files = len(corpus_hashes)
            
            # Calculate total cost
            total_input_tokens = estimated_input_tokens_per_file * total_files
            total_output_tokens = estimated_output_tokens_per_file * total_files
            
            input_cost = total_input_tokens * input_cost_per_token
            output_cost = total_output_tokens * output_cost_per_token
            total_cost = input_cost + output_cost
            
            # Add synthesis cost (if more than 1 file)
            if total_files > 1:
                # Synthesis combines all analysis results
                synthesis_input_tokens = 2000 + (500 * total_files)  # Framework + all analyses
                synthesis_output_tokens = 1000  # Comprehensive report
                
                synthesis_cost = (synthesis_input_tokens * input_cost_per_token + 
                                synthesis_output_tokens * output_cost_per_token)
                total_cost += synthesis_cost
            
            logger.info(f"Cost estimate for {model}: ${total_cost:.4f} ({total_files} files)")
            return total_cost
            
        except Exception as e:
            logger.error(f"LiteLLM cost estimation failed: {e}")
            # Fallback to conservative estimate
            return len(corpus_hashes) * 0.01  # $0.01 per file as safe fallback
    
    def pause_experiment(self, run_id: str):
        """Pause a running experiment"""
        try:
            self.redis_client.set(f'run:{run_id}:status', 'PAUSED')
            print(f"⏸️  Paused {run_id}")
        except Exception as e:
            logger.error(f"Failed to pause experiment: {e}")
            raise DiscernusCLIError(f"Pause failed: {e}")
    
    def resume_experiment(self, run_id: str):
        """Resume a paused experiment with PEL cleanup"""
        try:
            # Check if experiment exists and is paused
            status_key = f'run:{run_id}:status'
            current_status = self.redis_client.get(status_key)
            
            if not current_status:
                raise DiscernusCLIError(f"Run '{run_id}' not found")
                
            current_status = current_status.decode()
            if current_status != 'PAUSED':
                print(f"⚠️  Run '{run_id}' is {current_status}, not paused")
                return
            
            # Perform PEL cleanup before resuming
            logger.info(f"Performing PEL cleanup before resuming {run_id}...")
            reclaimed_count = cleanup_pending_tasks(
                self.redis_client,
                stream_name='tasks',
                group_name='discernus',
                max_idle_ms=30000  # 30 seconds
            )
            
            if reclaimed_count > 0:
                print(f"🔄 Reclaimed {reclaimed_count} orphaned tasks")
            else:
                print("✅ No orphaned tasks found")
            
            # Resume the experiment
            self.redis_client.set(status_key, 'RUNNING')
            print(f"▶️  Resumed {run_id}")
            
            # Log the resume action for provenance
            logger.info(f"Experiment {run_id} resumed with {reclaimed_count} tasks reclaimed")
            
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

    def results(self, run_id: str):
        """Fetch and display results for a given run_id from manifest.json"""
        from pathlib import Path
        manifest_path = Path(f"runs/{run_id}/manifest.json")
        if not manifest_path.exists():
            print(f"Run '{run_id}' not found or manifest missing")
            return
        with open(manifest_path) as f:
            data = json.load(f)
        artifacts = data.get("artifacts", [])
        grouped: Dict[str, List[Any]] = {}
        for art in artifacts:
            grouped.setdefault(art["task_type"], []).append(art)
        for task_type, arts in grouped.items():
            print(f"\n=== {task_type.upper()} ===")
            for art in arts:
                fname = art.get("original_filename", "N/A")
                sha = art["sha256"]
                print(f"{fname} -> {sha}")
        print(f"\nManifest run_id: {data.get('run_id')}, created: {data.get('created')}")

    def export(self, run_id: str, out_dir: str):
        """Export all artifacts for a given run_id into structured output directory"""
        from pathlib import Path
        # Load manifest
        manifest_path = Path(f"runs/{run_id}/manifest.json")
        if not manifest_path.exists():
            print(f"Run '{run_id}' not found or manifest missing")
            return
        with open(manifest_path) as f:
            data = json.load(f)
        artifacts = data.get('artifacts', [])
        # Prepare output directories
        base_dir = Path(out_dir)
        base_dir.mkdir(parents=True, exist_ok=True)
        for art in artifacts:
            task_type = art['task_type']
            sha = art['sha256']
            filename = art.get('original_filename', sha)
            dest_dir = base_dir / task_type
            dest_dir.mkdir(parents=True, exist_ok=True)
            # Retrieve artifact to file
            try:
                # Use default MinIO client to retrieve artifacts
                from minio_client import get_default_client
                client = get_default_client()
                client.get_to_file(sha, str(dest_dir / filename))
                print(f"Exported {task_type}/{filename}")
            except Exception as e:
                print(f"Failed to export {sha}: {e}")
        # Copy manifest files
        manifest_md = Path(f"runs/{run_id}/manifest.md")
        if manifest_md.exists():
            dest_manifest_md = base_dir / 'manifest.md'
            dest_manifest_json = base_dir / 'manifest.json'
            import shutil
            shutil.copy(manifest_path, dest_manifest_json)
            shutil.copy(manifest_md, dest_manifest_md)
            print(f"Exported manifest files to {base_dir}")
        print(f"Export completed: {base_dir}")

    def _get_mime_type(self, filename: str) -> str:
        """Simple MIME type detection for manifest"""
        ext = Path(filename).suffix.lower()
        mime_types = {
            '.txt': 'text/plain',
            '.md': 'text/markdown', 
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.pdf': 'application/pdf',
            '.json': 'application/json',
            '.yaml': 'application/x-yaml',
            '.yml': 'application/x-yaml'
        }
        return mime_types.get(ext, 'application/octet-stream')

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
            # Support run from manifest
            if sys.argv[2] == '--from-manifest' and len(sys.argv) >= 4:
                manifest_file = sys.argv[3]
                cli.run_from_manifest(manifest_file)
                return
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
            
        elif command == 'results' and len(sys.argv) >= 3:
            run_id = sys.argv[2]
            cli.results(run_id)
            
        elif command == 'export' and len(sys.argv) >= 4:
            run_id = sys.argv[2]
            out_dir = sys.argv[3]
            cli.export(run_id, out_dir)
            
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