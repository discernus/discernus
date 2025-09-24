#!/usr/bin/env python3
"""
Test whether base64 encoding vs plain text affects framework usage
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone

sys.path.append('/Volumes/code/discernus')
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway

def test_framework_encoding():
    """Test both base64 and plain text framework provision."""
    
    # Setup
    experiment_dir = Path("/Volumes/code/discernus/tmp")
    test_dir = Path("/Volumes/code/discernus/test_thin_approach")
    
    security = ExperimentSecurityBoundary(experiment_dir)
    audit = AuditLogger(security, experiment_dir / "logs")
    storage = LocalArtifactStorage(security, experiment_dir / "artifacts")
    gateway = EnhancedLLMGateway(audit)
    
    # Load framework and document
    with open(experiment_dir / "framework" / "pdaf_v10_0_2.md", 'r') as f:
        framework_content = f.read()
    
    with open(experiment_dir / "corpus" / "Trump_SOTU_2020.txt", 'r') as f:
        doc_content = f.read()
    
    print("=== TESTING FRAMEWORK ENCODING EFFECTS ===")
    print()
    
    # Test 1: Plain text framework
    print("TEST 1: Plain Text Framework")
    plain_text_prompt = f"""You are an expert discourse analyst. Analyze this document using the provided framework.

**CRITICAL: You MUST use the exact framework provided below. Do not create your own dimensions.**

{f"=== FRAMEWORK ===\n{framework_content}\n"}

=== DOCUMENT ===
{doc_content}

Please analyze this document using the provided framework and return the dimensional scores."""

    print(f"Plain text prompt length: {len(plain_text_prompt)} characters")
    
    response1 = gateway.execute_call(
        model="vertex_ai/gemini-2.5-flash",
        prompt=plain_text_prompt
    )
    
    if isinstance(response1, tuple):
        content1, metadata1 = response1
    else:
        content1 = response1.get('content', '')
        metadata1 = response1.get('metadata', {})
    
    print(f"Response length: {len(content1)} characters")
    
    # Test 2: Base64 encoded framework
    print("\nTEST 2: Base64 Encoded Framework")
    import base64
    framework_b64 = base64.b64encode(framework_content.encode('utf-8')).decode('utf-8')
    
    base64_prompt = f"""You are an expert discourse analyst. Analyze this document using the provided framework.

**CRITICAL: You MUST use the exact framework provided below. Do not create your own dimensions.**

=== FRAMEWORK 1 (base64 encoded) ===
{framework_b64}

=== DOCUMENT ===
{doc_content}

Please analyze this document using the provided framework and return the dimensional scores."""

    print(f"Base64 prompt length: {len(base64_prompt)} characters")
    
    response2 = gateway.execute_call(
        model="vertex_ai/gemini-2.5-flash",
        prompt=base64_prompt
    )
    
    if isinstance(response2, tuple):
        content2, metadata2 = response2
    else:
        content2 = response2.get('content', '')
        metadata2 = response2.get('metadata', {})
    
    print(f"Response length: {len(content2)} characters")
    
    # Save results
    results = {
        'test_timestamp': datetime.now(timezone.utc).isoformat(),
        'plain_text_test': {
            'prompt': plain_text_prompt,
            'response': content1,
            'metadata': metadata1
        },
        'base64_test': {
            'prompt': base64_prompt,
            'response': content2,
            'metadata': metadata2
        }
    }
    
    with open(test_dir / "artifacts" / "framework_encoding_test.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {test_dir / 'artifacts' / 'framework_encoding_test.json'}")
    
    # Quick analysis
    print("\n=== QUICK ANALYSIS ===")
    
    # Check if responses mention PDAF dimensions
    pdaf_dims = ['manichaean_people_elite_framing', 'crisis_restoration_narrative', 'popular_sovereignty_claims']
    
    plain_text_uses_pdaf = any(dim in content1 for dim in pdaf_dims)
    base64_uses_pdaf = any(dim in content2 for dim in pdaf_dims)
    
    print(f"Plain text uses PDAF dimensions: {plain_text_uses_pdaf}")
    print(f"Base64 uses PDAF dimensions: {base64_uses_pdaf}")
    
    if plain_text_uses_pdaf and not base64_uses_pdaf:
        print("CONCLUSION: Base64 encoding prevents framework usage!")
    elif not plain_text_uses_pdaf and base64_uses_pdaf:
        print("CONCLUSION: Plain text prevents framework usage!")
    elif plain_text_uses_pdaf and base64_uses_pdaf:
        print("CONCLUSION: Both formats work for framework usage")
    else:
        print("CONCLUSION: Neither format works for framework usage")

if __name__ == "__main__":
    test_framework_encoding()
