#!/usr/bin/env python3
"""
V2 Orchestrator - Agent-Native Architecture
===========================================

Simple, clean orchestrator that leverages standardized V2 agents.
Follows the strategy pattern for different execution modes.

Key Features:
- Agent registry for dynamic agent discovery
- Strategy pattern for different execution modes
- RunContext for explicit data handoffs
- Resume capability with manifest tracking
- Clean separation of concerns
"""

import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional, Type
from dataclasses import dataclass

from .security_boundary import ExperimentSecurityBoundary
from .audit_logger import AuditLogger
from .local_artifact_storage import LocalArtifactStorage
from .run_context import RunContext
from .agent_result import AgentResult
from .standard_agent import StandardAgent
from .execution_strategies import ExecutionStrategy, ExperimentResult

# Import for progress reporting
try:
    from ..cli_console import rich_console
except ImportError:
    # Fallback if not running from CLI context
    import sys
    print("⚠️ Progress reporting not available - running outside CLI context", file=sys.stderr)
    rich_console = None


@dataclass
class V2OrchestratorConfig:
    """Configuration for V2 Orchestrator"""
    experiment_id: str
    framework_path: str
    corpus_path: str
    output_dir: str
    resume_from_phase: Optional[str] = None
    verification_enabled: bool = True
    cache_enabled: bool = True
    debug_mode: bool = False
    skip_validation: bool = False


class V2Orchestrator:
    """
    V2 Orchestrator - Simple, agent-native architecture.
    
    This orchestrator follows the strategy pattern where different execution
    strategies handle different types of experiment runs. The orchestrator
    itself is just a thin layer that manages agents and delegates execution
    to strategies.
    """
    
    def __init__(self, 
                 config: V2OrchestratorConfig,
                 security: ExperimentSecurityBoundary,
                 storage: LocalArtifactStorage,
                 audit: AuditLogger):
        """
        Initialize V2 Orchestrator.
        
        Args:
            config: Orchestrator configuration
            security: Security boundary for the experiment
            storage: Artifact storage for persistence
            audit: Audit logger for provenance tracking
        """
        self.config = config
        self.security = security
        self.storage = storage
        self.audit = audit
        
        # Agent registry - will be populated by strategies
        self.agents: Dict[str, StandardAgent] = {}
        
        # Initialize logging
        from .logging_config import get_logger
        self.logger = get_logger("V2Orchestrator")
        
        # Log orchestrator initialization
        self.audit.log_agent_event("V2Orchestrator", "orchestrator_initialization", {
            "experiment_id": config.experiment_id,
            "framework_path": config.framework_path,
            "corpus_path": config.corpus_path,
            "resume_from_phase": config.resume_from_phase,
            "verification_enabled": config.verification_enabled
        })
    
    def register_agent(self, name: str, agent: StandardAgent) -> None:
        """
        Register an agent with the orchestrator.
        
        Args:
            name: Agent name/identifier
            agent: Agent instance implementing StandardAgent interface
        """
        self.agents[name] = agent
        self.logger.info(f"Registered agent: {name}")
        
        # Log agent registration
        self.audit.log_agent_event("V2Orchestrator", "agent_registration", {
            "agent_name": name,
            "agent_type": agent.__class__.__name__,
            "capabilities": agent.get_capabilities()
        })
    
    def execute_strategy(self, strategy: ExecutionStrategy) -> ExperimentResult:
        """
        Execute an experiment using the specified strategy.
        
        Args:
            strategy: Execution strategy to use
            
        Returns:
            ExperimentResult with execution results
        """
        self.logger.info(f"Executing strategy: {strategy.__class__.__name__}")
        
        # Create initial RunContext
        run_context = RunContext(
            experiment_id=self.config.experiment_id,
            framework_path=self.config.framework_path,
            corpus_path=self.config.corpus_path
        )
        
        # Add orchestrator metadata
        run_context.metadata.update({
            "orchestrator_version": "v2",
            "verification_enabled": self.config.verification_enabled,
            "cache_enabled": self.config.cache_enabled,
            "debug_mode": self.config.debug_mode,
            "resume_from_phase": self.config.resume_from_phase,
            "skip_validation": self.config.skip_validation
        })
        
        # Create input file snapshots for provenance (once per experiment)
        self._create_input_snapshots(run_context)
        
        # Log strategy execution start
        self.audit.log_agent_event("V2Orchestrator", "strategy_execution_start", {
            "strategy": strategy.__class__.__name__,
            "experiment_id": self.config.experiment_id,
            "agents_available": list(self.agents.keys())
        })
        
        try:
            # Show progress during execution
            if rich_console:
                rich_console.print_info("🚀 Starting experiment execution...")

            # Execute the strategy
            result = strategy.execute(self.agents, run_context, self.storage, self.audit)

            # Log successful completion
            self.audit.log_agent_event("V2Orchestrator", "strategy_execution_complete", {
                "strategy": strategy.__class__.__name__,
                "experiment_id": self.config.experiment_id,
                "success": result.success,
                "phases_completed": result.phases_completed,
                "artifacts_generated": len(result.artifacts)
            })

            return result
            
        except Exception as e:
            # Log execution failure
            self.audit.log_agent_event("V2Orchestrator", "strategy_execution_failed", {
                "strategy": strategy.__class__.__name__,
                "experiment_id": self.config.experiment_id,
                "error": str(e),
                "error_type": type(e).__name__
            })
            
            # Return failure result
            return ExperimentResult(
                success=False,
                error_message=str(e),
                phases_completed=[],
                artifacts=[],
                metadata={"error_type": type(e).__name__}
            )
    
    def get_agent(self, name: str) -> Optional[StandardAgent]:
        """Get a registered agent by name."""
        return self.agents.get(name)
    
    def list_agents(self) -> List[str]:
        """Get list of registered agent names."""
        return list(self.agents.keys())
    
    def get_agent_capabilities(self) -> Dict[str, List[str]]:
        """Get capabilities of all registered agents."""
        return {
            name: agent.get_capabilities() 
            for name, agent in self.agents.items()
        }
    
    def create_resume_manifest(self, run_context: RunContext) -> Dict[str, Any]:
        """
        Create a resume manifest for the current state.
        
        Args:
            run_context: Current run context
            
        Returns:
            Resume manifest dictionary
        """
        manifest = {
            "experiment_id": run_context.experiment_id,
            "framework_path": run_context.framework_path,
            "corpus_path": run_context.corpus_path,
            "current_phase": run_context.current_phase,
            "completed_phases": run_context.completed_phases,
            "artifact_hashes": run_context.artifact_hashes,
            "cache_keys": run_context.cache_keys,
            "versions": run_context.versions,
            "metadata": run_context.metadata,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "orchestrator_version": "v2"
        }
        
        # Store manifest
        manifest_json = json.dumps(manifest, indent=2)
        manifest_hash = hashlib.sha256(manifest_json.encode()).hexdigest()
        
        self.storage.put_artifact(
            manifest_json.encode('utf-8'),
            {
                "artifact_type": "resume_manifest",
                "experiment_id": run_context.experiment_id,
                "phase": run_context.current_phase
            }
        )
        
        self.logger.info(f"Created resume manifest: {manifest_hash}")
        return manifest
    
    def load_resume_manifest(self, manifest_path: str) -> Optional[Dict[str, Any]]:
        """
        Load a resume manifest from file.
        
        Args:
            manifest_path: Path to resume manifest file
            
        Returns:
            Resume manifest dictionary or None if not found
        """
        try:
            manifest_file = Path(manifest_path)
            if not manifest_file.exists():
                return None
                
            with open(manifest_file, 'r') as f:
                manifest = json.load(f)
                
            # Validate manifest
            if manifest.get("orchestrator_version") != "v2":
                self.logger.warning("Resume manifest is not from V2 orchestrator")
                return None
                
            return manifest
            
        except Exception as e:
            self.logger.error(f"Failed to load resume manifest: {e}")
            return None
    
    def resume_from_manifest(self, manifest: Dict[str, Any]) -> RunContext:
        """
        Resume execution from a manifest.
        
        Args:
            manifest: Resume manifest dictionary
            
        Returns:
            RunContext restored from manifest
        """
        run_context = RunContext(
            experiment_id=manifest["experiment_id"],
            framework_path=manifest["framework_path"],
            corpus_path=manifest["corpus_path"]
        )
        
        # Restore state from manifest
        run_context.current_phase = manifest.get("current_phase")
        run_context.completed_phases = manifest.get("completed_phases", [])
        run_context.artifact_hashes = manifest.get("artifact_hashes", {})
        run_context.cache_keys = manifest.get("cache_keys", {})
        run_context.versions = manifest.get("versions", {})
        run_context.metadata.update(manifest.get("metadata", {}))
        
        self.logger.info(f"Resumed from manifest: {manifest['experiment_id']}")
        return run_context
    
    def _create_input_snapshots(self, run_context: RunContext) -> None:
        """
        Create snapshots of input files for complete provenance tracking.
        
        Args:
            run_context: Current run context with file paths
        """
        try:
            # Get the artifacts directory from storage
            artifacts_dir = Path(self.storage.artifacts_dir)
            
            # Create snapshots of input files
            snapshots_created = []
            
            # Snapshot experiment.md
            experiment_path = Path(run_context.framework_path).parent / "experiment.md"
            if experiment_path.exists():
                experiment_content = experiment_path.read_text(encoding='utf-8')
                experiment_hash = hashlib.sha256(experiment_content.encode()).hexdigest()
                snapshot_path = artifacts_dir / f"experiment_{experiment_hash[:8]}.md"
                snapshot_path.write_text(experiment_content, encoding='utf-8')
                snapshots_created.append(f"experiment_{experiment_hash[:8]}.md")
            
            # Snapshot framework file
            framework_path = Path(run_context.framework_path)
            if framework_path.exists():
                framework_content = framework_path.read_text(encoding='utf-8')
                framework_hash = hashlib.sha256(framework_content.encode()).hexdigest()
                snapshot_path = artifacts_dir / f"framework_{framework_hash[:8]}.md"
                snapshot_path.write_text(framework_content, encoding='utf-8')
                snapshots_created.append(f"framework_{framework_hash[:8]}.md")
            
            # Snapshot corpus.md
            corpus_path = Path(run_context.corpus_path)
            if corpus_path.exists():
                corpus_content = corpus_path.read_text(encoding='utf-8')
                corpus_hash = hashlib.sha256(corpus_content.encode()).hexdigest()
                snapshot_path = artifacts_dir / f"corpus_{corpus_hash[:8]}.md"
                snapshot_path.write_text(corpus_content, encoding='utf-8')
                snapshots_created.append(f"corpus_{corpus_hash[:8]}.md")
            
            # Create comprehensive README for the run directory
            self._create_run_readme(artifacts_dir.parent, run_context, snapshots_created)
            
            # Log snapshot creation
            self.audit.log_agent_event("V2Orchestrator", "input_snapshots_created", {
                "snapshots_created": snapshots_created,
                "total_snapshots": len(snapshots_created)
            })
            
        except Exception as e:
            # Log error but don't fail the experiment
            self.audit.log_agent_event("V2Orchestrator", "input_snapshots_error", {
                "error": str(e),
                "error_type": type(e).__name__
            })
    
    def _create_run_readme(self, run_dir: Path, run_context: RunContext, snapshots: List[str]) -> None:
        """
        Create comprehensive README for the run directory.
        
        Args:
            run_dir: Run directory path
            run_context: Current run context
            snapshots: List of snapshot files created
        """
        try:
            # Get experiment name from run context
            experiment_name = run_context.experiment_id
            
            readme_content = f"""# Discernus Research Run

**Complete Research Package - {experiment_name}**

**Run ID**: {run_dir.name}  
**Generated**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}

## 📁 Directory Structure

### `artifacts/` - Complete Provenance Chain
- **Input Snapshots** (exact versions used in this run):
"""
            
            # Add snapshot files to README
            for snapshot in snapshots:
                if snapshot.startswith('experiment_'):
                    readme_content += f"  - `{snapshot}` - **SNAPSHOT**: Exact version of experiment.md used\n"
                elif snapshot.startswith('framework_'):
                    readme_content += f"  - `{snapshot}` - **SNAPSHOT**: Exact version of framework file used\n"
                elif snapshot.startswith('corpus_'):
                    readme_content += f"  - `{snapshot}` - **SNAPSHOT**: Exact version of corpus.md used\n"
            
            readme_content += f"""- **Analysis Artifacts**: Raw LLM outputs, processing plans, statistical results
- **Evidence Artifacts**: Curated supporting evidence and quotes
- **Report Artifacts**: Synthesis outputs and final reports

### `logs/` - Execution Logs
- `agents.jsonl` - Agent execution details and decisions
- `costs.jsonl` - API usage and cost tracking
- `system.jsonl` - System events and operations
- `llm_interactions.jsonl` - Complete LLM conversation history

### `results/` - Research Outputs (if present)
- `scores.csv` - Analysis scores and derived metrics
- `evidence.csv` - Supporting evidence with quotes
- `metadata.csv` - Document and run metadata
- `final_report.md` - Complete synthesis report

## 🔍 Quick Start

### For Data Analysis
- Check `results/` directory for CSV files ready for statistical analysis
- Use `artifacts/` for detailed analysis artifacts and provenance

### For Replication
- Use snapshot files in `artifacts/` to see exact input versions
- All necessary files for complete replication are preserved

### For Audit
- Review `logs/` for complete execution trace
- Check `artifacts/` for full provenance chain
- Verify input snapshots match original files using hash verification

## 📋 Provenance Verification

This run used exact versions of input files (see snapshots in `artifacts/`).

To verify a snapshot matches the original:
```bash
# Example verification
sha256sum artifacts/experiment_{snapshots[0].split('_')[1] if snapshots else 'hash'}.md
# Compare with: sha256sum ../../experiment.md
```

All files are content-addressable and fully traceable through the artifact system.

## 🏗️ Architecture

This run was generated using the Discernus V2 system with:
- **THIN Architecture**: Minimal orchestration, agent-native design
- **Content-Addressable Storage**: All artifacts stored with SHA-256 hashes
- **Complete Audit Trail**: Every operation logged and tracked
- **Self-Contained**: No external dependencies for replication

---
*Generated by Discernus Alpha System - Complete Research Transparency*
"""
            
            # Write README to run directory
            readme_path = run_dir / "README.md"
            readme_path.write_text(readme_content, encoding='utf-8')
            
        except Exception as e:
            # Don't fail the experiment if README creation fails
            pass
