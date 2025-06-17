#!/usr/bin/env python3
"""
Demo Enhanced Orchestration

Demonstrates the enhanced analysis pipeline using existing test data.
This shows how the orchestrator integrates with the enhanced analysis components
to provide end-to-end analysis capabilities.
"""

import sys
import json
import pandas as pd
from pathlib import Path
import logging
from datetime import datetime

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_mock_execution_results():
    """Create mock execution results for testing enhanced orchestration."""
    
    # Create mock results similar to what the orchestrator would produce
    mock_results = {
        'total_analyses': 4,
        'successful_analyses': 4,
        'failed_analyses': 0,
        'total_cost': 0.25,
        'cost_efficiency': 0.0625,
        'results': [
            {
                'analysis_id': 'demo_run_1_text_1',
                'text_id': 'demo_text_1',
                'framework': 'civic_virtue',
                'llm_model': 'gpt-4o',
                'success': True,
                'api_cost': 0.06,
                'duration_seconds': 25.4,
                'framework_fit_score': 0.85,
                'well_scores': {
                    'compassion': 0.9,
                    'equity': 0.8,
                    'solidarity': 0.7,
                    'hierarchy': 0.2,
                    'purity': 0.3,
                    'cruelty': 0.1,
                    'exploitation': 0.2,
                    'treachery': 0.1,
                    'rebellion': 0.6,
                    'corruption': 0.2
                },
                'narrative_position_x': 0.35,
                'narrative_position_y': 0.42,
                'timestamp': datetime.now().isoformat()
            },
            {
                'analysis_id': 'demo_run_1_text_2',
                'text_id': 'demo_text_2',
                'framework': 'civic_virtue',
                'llm_model': 'gpt-4o',
                'success': True,
                'api_cost': 0.058,
                'duration_seconds': 23.8,
                'framework_fit_score': 0.82,
                'well_scores': {
                    'compassion': 0.2,
                    'equity': 0.3,
                    'solidarity': 0.25,
                    'hierarchy': 0.85,
                    'purity': 0.9,
                    'cruelty': 0.15,
                    'exploitation': 0.2,
                    'treachery': 0.1,
                    'rebellion': 0.2,
                    'corruption': 0.15
                },
                'narrative_position_x': -0.32,
                'narrative_position_y': 0.38,
                'timestamp': datetime.now().isoformat()
            },
            {
                'analysis_id': 'demo_run_2_text_1',
                'text_id': 'demo_text_1',
                'framework': 'civic_virtue',
                'llm_model': 'gpt-4o',
                'success': True,
                'api_cost': 0.062,
                'duration_seconds': 26.1,
                'framework_fit_score': 0.87,
                'well_scores': {
                    'compassion': 0.85,
                    'equity': 0.82,
                    'solidarity': 0.75,
                    'hierarchy': 0.25,
                    'purity': 0.28,
                    'cruelty': 0.12,
                    'exploitation': 0.18,
                    'treachery': 0.08,
                    'rebellion': 0.65,
                    'corruption': 0.22
                },
                'narrative_position_x': 0.38,
                'narrative_position_y': 0.45,
                'timestamp': datetime.now().isoformat()
            },
            {
                'analysis_id': 'demo_run_2_text_2',
                'text_id': 'demo_text_2',
                'framework': 'civic_virtue',
                'llm_model': 'gpt-4o',
                'success': True,
                'api_cost': 0.07,
                'duration_seconds': 28.3,
                'framework_fit_score': 0.79,
                'well_scores': {
                    'compassion': 0.18,
                    'equity': 0.28,
                    'solidarity': 0.22,
                    'hierarchy': 0.88,
                    'purity': 0.92,
                    'cruelty': 0.12,
                    'exploitation': 0.25,
                    'treachery': 0.08,
                    'rebellion': 0.18,
                    'corruption': 0.12
                },
                'narrative_position_x': -0.35,
                'narrative_position_y': 0.41,
                'timestamp': datetime.now().isoformat()
            }
        ]
    }
    
    return mock_results

def demo_enhanced_orchestration():
    """Demonstrate the enhanced orchestration capabilities."""
    
    logger.info("🚀 Demo: Enhanced Analysis Pipeline Orchestration")
    
    try:
        # Import the enhanced analysis pipeline from the orchestrator
        from scripts.comprehensive_experiment_orchestrator import ExperimentOrchestrator
        
        # Create orchestrator instance
        orchestrator = ExperimentOrchestrator()
        
        # Create mock experiment data
        mock_experiment = {
            'experiment_meta': {
                'name': 'Enhanced_Orchestration_Demo',
                'description': 'Demonstration of enhanced analysis capabilities',
                'created': datetime.now().isoformat()
            },
            'enhanced_analysis': {
                'enabled': True,
                'generate_html_report': True,
                'generate_academic_exports': True,
                'configuration': {
                    'statistical_testing': {'enabled': True},
                    'reliability_analysis': {'enabled': True},
                    'visualizations': {'enabled': True}
                }
            }
        }
        
        # Create mock execution results
        execution_results = create_mock_execution_results()
        
        logger.info(f"📊 Mock execution results created: {execution_results['total_analyses']} analyses")
        
        # Run enhanced analysis pipeline
        logger.info("🎯 Running enhanced analysis pipeline...")
        enhanced_results = orchestrator.execute_enhanced_analysis_pipeline(
            execution_results, 
            mock_experiment
        )
        
        # Check results
        if enhanced_results['pipeline_status'] == 'success':
            logger.info("✅ Enhanced analysis pipeline completed successfully!")
            
            # Print summary
            summary = enhanced_results['summary']
            logger.info(f"📊 Analysis Summary:")
            logger.info(f"   • Total Analyses: {summary['total_analyses']}")
            logger.info(f"   • Statistical Tests: {summary['statistical_tests_run']}")
            logger.info(f"   • Hypotheses Supported: {summary['hypotheses_supported']}")
            logger.info(f"   • Reliability Metrics: {'✅' if summary['reliability_metrics_calculated'] else '❌'}")
            logger.info(f"   • Visualizations: {summary['visualizations_generated']}")
            logger.info(f"   • HTML Report: {'✅' if summary['html_report_generated'] else '❌'}")
            logger.info(f"   • Academic Exports: {'✅' if summary['academic_exports_generated'] else '❌'}")
            
            # Show output directories
            experiment_dir = enhanced_results['experiment_directory']
            enhanced_analysis_dir = enhanced_results['enhanced_analysis_directory']
            logger.info(f"📁 Experiment directory: {experiment_dir}")
            logger.info(f"📁 Enhanced analysis outputs: {enhanced_analysis_dir}")
            
            # List generated files
            files_generated = enhanced_results['files_generated']
            logger.info("📄 Generated Files:")
            for file_type, file_path in files_generated.items():
                if file_path:
                    status = "✅" if Path(file_path).exists() else "❌"
                    logger.info(f"   {status} {file_type}: {file_path}")
            
            return True, experiment_dir
            
        else:
            logger.error(f"❌ Enhanced analysis pipeline failed: {enhanced_results.get('error', 'Unknown error')}")
            return False, None
            
    except Exception as e:
        logger.error(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None

def main():
    """Main execution function."""
    print("="*60)
    print("🎯 ENHANCED ORCHESTRATION DEMO")
    print("="*60)
    print()
    print("This demo showcases the enhanced analysis pipeline capabilities")
    print("that are now integrated into the orchestrator for end-to-end")
    print("experiment orchestration.")
    print()
    print("The enhanced pipeline includes:")
    print("  • 📊 Results extraction and structuring")
    print("  • 🧪 Statistical hypothesis testing")
    print("  • 🔍 Interrater reliability analysis")
    print("  • 🎨 Comprehensive visualizations")
    print("  • 📄 Enhanced HTML reports")
    print("  • 🎓 Academic export integration")
    print()
    
    try:
        success, output_dir = demo_enhanced_orchestration()
        
        if success:
            print("\n" + "="*60)
            print("🎉 ENHANCED ORCHESTRATION DEMO SUCCESSFUL")
            print("="*60)
            print()
            print("✅ The enhanced analysis pipeline is now fully integrated!")
            print("✅ End-to-end orchestration capabilities demonstrated!")
            print()
            print(f"📁 Generated outputs: {output_dir}")
            print()
            print("🚀 Next Steps:")
            print("  • Review the generated HTML report")
            print("  • Examine statistical analysis results")
            print("  • Check visualizations for insights")
            print("  • Use academic exports for publication")
            print()
            print("🎯 The orchestrator now provides complete end-to-end")
            print("   experiment execution with advanced analytics!")
            
        else:
            print("\n" + "="*60)
            print("❌ ENHANCED ORCHESTRATION DEMO FAILED")
            print("="*60)
            print()
            print("Please check the logs above for details.")
        
    except Exception as e:
        logger.error(f"❌ Demo execution failed: {e}")
        return False

if __name__ == "__main__":
    main() 