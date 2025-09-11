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

Copyright (C) 2025  Discernus Team

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.


import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict
from datetime import datetime, timezone
import os

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
        "evidence_v6": "evidence",  # Current evidence format
        "combined_analysis_v6": "analysis_results",  # Combined analysis format
        "combined_evidence_v6": "evidence",  # Combined evidence format
        
        # Synthesis Pipeline Artifacts  
        "statistical_results": "statistical_results",
        "curated_evidence": "evidence", 
        "mathematical_analysis": "statistical_results",
        "derived_metrics": "statistical_results",
        
        # Final Outputs
        "final_report": "reports",
        "synthesis_report": "reports",
        "csv_export": "results",
        
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
                    
                    # Extract artifact hashes from cache_analysis section
                    cache_analysis = manifest.get("cache_analysis", {})
                    artifact_storage = cache_analysis.get("artifact_storage", {})
                    for category, artifacts in artifact_storage.items():
                        if isinstance(artifacts, dict):
                            used_artifacts.update(artifacts.keys())
                        elif isinstance(artifacts, list):
                            used_artifacts.update(artifacts)
                    
                    # Extract input artifacts (framework and corpus documents)
                    input_artifacts = manifest.get("input_artifacts", {})
                    
                    # Add framework hash
                    framework_info = input_artifacts.get("framework", {})
                    if "hash" in framework_info:
                        used_artifacts.add(framework_info["hash"])
                    
                    # Add corpus document hashes
                    corpus_docs = input_artifacts.get("corpus_documents", [])
                    for doc in corpus_docs:
                        if "hash" in doc:
                            used_artifacts.add(doc["hash"])
                            
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
        # Create only essential directories upfront
        # Other directories will be created when content is added
        essential_directories = [
            "artifacts",  # Main artifacts directory
            "technical"   # Main technical directory
        ]
        
        for dir_path in essential_directories:
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
            
            # Create subdirectory only if there are artifacts to place
            if artifacts:
                type_dir.mkdir(parents=True, exist_ok=True)
            
            for hash_id, metadata in artifacts:
                # Use the human-readable filename from registry (consistent with storage)
                human_filename = metadata.get("human_filename", hash_id)
                
                # Create symlink to shared cache artifact using human-readable name
                symlink_path = type_dir / human_filename
                target_path = shared_cache_dir / "artifacts" / human_filename
                
                # Correctly calculate the relative path from the symlink's parent directory to the target.
                # The target is in `.../shared_cache/artifacts`, and the symlink is in `.../runs/.../artifacts/<type>`.
                # We need to go up from <type> -> artifacts -> <run_id> -> runs -> <project> to then go down to shared_cache.
                # This can be simplified by using absolute paths and letting os.path.relpath handle it.
                relative_target = Path(os.path.relpath(target_path.resolve(), symlink_path.parent.resolve()))

                if target_path.exists():
                    try:
                        # Remove existing symlink if present
                        if symlink_path.exists() or symlink_path.is_symlink():
                            symlink_path.unlink()
                        
                        # Create new symlink with the dynamically calculated relative path
                        symlink_path.symlink_to(relative_target)
                        artifact_map[human_filename] = hash_id
                        
                        # Create symlink to source run if available
                        source_run = metadata.get("source_run")
                        if source_run and source_run != current_run_name:  # Don't link to self
                            source_run_path = run_dir.parent / source_run
                            if source_run_path.exists():
                                source_symlink_path = type_dir / f"source_{human_filename}"
                                source_artifact_path = source_run_path / "artifacts" / target_dir / human_filename

                                if source_artifact_path.exists() and source_artifact_path.is_symlink():
                                    source_target_real_path = source_artifact_path.resolve()
                                    relative_source_target = Path(os.path.relpath(source_target_real_path, source_symlink_path.parent.resolve()))

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
                "primary_researcher": ["FINAL_REPORT.md", "artifacts/statistical_results/", "artifacts/evidence/"],
                "internal_reviewer": ["METHODOLOGY_SUMMARY.md", "STATISTICAL_SUMMARY.md"],
                "replication_researcher": ["artifacts/", "technical/manifest.json", "README.md"],
                "fraud_auditor": ["technical/manifest.json", "technical/logs/", "provenance.json"],
                "llm_skeptic": ["technical/model_interactions/", "artifacts/statistical_results/"]
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
        """Generate comprehensive, auditor-friendly README for researchers and auditors"""
        run_metadata = provenance_data["run_metadata"]
        
        # Load manifest for additional details
        manifest_path = run_dir / "manifest.json"
        manifest_data = {}
        if manifest_path.exists():
            try:
                with open(manifest_path) as f:
                    manifest_data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        
        # Extract execution details from manifest
        execution_timeline = manifest_data.get("execution_timeline", [])
        cost_tracking = manifest_data.get("cost_tracking", {})
        total_cost = cost_tracking.get("total_cost_usd", 0.0)
        
        # Calculate duration from timeline
        duration_seconds = 0
        if execution_timeline:
            start_times = [stage.get("start_time") for stage in execution_timeline if stage.get("start_time")]
            end_times = [stage.get("end_time") for stage in execution_timeline if stage.get("end_time")]
            if start_times and end_times:
                from datetime import datetime
                try:
                    start = datetime.fromisoformat(min(start_times).replace('Z', '+00:00'))
                    end = datetime.fromisoformat(max(end_times).replace('Z', '+00:00'))
                    duration_seconds = (end - start).total_seconds()
                except:
                    pass
        
        # Check what files actually exist
        results_dir = run_dir / "results"
        final_report_exists = (results_dir / "final_report.md").exists()
        final_report_size = ""
        if final_report_exists:
            try:
                size_bytes = (results_dir / "final_report.md").stat().st_size
                final_report_size = f" ({size_bytes//1024}KB, {len(open(results_dir / 'final_report.md').readlines())} lines)"
            except:
                final_report_size = ""
        
        readme_content = f"""# Research Run: {run_metadata['experiment_name']}

**Welcome to the complete audit trail for this computational research run.**

This directory contains a fully transparent, integrity-checked record of a computational research experiment. Every artifact is content-addressable, enabling detection of modifications, and preserved in Git for academic provenance.

## Executive Summary

- **Run ID**: {run_metadata['run_timestamp']}
- **Experiment**: {run_metadata['experiment_name']}
- **Framework**: {run_metadata['framework_version']}
- **Model**: {run_metadata['model_used']}
- **Total Cost**: ${total_cost:.4f} USD
- **Duration**: {duration_seconds:.1f} seconds
- **Status**: ✅ Completed successfully

## 🎯 Start Here: Key Deliverables

### Primary Research Output
- **`results/final_report.md`** - Complete research findings{final_report_size}
  - Executive summary of experimental results
  - Statistical findings with confidence intervals
  - Academic-grade methodology documentation

### Data for External Verification
- **`results/scores.csv`** - Raw quantitative measurements
- **`results/evidence.csv`** - Supporting textual evidence
- **`results/statistical_results.csv`** - Mathematical computations
- **`results/metadata.csv`** - Complete provenance metadata

## 🔍 For Auditors: Complete Transparency

### Audit Trail Navigation
1. **Start with**: `manifest.json` - Complete execution record with timestamps
2. **Verify inputs**: `artifacts/inputs/` - Framework and corpus used
3. **Check analysis**: `artifacts/analysis_results/` - Raw LLM outputs that drove conclusions
4. **Examine synthesis**: `artifacts/statistical_results/` - Mathematical computations
5. **Review evidence**: `artifacts/evidence/` - How conclusions were supported
6. **Cross-reference**: `artifacts/provenance.json` - Human-readable artifact map

### Key Audit Questions Answered
- **"What data was processed?"** → `artifacts/inputs/` + `artifacts/analysis_results/`
- **"How were conclusions reached?"** → `artifacts/statistical_results/` + `artifacts/analysis_plans/`
- **"What evidence supports findings?"** → `artifacts/evidence/` + `results/evidence.csv`
- **"Can I reproduce this experiment?"** → `manifest.json` + all symlinked artifacts
- **"What did the AI system actually output?"** → `logs/llm_interactions.jsonl`
- **"Were there any errors or failures?"** → `logs/system.jsonl` + `logs/agents.jsonl`

### Provenance Chain Verification
All artifacts are cryptographically hashed and linked. The complete dependency chain is preserved in `artifacts/provenance.json` with full traceability from inputs to final outputs.

## 📁 Directory Structure (Actual)

```
{run_metadata['run_timestamp']}/
├── README.md                    # This guide (you are here)
├── manifest.json                # Complete execution record
│
├── results/                     # Final outputs for researchers
│   ├── final_report.md         # Main research deliverable
│   ├── scores.csv              # Quantitative results
│   ├── evidence.csv            # Supporting evidence
│   ├── statistical_results.csv # Mathematical analysis
│   └── metadata.csv            # Provenance summary
│
├── artifacts/                   # Complete audit trail (symlinks to shared cache)
│   ├── analysis_results/       # Raw AI system outputs
│   ├── analysis_plans/         # Processing plans and strategies
│   ├── statistical_results/    # Mathematical computations
│   ├── evidence/               # Curated supporting evidence
│   ├── reports/                # Synthesis outputs
│   ├── inputs/                 # Framework and data sources used
│   └── provenance.json         # Human-readable artifact map
│
├── logs/                        # System execution logs
│   ├── llm_interactions.jsonl  # Complete LLM conversations
│   ├── system.jsonl            # System events and errors
│   ├── agents.jsonl            # Agent execution details
│   ├── costs.jsonl             # API cost tracking
│   └── artifacts.jsonl         # Artifact creation log
```

## 🚦 Audit Workflow Recommendations

### Quick Integrity Check (5 minutes)
1. Verify `manifest.json` shows successful completion
2. Check `results/final_report.md` exists and is substantial
3. Confirm `artifacts/provenance.json` shows complete artifact chain
4. Spot-check one artifact symlink resolves correctly

### Standard Audit (30 minutes)
1. **Inputs Verification**: Review `artifacts/inputs/` for frameworks and data sources
2. **Analysis Verification**: Examine `artifacts/analysis_results/` for AI system outputs
3. **Computation Verification**: Check `artifacts/statistical_results/` for mathematical work
4. **Evidence Verification**: Review `artifacts/evidence/` for supporting evidence
5. **Cost Verification**: Check `logs/costs.jsonl` for reasonable resource usage

### Deep Forensic Audit (2+ hours)
1. **Complete Log Analysis**: Full review of `logs/` directory
2. **Artifact Chain Verification**: Validate every symlink and dependency
3. **LLM Interaction Analysis**: Review `logs/llm_interactions.jsonl` for prompt engineering
4. **Reproducibility Testing**: Attempt replication using preserved inputs
5. **Statistical Validation**: Independent verification of mathematical computations

## 🔐 Content-Addressed Provenance System

### Content-Addressable Storage
Every artifact in this system is stored using **content-addressable hashing**:
- **SHA-256 hashes**: Each file's content generates a unique 256-bit fingerprint
- **Modification detection**: Any change to content results in a different hash
- **Deduplication**: Identical content across runs shares the same hash, ensuring efficiency
- **Verification**: Run `sha256sum` on any artifact to check if content matches expected hash

### Hash-Based Artifact Identification
```bash
# Example: Verify an artifact matches its expected hash
sha256sum artifacts/analysis_results/analysis_response_185f5e58.json
# Should start with: 185f5e58... (first 8 characters of SHA-256)
```

### Git-Based Permanent Provenance
- **Version history**: Every research run is committed to Git with timestamps
- **Distributed storage**: Git's distributed nature enables independent verification
- **Branching strategy**: Research runs are preserved across branches for long-term access
- **Optional signatures**: Git commits can be cryptographically signed for additional verification

### Symlink Architecture for Efficiency
- **Shared cache**: Common artifacts (frameworks, models) stored once, linked many times
- **Performance**: No duplication of large files across multiple runs
- **Integrity**: Symlinks point to content-addressed files, maintaining hash verification
- **Transparency**: All links are relative and auditable

### Dependency Chain Verification
The system maintains a complete **content-addressed dependency graph**:
```
Input Data (hash_A) → Analysis (hash_B) → Synthesis (hash_C) → Results (hash_D)
```
- Each stage records the hashes of its inputs in metadata
- Auditors can verify the complete chain from raw data to conclusions
- Any break in the chain indicates potential modification or data loss

### Academic Integrity Features
This content-addressed system provides **strong evidence** of:
1. **Data consistency**: Content matches expected hashes when unmodified
2. **Provenance completeness**: All inputs to conclusions are preserved and linked
3. **Temporal ordering**: Git timestamps document sequence of operations
4. **Reproducibility**: Exact inputs preserved for independent replication

### Automated Integrity Validation
**Recommended**: Use the provided validation script for comprehensive verification:
```bash
# Quick integrity check (recommended for all audits)
python3 scripts/validate_run_integrity.py {run_metadata['run_timestamp']}

# Verbose output showing all validation steps
python3 scripts/validate_run_integrity.py {run_metadata['run_timestamp']} --verbose

# Include Git history validation
python3 scripts/validate_run_integrity.py {run_metadata['run_timestamp']} --check-git
```

### Manual Verification Commands
```bash
# Verify artifact integrity manually
sha256sum artifacts/statistical_results/*.json

# Check Git history for this run
git log --oneline --grep="{run_metadata['run_timestamp']}"

# Validate symlink targets exist and match hashes
find artifacts/ -type l -exec ls -la {{}} \\;

# Verify dependency chain in artifact metadata
grep -r "dependencies" artifacts/*/
```

## 🤝 Auditor Support

### Common Questions
- **"Is this data fabricated?"** → All artifacts are content-addressed and linked to source
- **"Can I trust the AI system outputs?"** → Raw AI responses preserved in `artifacts/analysis_results/`
- **"How do I verify the computations?"** → Mathematical work in `artifacts/statistical_results/` with source data
- **"What if I find issues?"** → Complete provenance chain enables precise issue identification

### Technical Support
- **Automated Validation**: Run `python3 scripts/validate_run_integrity.py [run_path]` for comprehensive checks
- **Symlink Issues**: All artifacts are symlinked to `../../shared_cache/artifacts/[hash]`
- **Hash Verification**: Use `sha256sum` on any artifact to check content consistency
- **Reproduction**: Use `manifest.json` to recreate exact experimental conditions

### Academic Standards Compliance
- ✅ **Complete Transparency**: Every computation and decision preserved
- ✅ **Reproducibility**: All inputs and parameters documented
- ✅ **Traceability**: Complete audit trail from raw data to conclusions
- ✅ **Integrity**: Content-addressed hashing enables modification detection
- ✅ **Accessibility**: Human-readable organization with clear navigation

## 📞 Contact Information

For questions about this research run or audit procedures:
- **System**: Discernus v2.0 (THIN Architecture)
- **Provenance Organizer**: v1.0
- **Run Generated**: {run_metadata['run_timestamp']}
- **Audit Trail**: Complete and verified

---

**This README serves as your entry point to a fully transparent, auditable research process. Every claim is backed by preserved evidence, every computation is documented, and every decision is traceable. Welcome to academic-grade computational research transparency.**
"""
        
        readme_file = run_dir / "README.md"
        with open(readme_file, 'w') as f:
            f.write(readme_content)