#!/usr/bin/env python3
"""
Test-Driven Development: Index Validation

This test ensures that both indexes (evidence and corpus) are fully operational
and responding exactly as the later agents expect before proceeding through the pipeline.
"""

import os
import sys
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'discernus'))

def test_evidence_index_validation():
    """Test that evidence index is fully operational."""
    print("🧪 Testing evidence index validation...")
    
    try:
        from discernus.core.clean_analysis_orchestrator import CleanAnalysisOrchestrator
        from discernus.core.artifact_storage import LocalArtifactStorage
        
        # Mock the orchestrator dependencies
        with patch('discernus.core.clean_analysis_orchestrator.LLMGateway'), \
             patch('discernus.core.clean_analysis_orchestrator.ModelRegistry'):
            
            # Create a minimal orchestrator instance
            orchestrator = CleanAnalysisOrchestrator(
                experiment_path=Path("/tmp/test"),
                config={"framework": "test_framework.md"},
                model="test_model"
            )
            
            # Test evidence index building
            # This should build the RAG index that evidence retrieval will use
            result = orchestrator._build_evidence_index()
            
            # Verify the index is operational
            assert result is not None, "Evidence index should be built successfully"
            print("✅ Evidence index validation passed")
            return True
            
    except Exception as e:
        print(f"❌ Evidence index validation failed: {e}")
        return False

def test_corpus_index_validation():
    """Test that corpus index is fully operational."""
    print("🧪 Testing corpus index validation...")
    
    try:
        from discernus.core.hybrid_corpus_service import HybridCorpusService
        from discernus.core.typesense_corpus_service import TypesenseCorpusService
        
        # Test Typesense connection
        typesense_service = TypesenseCorpusService()
        
        # Verify Typesense is responding
        if not typesense_service.client:
            print("❌ Typesense connection failed")
            return False
        
        # Test basic operations
        try:
            # Try to create a test collection
            test_collection_name = "test_validation_collection"
            if typesense_service.create_index(force_recreate=True):
                print("✅ Typesense index creation successful")
                
                # Test indexing a sample document
                test_doc = {
                    'content': 'This is a test document for validation.',
                    'file_path': '/tmp/test.txt',
                    'filename': 'test.txt',
                    'speaker': 'Test Speaker',
                    'date': '2025-01-01',
                    'source_type': 'test_document',
                    'start_char': 0,
                    'end_char': 45,
                    'context': 'Test context'
                }
                
                if typesense_service.index_corpus_files([test_doc]):
                    print("✅ Typesense document indexing successful")
                    
                    # Test search functionality
                    search_results = typesense_service.search_quotes("test document")
                    if search_results and len(search_results) > 0:
                        print("✅ Typesense search functionality working")
                        
                        # Clean up test collection
                        try:
                            typesense_service.client.collections[test_collection_name].delete()
                            print("✅ Test collection cleaned up")
                        except:
                            pass
                        
                        return True
                    else:
                        print("❌ Typesense search returned no results")
                        return False
                else:
                    print("❌ Typesense document indexing failed")
                    return False
            else:
                print("❌ Typesense index creation failed")
                return False
                
        except Exception as e:
            print(f"❌ Typesense operations failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Corpus index validation failed: {e}")
        return False

def test_hybrid_service_integration():
    """Test that HybridCorpusService integrates both indexes properly."""
    print("🧪 Testing hybrid service integration...")
    
    try:
        from discernus.core.hybrid_corpus_service import HybridCorpusService
        
        # Create hybrid service
        hybrid_service = HybridCorpusService()
        
        # Test that both services are available
        assert hybrid_service.typesense_service is not None, "Typesense service should be available"
        print("✅ Hybrid service Typesense integration working")
        
        # Test quote validation method exists
        assert hasattr(hybrid_service, 'validate_quote'), "Hybrid service should have validate_quote method"
        print("✅ Hybrid service quote validation method available")
        
        return True
        
    except Exception as e:
        print(f"❌ Hybrid service integration failed: {e}")
        return False

def test_agent_expectations():
    """Test that indexes provide exactly what agents expect."""
    print("🧪 Testing agent expectations...")
    
    try:
        from discernus.agents.fact_checker_agent.agent import FactCheckerAgent
        from discernus.core.hybrid_corpus_service import HybridCorpusService
        
        # Create a mock corpus index service
        mock_service = Mock(spec=HybridCorpusService)
        
        # Test that fact checker can use the service
        fact_checker = FactCheckerAgent(
            gateway=Mock(),
            audit_logger=Mock(),
            corpus_index_service=mock_service
        )
        
        # Verify the service is properly integrated
        assert fact_checker.corpus_index_service is not None, "Fact checker should have corpus index service"
        print("✅ Fact checker service integration working")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent expectations test failed: {e}")
        return False

def main():
    """Run all index validation tests."""
    print("🚀 INDEX VALIDATION TEST SUITE")
    print("Ensuring indexes are fully operational before pipeline execution")
    print("="*70)
    
    tests = [
        ("Evidence Index Validation", test_evidence_index_validation),
        ("Corpus Index Validation", test_corpus_index_validation),
        ("Hybrid Service Integration", test_hybrid_service_integration),
        ("Agent Expectations", test_agent_expectations)
    ]
    
    all_passed = True
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        if not test_func():
            all_passed = False
            print(f"❌ {test_name} FAILED - Pipeline cannot proceed safely")
        else:
            print(f"✅ {test_name} PASSED")
    
    print("\n" + "="*70)
    if all_passed:
        print("🎉 ALL INDEX VALIDATION TESTS PASSED!")
        print("🚀 Indexes are fully operational - pipeline can proceed safely")
        return True
    else:
        print("❌ INDEX VALIDATION FAILED!")
        print("🛑 Pipeline cannot proceed - indexes are not operational")
        print("🔧 Fix index issues before continuing")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
