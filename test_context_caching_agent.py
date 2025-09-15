#!/usr/bin/env python3
"""
Test Context Caching Analysis Agent
===================================

Test the new context caching agent with PDAF framework and Trump SOTU 2020.
This will help us validate the approach before implementing full context caching.
"""

import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

from discernus.agents.ContextCachingAnalysisAgent.main import ContextCachingAnalysisAgent
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage

def test_context_caching_agent():
    """Test the context caching agent with PDAF and Trump SOTU 2020"""
    
    print("Testing Context Caching Analysis Agent...")
    print("=" * 50)
    
    # Load PDAF framework
    framework_path = Path("frameworks/reference/flagship/pdaf_v10_0_2.md")
    with open(framework_path, 'r') as f:
        framework = f.read()
    
    print(f"Framework loaded: {len(framework)} characters")
    
    # Load Trump SOTU 2020
    document_path = Path("projects/2d_trump_populism/corpus/analysis_ready/02_presidential_2017_2020/Trump_SOTU_2020.txt")
    with open(document_path, 'r') as f:
        document_content = f.read()
    
    print(f"Document loaded: {len(document_content)} characters")
    
    # Create test document
    document = {
        'filename': 'Trump_SOTU_2020.txt',
        'content': document_content
    }
    
    # Create test components
    security = ExperimentSecurityBoundary(Path('test_context_caching'))
    audit = AuditLogger(security, Path('test_context_caching/debug_test'))
    storage = LocalArtifactStorage(security, Path('test_context_caching/shared_cache/artifacts'))
    
    # Create agent
    agent = ContextCachingAnalysisAgent(security, audit, storage)
    
    # Test configuration
    config = {
        'model': 'gemini-2.5-flash',
        'max_retries': 3
    }
    
    print("\nStarting analysis...")
    print("This will make 3 sequential LLM calls:")
    print("1. Dimensional scores (creates context cache)")
    print("2. Evidence quotes (uses context cache)")
    print("3. Computational work (uses context cache)")
    print()
    
    try:
        # Run analysis
        result = agent.analyze_documents(framework, [document], config)
        
        print("Analysis completed successfully!")
        print(f"Analysis ID: {result.get('analysis_id')}")
        print(f"Document count: {result.get('document_count')}")
        
        # Show results summary
        if 'results' in result and result['results']:
            doc_result = result['results'][0]
            print(f"Dimensional scores: {len(doc_result.get('dimensional_scores', {}))}")
            print(f"Evidence quotes: {len(doc_result.get('evidence', []))}")
            print(f"Computational work: {bool(doc_result.get('computational_work'))}")
        
        return True
        
    except Exception as e:
        print(f"Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_context_caching_agent()
    if success:
        print("\n✅ Test completed successfully!")
    else:
        print("\n❌ Test failed!")
        sys.exit(1)

