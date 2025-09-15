#!/usr/bin/env python3
"""
Test to see if we can make the LLM show us the three independent analyses
instead of just the final aggregated result
"""

import json
import sys
from pathlib import Path
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway

sys.path.append('/Volumes/code/discernus')
from tmp.AnalysisAgent.prompt_builder import create_analysis_prompt

def test_three_shot_visibility():
    """Test if we can see the three independent analyses."""
    
    # Setup experiment environment
    experiment_dir = Path("/Volumes/code/discernus/tmp")
    
    # Initialize components
    security = ExperimentSecurityBoundary(experiment_dir)
    audit = AuditLogger(security, experiment_dir / "logs")
    storage = LocalArtifactStorage(security, experiment_dir / "artifacts")
    gateway = EnhancedLLMGateway(audit)
    
    # Load framework
    framework_path = experiment_dir / "framework" / "pdaf_v10_0_2.md"
    with open(framework_path, 'r') as f:
        framework_content = f.read()
    
    # Load document
    doc_path = experiment_dir / "corpus" / "Trump_SOTU_2020.txt"
    with open(doc_path, 'r') as f:
        doc_content = f.read()
    
    # Prepare documents
    documents = [{
        'index': 0,
        'filename': 'Trump_SOTU_2020.txt',
        'hash': 'test_hash',
        'content': doc_content
    }]
    
    # Create a modified prompt that asks for the three analyses to be shown
    modified_prompt = f"""You are an expert discourse analyst specializing in dimensional analysis of political and social texts. Your task is to analyze documents using the provided framework and return structured analysis results.

**ANALYSIS REQUIREMENTS:**
- Apply the framework's dimensional definitions precisely
- Score each dimension on a 0.0-1.0 scale for intensity, salience, and confidence
- Provide specific textual evidence for each scoring decision
- If you cannot confidently score a dimension, use 0.0 score with low confidence and provide explanation in evidence

**THREE INDEPENDENT ANALYTICAL APPROACHES (NEW REQUIREMENT):**

**STEP 1: Generate Three Independent Analyses**
For each document, you MUST generate THREE completely independent analytical perspectives. Each approach should be genuinely different:

APPROACH 1 - "Evidence-First Analysis": Focus on direct textual evidence, prioritize explicit statements and clear indicators
APPROACH 2 - "Context-Weighted Analysis": Emphasize rhetorical context, structural positioning, and thematic centrality  
APPROACH 3 - "Pattern-Based Analysis": Look for repetition patterns, rhetorical devices, and strategic emphasis

**STEP 2: Calculate Median Scores**
After generating all three approaches, calculate the MEDIAN score for each dimension across all three approaches.

**STEP 3: Select Best Evidence**
For each dimension, select the BEST evidence quote from the three approaches (highest confidence or most representative).

**IMPORTANT: SHOW YOUR WORK**
Please show me the three independent analyses first, then the median calculation, then the final result.

**FORMAT:**
1. First show the three independent analyses with their scores
2. Then show the median calculation process
3. Finally show the final aggregated result

{f"=== FRAMEWORK 1 (base64 encoded) ===\n{framework_content[:1000]}...\n"}

=== DOCUMENT 0 (base64 encoded) ===
Filename: Trump_SOTU_2020.txt
Hash: test_hash...
{doc_content[:2000]}...

Please analyze this document using the three independent approaches and show your work."""

    print("=== Testing Three-Shot Visibility ===")
    print("Asking LLM to show the three independent analyses...")
    
    # Execute LLM call
    response = gateway.execute_call(
        model="vertex_ai/gemini-2.5-flash",
        prompt=modified_prompt
    )
    
    # Handle response
    if isinstance(response, tuple):
        content, metadata = response
    else:
        content = response.get('content', '')
        metadata = response.get('metadata', {})
    
    print(f"Response length: {len(content)} characters")
    print("\n=== LLM RESPONSE ===")
    print(content[:2000] + "..." if len(content) > 2000 else content)
    
    # Save the response
    with open(experiment_dir / "artifacts" / "three_shot_visibility_test.json", 'w') as f:
        json.dump({
            'prompt': modified_prompt,
            'response': content,
            'metadata': metadata
        }, f, indent=2)
    
    print(f"\nFull response saved to: {experiment_dir / 'artifacts' / 'three_shot_visibility_test.json'}")

if __name__ == "__main__":
    test_three_shot_visibility()
