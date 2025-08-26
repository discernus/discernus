#!/usr/bin/env python3
"""
Test script for the EvidenceRetriever agent
"""

import sys
import os
import json
sys.path.insert(0, '/Volumes/code/discernus')

from discernus.agents.evidence_retriever_agent import EvidenceRetrieverAgent

def test_evidence_retriever():
    """Test the EvidenceRetriever agent"""
    
    print("🧪 Testing EvidenceRetriever Agent")
    print("=" * 50)
    
    # Configuration
    config = {
        'experiment_path': '/Volumes/code/discernus/projects/simple_test_cff',
        'run_id': 'test_run'
    }
    
    # Create agent
    print("📋 Creating EvidenceRetriever agent...")
    agent = EvidenceRetrieverAgent(config)
    print("✅ Agent created successfully")
    
    # Get statistical results hash from registry
    print("\n📊 Loading artifact registry...")
    registry_file = "shared_cache/artifacts/artifact_registry.json"
    with open(registry_file, 'r') as f:
        registry = json.load(f)
    
    # Find framework and statistical results artifacts (use the most recent ones)
    framework_hash = None
    statistical_results_hash = None
    evidence_artifact_hashes = []
    
    for artifact_hash, metadata in registry.items():
        if metadata.get('metadata', {}).get('artifact_type') == 'framework_specification':
            if not framework_hash or metadata.get('created_at', '') > registry[framework_hash].get('created_at', ''):
                framework_hash = artifact_hash
        elif metadata.get('metadata', {}).get('artifact_type') == 'statistical_results_with_data':
            if not statistical_results_hash or metadata.get('created_at', '') > registry[statistical_results_hash].get('created_at', ''):
                statistical_results_hash = artifact_hash
        elif metadata.get('metadata', {}).get('artifact_type', '').startswith('evidence_v6'):
            evidence_artifact_hashes.append(artifact_hash)
    
    if not framework_hash:
        print("⚠️ No framework specification artifact found, creating one from CFF file...")
        # Create a framework specification artifact from the CFF file
        framework_spec = {
            "name": "Cohesive Flourishing Framework (CFF) v10.1",
            "description": "A comprehensive tool for analyzing political and social discourse to understand its impact on community cohesion and democratic health",
            "dimensions": [
                "Tribal Dominance vs Individual Dignity",
                "Fear vs Hope", 
                "Envy vs Compersion",
                "Enmity vs Amity",
                "Fragmentative Goals vs Cohesive Goals"
            ],
            "source_file": "cff_v10.md"
        }
        
        # Store it as an artifact
        framework_content = json.dumps(framework_spec, indent=2).encode('utf-8')
        framework_metadata = {
            "artifact_type": "framework_specification",
            "agent": "test_script",
            "type": "framework_spec"
        }
        framework_hash = agent.artifact_storage.put_artifact(framework_content, framework_metadata)
        print(f"✅ Created framework specification artifact: {framework_hash}")
    
    if not statistical_results_hash:
        print("❌ No statistical results artifact found")
        return
    
    if not evidence_artifact_hashes:
        print("❌ No evidence artifacts found")
        return
    
    print(f"✅ Found framework: {framework_hash}")
    print(f"✅ Found statistical results: {statistical_results_hash}")
    print(f"✅ Found {len(evidence_artifact_hashes)} evidence artifacts")
    
    # Test the agent
    print(f"\n🚀 Running EvidenceRetriever agent...")
    try:
        results = agent.run(
            framework_hash=framework_hash,
            statistical_results_hash=statistical_results_hash,
            evidence_artifact_hashes=evidence_artifact_hashes
        )
        
        print("✅ Agent execution successful!")
        print(f"🏗️ Framework: {results['framework']}")
        print(f"📝 Evidence quotes found: {results['evidence_quotes_found']}")
        print(f"💾 Evidence artifact hash: {results['evidence_artifact_hash']}")
        
        # Show some evidence results
        print(f"\n🔍 Evidence Results Preview:")
        for i, result in enumerate(results['evidence_results'][:3]):  # Show first 3
            finding = result['finding']
            quotes = result['quotes']
            print(f"  Finding {i+1}: {finding.get('type', 'unknown')} - {finding.get('description', 'No description')}")
            print(f"    Queries used: {', '.join(result.get('queries_used', [])[:2])}")
            print(f"    Quotes found: {len(quotes)}")
            if quotes:
                quote_text = quotes[0].get('quote_text', 'No quote')[:100]
                print(f"    Sample quote: \"{quote_text}...\"")
            print()
        
    except Exception as e:
        print(f"❌ Agent execution failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_evidence_retriever()
