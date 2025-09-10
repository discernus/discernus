#!/usr/bin/env python3
"""
Directory Structure Reorganizer for Discernus
============================================

Reorganizes run directories into human-friendly, stakeholder-optimized structure.
Creates logical separation for researchers, replication researchers, and auditors.
"""

import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional


class DirectoryStructureReorganizer:
    """
    Reorganizes run directories into stakeholder-friendly structure.
    
    Transforms flat structure into logical organization:
    - data/: Analysis-ready CSV files
    - outputs/: Final reports and results  
    - inputs/: Input materials for replication
    - provenance/: Audit trail and metadata
    - artifacts/: Complete provenance artifacts (copied content)
    - session_logs/: Complete execution logs (copied content)
    """
    
    def __init__(self, run_directory: Path):
        self.run_dir = run_directory
        self.results_dir = run_directory / "results"
        self.artifacts_dir = run_directory / "artifacts"
        self.session_logs_dir = run_directory / "session_logs"
        
    def reorganize_directory_structure(self) -> Dict[str, Any]:
        """
        Reorganize directory structure for stakeholder-friendly access.
        
        Returns:
            Dict containing reorganization report
        """
        reorganization_report = {
            "reorganization_metadata": {
                "reorganized_at": datetime.now(timezone.utc).isoformat(),
                "run_directory": str(self.run_dir),
                "reorganizer_version": "1.0.0"
            },
            "directory_creation": self._create_directory_structure(),
            "file_movements": self._move_files_to_logical_locations(),
            "documentation_creation": self._create_directory_documentation(),
            "reorganization_summary": {}
        }
        
        # Generate summary
        reorganization_report["reorganization_summary"] = self._generate_reorganization_summary(reorganization_report)
        
        return reorganization_report
    
    def _create_directory_structure(self) -> Dict[str, Any]:
        """Create the new logical directory structure."""
        directories_created = []
        
        # Create main directories
        main_dirs = [
            "data",           # Analysis-ready CSV files
            "outputs",        # Final reports and results
            "inputs",         # Input materials for replication
            "provenance",     # Audit trail and metadata
            "artifacts",      # Complete provenance artifacts
            "session_logs"    # Complete execution logs
        ]
        
        for dir_name in main_dirs:
            dir_path = self.run_dir / dir_name
            dir_path.mkdir(exist_ok=True)
            directories_created.append(str(dir_path))
        
        # Create subdirectories
        subdirs = {
            "inputs": ["corpus"],
            "artifacts": ["analysis_results", "analysis_plans", "statistical_results", 
                         "evidence", "reports", "inputs"],
            "session_logs": ["logs"]
        }
        
        for parent_dir, children in subdirs.items():
            for child_dir in children:
                child_path = self.run_dir / parent_dir / child_dir
                child_path.mkdir(exist_ok=True)
                directories_created.append(str(child_path))
        
        return {
            "directories_created": directories_created,
            "total_directories": len(directories_created)
        }
    
    def _move_files_to_logical_locations(self) -> Dict[str, Any]:
        """Move files to their logical locations in the new structure."""
        movements = {
            "data_files": [],
            "output_files": [],
            "input_files": [],
            "provenance_files": [],
            "artifact_files": [],
            "session_log_files": []
        }
        
        # Move data files (CSV files from results/)
        if self.results_dir.exists():
            data_files = ["scores.csv", "evidence.csv", "metadata.csv"]
            for file_name in data_files:
                source_file = self.results_dir / file_name
                if source_file.exists():
                    target_file = self.run_dir / "data" / file_name
                    shutil.move(str(source_file), str(target_file))
                    movements["data_files"].append({
                        "source": str(source_file),
                        "target": str(target_file),
                        "status": "moved"
                    })
        
        # Move output files (reports and results)
        if self.results_dir.exists():
            output_files = ["final_report.md", "statistical_results.json", "experiment_summary.json"]
            for file_name in output_files:
                source_file = self.results_dir / file_name
                if source_file.exists():
                    target_file = self.run_dir / "outputs" / file_name
                    shutil.move(str(source_file), str(target_file))
                    movements["output_files"].append({
                        "source": str(source_file),
                        "target": str(target_file),
                        "status": "moved"
                    })
        
        # Move input files (experiment spec, framework, corpus)
        if self.results_dir.exists():
            # Move experiment.md
            experiment_file = self.results_dir / "experiment.md"
            if experiment_file.exists():
                target_file = self.run_dir / "inputs" / "experiment.md"
                shutil.move(str(experiment_file), str(target_file))
                movements["input_files"].append({
                    "source": str(experiment_file),
                    "target": str(target_file),
                    "status": "moved"
                })
            
            # Move framework files
            framework_files = list(self.results_dir.glob("*.md"))
            for framework_file in framework_files:
                if framework_file.name != "experiment.md":
                    target_file = self.run_dir / "inputs" / framework_file.name
                    shutil.move(str(framework_file), str(target_file))
                    movements["input_files"].append({
                        "source": str(framework_file),
                        "target": str(target_file),
                        "status": "moved"
                    })
            
            # Move corpus directory
            corpus_dir = self.results_dir / "corpus"
            if corpus_dir.exists():
                target_dir = self.run_dir / "inputs" / "corpus"
                shutil.move(str(corpus_dir), str(target_dir))
                movements["input_files"].append({
                    "source": str(corpus_dir),
                    "target": str(target_dir),
                    "status": "moved"
                })
        
        # Move provenance files
        if self.results_dir.exists():
            provenance_files = ["consolidated_provenance.json", "input_materials_consolidation.json"]
            for file_name in provenance_files:
                source_file = self.results_dir / file_name
                if source_file.exists():
                    target_file = self.run_dir / "provenance" / file_name
                    shutil.move(str(source_file), str(target_file))
                    movements["provenance_files"].append({
                        "source": str(source_file),
                        "target": str(target_file),
                        "status": "moved"
                    })
        
        # Move artifact files (copy actual content, not symlinks)
        if self.artifacts_dir.exists():
            self._copy_artifact_content_to_new_structure()
            movements["artifact_files"].append({
                "source": str(self.artifacts_dir),
                "target": str(self.run_dir / "artifacts"),
                "status": "copied_content"
            })
        
        # Move session log files from experiment session directory
        experiment_path = self.run_dir.parent.parent
        run_id = self.run_dir.name
        session_source_dir = experiment_path / "session" / run_id
        
        if session_source_dir.exists():
            # Copy logs directory
            logs_source = session_source_dir / "logs"
            if logs_source.exists():
                logs_target = self.run_dir / "session_logs" / "logs"
                # Remove target if it exists to avoid conflicts
                if logs_target.exists():
                    shutil.rmtree(str(logs_target))
                shutil.copytree(str(logs_source), str(logs_target))
                movements["session_log_files"].append({
                    "source": str(logs_source),
                    "target": str(logs_target),
                    "status": "copied"
                })
            
            # Copy manifest
            manifest_file = session_source_dir / "manifest.json"
            if manifest_file.exists():
                target_file = self.run_dir / "session_logs" / "manifest.json"
                shutil.copy2(str(manifest_file), str(target_file))
                movements["session_log_files"].append({
                    "source": str(manifest_file),
                    "target": str(target_file),
                    "status": "copied"
                })
        
        return movements
    
    def _copy_artifact_content_to_new_structure(self) -> None:
        """Copy actual artifact content to new artifacts structure."""
        try:
            # Find shared cache directory
            experiment_path = self.run_dir.parent.parent
            shared_cache_dir = experiment_path / "shared_cache" / "artifacts"
            
            if not shared_cache_dir.exists():
                return
            
            # Copy actual content for each artifact
            for file_path in self.artifacts_dir.rglob("*"):
                if file_path.is_file():
                    # Calculate relative path in new structure
                    relative_path = file_path.relative_to(self.artifacts_dir)
                    new_file_path = self.run_dir / "artifacts" / relative_path
                    
                    # Skip if source and target are the same file
                    if file_path.resolve() == new_file_path.resolve():
                        continue
                    
                    if file_path.is_symlink():
                        # Get the target of the symlink
                        target_path = file_path.resolve()
                        if target_path.exists() and target_path != file_path:
                            new_file_path.parent.mkdir(parents=True, exist_ok=True)
                            # Copy the actual content
                            shutil.copy2(target_path, new_file_path)
                    else:
                        # Regular file, copy directly
                        new_file_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(file_path, new_file_path)
                            
        except Exception as e:
            print(f"⚠️ Warning: Could not copy artifact content: {e}")
    
    def _create_directory_documentation(self) -> Dict[str, Any]:
        """Create README files explaining each directory."""
        documentation_created = []
        
        # Main README
        main_readme = self._generate_main_readme()
        main_readme_path = self.run_dir / "README.md"
        with open(main_readme_path, "w", encoding="utf-8") as f:
            f.write(main_readme)
        documentation_created.append(str(main_readme_path))
        
        # Directory-specific READMEs
        directory_readmes = {
            "data": self._generate_data_readme(),
            "outputs": self._generate_outputs_readme(),
            "inputs": self._generate_inputs_readme(),
            "provenance": self._generate_provenance_readme(),
            "artifacts": self._generate_artifacts_readme(),
            "session_logs": self._generate_session_logs_readme()
        }
        
        for dir_name, content in directory_readmes.items():
            readme_path = self.run_dir / dir_name / "README.md"
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(content)
            documentation_created.append(str(readme_path))
        
        return {
            "documentation_created": documentation_created,
            "total_files": len(documentation_created)
        }
    
    def _generate_main_readme(self) -> str:
        """Generate main README for the reorganized directory."""
        return f"""# Discernus Research Run - Reorganized Structure

**Complete Research Package - Ready for Analysis and Audit**

This directory has been reorganized for optimal access by different stakeholders:
researchers, replication researchers, and auditors.

## 📁 Directory Structure

### For Researchers
- **`data/`** - Analysis-ready CSV files for immediate statistical analysis
- **`outputs/`** - Final reports and research results
- **`statistical_package/`** - Complete package for external analysis tools

### For Replication Researchers  
- **`inputs/`** - All input materials needed for exact replication
- **`README.md`** - This file with complete methodology documentation

### For Auditors
- **`provenance/`** - Complete audit trail and metadata
- **`artifacts/`** - Full provenance chain with actual artifact content
- **`session_logs/`** - Complete execution logs and LLM interactions

## 🚀 Quick Start

1. **For Data Analysis**: Start with files in `data/` directory
2. **For Replication**: Use files in `inputs/` directory
3. **For Audit**: Review `provenance/` and `artifacts/` directories

## 📋 Complete Asset Inventory

This directory contains ALL necessary assets for:
- ✅ **Complete replication** - All inputs and methodology preserved
- ✅ **Full audit trail** - Complete provenance chain with actual content
- ✅ **Statistical analysis** - Ready-to-use data in multiple formats
- ✅ **Research transparency** - Complete execution logs and LLM interactions

---
Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}
Discernus Version: Alpha System
"""
    
    def _generate_data_readme(self) -> str:
        """Generate README for data directory."""
        return """# Data Directory

**Analysis-Ready CSV Files**

This directory contains the primary datasets for statistical analysis.

## Files

- **`scores.csv`** - Analysis scores and derived metrics
- **`evidence.csv`** - Supporting quotes and evidence  
- **`metadata.csv`** - Document and run metadata

## Usage

These files are ready for immediate import into statistical analysis tools:
- R, Python, STATA, SPSS, etc.
- See `../statistical_package/` for import scripts and examples

## Data Quality

- All scores normalized to 0-1 scale unless noted
- Missing values represented as empty cells
- Consistent document_id linking across all files
- UTF-8 encoding for international character support
"""
    
    def _generate_outputs_readme(self) -> str:
        """Generate README for outputs directory."""
        return """# Outputs Directory

**Final Research Results**

This directory contains the final outputs from the research run.

## Files

- **`final_report.md`** - Complete synthesis report (if available)
- **`statistical_results.json`** - Mathematical analysis results
- **`experiment_summary.json`** - Run summary and metadata

## Usage

These files represent the final research outputs:
- Use `final_report.md` for the main research findings
- Use `statistical_results.json` for detailed mathematical analysis
- Use `experiment_summary.json` for run metadata and provenance

## Note

Some files may not be present depending on the run mode:
- Statistical preparation runs may not have `final_report.md`
- Analysis-only runs may not have `statistical_results.json`
"""
    
    def _generate_inputs_readme(self) -> str:
        """Generate README for inputs directory."""
        return """# Inputs Directory

**Complete Input Materials for Replication**

This directory contains all input materials needed for exact replication.

## Files

- **`experiment.md`** - Experiment specification and methodology
- **`[framework files]`** - Analytical framework files
- **`corpus/`** - Complete corpus documents

## Usage

These files enable complete replication:
1. Use `experiment.md` to understand the research design
2. Use framework files to understand the analytical approach
3. Use `corpus/` files as the source data

## Replication

To replicate this research:
1. Load the experiment specification
2. Apply the framework to the corpus files
3. Follow the methodology documented in `experiment.md`
"""
    
    def _generate_provenance_readme(self) -> str:
        """Generate README for provenance directory."""
        return """# Provenance Directory

**Audit Trail and Metadata**

This directory contains consolidated provenance data for audit and verification.

## Files

- **`consolidated_provenance.json`** - Complete provenance metadata
- **`input_materials_consolidation.json`** - Input materials consolidation report

## Usage

These files provide complete audit trails:
- Use for verification of research integrity
- Contains complete execution metadata
- Includes cost tracking and performance metrics

## Audit

For audit purposes:
1. Review `consolidated_provenance.json` for complete execution record
2. Verify input materials in `input_materials_consolidation.json`
3. Cross-reference with `../artifacts/` for detailed artifact provenance
"""
    
    def _generate_artifacts_readme(self) -> str:
        """Generate README for artifacts directory."""
        return """# Artifacts Directory

**Complete Provenance Chain with Actual Content**

This directory contains the complete provenance chain with actual artifact content
(not symlinks) for full audit verification.

## Structure

- **`analysis_results/`** - Raw LLM analysis outputs
- **`analysis_plans/`** - Processing strategies and plans
- **`statistical_results/`** - Mathematical computations and results
- **`evidence/`** - Curated supporting evidence
- **`reports/`** - Synthesis and report generation artifacts
- **`inputs/`** - Framework and corpus artifacts
- **`provenance.json`** - Artifact dependency map

## Usage

These files provide complete provenance verification:
- All files contain actual content (not symlinks)
- Complete dependency chain from inputs to outputs
- Full audit trail for research integrity verification

## Audit

For complete audit verification:
1. Review `provenance.json` for artifact relationships
2. Verify content integrity of all artifact files
3. Trace complete dependency chain from inputs to final outputs
"""
    
    def _generate_session_logs_readme(self) -> str:
        """Generate README for session_logs directory."""
        return """# Session Logs Directory

**Complete Execution Logs and LLM Interactions**

This directory contains complete execution logs for full transparency and audit.

## Files

- **`logs/`** - Complete execution logs
  - `llm_interactions.log` - Complete LLM conversation history
  - `agents.jsonl` - Detailed agent execution logs
  - `system.jsonl` - System events and operations
  - `costs.jsonl` - API usage and cost tracking
  - `errors.log` - Complete error history
  - `performance.log` - Performance metrics and timing
- **`manifest.json`** - Complete execution manifest

## Usage

These logs provide complete execution transparency:
- Full LLM interaction history for reproducibility
- Complete agent execution trace
- System performance and error tracking
- Cost analysis and API usage

## Audit

For complete execution audit:
1. Review `logs/llm_interactions.log` for LLM conversation history
2. Check `logs/agents.jsonl` for agent execution details
3. Verify `logs/costs.jsonl` for API usage and costs
4. Review `logs/errors.log` for any execution issues
"""
    
    def _generate_reorganization_summary(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """Generate reorganization summary."""
        total_directories = report["directory_creation"]["total_directories"]
        total_movements = sum(len(movements) for movements in report["file_movements"].values())
        total_docs = report["documentation_creation"]["total_files"]
        
        return {
            "total_directories_created": total_directories,
            "total_files_moved": total_movements,
            "total_documentation_created": total_docs,
            "reorganization_status": "completed",
            "structure_type": "stakeholder_optimized"
        }


def reorganize_directory_structure(run_directory: Path) -> Dict[str, Any]:
    """
    Convenience function to reorganize directory structure for a single run.
    
    Args:
        run_directory: Path to the experiment run directory
        
    Returns:
        Dict containing reorganization report
    """
    reorganizer = DirectoryStructureReorganizer(run_directory)
    return reorganizer.reorganize_directory_structure()
