"""
Provenance-First Artifact Organization System

Transforms hostile hash-based artifact storage into academic-grade provenance architecture.
Implements Issue #297: Create Provenance-First File Organization.

Key Features:
- Human-readable artifact names and organization
- Academic-standard directory structure  
- Performance maintained via symlinks to shared cache
- Complete provenance transparency for external review
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict
from datetime import datetime, timezone

from .security_boundary import ExperimentSecurityBoundary
from .audit_logger import AuditLogger


class ProvenanceOrganizerError(Exception):
    """Errors in provenance organization system"""
    pass


class ProvenanceOrganizer:
    """
    Organizes artifacts into human-readable, academic-standard structure.
    
    Transforms:
        shared_cache/artifacts/b8d95bda8af3... (hostile)
    Into:
        artifacts/statistical_results/anova_results.json (academic-friendly)
    """
    
    # Mapping from technical artifact types to human-readable directories
    ARTIFACT_TYPE_MAPPING = {
        # Analysis Pipeline Artifacts
        "analysis_plan": "analysis_plans",
        "raw_analysis_response_v6": "analysis_results", 
        "analysis_json_v6": "analysis_results",  # Combined analysis results
        "analysis_scores": "analysis_results",
        "evidence_extracts": "evidence",
        
        # Synthesis Pipeline Artifacts  
        "statistical_results": "statistical_results",
        "curated_evidence": "evidence", 
        "mathematical_analysis": "statistical_results",
        "derived_metrics": "statistical_results",
        
        # Final Outputs
        "final_report": "reports",
        "synthesis_report": "reports",
        "csv_export": "data",
        
        # Input Materials
        "framework": "inputs",
        "corpus_document": "inputs", 
        "experiment_config": "inputs",
        
        # System Artifacts
        "manifest": "technical",
        "audit_log": "technical",
        "model_interaction": "technical"
    }
    
    def __init__(self, security: ExperimentSecurityBoundary, audit_logger: AuditLogger):
        self.security = security
        self.audit_logger = audit_logger
        
    def organize_run_artifacts(self, 
                              run_dir: Path, 
                              shared_cache_dir: Path,
                              experiment_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create provenance-first artifact organization for a run.
        
        Args:
            run_dir: Run directory to organize
            shared_cache_dir: Shared cache directory with hash-based artifacts
            experiment_metadata: Experiment and run metadata
            
        Returns:
            Organization result with created structure
        """
        try:
            # Load artifact registry
            registry_path = shared_cache_dir / "artifacts" / "artifact_registry.json"
            if not registry_path.exists():
                raise ProvenanceOrganizerError(f"Artifact registry not found: {registry_path}")
                
            with open(registry_path) as f:
                full_artifact_registry = json.load(f)
            
            # Filter artifacts to only include those relevant to current run
            current_run_name = run_dir.name
            artifact_registry = self._filter_run_artifacts(full_artifact_registry, current_run_name, run_dir)
            
            # Create academic-standard directory structure
            self._create_directory_structure(run_dir)
            
            # Create human-readable artifact symlinks
            artifact_map = self._create_artifact_symlinks(
                run_dir, shared_cache_dir, artifact_registry, current_run_name
            )
            
            # Generate provenance metadata
            provenance_data = self._generate_provenance_metadata(
                artifact_registry, artifact_map, experiment_metadata
            )
            
            # Write provenance.json
            provenance_file = run_dir / "artifacts" / "provenance.json"
            with open(provenance_file, 'w') as f:
                json.dump(provenance_data, f, indent=2)
            
            # Generate README for researchers
            self._generate_researcher_readme(run_dir, provenance_data)
            
            # Log successful organization
            self.audit_logger.log_orchestrator_event("provenance_organization", {
                "run_dir": str(run_dir),
                "artifacts_organized": len(artifact_map),
                "directory_structure": "academic_standard_v1.0"
            })
            
            return {
                "success": True,
                "artifacts_organized": len(artifact_map),
                "provenance_file": str(provenance_file),
                "structure_version": "academic_standard_v1.0"
            }
            
        except Exception as e:
            error_msg = f"Provenance organization failed: {str(e)}"
            self.audit_logger.log_error("provenance_organization_error", error_msg, {
                "run_dir": str(run_dir),
                "shared_cache_dir": str(shared_cache_dir)
            })
            raise ProvenanceOrganizerError(error_msg)
    
    def _filter_run_artifacts(self, 
                             full_registry: Dict[str, Any], 
                             current_run_name: str,
                             run_dir: Path) -> Dict[str, Any]:
        """
        Filter artifact registry to include complete provenance chain for current run.
        
        Includes:
        1. Artifacts generated by current run (source_run matches)
        2. Artifacts used as inputs by current run (referenced in manifest)
        3. Complete dependency chain of all artifacts used (recursive dependencies)
        
        Args:
            full_registry: Complete artifact registry from shared cache
            current_run_name: Name of current run (e.g., "20250804T151125Z")
            run_dir: Path to current run directory
            
        Returns:
            Filtered registry containing complete provenance chain for current run
        """
        filtered_registry = {}
        
        # Load current run's manifest to find input artifacts
        manifest_path = run_dir / "manifest.json"
        used_artifacts = set()
        if manifest_path.exists():
            try:
                with open(manifest_path) as f:
                    manifest = json.load(f)
                    # Extract artifact hashes from manifest
                    cache_analysis = manifest.get("cache_analysis", {})
                    artifact_storage = cache_analysis.get("artifact_storage", {})
                    for category, artifacts in artifact_storage.items():
                        if isinstance(artifacts, dict):
                            used_artifacts.update(artifacts.keys())
                        elif isinstance(artifacts, list):
                            used_artifacts.update(artifacts)
            except (json.JSONDecodeError, KeyError):
                # If manifest parsing fails, continue with source_run filtering only
                pass
        
        # Step 1: Include artifacts directly related to current run
        for hash_id, metadata in full_registry.items():
            # Include if generated by current run
            if metadata.get("source_run") == current_run_name:
                filtered_registry[hash_id] = metadata
                # Add dependencies of generated artifacts to used_artifacts for recursive inclusion
                if "metadata" in metadata and "dependencies" in metadata["metadata"]:
                    try:
                        deps = json.loads(metadata["metadata"]["dependencies"])
                        if isinstance(deps, list):
                            used_artifacts.update(deps)
                    except (json.JSONDecodeError, TypeError):
                        pass
            # Include if used as input by current run
            elif hash_id in used_artifacts:
                filtered_registry[hash_id] = metadata
        
        # Step 2: Recursively follow dependency chains to ensure complete provenance
        # This is critical for audit trails - we need ALL artifacts that contributed to results
        dependency_queue = list(used_artifacts)
        processed_dependencies = set()
        
        while dependency_queue:
            dep_hash = dependency_queue.pop(0)
            if dep_hash in processed_dependencies or dep_hash in filtered_registry:
                continue
                
            processed_dependencies.add(dep_hash)
            
            # Include the dependency artifact if it exists
            if dep_hash in full_registry:
                filtered_registry[dep_hash] = full_registry[dep_hash]
                
                # Extract further dependencies from this artifact's metadata
                metadata = full_registry[dep_hash]
                if "metadata" in metadata and "dependencies" in metadata["metadata"]:
                    try:
                        nested_deps = json.loads(metadata["metadata"]["dependencies"])
                        if isinstance(nested_deps, list):
                            for nested_dep in nested_deps:
                                if nested_dep not in processed_dependencies:
                                    dependency_queue.append(nested_dep)
                    except (json.JSONDecodeError, TypeError):
                        pass
        
        return filtered_registry
    
    def _create_directory_structure(self, run_dir: Path) -> None:
        """Create academic-standard directory structure"""
        directories = [
            "data",                    # CSV files for external analysis
            "artifacts/analysis_plans", # What the LLM planned to analyze
            "artifacts/analysis_results", # Raw analysis outputs
            "artifacts/statistical_results", # Mathematical computations
            "artifacts/evidence",      # Curated quotes and supporting data
            "artifacts/reports",       # Final synthesis outputs
            "artifacts/inputs",        # Framework, corpus, experiment config
            "technical/model_interactions", # LLM API call logs
            "technical/logs"           # System logs
        ]
        
        for dir_path in directories:
            full_path = run_dir / dir_path
            self.security.secure_mkdir(full_path)
    
    def _create_artifact_symlinks(self, 
                                 run_dir: Path, 
                                 shared_cache_dir: Path,
                                 artifact_registry: Dict[str, Any],
                                 current_run_name: str) -> Dict[str, str]:
        """
        Create human-readable symlinks to hash-based artifacts.
        
        Returns:
            Mapping from human-readable names to hash IDs
        """
        artifact_map = {}
        artifacts_dir = run_dir / "artifacts"
        
        # Group artifacts by type
        by_type = defaultdict(list)
        for hash_id, metadata in artifact_registry.items():
            artifact_type = metadata.get("metadata", {}).get("artifact_type", "unknown")
            by_type[artifact_type].append((hash_id, metadata))
        
        # Create symlinks for each type
        for artifact_type, artifacts in by_type.items():
            # Map to human-readable directory
            target_dir = self.ARTIFACT_TYPE_MAPPING.get(artifact_type, "unknown")
            type_dir = artifacts_dir / target_dir
            
            for hash_id, metadata in artifacts:
                # Use existing human-readable filename from registry
                human_filename = metadata.get("human_filename", hash_id)
                
                # Create symlink to shared cache artifact (use relative path)
                symlink_path = type_dir / human_filename
                target_path = shared_cache_dir / "artifacts" / human_filename
                # Calculate relative path from run artifacts directory to shared cache
                # From: projects/simple_test/runs/20250804T111225Z/artifacts/analysis_results/
                # To:   projects/simple_test/shared_cache/artifacts/
                relative_target = Path("../../../../shared_cache/artifacts") / human_filename
                
                if target_path.exists():
                    try:
                        # Remove existing symlink if present
                        if symlink_path.exists() or symlink_path.is_symlink():
                            symlink_path.unlink()
                        
                        # Create new symlink with relative path
                        symlink_path.symlink_to(relative_target)
                        artifact_map[human_filename] = hash_id
                        
                        # Create symlink to source run if available
                        source_run = metadata.get("source_run")
                        if source_run and source_run != current_run_name:  # Don't link to self
                            source_run_path = run_dir.parent / source_run
                            if source_run_path.exists():
                                source_symlink_path = type_dir / f"source_{human_filename}"
                                # Use relative path to source run
                                relative_source_target = Path("../../../") / source_run / "artifacts" / target_dir / human_filename
                                if (source_run_path / "artifacts" / target_dir / human_filename).exists():
                                    try:
                                        if source_symlink_path.exists() or source_symlink_path.is_symlink():
                                            source_symlink_path.unlink()
                                        source_symlink_path.symlink_to(relative_source_target)
                                    except OSError:
                                        pass  # Skip if source symlink creation fails
                        
                    except OSError as e:
                        # Log but continue with other artifacts
                        self.audit_logger.log_error("symlink_creation_error", 
                                                   f"Failed to create symlink {symlink_path}: {e}", {})
        
        return artifact_map
    
    def _generate_human_name(self, hash_id: str, metadata: Dict[str, Any]) -> str:
        """Generate human-readable name for artifact"""
        artifact_metadata = metadata.get("metadata", {})
        artifact_type = artifact_metadata.get("artifact_type", "unknown")
        
        # Use original filename if available
        if "original_filename" in artifact_metadata:
            return artifact_metadata["original_filename"]
        
        # Generate descriptive name based on type
        timestamp = metadata.get("created_at", "")[:10]  # YYYY-MM-DD
        short_hash = hash_id[:8]
        
        type_names = {
            "analysis_plan": f"analysis_plan_{short_hash}.md",
            "raw_analysis_response_v6": f"analysis_response_{short_hash}.json",
            "analysis_scores": f"scores_{short_hash}.json", 
            "evidence_extracts": f"evidence_{short_hash}.json",
            "statistical_results": f"statistical_results_{short_hash}.json",
            "curated_evidence": f"curated_evidence_{short_hash}.json",
            "mathematical_analysis": f"mathematical_analysis_{short_hash}.json",
            "derived_metrics": f"derived_metrics_{short_hash}.json",
            "final_report": f"final_report_{timestamp}.md",
            "synthesis_report": f"synthesis_report_{timestamp}.md",
            "framework": f"framework_{short_hash}.md",
            "corpus_document": f"document_{short_hash}.txt",
            "experiment_config": f"experiment_{short_hash}.json"
        }
        
        return type_names.get(artifact_type, f"{artifact_type}_{short_hash}")
    
    def _generate_provenance_metadata(self, 
                                    artifact_registry: Dict[str, Any],
                                    artifact_map: Dict[str, str],
                                    experiment_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Generate human-readable provenance metadata"""
        
        # Calculate pipeline statistics
        pipeline_stats = self._calculate_pipeline_stats(artifact_registry)
        
        return {
            "run_metadata": {
                "experiment_name": experiment_metadata.get("experiment_name", "Unknown"),
                "run_timestamp": experiment_metadata.get("run_timestamp", "Unknown"),
                "framework_version": experiment_metadata.get("framework_version", "Unknown"),
                "model_used": experiment_metadata.get("model_used", "Unknown"),
                "total_artifacts": len(artifact_registry),
                "organized_artifacts": len(artifact_map)
            },
            "directory_structure": {
                "data/": "CSV files for external statistical analysis",
                "artifacts/analysis_plans/": "What the LLM planned to analyze",
                "artifacts/analysis_results/": "Raw analysis outputs from LLM",
                "artifacts/statistical_results/": "Mathematical computations and metrics",
                "artifacts/evidence/": "Curated quotes and supporting data",
                "artifacts/reports/": "Final synthesis outputs and reports",
                "artifacts/inputs/": "Framework, corpus, and experiment configuration",
                "technical/": "System logs and model interaction records"
            },
            "pipeline_stages": pipeline_stats,
            "artifact_descriptions": self._generate_artifact_descriptions(artifact_map, artifact_registry),
            "navigation_guide": {
                "primary_researcher": ["FINAL_REPORT.md", "data/scores.csv", "data/evidence.csv"],
                "internal_reviewer": ["METHODOLOGY_SUMMARY.md", "STATISTICAL_SUMMARY.md"],
                "replication_researcher": ["artifacts/", "technical/manifest.json", "README.md"],
                "fraud_auditor": ["technical/manifest.json", "technical/logs/", "provenance.json"],
                "llm_skeptic": ["technical/model_interactions/", "data/reliability_metrics.csv"]
            }
        }
    
    def _calculate_pipeline_stats(self, artifact_registry: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate pipeline stage statistics"""
        stages = defaultdict(lambda: {"artifacts": 0, "total_size_mb": 0.0})
        
        for hash_id, metadata in artifact_registry.items():
            artifact_type = metadata.get("metadata", {}).get("artifact_type", "unknown")
            size_bytes = metadata.get("size_bytes", 0)
            
            # Map artifact types to pipeline stages
            if artifact_type in ["analysis_plan", "raw_analysis_response_v6", "analysis_scores"]:
                stage = "analysis"
            elif artifact_type in ["statistical_results", "mathematical_analysis", "derived_metrics"]:
                stage = "statistical_computation"
            elif artifact_type in ["curated_evidence", "evidence_extracts"]:
                stage = "evidence_curation"
            elif artifact_type in ["final_report", "synthesis_report"]:
                stage = "synthesis"
            else:
                stage = "inputs_and_system"
            
            stages[stage]["artifacts"] += 1
            stages[stage]["total_size_mb"] += size_bytes / (1024 * 1024)
        
        return dict(stages)
    
    def _generate_artifact_descriptions(self, 
                                      artifact_map: Dict[str, str],
                                      artifact_registry: Dict[str, Any]) -> Dict[str, str]:
        """Generate human-readable descriptions for each artifact"""
        descriptions = {}
        
        for human_name, hash_id in artifact_map.items():
            metadata = artifact_registry.get(hash_id, {}).get("metadata", {})
            artifact_type = metadata.get("artifact_type", "unknown")
            
            # Generate description based on type
            type_descriptions = {
                "analysis_plan": "Analysis plan generated by LLM for systematic evaluation",
                "raw_analysis_response_v6": "Raw analysis response from LLM with scores and reasoning",
                "analysis_scores": "Quantitative scores extracted from analysis",
                "evidence_extracts": "Evidence quotes extracted during analysis",
                "statistical_results": "Statistical computations and significance tests",
                "curated_evidence": "Highest-confidence evidence supporting findings",
                "mathematical_analysis": "Mathematical validation and calculations",
                "derived_metrics": "Derived metrics and composite scores",
                "final_report": "Final research report with findings and implications",
                "synthesis_report": "Synthesis report combining multiple analyses",
                "framework": "Analytical framework used for evaluation",
                "corpus_document": "Source document from research corpus",
                "experiment_config": "Experiment configuration and parameters"
            }
            
            descriptions[human_name] = type_descriptions.get(
                artifact_type, 
                f"Artifact of type {artifact_type}"
            )
        
        return descriptions
    
    def _generate_researcher_readme(self, run_dir: Path, provenance_data: Dict[str, Any]) -> None:
        """Generate README.md for researcher navigation"""
        run_metadata = provenance_data["run_metadata"]
        
        readme_content = f"""# Research Run: {run_metadata['experiment_name']}

**Run Timestamp**: {run_metadata['run_timestamp']}  
**Framework**: {run_metadata['framework_version']}  
**Model**: {run_metadata['model_used']}  
**Total Artifacts**: {run_metadata['total_artifacts']}

## Quick Navigation

### 🎯 Primary Deliverables
- `FINAL_REPORT.md` - Main research findings and implications
- `data/scores.csv` - Quantitative results for statistical analysis
- `data/evidence.csv` - Supporting quotes and evidence

### 📊 Methodology Validation  
- `METHODOLOGY_SUMMARY.md` - Framework and corpus selection rationale
- `STATISTICAL_SUMMARY.md` - Reliability metrics and confidence intervals
- `technical/model_interactions/` - Complete LLM interaction logs

### 🔍 Artifact Organization
- `artifacts/analysis_plans/` - What the LLM planned to analyze
- `artifacts/statistical_results/` - Mathematical computations and metrics
- `artifacts/evidence/` - Curated quotes and supporting data
- `artifacts/reports/` - Final synthesis outputs

### ⚙️ Technical Details
- `technical/manifest.json` - Complete execution record
- `technical/logs/` - System logs and debugging information
- `artifacts/provenance.json` - Human-readable artifact map

## Directory Structure

```
{run_metadata['experiment_name']}/
├── FINAL_REPORT.md              # Main deliverable
├── METHODOLOGY_SUMMARY.md       # Framework + corpus + model decisions
├── STATISTICAL_SUMMARY.md       # Reliability metrics + confidence intervals
├── data/                        # CSV files for external analysis
├── artifacts/                   # Human-readable artifact organization
└── technical/                   # System logs and execution records
```

## For Different Stakeholders

**Primary Researcher**: Start with `FINAL_REPORT.md` and `data/` directory  
**Internal Reviewer**: Review `METHODOLOGY_SUMMARY.md` and `STATISTICAL_SUMMARY.md`  
**Replication Researcher**: Use `artifacts/` and `technical/manifest.json`  
**Fraud Auditor**: Examine `technical/logs/` and `provenance.json`  
**LLM Skeptic**: Check `technical/model_interactions/` and reliability metrics

## Academic Standards

This run follows academic-grade provenance standards:
- ✅ Complete transparency: All artifacts visible and traceable
- ✅ Human-readable organization: Logical structure matches researcher mental models  
- ✅ Performance maintained: Symlinks to shared cache for efficiency
- ✅ External review ready: Clear provenance trails for peer review
- ✅ Replication ready: Complete materials for independent validation

---
*Generated by Discernus Provenance Organizer v1.0*
"""
        
        readme_file = run_dir / "README.md"
        with open(readme_file, 'w') as f:
            f.write(readme_content)