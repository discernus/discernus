"""
End-to-End Academic Pipeline Testing Framework

Validates the complete workflow:
1. CLI batch analysis → PostgreSQL storage
2. Data export to academic formats  
3. Analysis template generation
4. Statistical analysis execution
5. Replication package creation
6. Publication-ready output validation

This ensures the entire academic integration pipeline works seamlessly.
"""

import os
import sys
import subprocess
import tempfile
import pytest
import pandas as pd
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any
import shutil

# Setup paths
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from src.academic import (
    AcademicDataExporter, ReplicationPackageBuilder,
    JupyterTemplateGenerator, RScriptGenerator, StataIntegration
)
from src.models import Experiment, Run
from src.utils.database import get_database_url


class TestAcademicPipelineEndToEnd:
    """End-to-end testing of the complete academic pipeline."""
    
    @pytest.fixture
    def temp_output_dir(self):
        """Create temporary output directory for tests."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @pytest.fixture
    def sample_experiment_data(self):
        """Create sample experiment data in the database."""
        db = next(get_db())
        
        # Create test experiment
        experiment = Experiment(
            name="End-to-End Test Study",
            description="Test experiment for academic pipeline validation",
            hypothesis="Test hypothesis for validation",
            prompt_template_id="test_template_v1",
            framework_config_id="civic_virtue_v1",
            scoring_algorithm_id="hierarchical_v1",
            selected_models=["gpt-4", "claude-3"],
            status="completed",
            total_runs=6,
            successful_runs=6,
            tags=["test", "e2e", "validation"]
        )
        
        db.add(experiment)
        db.commit()
        db.refresh(experiment)
        
        # Create test runs with realistic data
        test_runs = [
            {
                "text_content": "Democracy requires active citizen participation and civic engagement to function effectively.",
                "llm_model": "gpt-4",
                "raw_scores": {"Truth": 0.8, "Dignity": 0.7, "Liberty": 0.6, "Justice": 0.8, "Solidarity": 0.5},
                "cv": 0.15
            },
            {
                "text_content": "Economic inequality undermines social cohesion and democratic institutions.",
                "llm_model": "gpt-4", 
                "raw_scores": {"Truth": 0.7, "Dignity": 0.8, "Liberty": 0.5, "Justice": 0.9, "Solidarity": 0.8},
                "cv": 0.18
            },
            {
                "text_content": "Individual freedom must be balanced with collective responsibility.",
                "llm_model": "claude-3",
                "raw_scores": {"Truth": 0.6, "Dignity": 0.7, "Liberty": 0.9, "Justice": 0.6, "Solidarity": 0.7},
                "cv": 0.12
            },
            {
                "text_content": "Constitutional democracy protects minority rights while enabling majority rule.",
                "llm_model": "claude-3",
                "raw_scores": {"Truth": 0.8, "Dignity": 0.8, "Liberty": 0.7, "Justice": 0.8, "Solidarity": 0.6},
                "cv": 0.10
            },
            {
                "text_content": "Education is fundamental to democratic citizenship and social progress.",
                "llm_model": "gpt-4",
                "raw_scores": {"Truth": 0.9, "Dignity": 0.8, "Liberty": 0.6, "Justice": 0.7, "Solidarity": 0.7},
                "cv": 0.16
            },
            {
                "text_content": "Public trust in institutions is essential for effective governance.",
                "llm_model": "claude-3", 
                "raw_scores": {"Truth": 0.8, "Dignity": 0.7, "Liberty": 0.5, "Justice": 0.8, "Solidarity": 0.6},
                "cv": 0.19
            }
        ]
        
        for i, run_data in enumerate(test_runs, 1):
            run = Run(
                experiment_id=experiment.id,
                run_number=i,
                text_id=f"test_text_{i}",
                text_content=run_data["text_content"],
                input_length=len(run_data["text_content"]),
                llm_model=run_data["llm_model"],
                llm_version="latest",
                prompt_template_version="test_v1",
                framework_version="civic_virtue_v1",
                raw_scores=run_data["raw_scores"],
                hierarchical_ranking={"primary": "Justice", "secondary": "Truth", "tertiary": "Dignity"},
                framework_fit_score=0.85,
                narrative_elevation=0.65,
                polarity=0.25,
                coherence=0.78,
                directional_purity=0.82,
                narrative_position_x=0.15,
                narrative_position_y=0.35,
                duration_seconds=3.2,
                api_cost=0.024,
                success=True,
                complete_provenance={
                    "experiment_id": experiment.id,
                    "test_data": True,
                    "cv": run_data["cv"]
                }
            )
            db.add(run)
        
        db.commit()
        
        yield experiment.id
        
        # Cleanup
        db.query(Run).filter(Run.experiment_id == experiment.id).delete()
        db.query(Experiment).filter(Experiment.id == experiment.id).delete()
        db.commit()
    
    def test_complete_academic_workflow(self, sample_experiment_data, temp_output_dir):
        """Test the complete academic workflow end-to-end."""
        experiment_id = sample_experiment_data
        study_name = f"e2e_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"\n🧪 Testing complete academic workflow with experiment {experiment_id}")
        
        # Phase 1: Data Export Testing
        print("\n📊 Phase 1: Testing data export...")
        data_export_results = self._test_data_export(study_name, temp_output_dir)
        assert data_export_results['success'], f"Data export failed: {data_export_results.get('error')}"
        print("✅ Data export validation passed")
        
        # Phase 2: Template Generation Testing  
        print("\n📝 Phase 2: Testing template generation...")
        template_results = self._test_template_generation(study_name, temp_output_dir)
        assert template_results['success'], f"Template generation failed: {template_results.get('error')}"
        print("✅ Template generation validation passed")
        
        # Phase 3: Analysis Execution Testing
        print("\n🔬 Phase 3: Testing analysis execution...")
        analysis_results = self._test_analysis_execution(study_name, temp_output_dir, data_export_results['data_files'])
        # Analysis execution may have warnings but should not completely fail
        assert len(analysis_results.get('critical_failures', [])) == 0, f"Critical analysis failures: {analysis_results['critical_failures']}"
        print("✅ Analysis execution validation passed")
        
        # Phase 4: Replication Package Testing
        print("\n📦 Phase 4: Testing replication package creation...")
        replication_results = self._test_replication_package(study_name, temp_output_dir)
        assert replication_results['success'], f"Replication package failed: {replication_results.get('error')}"
        print("✅ Replication package validation passed")
        
        # Phase 5: Integration Validation
        print("\n🔍 Phase 5: Testing integration validation...")
        integration_results = self._test_integration_validation(study_name, temp_output_dir, data_export_results)
        assert integration_results['success'], f"Integration validation failed: {integration_results.get('error')}"
        print("✅ Integration validation passed")
        
        print(f"\n🎉 Complete academic workflow test PASSED for study: {study_name}")
    
    def _test_data_export(self, study_name: str, output_dir: str) -> Dict[str, Any]:
        """Test data export functionality."""
        try:
            exporter = AcademicDataExporter()
            
            # Test academic format export
            export_files = exporter.export_experiments_data(
                study_name=study_name,
                output_dir=output_dir
            )
            
            # Validate export files exist
            required_formats = ['csv', 'json', 'data_dictionary']
            missing_formats = [fmt for fmt in required_formats if fmt not in export_files]
            if missing_formats:
                return {'success': False, 'error': f"Missing export formats: {missing_formats}"}
            
            # Validate file contents
            for format_name, file_path in export_files.items():
                if not Path(file_path).exists():
                    return {'success': False, 'error': f"Export file not found: {file_path}"}
                
                if Path(file_path).stat().st_size == 0:
                    return {'success': False, 'error': f"Export file is empty: {file_path}"}
            
            # Validate CSV data structure
            if 'csv' in export_files:
                df = pd.read_csv(export_files['csv'])
                if len(df) == 0:
                    return {'success': False, 'error': "Exported CSV contains no data"}
                
                # Check for essential columns
                essential_columns = ['experiment_id', 'run_id', 'llm_model', 'framework']
                missing_columns = [col for col in essential_columns if col not in df.columns]
                if missing_columns:
                    return {'success': False, 'error': f"Missing essential columns: {missing_columns}"}
            
            return {
                'success': True,
                'data_files': export_files,
                'record_count': len(df) if 'df' in locals() else 0
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _test_template_generation(self, study_name: str, output_dir: str) -> Dict[str, Any]:
        """Test analysis template generation."""
        try:
            templates_dir = Path(output_dir) / 'templates'
            templates_dir.mkdir(exist_ok=True)
            
            generated_templates = {}
            
            # Test Jupyter notebook generation
            try:
                jupyter_generator = JupyterTemplateGenerator()
                jupyter_path = jupyter_generator.generate_exploration_notebook(
                    study_name, str(templates_dir)
                )
                if Path(jupyter_path).exists():
                    generated_templates['jupyter'] = jupyter_path
                    
                    # Validate notebook structure
                    with open(jupyter_path, 'r') as f:
                        notebook = json.load(f)
                    
                    if 'cells' not in notebook or len(notebook['cells']) == 0:
                        return {'success': False, 'error': "Generated notebook has no cells"}
                        
            except Exception as e:
                print(f"⚠️  Jupyter template generation warning: {e}")
            
            # Test R script generation
            try:
                r_generator = RScriptGenerator()
                r_path = r_generator.generate_statistical_analysis(
                    study_name, str(templates_dir)
                )
                if Path(r_path).exists():
                    generated_templates['r_analysis'] = r_path
                    
                    # Validate R script has content
                    with open(r_path, 'r') as f:
                        r_content = f.read()
                    
                    if len(r_content) < 100:  # Minimal content check
                        return {'success': False, 'error': "Generated R script is too short"}
                        
            except Exception as e:
                print(f"⚠️  R template generation warning: {e}")
            
            # Test Stata script generation  
            try:
                stata_generator = StataIntegration()
                stata_path = stata_generator.generate_publication_analysis(
                    study_name, str(templates_dir)
                )
                if Path(stata_path).exists():
                    generated_templates['stata'] = stata_path
                    
            except Exception as e:
                print(f"⚠️  Stata template generation warning: {e}")
            
            if not generated_templates:
                return {'success': False, 'error': "No templates were successfully generated"}
            
            return {
                'success': True,
                'generated_templates': generated_templates
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _test_analysis_execution(self, study_name: str, output_dir: str, data_files: Dict[str, str]) -> Dict[str, Any]:
        """Test analysis execution (with tolerance for environment issues)."""
        try:
            execution_results = {}
            warnings = []
            critical_failures = []
            
            # Create data directory and copy test data
            analysis_dir = Path(output_dir) / 'analysis'
            analysis_dir.mkdir(exist_ok=True)
            
            data_dir = analysis_dir / 'data'
            data_dir.mkdir(exist_ok=True)
            
            # Copy data files to analysis directory
            for format_name, file_path in data_files.items():
                if Path(file_path).exists():
                    target_path = data_dir / f"{study_name}.{format_name}"
                    shutil.copy2(file_path, target_path)
            
            # Test Python/Pandas analysis (should always work)
            try:
                python_result = self._execute_python_analysis(study_name, data_dir)
                execution_results['python'] = python_result
                if not python_result['success']:
                    critical_failures.append(f"Python analysis: {python_result['error']}")
            except Exception as e:
                critical_failures.append(f"Python analysis execution: {e}")
            
            # Test R analysis (may not be available)
            try:
                r_result = self._execute_r_analysis(study_name, data_dir)
                execution_results['r'] = r_result
                if not r_result['success']:
                    warnings.append(f"R analysis: {r_result['error']}")
            except Exception as e:
                warnings.append(f"R analysis: {e}")
            
            # Test Jupyter execution (may have environment issues)
            try:
                jupyter_result = self._execute_jupyter_analysis(study_name, data_dir)
                execution_results['jupyter'] = jupyter_result
                if not jupyter_result['success']:
                    warnings.append(f"Jupyter analysis: {jupyter_result['error']}")
            except Exception as e:
                warnings.append(f"Jupyter analysis: {e}")
            
            return {
                'success': len(critical_failures) == 0,
                'execution_results': execution_results,
                'warnings': warnings,
                'critical_failures': critical_failures
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'critical_failures': [str(e)]
            }
    
    def _execute_python_analysis(self, study_name: str, data_dir: Path) -> Dict[str, Any]:
        """Execute basic Python analysis to validate data."""
        try:
            # Look for CSV file
            csv_files = list(data_dir.glob(f"{study_name}.csv"))
            if not csv_files:
                return {'success': False, 'error': "No CSV data file found"}
            
            # Load and analyze data
            df = pd.read_csv(csv_files[0])
            
            # Basic validation analysis
            analysis_results = {
                'record_count': len(df),
                'column_count': len(df.columns), 
                'missing_data_pct': (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100,
                'unique_experiments': df['experiment_id'].nunique() if 'experiment_id' in df.columns else 0,
                'unique_models': df['llm_model'].nunique() if 'llm_model' in df.columns else 0
            }
            
            # Calculate basic statistics if numerical columns exist
            numerical_columns = df.select_dtypes(include=['number']).columns
            if len(numerical_columns) > 0:
                analysis_results['numerical_summary'] = df[numerical_columns].describe().to_dict()
            
            # Save analysis results
            results_file = data_dir / f"{study_name}_python_analysis.json"
            with open(results_file, 'w') as f:
                json.dump(analysis_results, f, indent=2, default=str)
            
            return {
                'success': True,
                'analysis_results': analysis_results,
                'output_file': str(results_file)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _execute_r_analysis(self, study_name: str, data_dir: Path) -> Dict[str, Any]:
        """Execute R analysis if R is available."""
        try:
            # Check if R is available
            result = subprocess.run(['R', '--version'], capture_output=True, text=True)
            if result.returncode != 0:
                return {'success': False, 'error': "R not available"}
            
            # Create basic R analysis script
            r_script = f"""
library(utils)
data <- read.csv("{data_dir}/{study_name}.csv")
summary_stats <- summary(data)
cat("Records:", nrow(data), "\\n")
cat("Variables:", ncol(data), "\\n") 
write.csv(summary_stats, "{data_dir}/{study_name}_r_summary.csv")
"""
            
            script_file = data_dir / f"{study_name}_analysis.R"
            with open(script_file, 'w') as f:
                f.write(r_script)
            
            # Execute R script
            result = subprocess.run(['Rscript', str(script_file)], 
                                  capture_output=True, text=True, cwd=data_dir)
            
            return {
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr if result.returncode != 0 else None
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _execute_jupyter_analysis(self, study_name: str, data_dir: Path) -> Dict[str, Any]:
        """Execute Jupyter notebook analysis if available."""
        try:
            # Check if jupyter is available
            result = subprocess.run(['jupyter', '--version'], capture_output=True, text=True)
            if result.returncode != 0:
                return {'success': False, 'error': "Jupyter not available"}
            
            # Create minimal notebook for testing
            notebook = {
                "cells": [
                    {
                        "cell_type": "code",
                        "source": [
                            "import pandas as pd\n",
                            f"data = pd.read_csv('{study_name}.csv')\n",
                            "print(f'Loaded {len(data)} records')\n",
                            "print(data.info())"
                        ]
                    }
                ],
                "metadata": {"kernelspec": {"name": "python3"}},
                "nbformat": 4,
                "nbformat_minor": 4
            }
            
            notebook_file = data_dir / f"{study_name}_test.ipynb"
            with open(notebook_file, 'w') as f:
                json.dump(notebook, f, indent=2)
            
            # Execute notebook
            result = subprocess.run([
                'jupyter', 'nbconvert', '--to', 'notebook', '--execute', 
                '--inplace', str(notebook_file)
            ], capture_output=True, text=True, cwd=data_dir)
            
            return {
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr if result.returncode != 0 else None
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _test_replication_package(self, study_name: str, output_dir: str) -> Dict[str, Any]:
        """Test replication package creation."""
        try:
            builder = ReplicationPackageBuilder()
            
            package_path = builder.build_replication_package(
                study_name=study_name,
                study_description="End-to-end test replication package",
                output_path=output_dir
            )
            
            # Validate package structure
            package_dir = Path(package_path)
            if not package_dir.exists():
                return {'success': False, 'error': f"Replication package not created: {package_path}"}
            
            # Check for essential files
            essential_files = ['README.md', 'data_documentation.md']
            missing_files = []
            
            for file_name in essential_files:
                if not (package_dir / file_name).exists():
                    missing_files.append(file_name)
            
            if missing_files:
                return {'success': False, 'error': f"Missing essential files: {missing_files}"}
            
            return {
                'success': True,
                'package_path': package_path,
                'package_size': sum(f.stat().st_size for f in package_dir.rglob('*') if f.is_file())
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _test_integration_validation(self, study_name: str, output_dir: str, export_results: Dict[str, Any]) -> Dict[str, Any]:
        """Test integration between all components."""
        try:
            validation_results = {
                'data_integrity': True,
                'format_consistency': True,
                'cross_tool_compatibility': True,
                'errors': []
            }
            
            # Test data integrity across formats
            if 'csv' in export_results['data_files'] and 'json' in export_results['data_files']:
                try:
                    csv_df = pd.read_csv(export_results['data_files']['csv'])
                    
                    with open(export_results['data_files']['json'], 'r') as f:
                        json_data = json.load(f)
                    
                    json_records = len(json_data.get('data', []))
                    csv_records = len(csv_df)
                    
                    if json_records != csv_records:
                        validation_results['data_integrity'] = False
                        validation_results['errors'].append(
                            f"Record count mismatch: CSV={csv_records}, JSON={json_records}"
                        )
                        
                except Exception as e:
                    validation_results['data_integrity'] = False
                    validation_results['errors'].append(f"Data integrity check failed: {e}")
            
            # Test that data dictionary exists and is valid
            if 'data_dictionary' in export_results['data_files']:
                try:
                    with open(export_results['data_files']['data_dictionary'], 'r') as f:
                        data_dict = json.load(f)
                    
                    if 'variables' not in data_dict or len(data_dict['variables']) == 0:
                        validation_results['format_consistency'] = False
                        validation_results['errors'].append("Data dictionary is incomplete")
                        
                except Exception as e:
                    validation_results['format_consistency'] = False
                    validation_results['errors'].append(f"Data dictionary validation failed: {e}")
            
            # Overall success determination
            overall_success = all([
                validation_results['data_integrity'],
                validation_results['format_consistency'],
                validation_results['cross_tool_compatibility']
            ])
            
            return {
                'success': overall_success,
                'validation_results': validation_results
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


def test_cli_integration():
    """Test CLI integration with academic export functionality."""
    # Test the CLI wrapper
    try:
        result = subprocess.run([
            'python3', 'export_academic_data.py', '--help'
        ], capture_output=True, text=True)
        
        assert result.returncode == 0, f"CLI help failed: {result.stderr}"
        assert 'export academic data' in result.stdout.lower(), "CLI help output is incorrect"
        
        print("✅ CLI integration test passed")
        
    except Exception as e:
        pytest.fail(f"CLI integration test failed: {e}")


def test_academic_tool_installation():
    """Test academic tool installation verification."""
    try:
        result = subprocess.run([
            'python3', 'install_academic_tools.py', '--verify-installation'
        ], capture_output=True, text=True)
        
        # Installation verification may fail but should not crash
        assert 'Installation Verification Results' in result.stdout, "Installation verification output is incorrect"
        
        print("✅ Academic tool installation test passed")
        
    except Exception as e:
        pytest.fail(f"Academic tool installation test failed: {e}")


if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v", "--tb=short"]) 