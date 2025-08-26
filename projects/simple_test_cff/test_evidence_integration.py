#!/usr/bin/env python3
"""
Test script to verify evidence integration in the synthesis pipeline
"""

import sys
import os
import json
sys.path.insert(0, '/Volumes/code/discernus')

def test_evidence_discovery():
    """Test if evidence artifacts can be discovered"""
    
    print("🔍 Testing Evidence Discovery...")
    
    # Check artifact registry
    registry_file = "shared_cache/artifacts/artifact_registry.json"
    if not os.path.exists(registry_file):
        print(f"❌ Registry file not found: {registry_file}")
        return
    
    with open(registry_file, 'r') as f:
        registry = json.load(f)
    
    print(f"✅ Registry loaded with {len(registry)} artifacts")
    
    # Look for evidence artifacts
    evidence_artifacts = []
    for artifact_hash, artifact_info in registry.items():
        metadata = artifact_info.get("metadata", {})
        artifact_type = metadata.get("artifact_type", "")
        if artifact_type.startswith("evidence_v6"):
            evidence_artifacts.append({
                'hash': artifact_hash,
                'type': artifact_type,
                'filename': artifact_info.get('human_filename', 'Unknown'),
                'size': artifact_info.get('size_bytes', 0)
            })
    
    print(f"\n📊 Evidence Artifacts Found: {len(evidence_artifacts)}")
    for ev in evidence_artifacts[:5]:  # Show first 5
        print(f"  - {ev['filename']} ({ev['type']}) - {ev['size']} bytes")
    
    if len(evidence_artifacts) > 5:
        print(f"  ... and {len(evidence_artifacts) - 5} more")
    
    # Test loading one evidence artifact
    if evidence_artifacts:
        test_artifact = evidence_artifacts[0]
        print(f"\n🧪 Testing loading of {test_artifact['filename']}...")
        
        evidence_file = f"shared_cache/artifacts/{test_artifact['filename']}"
        if os.path.exists(evidence_file):
            with open(evidence_file, 'r') as f:
                evidence_data = json.load(f)
            
            print(f"✅ Evidence file loaded successfully!")
            print(f"   - Total evidence pieces: {evidence_data.get('evidence_metadata', {}).get('total_evidence_pieces', 0)}")
            
            evidence_list = evidence_data.get('evidence_data', [])
            if evidence_list:
                first_evidence = evidence_list[0]
                print(f"   - First evidence: {first_evidence.get('quote_text', 'No quote')[:100]}...")
                print(f"   - Document: {first_evidence.get('document_name', 'Unknown')}")
                print(f"   - Dimension: {first_evidence.get('dimension', 'Unknown')}")
            else:
                print("   - No evidence_data found in file")
        else:
            print(f"❌ Evidence file not found: {evidence_file}")
    
    return evidence_artifacts

def test_synthesis_evidence_flow():
    """Test the synthesis evidence flow"""
    
    print("\n🔧 Testing Synthesis Evidence Flow...")
    
    # Simulate the orchestrator's evidence discovery logic
    registry_file = "shared_cache/artifacts/artifact_registry.json"
    with open(registry_file, 'r') as f:
        registry = json.load(f)
    
    # Collect evidence artifact hashes (same logic as orchestrator)
    evidence_hashes = []
    for artifact_hash, artifact_info in registry.items():
        metadata = artifact_info.get("metadata", {})
        if metadata.get("artifact_type", "").startswith("evidence_v6"):
            evidence_hashes.append(artifact_hash)
    
    print(f"📋 Orchestrator would find {len(evidence_hashes)} evidence artifacts")
    
    if evidence_hashes:
        print("✅ Evidence discovery working correctly")
        print(f"   - First evidence hash: {evidence_hashes[0][:8]}...")
        
        # Test if the evidence can be loaded
        test_hash = evidence_hashes[0]
        test_artifact = registry[test_hash]
        test_filename = test_artifact.get('human_filename', 'Unknown')
        
        print(f"   - Test artifact: {test_filename}")
        
        # Check if file exists
        evidence_file = f"shared_cache/artifacts/{test_filename}"
        if os.path.exists(evidence_file):
            print(f"   - File exists: ✅")
            
            # Try to load content
            try:
                with open(evidence_file, 'r') as f:
                    evidence_data = json.load(f)
                
                evidence_count = len(evidence_data.get('evidence_data', []))
                print(f"   - Evidence pieces: {evidence_count}")
                
                if evidence_count > 0:
                    print(f"   - Evidence loading: ✅")
                else:
                    print(f"   - Evidence loading: ❌ (no evidence data)")
                    
            except Exception as e:
                print(f"   - Evidence loading: ❌ (error: {e})")
        else:
            print(f"   - File exists: ❌")
    else:
        print("❌ No evidence artifacts found - this explains why synthesis has no evidence!")

if __name__ == "__main__":
    print("🚀 Evidence Integration Test")
    print("=" * 50)
    
    evidence_artifacts = test_evidence_discovery()
    test_synthesis_evidence_flow()
    
    print("\n" + "=" * 50)
    if evidence_artifacts:
        print("✅ Evidence discovery working - synthesis should have evidence")
    else:
        print("❌ Evidence discovery failed - synthesis will have no evidence")
