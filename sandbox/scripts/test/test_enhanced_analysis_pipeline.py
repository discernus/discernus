#!/usr/bin/env python3
"""
Test Enhanced Analysis Pipeline
Tests the complete pipeline with real IDITI data
"""

import sys
import pandas as pd
from pathlib import Path
import logging
import json

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import pipeline components
from scripts.extract_experiment_results import ExperimentResultsExtractor
from scripts.statistical_hypothesis_testing import StatisticalHypothesisTester
from scripts.interrater_reliability_analysis import InterraterReliabilityAnalyzer
from scripts.generate_comprehensive_visualizations import VisualizationGenerator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_enhanced_pipeline():
    """Test the complete enhanced analysis pipeline."""
    
    logger.info("🚀 Testing Enhanced Analysis Pipeline...")
    
    # Step 1: Create mock execution results (simulating orchestrator output)
    logger.info("📊 Step 1: Loading experimental data...")
    
    # Load real data from extracted results
    data_files = list(Path("exports/analysis_results/").glob("extracted_results_*.csv"))
    
    if not data_files:
        logger.error("No extracted results files found. Run extract_experiment_results.py first.")
        return False
    
    # Use most recent file
    latest_file = max(data_files, key=lambda x: x.stat().st_mtime)
    df = pd.read_csv(latest_file)
    
    logger.info(f"✅ Loaded {len(df)} analyses from {latest_file}")
    
    # Create mock execution results structure
    execution_results = {
        'total_analyses': len(df),
        'successful_analyses': len(df[df.get('success', True) == True]) if 'success' in df.columns else len(df),
        'failed_analyses': len(df[df.get('success', True) == False]) if 'success' in df.columns else 0,
        'total_cost': df['cost'].sum() if 'cost' in df.columns else 0.0,
        'cost_efficiency': df['cost'].mean() if 'cost' in df.columns else 0.0,
        'results': []
    }
    
    # Convert DataFrame rows to results format
    for _, row in df.iterrows():
        # Extract well scores
        well_scores = {}
        for col in df.columns:
            if col.startswith('well_'):
                if pd.notna(row[col]):
                    well_scores[col.replace('well_', '')] = row[col]
        
        result = {
            'analysis_id': row.get('run_id', f'analysis_{row.name}'),
            'text_id': row.get('analysis_text', f'text_{row.name}'),
            'framework': row.get('framework', 'unknown'),
            'llm_model': row.get('model_name', 'unknown'),
            'success': row.get('success', True),
            'api_cost': row.get('cost', 0.0),
            'duration_seconds': row.get('duration_seconds', 0.0),
            'framework_fit_score': 0.8,  # Mock quality score
            'well_scores': well_scores,
            'raw_scores': well_scores,  # Fallback for compatibility
            'narrative_position_x': row.get('narrative_x', 0.0),
            'narrative_position_y': row.get('narrative_y', 0.0),
            'timestamp': pd.Timestamp.now().isoformat()
        }
        
        execution_results['results'].append(result)
    
    logger.info(f"✅ Prepared {len(execution_results['results'])} results for analysis")
    
    # Step 2: Extract and structure results
    logger.info("📊 Step 2: Extracting and structuring results...")
    
    extractor = ExperimentResultsExtractor()
    structured_results = extractor.extract_results(execution_results)
    
    if 'error' in structured_results:
        logger.error(f"❌ Results extraction failed: {structured_results['error']}")
        return False
    
    logger.info(f"✅ Structured {len(structured_results['structured_data'])} records")
    
    # Step 3: Statistical hypothesis testing
    logger.info("🧪 Step 3: Running statistical hypothesis testing...")
    
    tester = StatisticalHypothesisTester()
    statistical_results = tester.test_hypotheses(structured_results)
    
    if 'error' in statistical_results:
        logger.error(f"❌ Statistical testing failed: {statistical_results['error']}")
        return False
    
    # Print hypothesis results
    summary = statistical_results.get('summary', {})
    logger.info(f"✅ Hypothesis testing complete - {summary.get('hypotheses_supported', 0)}/3 supported")
    
    # Step 4: Interrater reliability analysis
    logger.info("🔍 Step 4: Analyzing interrater reliability...")
    
    reliability_analyzer = InterraterReliabilityAnalyzer()
    reliability_results = reliability_analyzer.analyze_reliability(structured_results)
    
    if 'error' in reliability_results:
        logger.warning(f"⚠️ Reliability analysis limited: {reliability_results['error']}")
    else:
        logger.info("✅ Reliability analysis complete")
    
    # Step 5: Generate comprehensive visualizations
    logger.info("🎨 Step 5: Generating visualizations...")
    
    visualizer = VisualizationGenerator(output_dir="experiment_reports/analysis/test_visualizations")
    visualization_results = visualizer.generate_visualizations(
        structured_results,
        statistical_results,
        reliability_results
    )
    
    if 'error' in visualization_results:
        logger.error(f"❌ Visualization generation failed: {visualization_results['error']}")
        return False
    
    # Create visualization index
    index_file = visualizer.save_visualization_index()
    logger.info(f"✅ Generated {len(visualizer.generated_files)} visualizations")
    
    # Step 6: Combine all results (simulate enhanced analysis pipeline output)
    logger.info("📋 Step 6: Compiling comprehensive results...")
    
    enhanced_results = {
        'structured_results': structured_results,
        'statistical_results': statistical_results,
        'reliability_results': reliability_results,
        'visualization_results': visualization_results,
        'pipeline_status': 'success',
        'timestamp': pd.Timestamp.now().isoformat(),
        'summary': {
            'total_analyses': len(structured_results['structured_data']),
            'hypotheses_supported': summary.get('hypotheses_supported', 0),
            'overall_assessment': summary.get('overall_assessment', 'unknown'),
            'visualizations_generated': len(visualizer.generated_files),
            'key_findings': summary.get('key_findings', []),
            'recommendations': summary.get('recommendations', [])
        }
    }
    
    # Save comprehensive results
    output_dir = Path('experiment_reports/analysis')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    results_file = output_dir / f'enhanced_pipeline_test_results_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.json'
    
    with open(results_file, 'w') as f:
        json.dump(enhanced_results, f, indent=2, default=str)
    
    logger.info(f"✅ Enhanced analysis pipeline test complete!")
    logger.info(f"📁 Results saved to: {results_file}")
    logger.info(f"📊 Visualizations index: {index_file}")
    
    # Print final summary
    print("\n" + "="*60)
    print("🎉 ENHANCED ANALYSIS PIPELINE TEST RESULTS")
    print("="*60)
    print(f"📊 Total Analyses: {enhanced_results['summary']['total_analyses']}")
    print(f"🧪 Hypotheses Supported: {enhanced_results['summary']['hypotheses_supported']}/3")
    print(f"📈 Overall Assessment: {enhanced_results['summary']['overall_assessment']}")
    print(f"🎨 Visualizations Generated: {enhanced_results['summary']['visualizations_generated']}")
    
    if enhanced_results['summary']['key_findings']:
        print("\n📋 Key Findings:")
        for finding in enhanced_results['summary']['key_findings']:
            print(f"  • {finding}")
    
    if enhanced_results['summary']['recommendations']:
        print("\n💡 Recommendations:")
        for rec in enhanced_results['summary']['recommendations']:
            print(f"  • {rec}")
    
    print(f"\n📁 Detailed Results: {results_file}")
    print(f"📊 Visualizations: {index_file}")
    
    return True

def main():
    """Main execution function."""
    try:
        success = test_enhanced_pipeline()
        if success:
            logger.info("✅ Enhanced analysis pipeline test PASSED")
            sys.exit(0)
        else:
            logger.error("❌ Enhanced analysis pipeline test FAILED")
            sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Test execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 