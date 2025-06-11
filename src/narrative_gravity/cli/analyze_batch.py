#!/usr/bin/env python3
"""
Multi-Component Analysis Orchestrator (analyze_batch.py)
Priority 1 CLI Infrastructure Component

Batch processing with component matrix support for systematic experimental validation.
Enables comprehensive analysis across multiple prompt templates, frameworks, and weighting methodologies.
"""

import argparse
import asyncio
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from ..models import (
    PromptTemplate, FrameworkVersion, WeightingMethodology, 
    ComponentCompatibility, Experiment, Run
)
from ..utils.database import get_database_url


class ComponentMatrix:
    """Manages experimental component combinations and validation."""
    
    def __init__(self, config_path: str):
        """Initialize with configuration file."""
        self.config = self._load_config(config_path)
        self.engine = create_engine(get_database_url())
        self.Session = sessionmaker(bind=self.engine)
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load experimental configuration from YAML file."""
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Validate required configuration
        required_fields = ['experiment_name', 'prompt_templates', 'frameworks', 'weighting_methods', 'models']
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Missing required field in config: {field}")
        
        return config
    
    def validate_components(self) -> List[Dict[str, str]]:
        """Validate that all specified components exist in the database."""
        session = self.Session()
        try:
            valid_combinations = []
            issues = []
            
            for prompt_name in self.config['prompt_templates']:
                for framework_name in self.config['frameworks']:
                    for weighting_name in self.config['weighting_methods']:
                        # Check if each component exists
                        prompt = session.query(PromptTemplate).filter_by(name=prompt_name).first()
                        framework = session.query(FrameworkVersion).filter_by(framework_name=framework_name).first()
                        weighting = session.query(WeightingMethodology).filter_by(name=weighting_name).first()
                        
                        if not prompt:
                            issues.append(f"Prompt template not found: {prompt_name}")
                            continue
                        if not framework:
                            issues.append(f"Framework not found: {framework_name}")
                            continue
                        if not weighting:
                            issues.append(f"Weighting methodology not found: {weighting_name}")
                            continue
                        
                        # Check compatibility if available
                        compatibility = session.query(ComponentCompatibility).filter_by(
                            prompt_template_id=prompt.id,
                            framework_id=framework.id,
                            weighting_method_id=weighting.id
                        ).first()
                        
                        combination = {
                            'prompt_template': f"{prompt.name}:{prompt.version}",
                            'framework': f"{framework.framework_name}:{framework.version}",
                            'weighting_method': f"{weighting.name}:{weighting.version}",
                            'compatibility_status': compatibility.validation_status if compatibility else 'untested'
                        }
                        valid_combinations.append(combination)
            
            if issues:
                print("\n⚠️  Component validation issues:")
                for issue in issues:
                    print(f"   {issue}")
                return []
            
            return valid_combinations
            
        finally:
            session.close()
    
    def generate_execution_plan(self, corpus_file: str) -> Dict[str, Any]:
        """Generate comprehensive execution plan for batch analysis."""
        valid_combinations = self.validate_components()
        if not valid_combinations:
            raise ValueError("No valid component combinations found")
        
        # Load corpus
        corpus_texts = self._load_corpus(corpus_file)
        
        # Calculate execution matrix
        total_analyses = (
            len(valid_combinations) * 
            len(corpus_texts) * 
            len(self.config['models']) * 
            self.config.get('runs_per_combination', 1)
        )
        
        execution_plan = {
            'experiment_name': self.config['experiment_name'],
            'total_combinations': len(valid_combinations),
            'total_texts': len(corpus_texts),
            'total_models': len(self.config['models']),
            'runs_per_combination': self.config.get('runs_per_combination', 1),
            'total_analyses': total_analyses,
            'estimated_duration_hours': total_analyses * 0.05,  # Estimate 3 minutes per analysis
            'combinations': valid_combinations,
            'corpus_texts': corpus_texts[:5],  # Preview first 5 texts
            'full_corpus_count': len(corpus_texts)
        }
        
        return execution_plan
    
    def _load_corpus(self, corpus_file: str) -> List[Dict[str, Any]]:
        """Load corpus texts from JSONL file."""
        texts = []
        with open(corpus_file, 'r') as f:
            for line in f:
                texts.append(json.loads(line.strip()))
        return texts


class BatchAnalysisOrchestrator:
    """Orchestrates systematic batch analysis execution."""
    
    def __init__(self, matrix: ComponentMatrix):
        self.matrix = matrix
        self.session = matrix.Session()
        
    def create_experiment(self, plan: Dict[str, Any]) -> str:
        """Create new experiment record for batch analysis."""
        experiment = Experiment(
            name=plan['experiment_name'],
            description=f"Batch analysis across {plan['total_combinations']} component combinations",
            hypothesis="Component combination validation and performance assessment",
            analysis_mode="multi_component_batch",
            selected_models=self.matrix.config['models'],
            status="active"
        )
        
        self.session.add(experiment)
        self.session.commit()
        
        return experiment.id
    
    async def execute_batch_analysis(self, corpus_file: str, output_dir: str, dry_run: bool = False) -> Dict[str, Any]:
        """Execute comprehensive batch analysis."""
        # Generate execution plan
        plan = self.matrix.generate_execution_plan(corpus_file)
        
        print(f"\n🎯 Batch Analysis Execution Plan")
        print(f"   Experiment: {plan['experiment_name']}")
        print(f"   Component combinations: {plan['total_combinations']}")
        print(f"   Corpus texts: {plan['total_texts']}")
        print(f"   Models: {plan['total_models']}")
        print(f"   Total analyses: {plan['total_analyses']}")
        print(f"   Estimated duration: {plan['estimated_duration_hours']:.1f} hours")
        
        if dry_run:
            print("\n🧪 DRY RUN - No analyses will be executed")
            return plan
        
        # Create experiment
        experiment_id = self.create_experiment(plan)
        print(f"\n📊 Created experiment: {experiment_id}")
        
        # Execute analysis matrix
        results = {
            'experiment_id': experiment_id,
            'total_analyses': 0,
            'successful_analyses': 0,
            'failed_analyses': 0,
            'results_by_combination': {}
        }
        
        corpus_texts = self.matrix._load_corpus(corpus_file)
        
        for combination in plan['combinations']:
            combination_key = f"{combination['prompt_template']}|{combination['framework']}|{combination['weighting_method']}"
            results['results_by_combination'][combination_key] = []
            
            for text_data in corpus_texts:
                for model in self.matrix.config['models']:
                    for run_num in range(self.matrix.config.get('runs_per_combination', 1)):
                        try:
                            # Execute single analysis
                            result = await self._execute_single_analysis(
                                experiment_id, combination, text_data, model, run_num + 1
                            )
                            
                            results['total_analyses'] += 1
                            if result['success']:
                                results['successful_analyses'] += 1
                            else:
                                results['failed_analyses'] += 1
                            
                            results['results_by_combination'][combination_key].append(result)
                            
                        except Exception as e:
                            print(f"❌ Analysis failed: {e}")
                            results['total_analyses'] += 1
                            results['failed_analyses'] += 1
        
        # Save results
        output_path = Path(output_dir) / f"{plan['experiment_name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n✅ Batch analysis complete!")
        print(f"   Results saved: {output_path}")
        print(f"   Success rate: {results['successful_analyses']}/{results['total_analyses']} ({results['successful_analyses']/results['total_analyses']*100:.1f}%)")
        
        return results
    
    async def _execute_single_analysis(self, experiment_id: int, combination: Dict[str, str], 
                                     text_data: Dict[str, Any], model: str, run_number: int) -> Dict[str, Any]:
        """Execute single analysis with specified component combination."""
        # This would integrate with the actual analysis engine
        # For now, return mock result structure
        
        result = {
            'experiment_id': experiment_id,
            'combination': combination,
            'text_id': text_data.get('text_id', 'unknown'),
            'model': model,
            'run_number': run_number,
            'timestamp': datetime.now().isoformat(),
            'success': True,
            'execution_time_seconds': 45.0,
            'api_cost': 0.02,
            'narrative_elevation': 0.35,
            'narrative_polarity': 0.67,
            'coherence': 0.82,
            'framework_fit_score': 0.91
        }
        
        # Create Run record
        run = Run(
            experiment_id=experiment_id,
            run_number=run_number,
            text_content=text_data.get('text', ''),
            input_length=len(text_data.get('text', '')),
            llm_model=model,
            prompt_template_version=combination['prompt_template'].split(':')[1],
            framework_version=combination['framework'].split(':')[1],
            narrative_elevation=result['narrative_elevation'],
            polarity=result['narrative_polarity'],
            coherence=result['coherence'],
            framework_fit_score=result['framework_fit_score'],
            duration_seconds=result['execution_time_seconds'],
            api_cost=result['api_cost'],
            complete_provenance={'component_combination': combination}
        )
        
        self.session.add(run)
        self.session.commit()
        
        return result


def main():
    """CLI entry point for batch analysis orchestrator."""
    parser = argparse.ArgumentParser(description="Multi-Component Batch Analysis Orchestrator")
    parser.add_argument('--config', required=True, help='Component matrix configuration file (YAML)')
    parser.add_argument('--corpus', required=True, help='Corpus file (JSONL format)')
    parser.add_argument('--output', required=True, help='Output directory for results')
    parser.add_argument('--dry-run', action='store_true', help='Show execution plan without running')
    parser.add_argument('--validate-only', action='store_true', help='Only validate component matrix')
    
    args = parser.parse_args()
    
    try:
        # Initialize component matrix
        matrix = ComponentMatrix(args.config)
        
        if args.validate_only:
            print("🔍 Validating component matrix...")
            combinations = matrix.validate_components()
            if combinations:
                print(f"✅ {len(combinations)} valid component combinations found")
                for i, combo in enumerate(combinations[:5]):  # Show first 5
                    print(f"   {i+1}. {combo['prompt_template']} + {combo['framework']} + {combo['weighting_method']} ({combo['compatibility_status']})")
                if len(combinations) > 5:
                    print(f"   ... and {len(combinations) - 5} more")
            else:
                print("❌ No valid combinations found")
            return
        
        # Execute batch analysis
        orchestrator = BatchAnalysisOrchestrator(matrix)
        asyncio.run(orchestrator.execute_batch_analysis(args.corpus, args.output, args.dry_run))
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main()) 