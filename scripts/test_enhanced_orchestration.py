#!/usr/bin/env python3
"""
Test Enhanced Orchestration

Demonstrates end-to-end orchestration with the enhanced analysis pipeline.
This script shows how the orchestrator automatically runs experiments and 
generates comprehensive analysis reports.
"""

import sys
import json
import subprocess
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_enhanced_orchestration():
    """Test the enhanced orchestration with the demo experiment."""
    
    logger.info("🚀 Testing Enhanced End-to-End Orchestration")
    
    # Check if demo experiment exists
    experiment_file = Path("experiments/example_enhanced_orchestration.json")
    
    if not experiment_file.exists():
        logger.error(f"❌ Demo experiment file not found: {experiment_file}")
        return False
    
    # Check if demo corpus exists
    corpus_dir = Path("corpus/demo_texts")
    if not corpus_dir.exists() or not any(corpus_dir.glob("*.txt")):
        logger.error(f"❌ Demo corpus not found: {corpus_dir}")
        return False
    
    logger.info("✅ Prerequisites verified")
    
    # Run orchestrator with demo experiment
    logger.info("🎯 Running enhanced orchestration...")
    
    try:
        # Execute the orchestrator
        cmd = [
            sys.executable,
            "scripts/comprehensive_experiment_orchestrator.py",
            str(experiment_file),
            "--force-reregister"
        ]
        
        logger.info(f"Executing: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd="."
        )
        
        if result.returncode == 0:
            logger.info("✅ Orchestration completed successfully!")
            
            # Check for enhanced analysis outputs
            reports_dir = Path("experiment_reports/enhanced_analysis")
            if reports_dir.exists():
                logger.info("📊 Enhanced analysis outputs generated:")
                for report_dir in reports_dir.iterdir():
                    if report_dir.is_dir() and "Enhanced_Orchestration_Demo" in report_dir.name:
                        logger.info(f"   📁 Report directory: {report_dir}")
                        
                        # List key files
                        key_files = [
                            "pipeline_results.json",
                            "structured_results.json", 
                            "statistical_results.json",
                            "reliability_results.json",
                            "enhanced_analysis_report.html",
                            "README.md"
                        ]
                        
                        for filename in key_files:
                            file_path = report_dir / filename
                            if file_path.exists():
                                logger.info(f"   ✅ {filename}")
                            else:
                                logger.warning(f"   ⚠️ {filename} missing")
                        
                        # Check visualizations directory
                        viz_dir = report_dir / "visualizations"
                        if viz_dir.exists():
                            viz_count = len(list(viz_dir.glob("*.html")))
                            logger.info(f"   🎨 {viz_count} visualizations generated")
                        
                        break
            else:
                logger.warning("⚠️ No enhanced analysis outputs found")
            
            return True
        else:
            logger.error("❌ Orchestration failed!")
            logger.error(f"STDOUT: {result.stdout}")
            logger.error(f"STDERR: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error running orchestration: {e}")
        return False

def main():
    """Main execution function."""
    print("="*60)
    print("🎯 ENHANCED ORCHESTRATION TEST")
    print("="*60)
    print()
    print("This test demonstrates the enhanced end-to-end orchestration")
    print("capabilities of the narrative gravity analysis system.")
    print()
    print("The orchestrator will:")
    print("  • Run complete experiment with demo texts")
    print("  • Extract and structure results")
    print("  • Perform statistical hypothesis testing")
    print("  • Calculate interrater reliability metrics")
    print("  • Generate comprehensive visualizations")
    print("  • Create enhanced HTML reports")
    print("  • Export academic-ready data")
    print()
    
    try:
        success = test_enhanced_orchestration()
        
        if success:
            print("\n" + "="*60)
            print("🎉 ENHANCED ORCHESTRATION TEST PASSED")
            print("="*60)
            print()
            print("✅ End-to-end orchestration is working correctly!")
            print("📁 Check experiment_reports/enhanced_analysis/ for outputs")
            print("🌐 Open the HTML report for interactive analysis")
            print()
            sys.exit(0)
        else:
            print("\n" + "="*60)
            print("❌ ENHANCED ORCHESTRATION TEST FAILED")
            print("="*60)
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"❌ Test execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 