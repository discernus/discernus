#!/usr/bin/env python3
"""
Academic Pipeline Orchestrator - Priority 3 Enhancement

Master orchestration script that executes complete academic analysis workflow.
Integrates data export, template generation, documentation, and validation.

Usage:
    python academic_pipeline.py --study-name study2025 --execute-all
    python academic_pipeline.py --study-config config.yaml
"""

import argparse
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# Add src to path for development mode
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.narrative_gravity.academic.data_export import AcademicDataExporter, ReplicationPackageBuilder


class AcademicPipeline:
    """Master orchestrator for complete academic analysis workflow."""
    
    def __init__(self, study_name: str, output_dir: str = "academic_output"):
        self.study_name = study_name
        self.output_base = Path(output_dir)
        self.cli_base = Path(__file__).parent
        
        # Create output directories
        for subdir in ['data', 'analysis', 'documentation', 'validation']:
            (self.output_base / subdir).mkdir(parents=True, exist_ok=True)
    
    def execute_full_pipeline(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute complete academic analysis pipeline."""
        
        print("🚀 Academic Analysis Pipeline Starting")
        print(f"📊 Study: {self.study_name}")
        print(f"📁 Output: {self.output_base}")
        print("=" * 50)
        
        results = {
            'study_name': self.study_name,
            'execution_date': datetime.now().isoformat(),
            'stages': {}
        }
        
        try:
            # Stage 1: Data Export
            if config.get('export_data', True):
                print("\n📊 STAGE 1: Data Export")
                results['stages']['data_export'] = self.run_data_export(config)
            
            # Stage 2: Analysis Templates
            if config.get('generate_templates', True):
                print("\n💻 STAGE 2: Analysis Templates")
                results['stages']['templates'] = self.run_template_generation(config)
            
            # Stage 3: Documentation
            if config.get('generate_docs', True):
                print("\n📚 STAGE 3: Documentation")
                results['stages']['documentation'] = self.run_documentation(config)
            
            # Stage 4: Replication Package
            if config.get('create_package', True):
                print("\n📦 STAGE 4: Replication Package")
                results['stages']['package'] = self.run_package_creation(config)
            
            # Stage 5: Validation
            if config.get('run_validation', True):
                print("\n✅ STAGE 5: Validation")
                results['stages']['validation'] = self.run_validation()
            
            print("\n🎉 Pipeline Complete!")
            self.save_results(results)
            return results
            
        except Exception as e:
            print(f"\n❌ Pipeline failed: {e}")
            results['error'] = str(e)
            self.save_results(results)
            raise
    
    def run_data_export(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute data export stage."""
        
        cmd = [
            'python3', str(self.cli_base / 'export_academic_data.py'),
            '--study-name', self.study_name,
            '--output-dir', str(self.output_base / 'data'),
            '--format', 'all'
        ]
        
        # Add optional filters
        if config.get('frameworks'):
            cmd.extend(['--frameworks', ','.join(config['frameworks'])])
        if config.get('start_date'):
            cmd.extend(['--start-date', config['start_date']])
        if config.get('end_date'):
            cmd.extend(['--end-date', config['end_date']])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Data export completed")
            return {'status': 'success', 'output': result.stdout}
        else:
            print(f"   ❌ Data export failed: {result.stderr}")
            return {'status': 'failed', 'error': result.stderr}
    
    def run_template_generation(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute template generation stage."""
        
        cmd = [
            'python3', str(self.cli_base / 'generate_analysis_templates.py'),
            '--study-name', self.study_name,
            '--templates', 'all',
            '--output-dir', str(self.output_base / 'analysis')
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Template generation completed")
            return {'status': 'success', 'output': result.stdout}
        else:
            print(f"   ❌ Template generation failed: {result.stderr}")
            return {'status': 'failed', 'error': result.stderr}
    
    def run_documentation(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute documentation generation stage."""
        
        cmd = [
            'python3', str(self.cli_base / 'generate_documentation.py'),
            '--study-name', self.study_name,
            '--doc-type', 'all',
            '--output-dir', str(self.output_base / 'documentation')
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Documentation generation completed")
            return {'status': 'success', 'output': result.stdout}
        else:
            print(f"   ❌ Documentation generation failed: {result.stderr}")
            return {'status': 'failed', 'error': result.stderr}
    
    def run_package_creation(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute replication package creation."""
        
        cmd = [
            'python3', str(self.cli_base / 'export_academic_data.py'),
            '--study-name', self.study_name,
            '--replication-package',
            '--description', f'Academic analysis study: {self.study_name}'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Replication package created")
            return {'status': 'success', 'output': result.stdout}
        else:
            print(f"   ❌ Package creation failed: {result.stderr}")
            return {'status': 'failed', 'error': result.stderr}
    
    def run_validation(self) -> Dict[str, Any]:
        """Execute validation tests."""
        
        validation_results = {}
        
        # Validate data export
        data_dir = self.output_base / 'data'
        expected_files = [f"{self.study_name}.csv", f"{self.study_name}.json"]
        
        missing_files = [f for f in expected_files if not (data_dir / f).exists()]
        
        if missing_files:
            validation_results['data_export'] = {
                'status': 'fail',
                'missing_files': missing_files
            }
        else:
            validation_results['data_export'] = {
                'status': 'pass',
                'files_created': len(expected_files)
            }
        
        # Validate templates
        templates_dir = self.output_base / 'analysis'
        template_files = [
            f"notebooks/{self.study_name}_exploration.ipynb",
            f"r_scripts/{self.study_name}_analysis.R",
            f"stata_scripts/{self.study_name}_publication.do"
        ]
        
        missing_templates = [f for f in template_files if not (templates_dir / f).exists()]
        
        if missing_templates:
            validation_results['templates'] = {
                'status': 'fail',
                'missing_templates': missing_templates
            }
        else:
            validation_results['templates'] = {
                'status': 'pass',
                'templates_created': len(template_files)
            }
        
        # Summary
        passed_tests = sum(1 for result in validation_results.values() 
                          if result['status'] == 'pass')
        total_tests = len(validation_results)
        
        validation_results['summary'] = {
            'passed': passed_tests,
            'total': total_tests,
            'success_rate': (passed_tests / total_tests) * 100
        }
        
        print(f"   ✅ Validation: {passed_tests}/{total_tests} tests passed")
        
        return validation_results
    
    def save_results(self, results: Dict[str, Any]):
        """Save pipeline results."""
        results_path = self.output_base / 'validation' / f"{self.study_name}_results.json"
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"📋 Results saved: {results_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Academic Analysis Pipeline Orchestrator"
    )
    
    parser.add_argument(
        "--study-name",
        required=True,
        help="Study name for pipeline execution"
    )
    
    parser.add_argument(
        "--output-dir",
        default="academic_pipeline_output",
        help="Output directory for pipeline results"
    )
    
    parser.add_argument(
        "--frameworks",
        help="Comma-separated framework names"
    )
    
    parser.add_argument(
        "--start-date",
        help="Start date for data filtering (YYYY-MM-DD)"
    )
    
    parser.add_argument(
        "--end-date", 
        help="End date for data filtering (YYYY-MM-DD)"
    )
    
    parser.add_argument(
        "--execute-all",
        action="store_true",
        help="Execute all pipeline stages"
    )
    
    parser.add_argument(
        "--export-data",
        action="store_true",
        help="Export data only"
    )
    
    parser.add_argument(
        "--generate-templates",
        action="store_true",
        help="Generate templates only"
    )
    
    args = parser.parse_args()
    
    # Build configuration
    config = {
        'export_data': args.execute_all or args.export_data,
        'generate_templates': args.execute_all or args.generate_templates,
        'generate_docs': args.execute_all,
        'create_package': args.execute_all,
        'run_validation': args.execute_all
    }
    
    if args.frameworks:
        config['frameworks'] = args.frameworks.split(',')
    if args.start_date:
        config['start_date'] = args.start_date
    if args.end_date:
        config['end_date'] = args.end_date
    
    try:
        # Execute pipeline
        pipeline = AcademicPipeline(args.study_name, args.output_dir)
        results = pipeline.execute_full_pipeline(config)
        
        # Print summary
        print("\n" + "="*50)
        print("🎉 ACADEMIC PIPELINE COMPLETE")
        print("="*50)
        print(f"📊 Study: {results['study_name']}")
        print(f"📁 Output: {args.output_dir}")
        
        if 'validation' in results['stages']:
            validation = results['stages']['validation']
            success_rate = validation['summary']['success_rate']
            print(f"✅ Validation: {success_rate:.1f}% passed")
        
    except Exception as e:
        print(f"❌ Pipeline failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 