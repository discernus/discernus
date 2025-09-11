#!/usr/bin/env python3
"""
Input Materials Consolidator for Discernus
==========================================

Ensures all input materials (corpus files, corpus manifest, experiment specification, 
and framework) are included in the "golden run" archive for complete reproducibility.
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


import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional


class InputMaterialsConsolidator:
    """
    Consolidates all input materials into the results directory for complete reproducibility.
    
    This ensures that replication researchers have everything they need to understand
    and reproduce the experiment without external dependencies.
    """
    
    def __init__(self, run_directory: Path):
        self.run_dir = run_directory
        self.results_dir = run_directory / "outputs"
        self.experiment_path = run_directory.parent.parent  # Go up from runs/run_id to experiment root
        
    def consolidate_input_materials(self) -> Dict[str, Any]:
        """
        Consolidate all input materials into the results directory.
        
        Returns:
            Dict containing consolidation report
        """
        consolidation_report = {
            "consolidation_metadata": {
                "consolidated_at": datetime.now(timezone.utc).isoformat(),
                "run_directory": str(self.run_dir),
                "experiment_path": str(self.experiment_path),
                "consolidator_version": "1.0.0"
            },
            "corpus_materials": self._consolidate_corpus_materials(),
            "experiment_specification": self._consolidate_experiment_specification(),
            "framework_materials": self._consolidate_framework_materials(),
            "consolidation_summary": {}
        }
        
        # Generate summary
        consolidation_report["consolidation_summary"] = self._generate_consolidation_summary(consolidation_report)
        
        return consolidation_report
    
    def _consolidate_corpus_materials(self) -> Dict[str, Any]:
        """Consolidate corpus files and manifest."""
        corpus_report = {
            "corpus_files_copied": 0,
            "corpus_manifest_copied": False,
            "corpus_files": [],
            "errors": []
        }
        
        try:
            # Create corpus directory in results
            corpus_results_dir = self.results_dir / "corpus"
            corpus_results_dir.mkdir(exist_ok=True)
            
            # Copy corpus manifest
            corpus_manifest_path = self.experiment_path / "corpus.md"
            if corpus_manifest_path.exists():
                dest_manifest = corpus_results_dir / "corpus.md"
                shutil.copy2(corpus_manifest_path, dest_manifest)
                corpus_report["corpus_manifest_copied"] = True
            else:
                corpus_report["errors"].append("Corpus manifest (corpus.md) not found")
            
            # Copy corpus files
            corpus_dir = self.experiment_path / "corpus"
            if corpus_dir.exists():
                for corpus_file in corpus_dir.glob("*.txt"):
                    dest_file = corpus_results_dir / corpus_file.name
                    shutil.copy2(corpus_file, dest_file)
                    corpus_report["corpus_files_copied"] += 1
                    corpus_report["corpus_files"].append({
                        "filename": corpus_file.name,
                        "size_bytes": corpus_file.stat().st_size,
                        "copied_to": str(dest_file)
                    })
            else:
                corpus_report["errors"].append("Corpus directory not found")
                
        except Exception as e:
            corpus_report["errors"].append(f"Error consolidating corpus materials: {str(e)}")
        
        return corpus_report
    
    def _consolidate_experiment_specification(self) -> Dict[str, Any]:
        """Consolidate experiment specification file."""
        experiment_report = {
            "experiment_spec_copied": False,
            "experiment_spec_path": None,
            "errors": []
        }
        
        try:
            # Copy experiment specification
            experiment_spec_path = self.experiment_path / "experiment.md"
            if experiment_spec_path.exists():
                dest_spec = self.results_dir / "experiment.md"
                shutil.copy2(experiment_spec_path, dest_spec)
                experiment_report["experiment_spec_copied"] = True
                experiment_report["experiment_spec_path"] = str(dest_spec)
            else:
                experiment_report["errors"].append("Experiment specification (experiment.md) not found")
                
        except Exception as e:
            experiment_report["errors"].append(f"Error consolidating experiment specification: {str(e)}")
        
        return experiment_report
    
    def _consolidate_framework_materials(self) -> Dict[str, Any]:
        """Consolidate framework file."""
        framework_report = {
            "framework_copied": False,
            "framework_path": None,
            "framework_name": None,
            "errors": []
        }
        
        try:
            # Find framework file (could be named framework.md or have descriptive name)
            framework_candidates = [
                "framework.md",
                "cff_v10.md",  # Specific to this experiment
                "pdaf_v1.0.md",
                "paf_v1.0.md"
            ]
            
            framework_found = False
            for candidate in framework_candidates:
                framework_path = self.experiment_path / candidate
                if framework_path.exists():
                    dest_framework = self.results_dir / candidate
                    shutil.copy2(framework_path, dest_framework)
                    framework_report["framework_copied"] = True
                    framework_report["framework_path"] = str(dest_framework)
                    framework_report["framework_name"] = candidate
                    framework_found = True
                    break
            
            if not framework_found:
                # Try to find any .md file that might be a framework
                for md_file in self.experiment_path.glob("*.md"):
                    if md_file.name not in ["corpus.md", "experiment.md", "README.md"]:
                        dest_framework = self.results_dir / md_file.name
                        shutil.copy2(md_file, dest_framework)
                        framework_report["framework_copied"] = True
                        framework_report["framework_path"] = str(dest_framework)
                        framework_report["framework_name"] = md_file.name
                        framework_found = True
                        break
                
                if not framework_found:
                    framework_report["errors"].append("Framework file not found")
                    
        except Exception as e:
            framework_report["errors"].append(f"Error consolidating framework materials: {str(e)}")
        
        return framework_report
    
    def _generate_consolidation_summary(self, consolidation_report: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary of consolidation results."""
        summary = {
            "total_input_files": 0,
            "successfully_consolidated": 0,
            "consolidation_status": "complete",
            "missing_critical_files": [],
            "reproducibility_score": 0
        }
        
        # Count total files
        corpus_files = consolidation_report["corpus_materials"]["corpus_files_copied"]
        experiment_spec = 1 if consolidation_report["experiment_specification"]["experiment_spec_copied"] else 0
        framework = 1 if consolidation_report["framework_materials"]["framework_copied"] else 0
        corpus_manifest = 1 if consolidation_report["corpus_materials"]["corpus_manifest_copied"] else 0
        
        summary["total_input_files"] = corpus_files + experiment_spec + framework + corpus_manifest
        summary["successfully_consolidated"] = corpus_files + experiment_spec + framework + corpus_manifest
        
        # Check for missing critical files
        if not consolidation_report["corpus_materials"]["corpus_manifest_copied"]:
            summary["missing_critical_files"].append("corpus.md")
        if not consolidation_report["experiment_specification"]["experiment_spec_copied"]:
            summary["missing_critical_files"].append("experiment.md")
        if not consolidation_report["framework_materials"]["framework_copied"]:
            summary["missing_critical_files"].append("framework file")
        
        # Calculate reproducibility score
        if summary["missing_critical_files"]:
            summary["consolidation_status"] = "incomplete"
            summary["reproducibility_score"] = max(0, 100 - (len(summary["missing_critical_files"]) * 25))
        else:
            summary["reproducibility_score"] = 100
        
        return summary
    
    def save_consolidation_report(self, output_path: Optional[Path] = None) -> Path:
        """
        Save consolidation report to file.
        
        Args:
            output_path: Optional path to save the report
            
        Returns:
            Path to the saved report file
        """
        if output_path is None:
            output_path = self.results_dir / "input_materials_consolidation.json"
        
        consolidation_report = self.consolidate_input_materials()
        
        import json
        with open(output_path, 'w') as f:
            json.dump(consolidation_report, f, indent=2, default=str)
        
        return output_path


def consolidate_input_materials(run_directory: Path, output_path: Optional[Path] = None) -> Path:
    """
    Convenience function to consolidate input materials for a single run.
    
    Args:
        run_directory: Path to the experiment run directory
        output_path: Optional path to save the consolidation report
        
    Returns:
        Path to the saved consolidation report file
    """
    consolidator = InputMaterialsConsolidator(run_directory)
    return consolidator.save_consolidation_report(output_path)
