#!/usr/bin/env python3
"""
Monitored Experiment Runner
===========================

Enhanced experiment runner with comprehensive error monitoring and logging.
Captures all errors, parsing failures, and issues for debugging.

Usage:
    python3 monitored_experiment_runner.py path/to/experiment.yaml
"""

import os
import sys
import json
import yaml
import asyncio
import logging
import traceback
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

class ExperimentErrorMonitor:
    """Comprehensive error monitoring and logging system"""
    
    def __init__(self, experiment_name: str):
        self.experiment_name = experiment_name
        self.start_time = datetime.now()
        self.errors = []
        self.parsing_failures = []
        self.model_failures = []
        self.raw_responses = {}
        
        # Setup logging directory
        self.log_dir = Path(f"error_logs_{self.start_time.strftime('%Y%m%d_%H%M%S')}")
        self.log_dir.mkdir(exist_ok=True)
        
        # Setup comprehensive logging
        self.setup_logging()
        
    def setup_logging(self):
        """Setup detailed logging to files"""
        # Main error log
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_dir / 'experiment_errors.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger('ExperimentMonitor')
        self.logger.info(f"🔍 Error monitoring started for: {self.experiment_name}")
        self.logger.info(f"📁 Log directory: {self.log_dir}")
        
    def log_parsing_failure(self, model: str, raw_response: str, error: str):
        """Log detailed parsing failure information"""
        failure_info = {
            'timestamp': datetime.now().isoformat(),
            'model': model,
            'error': str(error),
            'raw_response_length': len(raw_response),
            'raw_response_preview': raw_response[:500] if raw_response else "EMPTY",
            'contains_json': '{' in raw_response if raw_response else False,
            'starts_with_json': raw_response.strip().startswith('{') if raw_response else False
        }
        
        self.parsing_failures.append(failure_info)
        self.raw_responses[f"{model}_{len(self.parsing_failures)}"] = raw_response
        
        # Save detailed parsing failure
        failure_file = self.log_dir / f"parsing_failure_{model}_{len(self.parsing_failures)}.json"
        with open(failure_file, 'w', encoding='utf-8') as f:
            json.dump(failure_info, f, indent=2, ensure_ascii=False)
            
        # Save raw response for inspection
        if raw_response:
            raw_file = self.log_dir / f"raw_response_{model}_{len(self.parsing_failures)}.txt"
            with open(raw_file, 'w', encoding='utf-8') as f:
                f.write(raw_response)
        
        self.logger.error(f"❌ PARSING FAILURE - {model}: {error}")
        self.logger.error(f"   Response length: {len(raw_response)} chars")
        self.logger.error(f"   Contains JSON: {'{' in raw_response if raw_response else False}")
        
    def generate_final_report(self):
        """Generate comprehensive final error report"""
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        report = {
            'experiment_name': self.experiment_name,
            'start_time': self.start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'duration_minutes': duration.total_seconds() / 60,
            'summary': {
                'total_parsing_failures': len(self.parsing_failures),
                'total_model_failures': len(self.model_failures),
                'total_general_errors': len(self.errors),
                'models_with_issues': list(set([f['model'] for f in self.parsing_failures + self.model_failures]))
            },
            'parsing_failures': self.parsing_failures,
            'model_failures': self.model_failures,
            'general_errors': self.errors
        }
        
        # Save final report
        report_file = self.log_dir / "FINAL_ERROR_REPORT.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        # Generate human-readable summary
        summary_file = self.log_dir / "ERROR_SUMMARY.md"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"# Error Report: {self.experiment_name}\n\n")
            f.write(f"**Duration**: {duration}\n")
            f.write(f"**Generated**: {end_time.isoformat()}\n\n")
            
            f.write("## Summary\n\n")
            f.write(f"- 🔴 Parsing Failures: {len(self.parsing_failures)}\n")
            f.write(f"- 🔴 Model Failures: {len(self.model_failures)}\n")
            f.write(f"- 🔴 General Errors: {len(self.errors)}\n")
            
            if self.parsing_failures:
                f.write("\n## Parsing Failures\n\n")
                for i, failure in enumerate(self.parsing_failures):
                    f.write(f"### {failure['model']} (#{i+1})\n")
                    f.write(f"- **Error**: {failure['error']}\n")
                    f.write(f"- **Response Length**: {failure['raw_response_length']} chars\n")
                    f.write(f"- **Contains JSON**: {failure['contains_json']}\n")
                    f.write(f"- **Raw File**: `raw_response_{failure['model']}_{i+1}.txt`\n\n")
        
        self.logger.info(f"📋 Final error report saved to: {report_file}")
        return report

def main():
    """Main entry point"""
    if len(sys.argv) != 2:
        print("Usage: python3 monitored_experiment_runner.py <experiment_yaml_file>")
        print("\nExample:")
        print("  python3 monitored_experiment_runner.py 0_workspace/byu_populism_project/experiments/exp_02_flagship_ensemble/exp_02_flagship_ensemble.yaml")
        sys.exit(1)
    
    experiment_path = sys.argv[1]
    
    if not Path(experiment_path).exists():
        print(f"❌ Experiment file not found: {experiment_path}")
        sys.exit(1)
    
    # Load experiment name for monitoring
    with open(experiment_path, 'r') as f:
        experiment_def = yaml.safe_load(f)
    experiment_name = experiment_def.get('name', 'Unknown Experiment')
    
    # Initialize monitor
    monitor = ExperimentErrorMonitor(experiment_name)
    
    try:
        print(f"🔍 Starting monitored experiment: {experiment_name}")
        print(f"📁 Error logs will be saved to: {monitor.log_dir}")
        print("="*80)
        
        # Import and run the actual experiment
        from discernus.experiments.run_experiment import ExperimentRunner
        
        # Create and run the experiment
        async def run_experiment():
            async with ExperimentRunner() as runner:
                return await runner.execute_experiment(experiment_path)
        
        result = asyncio.run(run_experiment())
        monitor.logger.info("✅ Experiment completed successfully!")
        
    except Exception as e:
        monitor.logger.error(f"💥 Experiment failed: {e}")
        monitor.logger.error(f"Full traceback: {traceback.format_exc()}")
        
    finally:
        # Always generate final report
        report = monitor.generate_final_report()
        
        print("\n" + "="*80)
        print("📊 FINAL ERROR MONITORING REPORT")
        print("="*80)
        print(f"Experiment: {experiment_name}")
        print(f"Duration: {report['summary'].get('duration_minutes', 0):.1f} minutes")
        print(f"Parsing Failures: {report['summary']['total_parsing_failures']}")
        print(f"Model Failures: {report['summary']['total_model_failures']}")
        print(f"General Errors: {report['summary']['total_general_errors']}")
        
        if report['summary']['models_with_issues']:
            print(f"Models with Issues: {', '.join(report['summary']['models_with_issues'])}")
            
        print(f"\n📁 All error logs saved to: {monitor.log_dir}")
        print(f"📋 Human-readable summary: {monitor.log_dir}/ERROR_SUMMARY.md")
        print(f"📋 Full JSON report: {monitor.log_dir}/FINAL_ERROR_REPORT.json")
        print("="*80)

if __name__ == "__main__":
    main() 