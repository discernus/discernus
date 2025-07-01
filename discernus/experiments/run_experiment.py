#!/usr/bin/env python3
"""
Simple Experiment Runner for Discernus Reboot
=============================================

Executes experiments based on YAML configuration files without requiring
manual curl commands or ad-hoc parameter construction.

Usage:
    python3 run_experiment.py experiment_config.yaml

Examples:
    python3 run_experiment.py flagship_model_statistical_comparison.yaml
    python3 run_experiment.py reboot_mft_experiment.yaml
"""

import sys
import asyncio
import yaml
import json
import aiohttp
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime

# Configure logging
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import validation system
from discernus.validation import ExperimentValidator, ValidationError

# Import LLM gateway and coordinate calculation
from discernus.gateway.llm_gateway import get_llm_analysis
from discernus.engine.signature_engine import calculate_coordinates

# 🎯 Import DCS Metrics System for validation
from discernus.metrics import (
    validate_hybrid_architecture,
    validate_framework_v32_compliance,
    calculate_framework_fitness_score,
    validate_brazil_2018_specific_requirements
)


class ExperimentRunner:
    """
    Clean experiment execution based on YAML configuration.
    
    Implements the architectural decision to move from implicit curl commands
    to explicit YAML-driven experiment execution.
    """
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def __aenter__(self):
        # Set longer timeout for corpus-based experiments that can take 20+ minutes
        timeout = aiohttp.ClientTimeout(total=30*60)  # 30 minutes
        self.session = aiohttp.ClientSession(timeout=timeout)
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def execute_experiment(self, yaml_path: str) -> Dict[str, Any]:
        """
        Execute experiment based on YAML configuration.
        
        Args:
            yaml_path: Path to experiment YAML file
            
        Returns:
            Experiment results dictionary
        """
        # Load experiment definition
        experiment_def = self._load_experiment_definition(yaml_path)
        
        # Determine experiment type and route accordingly
        experiment_meta = experiment_def.get('experiment_meta', {})
        study_design = experiment_meta.get('study_design', {})
        comparison_type = study_design.get('comparison_type')
        
        logger.info(f"🚀 Starting experiment: {experiment_meta.get('display_name', 'Unknown')}")
        logger.info(f"📊 Comparison type: {comparison_type}")
        
        if comparison_type == 'multi_model':
            return await self._execute_multi_model_comparison(experiment_def, yaml_path)
        else:
            raise ValueError(f"Unsupported comparison type: {comparison_type}")
    
    def _load_experiment_definition(self, yaml_path: str) -> Dict[str, Any]:
        """Load and validate experiment definition from YAML file"""
        yaml_file = Path(yaml_path)
        
        if not yaml_file.exists():
            # Try relative to experiments directory
            experiments_dir = Path(__file__).parent
            yaml_file = experiments_dir / yaml_path
            
        if not yaml_file.exists():
            raise FileNotFoundError(f"Experiment file not found: {yaml_path}")
        
        logger.info(f"📋 Loading experiment: {yaml_file}")
        
        with open(yaml_file, 'r') as f:
            experiment_def = yaml.safe_load(f)
        
        # SPEC VALIDATION: Validate experiment and embedded framework
        logger.info("🔍 Validating experiment specification compliance...")
        
        try:
            validator = ExperimentValidator()
            validated_experiment = validator.validate_experiment(
                experiment_def, 
                experiment_file_path=str(yaml_file)
            )
            
            # Extract validation results for logging
            anchors = validator.get_framework_anchors(experiment_def)
            anchor_count = len(anchors)
            framework_name = experiment_def['framework']['name']
            
            logger.info(f"✅ Experiment validation passed")
            logger.info(f"✅ Framework '{framework_name}' validation passed")
            logger.info(f"📊 Extracted {anchor_count} anchors: {list(anchors.keys())}")
            
            # 🎯 DCS METRICS VALIDATION: Mathematical foundation validation
            logger.info("📊 Running DCS metrics validation...")
            
            framework_config = experiment_def.get('framework', {})
            
            # Component registry and architecture validation
            hybrid_validation = validate_hybrid_architecture(framework_config)
            v32_compliance = validate_framework_v32_compliance(framework_config)
            
            if hybrid_validation.get('framework_valid', False):
                logger.info("✅ DCS hybrid architecture validation passed")
            else:
                logger.warning(f"⚠️ DCS hybrid architecture issues: {hybrid_validation.get('overall_errors', [])}")
            
            if v32_compliance.get('v32_compliant', False):
                logger.info("✅ Framework Specification v3.2 compliance passed")
                logger.info(f"📊 Compliance score: {v32_compliance.get('compliance_score', 0):.1%}")
            else:
                logger.warning(f"⚠️ v3.2 compliance issues: {v32_compliance.get('compliance_errors', [])}")
            
            # Brazil 2018 specific validation (if applicable)
            if 'brazil' in framework_name.lower() or 'tension' in framework_name.lower():
                brazil_validation = validate_brazil_2018_specific_requirements({
                    'framework_config': framework_config,
                    'signatures': []  # Will validate structure only
                })
                
                if brazil_validation.get('brazil_2018_compliant', False):
                    logger.info("✅ Brazil 2018 framework requirements passed")
                    logger.info(f"📊 Brazil compliance: {brazil_validation.get('compliance_score', 0):.1%}")
                else:
                    logger.warning(f"⚠️ Brazil 2018 specific issues detected")
            
            # Store validation results in experiment definition for Stage 6
            validated_experiment['_dcs_validation'] = {
                'hybrid_architecture': hybrid_validation,
                'v32_compliance': v32_compliance,
                'brazil_2018_validation': brazil_validation if 'brazil_validation' in locals() else None,
                'validation_timestamp': datetime.now().isoformat()
            }
            
            logger.info("✅ DCS metrics validation complete")
            
            return validated_experiment
            
        except ValidationError as e:
            logger.error(f"❌ Validation failed: {e}")
            raise ValueError(f"Experiment validation failed: {e}")
        
        return experiment_def
    
    async def _execute_multi_model_comparison(self, experiment_def: Dict[str, Any], yaml_path: str) -> Dict[str, Any]:
        """Execute multi-model statistical comparison"""
        
        # Extract configuration
        models_config = experiment_def.get('models', {})
        corpus_config = experiment_def.get('corpus')
        statistical_config = experiment_def.get('statistical_analysis', {})
        
        # Resolve the YAML file path (same logic as _load_experiment_definition)
        yaml_file = Path(yaml_path)
        if not yaml_file.exists():
            experiments_dir = Path(__file__).parent
            yaml_file = experiments_dir / yaml_path
        
        # Build request payload with resolved path
        request_payload = {
            "comparison_type": "multi_model",
            "experiment_file_path": str(yaml_file.resolve()),
            "statistical_methods": self._extract_statistical_methods(statistical_config)
        }
        
        # Add models if specified
        enabled_models = self._extract_enabled_models(models_config)
        if enabled_models:
            request_payload["models"] = enabled_models
            
        logger.info(f"🔬 Models to compare: {', '.join(enabled_models)}")
        logger.info(f"📈 Statistical methods: {', '.join(request_payload['statistical_methods'])}")
        
        if corpus_config:
            total_texts = self._estimate_corpus_size(corpus_config)
            total_analyses = len(enabled_models) * total_texts
            logger.info(f"📚 Corpus-based analysis: ~{total_texts} texts × {len(enabled_models)} models = {total_analyses} analyses")
        
        # DIRECT DATA COLLECTION: Process corpus with LLM calls
        logger.info("🎯 Executing corpus processing with LLM analysis...")
        
        # Process corpus and generate real results
        result = await self._process_corpus_with_llms(experiment_def, enabled_models)
        
        logger.info("✅ Corpus processing completed with real LLM data")
        logger.info("📊 All statistical analysis deferred to Stage 6 notebooks as intended")
            
        logger.info(f"✅ Experiment complete! Job ID: {result.get('job_id', 'unknown')}")
        
        # Display results summary
        self._display_results_summary(result, experiment_def)
        
        return result
    
    def _extract_statistical_methods(self, statistical_config: Dict[str, Any]) -> list:
        """Extract enabled statistical methods from configuration"""
        # STRATEGIC DECISION: Defer all statistical analysis to Stage 6 notebooks
        # Statistical configuration is preserved in YAML for experimental context
        # but not executed during runtime for better research workflow flexibility
        return []
    
    def _extract_enabled_models(self, models_config: Dict[str, Any]) -> list:
        """Extract enabled models from configuration"""
        flagship_models = models_config.get('flagship_models', {})
        enabled_models = []
        
        for model_key, model_info in flagship_models.items():
            if model_info.get('enabled', True):  # Default to enabled
                enabled_models.append(model_info['model_id'])
        
        return enabled_models
    
    def _estimate_corpus_size(self, corpus_config: Dict[str, Any]) -> int:
        """Estimate number of texts in corpus"""
        file_path = corpus_config.get('file_path')
        pattern = corpus_config.get('pattern', '*.txt')
        
        if not file_path:
            return 0
            
        # Resolve path relative to project root  
        corpus_path = Path(file_path)
        if not corpus_path.is_absolute():
            # Find project root (look for discernus directory)
            current = Path.cwd()
            project_root = current
            while project_root.parent != project_root:
                if (project_root / 'discernus').exists():
                    break
                project_root = project_root.parent
            corpus_path = project_root / file_path
            
        if not corpus_path.exists():
            return 0
            
        text_files = list(corpus_path.glob(pattern))
        return len(text_files)
    
    async def _process_corpus_with_llms(self, experiment_def: Dict[str, Any], enabled_models: List[str]) -> Dict[str, Any]:
        """Process corpus files with LLM analysis and generate coordinates"""
        corpus_config = experiment_def.get('corpus', {})
        file_path = corpus_config.get('file_path')
        pattern = corpus_config.get('pattern', '*.txt')
        
        if not file_path:
            raise ValueError("No corpus file_path specified in experiment configuration")
        
        # Resolve corpus path relative to project root
        corpus_path = Path(file_path)
        if not corpus_path.is_absolute():
            # Find project root (look for discernus directory)
            current = Path.cwd()
            project_root = current
            while project_root.parent != project_root:
                if (project_root / 'discernus').exists():
                    break
                project_root = project_root.parent
            corpus_path = project_root / file_path
        
        if not corpus_path.exists():
            raise ValueError(f"Corpus directory not found: {corpus_path}")
        
        # Get text files
        text_files = list(corpus_path.glob(pattern))
        if not text_files:
            raise ValueError(f"No text files found in {corpus_path} matching pattern {pattern}")
        
        logger.info(f"📚 Found {len(text_files)} text files to process")
        
        # Process each model
        condition_results = []
        total_analyses = 0
        
        for model in enabled_models:
            logger.info(f"🤖 Processing model: {model}")
            
            model_coordinates = []
            model_scores_all = []
            
            # Process each text file with this model
            for text_file in text_files:
                logger.info(f"  📄 Processing: {text_file.name}")
                
                # Read text content
                try:
                    with open(text_file, 'r', encoding='utf-8') as f:
                        text_content = f.read().strip()
                except Exception as e:
                    logger.warning(f"  ⚠️  Could not read {text_file.name}: {e}")
                    continue
                
                if not text_content:
                    logger.warning(f"  ⚠️  Empty file: {text_file.name}")
                    continue
                
                try:
                    # Get LLM analysis
                    analysis_result = await get_llm_analysis(
                        text=text_content,
                        experiment_def=experiment_def,
                        model=model
                    )
                    
                    if 'error' in analysis_result:
                        logger.error(f"  ❌ LLM analysis failed: {analysis_result['error']}")
                        continue
                    
                    # Extract scores
                    scores = analysis_result.get('scores', {})
                    if not scores:
                        logger.warning(f"  ⚠️  No scores returned for {text_file.name}")
                        continue
                    
                    # Calculate coordinates
                    x, y = calculate_coordinates(experiment_def, scores)
                    model_coordinates.append([x, y])
                    model_scores_all.append(scores)
                    total_analyses += 1
                    
                    logger.info(f"  ✅ Coordinates: ({x:.3f}, {y:.3f})")
                    
                except Exception as e:
                    logger.error(f"  ❌ Error processing {text_file.name}: {e}")
                    continue
            
            # Calculate centroid for this model
            if model_coordinates:
                centroid_x = sum(coord[0] for coord in model_coordinates) / len(model_coordinates)
                centroid_y = sum(coord[1] for coord in model_coordinates) / len(model_coordinates)
                centroid = [centroid_x, centroid_y]
                
                logger.info(f"✅ {model} centroid: ({centroid_x:.3f}, {centroid_y:.3f}) from {len(model_coordinates)} analyses")
            else:
                logger.warning(f"⚠️  No successful analyses for {model}")
                centroid = [0.0, 0.0]
            
            condition_results.append({
                "condition_identifier": model,
                "centroid": centroid,
                "total_analyses": len(model_coordinates),
                "coordinates": model_coordinates,
                "raw_scores": model_scores_all
            })
        
        # Create final result
        job_id = f"corpus_job_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        result = {
            "job_id": job_id,
            "comparison_type": "multi_model",
            "condition_results": condition_results,
            "statistical_metrics": {},  # Deferred to Stage 6
            "similarity_classification": "DEFERRED_TO_STAGE6",
            "corpus_info": {
                "total_texts": len(text_files),
                "total_analyses": total_analyses,
                "corpus_path": str(corpus_path),
                "pattern": pattern
            }
        }
        
        # 🎯 POST-EXPERIMENT: Calculate DCS metrics on results
        logger.info("📊 Calculating post-experiment DCS metrics...")
        
        if condition_results:
            try:
                # Extract signatures for metrics calculation
                import numpy as np
                all_signatures = []
                model_signatures = {}
                
                for condition in condition_results:
                    model_name = condition.get('condition_identifier', 'Unknown')
                    coordinates = condition.get('coordinates', [])
                    
                    if coordinates:
                        all_signatures.extend(coordinates)
                        model_signatures[model_name] = np.array(coordinates)
                
                signatures_array = np.array(all_signatures) if all_signatures else np.array([[0, 0]])
                
                # Calculate framework fitness metrics
                from discernus.metrics import (
                    calculate_territorial_coverage,
                    calculate_anchor_independence_index,
                    calculate_cartographic_resolution
                )
                
                # Calculate core metrics
                territorial_coverage = calculate_territorial_coverage(
                    signatures_array, 
                    experiment_def.get('framework', {})
                )
                
                # For anchor independence, extract anchor scores if available
                anchor_scores = {}
                for condition in condition_results:
                    raw_scores = condition.get('raw_scores', [])
                    if raw_scores:
                        # Group by anchor from raw scores
                        for score_dict in raw_scores:
                            for anchor, score in score_dict.items():
                                if anchor not in anchor_scores:
                                    anchor_scores[anchor] = []
                                anchor_scores[anchor].append(score)
                
                anchor_independence = calculate_anchor_independence_index(anchor_scores)
                
                cartographic_resolution = calculate_cartographic_resolution(signatures_array)
                
                # Calculate composite fitness score
                fitness_score = calculate_framework_fitness_score(
                    territorial_coverage.get('territorial_coverage', 0),
                    anchor_independence.get('anchor_independence_index', 0),
                    cartographic_resolution.get('cartographic_resolution', 0)
                )
                
                # Store metrics in result
                result['dcs_metrics'] = {
                    'territorial_coverage': territorial_coverage,
                    'anchor_independence': anchor_independence,
                    'cartographic_resolution': cartographic_resolution,
                    'framework_fitness': fitness_score,
                    'signature_count': len(all_signatures),
                    'model_count': len(condition_results)
                }
                
                logger.info(f"✅ DCS metrics calculated successfully")
                logger.info(f"📊 Framework fitness: {fitness_score.get('framework_fitness_score', 0):.3f} (Grade: {fitness_score.get('fitness_grade', 'Unknown')})")
                logger.info(f"📊 Territorial coverage: {territorial_coverage.get('territorial_coverage', 0):.3f}")
                logger.info(f"📊 Anchor independence: {anchor_independence.get('anchor_independence_index', 0):.3f}")
                
            except Exception as e:
                logger.warning(f"⚠️ Error calculating DCS metrics: {e}")
                result['dcs_metrics'] = {'error': str(e)}
        
        return result
    
    def _display_results_summary(self, result: Dict[str, Any], experiment_def: Dict[str, Any]):
        """Display a summary of experiment results"""
        print("\n" + "="*60)
        print("📊 EXPERIMENT RESULTS SUMMARY")
        print("="*60)
        
        # Basic info
        job_id = result.get('job_id', 'unknown')
        comparison_type = result.get('comparison_type', 'unknown')
        classification = result.get('similarity_classification', 'unknown')
        
        print(f"Job ID: {job_id}")
        print(f"Comparison Type: {comparison_type}")
        print(f"Similarity Classification: {classification}")
        
        # Model results
        condition_results = result.get('condition_results', [])
        if condition_results:
            print(f"\n🤖 MODEL RESULTS ({len(condition_results)} models):")
            for condition in condition_results:
                model = condition.get('condition_identifier', 'unknown')
                centroid = condition.get('centroid', (0, 0))
                print(f"  • {model}: centroid ({centroid[0]:.3f}, {centroid[1]:.3f})")
        
        # Runtime architecture: pure data collection only
        print(f"\n📈 RUNTIME ARCHITECTURE:")
        print("  • ✅ NO statistical analysis in orchestration runtime")
        print("  • ✅ Pure data collection: LLM calls → coordinate generation")
        print("  • ✅ All analysis deferred to Stage 6 interactive notebooks")
        print("  • ✅ Real corpus processing with LLM analysis complete")
        
        # Report URL
        report_url = result.get('report_url')
        if report_url:
            print(f"\n📋 DETAILED REPORT:")
            print(f"  View results: http://localhost:8000{report_url}")
        
        print("="*60)

    def _setup_stage6_template(
        self, 
        experiment_result: Dict[str, Any], 
        experiment_file_path: str,
        experiment_def: Dict[str, Any]
    ) -> str:
        """
        Simple Stage 6 template setup - copies universal template and saves metadata.
        Replaces the complex broken handoff orchestrator with clean file operations.
        """
        
        # Determine experiment directory from file path
        experiment_path = Path(experiment_file_path)
        experiment_dir = experiment_path.parent
        
        # Create results directory within the experiment folder
        experiment_results_dir_base = experiment_dir / "results"
        experiment_results_dir_base.mkdir(exist_ok=True)
        
        # Create timestamped run directory
        run_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        experiment_results_dir = experiment_results_dir_base / run_timestamp
        experiment_results_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy universal template - find project root first
        current = Path.cwd()
        project_root = current
        while project_root.parent != project_root:
            if (project_root / 'discernus').exists():
                break
            project_root = project_root.parent
        
        template_source = project_root / "discernus/pipeline/notebook_generation/templates/universal_stage6_template.ipynb"
        template_destination = experiment_results_dir / "stage6_interactive_analysis.ipynb"
        
        if template_source.exists():
            import shutil
            shutil.copy2(template_source, template_destination)
            logger.info(f"✅ Universal template copied to: {template_destination}")
        else:
            logger.warning(f"⚠️ Template not found at: {template_source}")
            # Create a simple fallback template
            self._create_fallback_template(template_destination)
        
        # Save run metadata for template to load
        run_metadata = {
            "job_id": experiment_result.get('job_id'),
            "experiment_path": str(experiment_file_path),
            "models_used": [condition['condition_identifier'] 
                           for condition in experiment_result.get('condition_results', [])],
            "timestamp": run_timestamp,
            "results": experiment_result
        }
        
        metadata_path = experiment_results_dir / "run_metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(run_metadata, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"✅ Run metadata saved: {metadata_path}")
        return str(template_destination)
    
    def _create_fallback_template(self, template_path: Path):
        """Create a simple fallback template if the universal template is missing"""
        
        fallback_notebook = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        "# Stage 6: Analysis Template (Fallback)\n",
                        "\n",
                        "**Note:** Universal template not found, using fallback.\n",
                        "\n",
                        "## Quick Start\n",
                        "```python\n",
                        "import json\n",
                        "with open('run_metadata.json', 'r') as f:\n",
                        "    data = json.load(f)\n",
                        "print(data.keys())\n",
                        "```"
                    ]
                },
                {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": [
                        "# Load experiment data\n",
                        "import json\n",
                        "import pandas as pd\n",
                        "import matplotlib.pyplot as plt\n",
                        "\n",
                        "# Load run metadata\n",
                        "with open('run_metadata.json', 'r') as f:\n",
                        "    run_data = json.load(f)\n",
                        "\n",
                        "print('Experiment data loaded!')\n",
                        "print(f\"Job ID: {run_data.get('job_id')}\")\n",
                        "print(f\"Models: {run_data.get('models_used')}\")"
                    ]
                }
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3"
                },
                "language_info": {
                    "name": "python",
                    "version": "3.8.5"
                }
            },
            "nbformat": 4,
            "nbformat_minor": 4
        }
        
        with open(template_path, 'w', encoding='utf-8') as f:
            json.dump(fallback_notebook, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Fallback template created: {template_path}")


def main():
    """Main entry point for experiment runner"""
    if len(sys.argv) != 2:
        print("Usage: python3 run_experiment.py <experiment_yaml_file>")
        print("\nExamples:")
        print("  python3 run_experiment.py flagship_model_statistical_comparison.yaml")
        print("  python3 run_experiment.py reboot_mft_experiment.yaml")
        sys.exit(1)
    
    yaml_path = sys.argv[1]
    
    async def run_experiment():
        async with ExperimentRunner() as runner:
            try:
                start_time = datetime.now()
                result = await runner.execute_experiment(yaml_path)
                end_time = datetime.now()
                duration = end_time - start_time
                
                print(f"\n⏱️  Total execution time: {duration}")
                
                # STAGE 5→6 HANDOFF: Copy universal template
                try:
                    print("\n🔄 Setting up Stage 6 analysis template...")
                    experiment_def = runner._load_experiment_definition(yaml_path)
                    notebook_path = runner._setup_stage6_template(result, yaml_path, experiment_def)
                    
                    print(f"✅ Stage 6 template ready: {notebook_path}")
                    print(f"🚀 Ready for interactive analysis: jupyter lab {notebook_path}")
                    
                except Exception as e:
                    logger.warning(f"⚠️  Stage 6 template setup failed: {e}")
                    print(f"⚠️  Template setup failed, but experiment completed successfully")
                
                return result
                
            except Exception as e:
                logger.error(f"❌ Experiment failed: {e}")
                raise
    
    # Run the experiment
    try:
        asyncio.run(run_experiment())
        print("\n🎉 Experiment completed successfully!")
    except KeyboardInterrupt:
        print("\n⏹️  Experiment interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Experiment failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 