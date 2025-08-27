#!/usr/bin/env python3
"""
Test Fact Checker Agent with Real Data

This script tests the fact checker agent using the actual synthesis report,
evidence data, and framework specification from the simple_test_cff project.
"""

import os
import sys
import json
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../discernus'))

from discernus.agents.fact_checker_agent.agent import FactCheckerAgent
from discernus.core.hybrid_corpus_service import HybridCorpusService

def test_fact_checker_with_real_data():
    """Test the fact checker agent with real project data."""
    print("🧪 Testing Fact Checker Agent with Real Data")
    print("=" * 60)
    
    try:
        # Create the fact checker agent
        print("🔧 Creating Fact Checker Agent...")
        agent = FactCheckerAgent()
        
        # Set the working directory to this project
        agent.working_dir = Path.cwd()
        print(f"📁 Working directory: {agent.working_dir}")
        
        # Create a mock corpus index service (since we don't have Typesense running)
        print("🔍 Creating mock corpus index service...")
        agent.corpus_index_service = HybridCorpusService()
        
        # Debug: Check what resources are being discovered
        print("\n🔍 DEBUGGING RESOURCE DISCOVERY:")
        print(f"Synthesis report found: {bool(agent._discover_synthesis_report())}")
        print(f"Evidence data found: {bool(agent._discover_evidence_data())}")
        print(f"Framework spec found: {bool(agent._discover_framework_spec())}")
        print(f"Raw analysis data found: {bool(agent._discover_raw_analysis_data())}")
        print(f"Derived metrics data found: {bool(agent._discover_derived_metrics_data())}")
        print(f"Statistical results data found: {bool(agent._discover_statistical_results_data())}")
        
        # Debug: Check the actual content being sent to LLM
        if hasattr(agent, '_prepare_fact_checking_context'):
            synthesis_report = agent._discover_synthesis_report()
            evidence_data = agent._discover_evidence_data()
            framework_spec = agent._discover_framework_spec()
            corpus_index, search_wrappers = agent._discover_semantic_index_with_wrapper(['corpus_search', 'quote_validation'])
            raw_analysis_data = agent._discover_raw_analysis_data()
            derived_metrics_data = agent._discover_derived_metrics_data()
            statistical_results_data = agent._discover_statistical_results_data()
            
            context = agent._prepare_fact_checking_context(
                synthesis_report, evidence_data, framework_spec, corpus_index, 
                search_wrappers, raw_analysis_data, derived_metrics_data, statistical_results_data
            )
            print(f"\n📝 CONTEXT BEING SENT TO LLM (first 500 chars):")
            print(context[:500])
            print(f"\n📊 CONTEXT LENGTH: {len(context)} characters")
        
        # Run the fact checker
        print("\n🚀 Running fact checker agent...")
        result = agent.run()
        
        print("\n📊 FACT CHECKER RESULTS:")
        print("=" * 40)
        print(f"Status: {result.get('status', 'unknown')}")
        
        if result.get('status') == 'failed':
            print(f"Error: {result.get('error', 'unknown error')}")
            print(f"Summary: {result.get('summary', 'no summary')}")
        else:
            print(f"Findings count: {len(result.get('findings', []))}")
            print(f"Resources used: {result.get('resources_used', {})}")
            print(f"Validation summary: {result.get('validation_summary', {})}")
            
            # Show findings
            if result.get('findings'):
                print("\n🔍 FINDINGS:")
                for i, finding in enumerate(result['findings'], 1):
                    print(f"\n{i}. {finding.get('check_name', 'Unknown check')}")
                    print(f"   Severity: {finding.get('severity', 'Unknown')}")
                    print(f"   Category: {finding.get('category', 'Unknown')}")
                    print(f"   Description: {finding.get('description', 'No description')}")
                    print(f"   Priority: {finding.get('priority', 'Unknown')}")
        
        return result
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = test_fact_checker_with_real_data()
    if result:
        print(f"\n✅ Test completed successfully")
    else:
        print(f"\n❌ Test failed")
