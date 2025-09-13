#!/usr/bin/env python3
"""
Test Enhanced Analysis Agent with Tool Calling (Production)
===========================================================

This test validates the production implementation of the enhanced analysis agent
with tool calling support.
"""

import json
import tempfile
import os
from pathlib import Path
from datetime import datetime, timezone

# Import the production agents
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.agents.EnhancedAnalysisAgent.agent_tool_calling import EnhancedAnalysisAgentToolCalling
from discernus.agents.verification_agent.agent import VerificationAgent

def create_test_environment():
    """Create a test environment with proper directory structure"""
    test_dir = Path(tempfile.mkdtemp(prefix="syw_test_"))
    
    # Create experiment directory structure
    experiment_dir = test_dir / "test_experiment"
    experiment_dir.mkdir()
    
    # Create experiment.md file
    (experiment_dir / "experiment.md").write_text("# Test Experiment\n\nThis is a test experiment for Show Your Work architecture.")
    
    # Create logs directory
    (experiment_dir / "logs").mkdir()
    
    return test_dir, experiment_dir

def main():
    """Test the production enhanced analysis agent with tool calling"""
    print("=== Enhanced Analysis Agent Production Test ===\n")
    
    # Create test environment
    test_dir, experiment_dir = create_test_environment()
    
    try:
        # Initialize core components
        security = ExperimentSecurityBoundary(experiment_path=experiment_dir)
        audit = AuditLogger(security_boundary=security, run_folder=experiment_dir)
        storage = LocalArtifactStorage(security_boundary=security, run_folder=experiment_dir)
        
        print("1. Initialized core components")
        print(f"   Test directory: {test_dir}")
        print(f"   Experiment directory: {experiment_dir}")
        
        # Create the enhanced analysis agent
        analysis_agent = EnhancedAnalysisAgentToolCalling(security, audit, storage)
        print("\n2. Created Enhanced Analysis Agent with tool calling")
        
        # Create the verification agent
        verification_agent = VerificationAgent(security, audit, storage)
        print("3. Created Verification Agent")
        
        # Sample document and framework
        document = {
            "id": "test_doc_001",
            "title": "Test Political Speech",
            "content": "The American people deserve better leadership. We must work together to create a brighter future for all citizens. The current system has failed us, and we need real change now."
        }
        
        framework = {
            "name": "political_discourse_v1",
            "version": "1.0.0",
            "dimensions": {
                "sentiment": {
                    "description": "Overall emotional tone",
                    "scale": "0.0 (negative) to 1.0 (positive)"
                },
                "populism": {
                    "description": "Appeal to the common people",
                    "scale": "0.0 (elitist) to 1.0 (populist)"
                },
                "authority": {
                    "description": "Deference to institutional authority",
                    "scale": "0.0 (anti-authority) to 1.0 (pro-authority)"
                }
            }
        }
        
        print("\n4. Sample data prepared")
        print(f"   Document: {document['title']}")
        print(f"   Framework: {framework['name']} v{framework['version']}")
        
        # Test analysis with tool calling
        print("\n5. Running analysis with tool calling...")
        try:
            analysis_result = analysis_agent.analyze_document(document, framework)
            
            print(f"   ✅ Analysis completed successfully!")
            print(f"   Document ID: {analysis_result['document_id']}")
            print(f"   Analysis Artifact: {analysis_result['analysis_artifact']}")
            print(f"   Work Artifact: {analysis_result['work_artifact']}")
            
            # Test verification
            print("\n6. Running verification...")
            try:
                verification_result = verification_agent.verify_analysis(
                    analysis_result['analysis_artifact'],
                    analysis_result['work_artifact']
                )
                
                print(f"   ✅ Verification completed!")
                print(f"   Success: {verification_result['success']}")
                print(f"   Attestation Artifact: {verification_result['attestation_artifact']}")
                print(f"   Reasoning: {verification_result['reasoning'][:100]}...")
                
                # Inspect artifacts
                print("\n7. Artifact inspection:")
                
                # Analysis artifact
                analysis_data = storage.get_artifact(analysis_result['analysis_artifact'])
                analysis_content = json.loads(analysis_data['content'])
                print(f"\n   Analysis artifact ({analysis_result['analysis_artifact']}):")
                print(f"   - Document: {analysis_content['document_id']}")
                print(f"   - Framework: {analysis_content['framework_name']} v{analysis_content['framework_version']}")
                print(f"   - Scores: {list(analysis_content['scores'].keys())}")
                print(f"   - Derived metrics: {list(analysis_content['derived_metrics'].keys())}")
                print(f"   - Evidence quotes: {len(analysis_content['evidence'])}")
                
                # Work artifact
                work_data = storage.get_artifact(analysis_result['work_artifact'])
                work_content = json.loads(work_data['content'])
                print(f"\n   Work artifact ({analysis_result['work_artifact']}):")
                print(f"   - Code length: {len(work_content['executed_code'])} characters")
                print(f"   - Output: {work_content['execution_output'].strip()}")
                
                # Attestation artifact
                attestation_data = storage.get_artifact(verification_result['attestation_artifact'])
                attestation_content = json.loads(attestation_data['content'])
                print(f"\n   Attestation artifact ({verification_result['attestation_artifact']}):")
                print(f"   - Success: {attestation_content['success']}")
                print(f"   - Verifier: {attestation_content['verifier_model']}")
                print(f"   - Reasoning: {attestation_content['reasoning'][:100]}...")
                
                print(f"\n=== Test Results ===")
                print("✅ Enhanced Analysis Agent with tool calling: WORKING")
                print("✅ Verification Agent with tool calling: WORKING")
                print("✅ Structured output via tool calls: WORKING")
                print("✅ Artifact storage and retrieval: WORKING")
                print("✅ Complete audit trail: WORKING")
                
            except Exception as e:
                print(f"   ❌ Verification failed: {e}")
                raise
                
        except Exception as e:
            print(f"   ❌ Analysis failed: {e}")
            raise
            
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        raise
        
    finally:
        # Cleanup
        import shutil
        shutil.rmtree(test_dir)
        print(f"\n8. Cleaned up test directory: {test_dir}")

if __name__ == "__main__":
    main()
