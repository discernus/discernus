#!/usr/bin/env python3
"""
Experiment Package Generator
Creates standardized, self-contained experiment packages for reproducible research.

Usage:
    python scripts/create_experiment_package.py <experiment_id> [--template=<template>]
    
Examples:
    python scripts/create_experiment_package.py mft_validation_study_20250618
    python scripts/create_experiment_package.py civic_virtue_reliability_study --template=multi_llm
"""

import os
import json
import argparse
from datetime import datetime
from pathlib import Path
import shutil

class ExperimentPackageGenerator:
    """Generates standardized experiment packages for reproducible research."""
    
    def __init__(self, base_dir: str = "experiments"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        
    def create_package(self, experiment_id: str, template: str = "basic", 
                      framework: str = None, description: str = None):
        """Create a complete experiment package with standardized structure."""
        
        package_dir = self.base_dir / experiment_id
        if package_dir.exists():
            raise ValueError(f"Experiment package {experiment_id} already exists")
            
        print(f"Creating experiment package: {experiment_id}")
        
        # Create directory structure
        self._create_directory_structure(package_dir)
        
        # Generate core documentation
        self._create_readme(package_dir, experiment_id, framework, description)
        self._create_corpus_manifest(package_dir, experiment_id, framework)
        self._create_metadata_files(package_dir, experiment_id, framework)
        
        # Create template-specific files
        if template == "multi_llm":
            self._create_multi_llm_config(package_dir, experiment_id, framework)
        elif template == "single_llm":
            self._create_single_llm_config(package_dir, experiment_id, framework)
        else:
            self._create_basic_config(package_dir, experiment_id, framework)
            
        print(f"✅ Experiment package created: {package_dir}")
        print(f"📁 Next steps:")
        print(f"   1. Edit inputs/experiment_config.yaml")
        print(f"   2. Add corpus files to inputs/corpus/")
        print(f"   3. Run: python scripts/comprehensive_experiment_orchestrator.py {package_dir}/inputs/experiment_config.yaml")
        
    def _create_directory_structure(self, package_dir: Path):
        """Create the standardized directory structure."""
        directories = [
            "inputs",
            "inputs/corpus", 
            "outputs",
            "analysis",
            "analysis/visualizations",
            "documentation",
            "metadata"
        ]
        
        for dir_name in directories:
            (package_dir / dir_name).mkdir(parents=True, exist_ok=True)
            
    def _create_readme(self, package_dir: Path, experiment_id: str, 
                      framework: str, description: str):
        """Generate comprehensive README documentation."""
        
        framework_name = framework or "Framework_Name"
        description_text = description or "Experiment description here"
        date_str = datetime.now().strftime("%B %d, %Y")
        
        readme_content = f"""# {experiment_id.replace('_', ' ').title()}
**Experiment ID**: `{experiment_id}`  
**Date**: {date_str}  
**Status**: Planning  
**Framework**: {framework_name}  
**LLM Provider**: TBD  

## Overview

{description_text}

## Experimental Design

### Corpus Composition
- **Category 1**: Description and expected outcomes
- **Category 2**: Description and expected outcomes  
- **Controls**: Validation texts

### Hypotheses Tested

**H1: Primary Hypothesis**  
Description of main hypothesis being tested.
- Test: Statistical method to be used

**H2: Secondary Hypothesis**  
Description of secondary hypothesis.
- Test: Statistical method to be used

### Execution Parameters
- **LLM Model**: To be determined
- **Estimated Cost**: TBD
- **Expected Duration**: TBD
- **Quality Control**: Confidence thresholds and validation

## Directory Structure

```
{experiment_id}/
├── inputs/                           # Experiment inputs
│   ├── experiment_config.yaml            # Experiment definition
│   ├── corpus_manifest.json              # Input texts metadata
│   └── corpus/                            # Text files organized by category
├── outputs/                          # Raw experiment outputs  
│   ├── final_results.json                 # Complete analysis results
│   ├── intermediate_results.json          # Processing intermediate data
│   └── results.csv                        # Tabular results summary
├── analysis/                         # Statistical analysis
│   ├── analysis_report.json              # Hypothesis testing results
│   ├── analysis_script.py                # Analysis script
│   └── visualizations/                   # Generated charts
├── documentation/                    # Study documentation
│   ├── methodology.md                     # Detailed methodology
│   ├── statistical_analysis_plan.md      # Pre-registered analysis plan
│   └── results_interpretation.md          # Results discussion
└── metadata/                         # Experiment metadata
    ├── experiment_log.json                # Execution log
    ├── system_info.json                   # Technical environment
    └── reproducibility_info.json          # Reproduction instructions
```

## Reproduction Instructions

### Prerequisites
- Python 3.9+ with narrative_gravity package installed
- API key for chosen LLM provider
- PostgreSQL database with narrative_gravity schema

### Execution Steps
1. **Setup Environment**: `cd narrative_gravity_analysis && source venv/bin/activate`
2. **Configure Experiment**: Edit `inputs/experiment_config.yaml`
3. **Add Corpus**: Place text files in `inputs/corpus/` organized by category
4. **Run Orchestrator**: `python3 scripts/comprehensive_experiment_orchestrator.py inputs/experiment_config.yaml`
5. **Generate Analysis**: `python3 analysis/analysis_script.py outputs/final_results.json`
6. **View Results**: Open generated HTML report in browser

## Data Availability

All raw data, processed results, and analysis scripts are included in this package for full reproducibility.

## Citation

If using this experiment or its methodology, please cite:
```
{experiment_id.replace('_', ' ').title()} (2025). Narrative Gravity Analysis Project. 
Experiment ID: {experiment_id}.
```
"""
        
        with open(package_dir / "README.md", "w") as f:
            f.write(readme_content)
            
    def _create_corpus_manifest(self, package_dir: Path, experiment_id: str, framework: str):
        """Create corpus manifest template."""
        
        manifest = {
            "corpus_name": f"{experiment_id.replace('_', ' ').title()} Corpus",
            "experiment_id": experiment_id,
            "framework": framework or "Framework_Name",
            "total_texts": 0,
            "creation_date": datetime.now().strftime("%Y-%m-%d"),
            "validation_purpose": "Describe validation goals",
            
            "categories": {
                "category_1": {
                    "description": "Description of first category",
                    "expected_scores": {
                        "dimension_1": "> 0.6",
                        "dimension_2": "< 0.4"
                    },
                    "text_count": 0,
                    "example_authors": ["Author 1", "Author 2"]
                }
            },
            
            "corpus_construction": {
                "selection_criteria": [
                    "Criterion 1",
                    "Criterion 2"
                ],
                "exclusion_criteria": [
                    "Exclusion 1",
                    "Exclusion 2" 
                ],
                "validation_strategy": {
                    "expert_review": "Review process description",
                    "quality_controls": "Quality control measures"
                }
            }
        }
        
        with open(package_dir / "inputs" / "corpus_manifest.json", "w") as f:
            json.dump(manifest, f, indent=2)
            
    def _create_metadata_files(self, package_dir: Path, experiment_id: str, framework: str):
        """Create metadata file templates."""
        
        # Experiment log template
        experiment_log = {
            "experiment_id": experiment_id,
            "experiment_name": experiment_id.replace('_', ' ').title(),
            "execution_date": "TBD",
            "status": "PLANNING", 
            "framework": framework or "Framework_Name",
            "execution_summary": {
                "total_analyses": 0,
                "successful_analyses": 0,
                "failed_analyses": 0,
                "success_rate": "TBD",
                "total_api_cost": 0.0
            }
        }
        
        # Reproducibility info template
        reproducibility_info = {
            "experiment_id": experiment_id,
            "reproducibility_level": "FULL",
            "verification_status": "PENDING",
            "reproduction_requirements": {
                "software_dependencies": {
                    "python": ">=3.9",
                    "packages": {
                        "narrative_gravity": "latest",
                        "pandas": ">=1.5.0",
                        "numpy": ">=1.20.0"
                    }
                },
                "api_requirements": {
                    "provider": "TBD",
                    "estimated_cost": "TBD"
                }
            },
            "exact_reproduction_steps": [
                {
                    "step": 1,
                    "description": "Environment Setup",
                    "commands": ["cd narrative_gravity_analysis", "source venv/bin/activate"]
                }
            ]
        }
        
        metadata_dir = package_dir / "metadata"
        with open(metadata_dir / "experiment_log.json", "w") as f:
            json.dump(experiment_log, f, indent=2)
            
        with open(metadata_dir / "reproducibility_info.json", "w") as f:
            json.dump(reproducibility_info, f, indent=2)
            
    def _create_basic_config(self, package_dir: Path, experiment_id: str, framework: str):
        """Create basic experiment configuration."""
        
        config = {
            "experiment_id": experiment_id,
            "experiment_name": experiment_id.replace('_', ' ').title(),
            "framework": framework or "framework_name",
            "llm_provider": "openai",
            "model": "gpt-4o",
            "corpus_source": "validation_set",
            "quality_controls": {
                "confidence_threshold": 0.8,
                "max_retries": 3
            },
            "output_formats": ["json", "csv"],
            "analysis_pipeline": {
                "statistical_testing": True,
                "visualization_generation": True,
                "html_report": True
            }
        }
        
        with open(package_dir / "inputs" / "experiment_config.yaml", "w") as f:
            import yaml
            yaml.dump(config, f, default_flow_style=False, indent=2)


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(description="Generate standardized experiment packages")
    parser.add_argument("experiment_id", help="Unique experiment identifier")
    parser.add_argument("--template", choices=["basic", "single_llm", "multi_llm"], 
                       default="basic", help="Experiment template type")
    parser.add_argument("--framework", help="Framework name (optional)")
    parser.add_argument("--description", help="Experiment description (optional)")
    parser.add_argument("--base-dir", default="experiments", help="Base directory for experiments")
    
    args = parser.parse_args()
    
    try:
        generator = ExperimentPackageGenerator(args.base_dir)
        generator.create_package(
            experiment_id=args.experiment_id,
            template=args.template,
            framework=args.framework, 
            description=args.description
        )
    except Exception as e:
        print(f"❌ Error creating experiment package: {e}")
        return 1
        
    return 0


if __name__ == "__main__":
    exit(main()) 