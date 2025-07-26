#!/usr/bin/env python3
"""
Discernus Enhanced Analysis Agent Evaluation Runner
=================================================

This script runs the promptfoo evaluation pipeline for the EnhancedAnalysisAgent
and provides summary results for quality assurance.

Usage:
    python run_eval.py [--model gemini-pro|gemini-flash]
"""

import json
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime
import argparse


def run_promptfoo_eval(model_filter=None):
    """
    Run the promptfoo evaluation and return results.
    
    Args:
        model_filter: Optional model to test (gemini-pro or gemini-flash)
    """
    print("🧪 Starting Discernus EnhancedAnalysisAgent Evaluation...")
    print(f"📍 Working directory: {os.getcwd()}")
    
    # Change to eval directory
    eval_dir = Path(__file__).parent
    os.chdir(eval_dir)
    
    try:
        # Build promptfoo command
        cmd = ["npx", "promptfoo", "eval"]
        if model_filter:
            cmd.extend(["--filter", model_filter])
            
        print(f"🚀 Running: {' '.join(cmd)}")
        
        # Run promptfoo evaluation
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode != 0:
            print(f"❌ Evaluation failed with return code {result.returncode}")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            return None
            
        print("✅ Evaluation completed successfully")
        
        # Load and return results
        results_file = eval_dir / "eval_results.json"
        if results_file.exists():
            with open(results_file, 'r') as f:
                return json.load(f)
        else:
            print(f"⚠️ Results file not found: {results_file}")
            return None
            
    except subprocess.TimeoutExpired:
        print("❌ Evaluation timed out after 5 minutes")
        return None
    except Exception as e:
        print(f"❌ Evaluation failed with error: {e}")
        return None


def analyze_results(results):
    """
    Analyze and report on evaluation results.
    
    Args:
        results: The promptfoo evaluation results
    """
    print("\n" + "="*60)
    print("📊 EVALUATION RESULTS SUMMARY")
    print("="*60)
    
    if not results or not results.get('results'):
        print("❌ No results to analyze")
        return
        
    total_tests = len(results['results'])
    passed_tests = 0
    failed_tests = 0
    
    print(f"🧪 Total test cases: {total_tests}")
    
    for i, result in enumerate(results['results']):
        test_desc = result.get('description', f'Test {i+1}')
        provider = result.get('provider', 'unknown')
        
        # Check if all assertions passed
        assertions = result.get('gradingResult', {}).get('componentResults', [])
        test_passed = all(assertion.get('pass', False) for assertion in assertions)
        
        if test_passed:
            passed_tests += 1
            status = "✅ PASS"
        else:
            failed_tests += 1
            status = "❌ FAIL"
            
        print(f"{status} | {provider} | {test_desc}")
        
        # Show failed assertions
        if not test_passed:
            for assertion in assertions:
                if not assertion.get('pass', False):
                    assertion_type = assertion.get('assertion', {}).get('type', 'unknown')
                    print(f"    ❌ Failed assertion: {assertion_type}")
    
    print(f"\n📈 Summary: {passed_tests}/{total_tests} tests passed ({passed_tests/total_tests*100:.1f}%)")
    
    if failed_tests > 0:
        print(f"⚠️  {failed_tests} tests failed - review output quality")
        return False
    else:
        print("🎉 All tests passed - agent is performing correctly!")
        return True


def main():
    """Main evaluation runner."""
    parser = argparse.ArgumentParser(description="Run Discernus EnhancedAnalysisAgent evaluation")
    parser.add_argument('--model', choices=['gemini-pro', 'gemini-flash'], 
                       help='Filter to specific model for testing')
    
    args = parser.parse_args()
    
    # Run evaluation
    results = run_promptfoo_eval(args.model)
    
    if results:
        success = analyze_results(results)
        sys.exit(0 if success else 1)
    else:
        print("❌ Evaluation failed to produce results")
        sys.exit(1)


if __name__ == "__main__":
    main() 