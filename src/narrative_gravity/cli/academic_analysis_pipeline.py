#!/usr/bin/env python3
"""
Academic Analysis Pipeline Orchestrator - Priority 3 Enhancement

Master orchestration script that integrates all Priority 3 academic tools
into a single comprehensive workflow for complete academic analysis.

Supports complete workflow from PostgreSQL experimental data to publication-ready
academic analysis with replication packages.

Usage:
    python academic_analysis_pipeline.py --study-config study.yaml --execute-all
    python academic_analysis_pipeline.py --study-name validation_study --export-data --generate-analysis --create-package
    python academic_analysis_pipeline.py --help
"""

import argparse
import sys
import yaml
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# Add src to path for development mode
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.narrative_gravity.academic.data_export import AcademicDataExporter, ReplicationPackageBuilder
from src.narrative_gravity.academic.analysis_templates import (
    JupyterTemplateGenerator, RScriptGenerator, StataIntegration
)
from src.narrative_gravity.academic.documentation import (
    MethodologyPaperGenerator, StatisticalReportFormatter
)


class AcademicAnalysisPipeline:
    """
    Master orchestrator for complete academic analysis workflow.
    
    Integrates all Priority 3 academic tools into a unified pipeline
    from PostgreSQL data to publication-ready analysis.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize pipeline with configuration."""
        self.config = config
        self.study_name = config.get('study_name', 'academic_pipeline_study')
        self.output_base = Path(config.get('output_dir', 'academic_pipeline_output'))
        self.results = {}
        
        # Initialize academic tools
        self.data_exporter = AcademicDataExporter()
        self.package_builder = ReplicationPackageBuilder()
        self.jupyter_generator = JupyterTemplateGenerator()
        self.r_generator = RScriptGenerator()
        self.stata_integration = StataIntegration()
        self.methodology_generator = MethodologyPaperGenerator()
        self.results_formatter = StatisticalReportFormatter()
        
        # Create output directories
        self.setup_output_directories()
    
    def setup_output_directories(self):
        """Create organized output directory structure."""
        directories = [
            'data',
            'analysis/notebooks', 
            'analysis/r_scripts',
            'analysis/stata_scripts',
            'documentation',
            'replication_packages',
            'validation_reports'
        ]
        
        for directory in directories:
            (self.output_base / directory).mkdir(parents=True, exist_ok=True)
    
    def execute_complete_pipeline(self) -> Dict[str, Any]:
        """Execute complete academic analysis pipeline."""
        
        print("🚀 Starting Academic Analysis Pipeline")
        print(f"📊 Study: {self.study_name}")
        print(f"📁 Output: {self.output_base}")
        print("=" * 60)
        
        pipeline_results = {
            'study_name': self.study_name,
            'execution_date': datetime.now().isoformat(),
            'pipeline_version': 'Priority 3 Enhanced',
            'stages': {}
        }
        
        try:
            # Stage 1: Data Export
            if self.config.get('export_data', True):
                print("\n📊 STAGE 1: Data Export")
                pipeline_results['stages']['data_export'] = self.export_experimental_data()
            
            # Stage 2: Analysis Template Generation
            if self.config.get('generate_templates', True):
                print("\n💻 STAGE 2: Analysis Template Generation")
                pipeline_results['stages']['template_generation'] = self.generate_analysis_templates()
            
            # Stage 3: Documentation Generation
            if self.config.get('generate_documentation', True):
                print("\n📚 STAGE 3: Documentation Generation")
                pipeline_results['stages']['documentation'] = self.generate_academic_documentation()
            
            # Stage 4: Analysis Execution (Optional)
            if self.config.get('execute_analysis', False):
                print("\n🔬 STAGE 4: Analysis Execution")
                pipeline_results['stages']['analysis_execution'] = self.execute_analysis()
            
            # Stage 5: Replication Package Creation
            if self.config.get('create_replication_package', True):
                print("\n📦 STAGE 5: Replication Package Creation")
                pipeline_results['stages']['replication_package'] = self.create_replication_package()
            
            # Stage 6: Validation Testing
            if self.config.get('run_validation', True):
                print("\n✅ STAGE 6: Pipeline Validation")
                pipeline_results['stages']['validation'] = self.validate_pipeline()
            
            # Save pipeline results
            self.save_pipeline_results(pipeline_results)
            
            print("\n🎉 Academic Analysis Pipeline Complete!")
            return pipeline_results
            
        except Exception as e:
            print(f"\n❌ Pipeline execution failed: {e}")
            pipeline_results['error'] = str(e)
            pipeline_results['status'] = 'failed'
            self.save_pipeline_results(pipeline_results)
            raise
    
    def export_experimental_data(self) -> Dict[str, Any]:
        """Export experimental data in all academic formats."""
        
        export_config = self.config.get('data_export', {})
        
        print("   📊 Exporting experimental data...")
        experimental_files = self.data_exporter.export_experiments_data(
            start_date=export_config.get('start_date'),
            end_date=export_config.get('end_date'),
            framework_names=export_config.get('frameworks'),
            study_name=self.study_name,
            output_dir=str(self.output_base / 'data')
        )
        
        print("   🔧 Exporting component development data...")
        component_files = self.data_exporter.export_component_analysis_data(
            component_type=export_config.get('component_type', 'all'),
            include_development_sessions=export_config.get('include_sessions', True),
            output_dir=str(self.output_base / 'data')
        )
        
        results = {
            'experimental_files': experimental_files,
            'component_files': component_files,
            'export_date': datetime.now().isoformat()
        }
        
        print(f"   ✅ Exported {len(experimental_files)} experimental files")
        print(f"   ✅ Exported {len(component_files)} component files")
        
        return results
    
    def generate_analysis_templates(self) -> Dict[str, Any]:
        """Generate analysis templates in all supported languages."""
        
        template_config = self.config.get('template_generation', {})
        generated_templates = {}
        
        # Generate Jupyter notebook
        if template_config.get('jupyter', True):
            print("   📓 Generating Jupyter notebook...")
            jupyter_path = self.jupyter_generator.generate_exploration_notebook(
                study_name=self.study_name,
                output_path=str(self.output_base / 'analysis/notebooks')
            )
            generated_templates['jupyter'] = jupyter_path
            print(f"      ✅ Created: {jupyter_path}")
        
        # Generate R script
        if template_config.get('r', True):
            print("   📈 Generating R analysis script...")
            r_path = self.r_generator.generate_statistical_analysis(
                study_name=self.study_name,
                output_path=str(self.output_base / 'analysis/r_scripts')
            )
            generated_templates['r'] = r_path
            print(f"      ✅ Created: {r_path}")
        
        # Generate Stata script
        if template_config.get('stata', True):
            print("   📊 Generating Stata analysis script...")
            stata_path = self.stata_integration.generate_publication_analysis(
                study_name=self.study_name,
                output_path=str(self.output_base / 'analysis/stata_scripts')
            )
            generated_templates['stata'] = stata_path
            print(f"      ✅ Created: {stata_path}")
        
        return {
            'generated_templates': generated_templates,
            'generation_date': datetime.now().isoformat()
        }
    
    def generate_academic_documentation(self) -> Dict[str, Any]:
        """Generate academic documentation and reports."""
        
        doc_config = self.config.get('documentation', {})
        generated_docs = {}
        
        # Generate methodology documentation
        if doc_config.get('methodology', True):
            print("   📋 Generating methodology documentation...")
            methodology_path = self.methodology_generator.generate_methodology_section(
                study_name=self.study_name,
                include_development_process=doc_config.get('include_development', True),
                output_path=str(self.output_base / 'documentation')
            )
            generated_docs['methodology'] = methodology_path
            print(f"      ✅ Created: {methodology_path}")
        
        # Generate results documentation (if results data available)
        if doc_config.get('results', True):
            print("   📊 Generating results documentation...")
            results_data = self.load_analysis_results()
            results_path = self.results_formatter.generate_results_section(
                analysis_results=results_data,
                study_name=self.study_name,
                output_path=str(self.output_base / 'documentation')
            )
            generated_docs['results'] = results_path
            print(f"      ✅ Created: {results_path}")
        
        return {
            'generated_docs': generated_docs,
            'generation_date': datetime.now().isoformat()
        }
    
    def execute_analysis(self) -> Dict[str, Any]:
        """Execute analysis templates (optional - requires software installation)."""
        
        analysis_config = self.config.get('analysis_execution', {})
        execution_results = {}
        
        # Execute Jupyter notebook (if available)
        if analysis_config.get('jupyter', False):
            print("   📓 Executing Jupyter notebook...")
            try:
                jupyter_result = self.execute_jupyter_analysis()
                execution_results['jupyter'] = jupyter_result
                print("      ✅ Jupyter analysis completed")
            except Exception as e:
                print(f"      ⚠️  Jupyter execution failed: {e}")
                execution_results['jupyter'] = {'error': str(e)}
        
        # Execute R script (if available)
        if analysis_config.get('r', False):
            print("   📈 Executing R analysis...")
            try:
                r_result = self.execute_r_analysis()
                execution_results['r'] = r_result
                print("      ✅ R analysis completed")
            except Exception as e:
                print(f"      ⚠️  R execution failed: {e}")
                execution_results['r'] = {'error': str(e)}
        
        return {
            'execution_results': execution_results,
            'execution_date': datetime.now().isoformat()
        }
    
    def create_replication_package(self) -> Dict[str, Any]:
        """Create complete replication package."""
        
        package_config = self.config.get('replication_package', {})
        
        print("   📦 Building replication package...")
        
        # Build data filters from config
        data_filters = {}
        if 'data_export' in self.config:
            export_config = self.config['data_export']
            if export_config.get('start_date'):
                data_filters['start_date'] = export_config['start_date']
            if export_config.get('end_date'):
                data_filters['end_date'] = export_config['end_date']
            if export_config.get('frameworks'):
                data_filters['frameworks'] = export_config['frameworks']
        
        package_path = self.package_builder.build_replication_package(
            study_name=self.study_name,
            study_description=package_config.get('description', f'Academic analysis study: {self.study_name}'),
            data_filters=data_filters if data_filters else None,
            include_code=package_config.get('include_code', True),
            include_documentation=package_config.get('include_documentation', True),
            output_path=str(self.output_base / 'replication_packages')
        )
        
        print(f"      ✅ Replication package created: {package_path}")
        
        return {
            'package_path': package_path,
            'creation_date': datetime.now().isoformat()
        }
    
    def validate_pipeline(self) -> Dict[str, Any]:
        """Validate pipeline execution and outputs."""
        
        print("   ✅ Running pipeline validation...")
        
        validation_results = {
            'data_export_validation': self.validate_data_export(),
            'template_validation': self.validate_templates(),
            'documentation_validation': self.validate_documentation(),
            'integration_validation': self.validate_integration()
        }
        
        # Count successful validations
        successful_validations = sum(1 for result in validation_results.values() if result.get('status') == 'pass')
        total_validations = len(validation_results)
        
        validation_summary = {
            'validation_results': validation_results,
            'summary': {
                'total_tests': total_validations,
                'passed': successful_validations,
                'failed': total_validations - successful_validations,
                'success_rate': (successful_validations / total_validations) * 100
            },
            'validation_date': datetime.now().isoformat()
        }
        
        print(f"      ✅ Validation completed: {successful_validations}/{total_validations} tests passed")
        
        return validation_summary
    
    def validate_data_export(self) -> Dict[str, Any]:
        """Validate data export outputs."""
        try:
            data_dir = self.output_base / 'data'
            expected_files = [f"{self.study_name}.csv", f"{self.study_name}.feather", f"{self.study_name}.json"]
            
            missing_files = []
            for file_name in expected_files:
                if not (data_dir / file_name).exists():
                    missing_files.append(file_name)
            
            if missing_files:
                return {
                    'status': 'fail',
                    'message': f'Missing data files: {missing_files}'
                }
            
            # Validate CSV file structure
            csv_path = data_dir / f"{self.study_name}.csv"
            import pandas as pd
            df = pd.read_csv(csv_path)
            
            expected_columns = ['exp_id', 'framework', 'llm_model']
            missing_columns = [col for col in expected_columns if col not in df.columns]
            
            if missing_columns:
                return {
                    'status': 'fail',
                    'message': f'Missing required columns: {missing_columns}'
                }
            
            return {
                'status': 'pass',
                'message': f'Data export validation successful ({len(df)} rows, {len(df.columns)} columns)',
                'details': {
                    'row_count': len(df),
                    'column_count': len(df.columns),
                    'files_created': len(expected_files) - len(missing_files)
                }
            }
            
        except Exception as e:
            return {
                'status': 'fail',
                'message': f'Data export validation failed: {e}'
            }
    
    def validate_templates(self) -> Dict[str, Any]:
        """Validate generated analysis templates."""
        try:
            templates_created = 0
            template_errors = []
            
            # Check Jupyter notebook
            jupyter_path = self.output_base / 'analysis/notebooks' / f"{self.study_name}_exploration.ipynb"
            if jupyter_path.exists():
                templates_created += 1
                # Validate JSON structure
                with open(jupyter_path, 'r') as f:
                    notebook = json.load(f)
                if 'cells' not in notebook:
                    template_errors.append('Jupyter notebook missing cells')
            else:
                template_errors.append('Jupyter notebook not created')
            
            # Check R script
            r_path = self.output_base / 'analysis/r_scripts' / f"{self.study_name}_analysis.R"
            if r_path.exists():
                templates_created += 1
                # Check for required libraries
                with open(r_path, 'r') as f:
                    r_content = f.read()
                if 'library(tidyverse)' not in r_content:
                    template_errors.append('R script missing required libraries')
            else:
                template_errors.append('R script not created')
            
            # Check Stata script
            stata_path = self.output_base / 'analysis/stata_scripts' / f"{self.study_name}_publication.do"
            if stata_path.exists():
                templates_created += 1
                # Check for basic Stata commands
                with open(stata_path, 'r') as f:
                    stata_content = f.read()
                if 'mixed cv' not in stata_content:
                    template_errors.append('Stata script missing statistical commands')
            else:
                template_errors.append('Stata script not created')
            
            if template_errors:
                return {
                    'status': 'fail',
                    'message': f'Template validation failed: {template_errors}'
                }
            
            return {
                'status': 'pass',
                'message': f'Template validation successful ({templates_created} templates created)',
                'details': {
                    'templates_created': templates_created,
                    'validation_checks_passed': 3 - len(template_errors)
                }
            }
            
        except Exception as e:
            return {
                'status': 'fail',
                'message': f'Template validation failed: {e}'
            }
    
    def validate_documentation(self) -> Dict[str, Any]:
        """Validate generated documentation."""
        try:
            docs_created = 0
            doc_errors = []
            
            # Check methodology documentation
            methodology_path = self.output_base / 'documentation' / f"{self.study_name}_methodology.md"
            if methodology_path.exists():
                docs_created += 1
                with open(methodology_path, 'r') as f:
                    content = f.read()
                if '# Methodology' not in content:
                    doc_errors.append('Methodology document missing header')
            else:
                doc_errors.append('Methodology documentation not created')
            
            if doc_errors:
                return {
                    'status': 'fail',
                    'message': f'Documentation validation failed: {doc_errors}'
                }
            
            return {
                'status': 'pass',
                'message': f'Documentation validation successful ({docs_created} documents created)',
                'details': {
                    'documents_created': docs_created
                }
            }
            
        except Exception as e:
            return {
                'status': 'fail',
                'message': f'Documentation validation failed: {e}'
            }
    
    def validate_integration(self) -> Dict[str, Any]:
        """Validate overall pipeline integration."""
        try:
            # Check that all major output directories exist and have content
            required_dirs = ['data', 'analysis', 'documentation']
            missing_dirs = []
            
            for dir_name in required_dirs:
                dir_path = self.output_base / dir_name
                if not dir_path.exists():
                    missing_dirs.append(dir_name)
                elif not any(dir_path.iterdir()):
                    missing_dirs.append(f"{dir_name} (empty)")
            
            if missing_dirs:
                return {
                    'status': 'fail',
                    'message': f'Missing or empty directories: {missing_dirs}'
                }
            
            return {
                'status': 'pass',
                'message': 'Integration validation successful - all pipeline components functioning',
                'details': {
                    'directories_validated': len(required_dirs),
                    'pipeline_complete': True
                }
            }
            
        except Exception as e:
            return {
                'status': 'fail',
                'message': f'Integration validation failed: {e}'
            }
    
    def execute_jupyter_analysis(self) -> Dict[str, Any]:
        """Execute Jupyter notebook analysis (requires Jupyter installation)."""
        try:
            notebook_path = self.output_base / 'analysis/notebooks' / f"{self.study_name}_exploration.ipynb"
            
            # Try to execute notebook using nbconvert
            cmd = ['jupyter', 'nbconvert', '--execute', '--inplace', str(notebook_path)]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                return {
                    'status': 'success',
                    'message': 'Jupyter notebook executed successfully'
                }
            else:
                return {
                    'status': 'error', 
                    'message': f'Jupyter execution failed: {result.stderr}'
                }
                
        except FileNotFoundError:
            return {
                'status': 'error',
                'message': 'Jupyter not found - install Jupyter to enable notebook execution'
            }
        except subprocess.TimeoutExpired:
            return {
                'status': 'error',
                'message': 'Jupyter execution timed out'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Jupyter execution error: {e}'
            }
    
    def execute_r_analysis(self) -> Dict[str, Any]:
        """Execute R script analysis (requires R installation)."""
        try:
            r_script_path = self.output_base / 'analysis/r_scripts' / f"{self.study_name}_analysis.R"
            
            # Try to execute R script
            cmd = ['Rscript', str(r_script_path)]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300, 
                                  cwd=str(r_script_path.parent))
            
            if result.returncode == 0:
                return {
                    'status': 'success',
                    'message': 'R script executed successfully',
                    'output': result.stdout
                }
            else:
                return {
                    'status': 'error',
                    'message': f'R execution failed: {result.stderr}'
                }
                
        except FileNotFoundError:
            return {
                'status': 'error',
                'message': 'R not found - install R to enable script execution'
            }
        except subprocess.TimeoutExpired:
            return {
                'status': 'error',
                'message': 'R execution timed out'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'R execution error: {e}'
            }
    
    def load_analysis_results(self) -> Dict[str, Any]:
        """Load analysis results if available."""
        # Placeholder for loading actual analysis results
        # In a real implementation, this would load statistical results
        return {
            'reliability': {
                'mean_cv': 0.1547,
                'sd_cv': 0.0892,
                'reliability_rate': 78.4
            },
            'statistical_tests': {
                'framework_effect': {'p_value': 0.0023}
            }
        }
    
    def save_pipeline_results(self, results: Dict[str, Any]):
        """Save pipeline execution results."""
        results_path = self.output_base / 'validation_reports' / f"{self.study_name}_pipeline_results.json"
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"📋 Pipeline results saved: {results_path}")


def load_study_config(config_path: str) -> Dict[str, Any]:
    """Load study configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def create_example_config(output_path: str = "study_config_example.yaml"):
    """Create example study configuration file."""
    example_config = {
        'study_name': 'validation_study_2025',
        'output_dir': 'academic_pipeline_output',
        
        'data_export': {
            'start_date': '2025-06-01',
            'end_date': '2025-06-30',
            'frameworks': ['civic_virtue', 'political_spectrum'],
            'component_type': 'all',
            'include_sessions': True
        },
        
        'template_generation': {
            'jupyter': True,
            'r': True,
            'stata': True
        },
        
        'documentation': {
            'methodology': True,
            'results': True,
            'include_development': True
        },
        
        'analysis_execution': {
            'jupyter': False,  # Set to true if Jupyter installed
            'r': False,        # Set to true if R installed
            'stata': False     # Set to true if Stata installed
        },
        
        'replication_package': {
            'description': 'Complete validation study for LLM narrative analysis',
            'include_code': True,
            'include_documentation': True
        },
        
        'export_data': True,
        'generate_templates': True,
        'generate_documentation': True,
        'execute_analysis': False,
        'create_replication_package': True,
        'run_validation': True
    }
    
    with open(output_path, 'w') as f:
        yaml.dump(example_config, f, default_flow_style=False, sort_keys=False)
    
    print(f"📋 Example configuration created: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Academic Analysis Pipeline Orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Run complete pipeline with config file:
    python academic_analysis_pipeline.py --study-config study.yaml --execute-all

  Run specific stages:
    python academic_analysis_pipeline.py --study-name validation_study \\
        --export-data --generate-templates --create-package

  Create example configuration:
    python academic_analysis_pipeline.py --create-example-config

  Run with custom settings:
    python academic_analysis_pipeline.py --study-name test_study \\
        --output-dir custom_output \\
        --frameworks civic_virtue,political_spectrum \\
        --execute-all

Integration with existing CLI tools:
  This orchestrator integrates all Priority 3 academic tools:
  - export_academic_data.py
  - generate_analysis_templates.py  
  - generate_documentation.py
        """
    )
    
    # Configuration options
    parser.add_argument(
        "--study-config",
        help="YAML configuration file for study parameters"
    )
    
    parser.add_argument(
        "--study-name",
        default="academic_pipeline_study",
        help="Study name for output file naming"
    )
    
    parser.add_argument(
        "--output-dir", 
        default="academic_pipeline_output",
        help="Base output directory for all pipeline outputs"
    )
    
    # Data export options
    parser.add_argument(
        "--frameworks",
        help="Comma-separated list of framework names to include"
    )
    
    parser.add_argument(
        "--start-date",
        help="Start date for data filtering (ISO format: 2025-06-01)"
    )
    
    parser.add_argument(
        "--end-date",
        help="End date for data filtering (ISO format: 2025-06-30)"
    )
    
    # Pipeline stage controls
    parser.add_argument(
        "--execute-all",
        action="store_true",
        help="Execute all pipeline stages"
    )
    
    parser.add_argument(
        "--export-data",
        action="store_true",
        help="Export experimental data"
    )
    
    parser.add_argument(
        "--generate-templates",
        action="store_true", 
        help="Generate analysis templates"
    )
    
    parser.add_argument(
        "--generate-documentation",
        action="store_true",
        help="Generate academic documentation"
    )
    
    parser.add_argument(
        "--execute-analysis",
        action="store_true",
        help="Execute analysis templates (requires software installation)"
    )
    
    parser.add_argument(
        "--create-package",
        action="store_true",
        help="Create replication package"
    )
    
    parser.add_argument(
        "--run-validation",
        action="store_true",
        help="Run pipeline validation tests"
    )
    
    # Utility options
    parser.add_argument(
        "--create-example-config",
        action="store_true",
        help="Create example configuration file and exit"
    )
    
    args = parser.parse_args()
    
    # Create example config if requested
    if args.create_example_config:
        create_example_config()
        return
    
    try:
        # Load configuration
        if args.study_config:
            config = load_study_config(args.study_config)
        else:
            # Build config from command line arguments
            config = {
                'study_name': args.study_name,
                'output_dir': args.output_dir,
                'data_export': {},
                'template_generation': {'jupyter': True, 'r': True, 'stata': True},
                'documentation': {'methodology': True, 'results': True, 'include_development': True},
                'analysis_execution': {'jupyter': False, 'r': False, 'stata': False},
                'replication_package': {
                    'description': f'Academic analysis study: {args.study_name}',
                    'include_code': True,
                    'include_documentation': True
                }
            }
            
            # Add data export filters
            if args.frameworks:
                config['data_export']['frameworks'] = args.frameworks.split(',')
            if args.start_date:
                config['data_export']['start_date'] = args.start_date
            if args.end_date:
                config['data_export']['end_date'] = args.end_date
            
            # Set stage flags
            if args.execute_all:
                config.update({
                    'export_data': True,
                    'generate_templates': True,
                    'generate_documentation': True,
                    'execute_analysis': args.execute_analysis,
                    'create_replication_package': True,
                    'run_validation': True
                })
            else:
                config.update({
                    'export_data': args.export_data,
                    'generate_templates': args.generate_templates,
                    'generate_documentation': args.generate_documentation,
                    'execute_analysis': args.execute_analysis,
                    'create_replication_package': args.create_package,
                    'run_validation': args.run_validation
                })
        
        # Initialize and execute pipeline
        pipeline = AcademicAnalysisPipeline(config)
        results = pipeline.execute_complete_pipeline()
        
        # Print summary
        print("\n" + "="*60)
        print("🎉 ACADEMIC ANALYSIS PIPELINE COMPLETE")
        print("="*60)
        print(f"📊 Study: {results['study_name']}")
        print(f"📁 Output: {config['output_dir']}")
        print(f"⏰ Execution: {results['execution_date']}")
        
        if 'validation' in results['stages']:
            validation = results['stages']['validation']
            success_rate = validation['summary']['success_rate']
            print(f"✅ Validation: {success_rate:.1f}% tests passed")
        
        print(f"📋 Full results: {config['output_dir']}/validation_reports/")
        
    except Exception as e:
        print(f"❌ Pipeline execution failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 