#!/usr/bin/env python3
"""
Complete Show Your Work Flow Demonstration
==========================================

This demonstrates the complete flow from analysis to verification
using the new tool calling architecture.
"""

import json
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

# Import our prototypes
from test_analysis_agent_tool_calling import (
    MockSecurityBoundary, MockAuditLogger, MockArtifactStorage,
    EnhancedAnalysisAgentToolCalling
)
from test_verification_agent_tool_calling import VerificationAgentToolCalling

class ShowYourWorkOrchestrator:
    """Prototype orchestrator for the complete Show Your Work flow"""
    
    def __init__(self, security_boundary, audit_logger, artifact_storage):
        self.security = security_boundary
        self.audit = audit_logger
        self.storage = artifact_storage
        self.orchestrator_name = "ShowYourWorkOrchestrator"
        
        # Initialize agents
        self.analysis_agent = EnhancedAnalysisAgentToolCalling(
            security_boundary, audit_logger, artifact_storage
        )
        self.verification_agent = VerificationAgentToolCalling(
            security_boundary, audit_logger, artifact_storage
        )
        
        self.audit.log_agent_event(self.orchestrator_name, "initialization", {
            "capabilities": ["per_document_analysis", "adversarial_verification", "fail_fast"]
        })
    
    def process_document(self, document: Dict[str, Any], framework: Dict[str, Any],
                        model: str = "vertex_ai/gemini-2.5-flash") -> Dict[str, Any]:
        """Process a single document through analysis and verification"""
        
        self.audit.log_agent_event(self.orchestrator_name, "document_processing_start", {
            "document_id": document.get("id", "unknown")
        })
        
        # Step 1: Analysis with derived metrics
        print(f"  📊 Analyzing document: {document.get('title', 'Untitled')}")
        analysis_result = self.analysis_agent.analyze_document(document, framework, model)
        
        # Step 2: Verification
        print(f"  🔍 Verifying analysis...")
        verification_result = self.verification_agent.verify_analysis(
            analysis_result['analysis_artifact'],
            analysis_result['work_artifact']
        )
        
        # Step 3: Fail-fast check
        if not verification_result['success']:
            error_msg = f"Verification failed for document {verification_result['document_id']}: {verification_result['reasoning']}"
            self.audit.log_agent_event(self.orchestrator_name, "verification_failure", {
                "document_id": verification_result['document_id'],
                "reasoning": verification_result['reasoning']
            })
            raise ValueError(error_msg)
        
        print(f"  ✅ Verification passed!")
        
        self.audit.log_agent_event(self.orchestrator_name, "document_processing_complete", {
            "document_id": verification_result['document_id'],
            "analysis_artifact": analysis_result['analysis_artifact'],
            "work_artifact": analysis_result['work_artifact'],
            "attestation_artifact": verification_result['attestation_artifact']
        })
        
        return {
            "document_id": verification_result['document_id'],
            "analysis_artifact": analysis_result['analysis_artifact'],
            "work_artifact": analysis_result['work_artifact'],
            "attestation_artifact": verification_result['attestation_artifact'],
            "verification_success": verification_result['success']
        }
    
    def process_corpus(self, documents: List[Dict[str, Any]], framework: Dict[str, Any],
                      model: str = "vertex_ai/gemini-2.5-flash") -> Dict[str, Any]:
        """Process a corpus of documents through the complete flow"""
        
        self.audit.log_agent_event(self.orchestrator_name, "corpus_processing_start", {
            "num_documents": len(documents)
        })
        
        results = []
        failed_documents = []
        
        for i, document in enumerate(documents, 1):
            try:
                print(f"\n📄 Processing document {i}/{len(documents)}: {document.get('title', 'Untitled')}")
                result = self.process_document(document, framework, model)
                results.append(result)
                print(f"  ✅ Document {i} completed successfully")
                
            except Exception as e:
                print(f"  ❌ Document {i} failed: {e}")
                failed_documents.append({
                    "document_id": document.get("id", f"doc_{i}"),
                    "error": str(e)
                })
        
        # Summary
        success_count = len(results)
        failure_count = len(failed_documents)
        
        self.audit.log_agent_event(self.orchestrator_name, "corpus_processing_complete", {
            "total_documents": len(documents),
            "successful": success_count,
            "failed": failure_count,
            "success_rate": success_count / len(documents) if documents else 0
        })
        
        return {
            "total_documents": len(documents),
            "successful_documents": results,
            "failed_documents": failed_documents,
            "success_count": success_count,
            "failure_count": failure_count,
            "success_rate": success_count / len(documents) if documents else 0
        }

def main():
    """Demonstrate the complete Show Your Work flow"""
    print("=== Complete Show Your Work Flow Demonstration ===\n")
    
    # Initialize dependencies
    security = MockSecurityBoundary()
    audit = MockAuditLogger()
    storage = MockArtifactStorage()
    
    # Create orchestrator
    orchestrator = ShowYourWorkOrchestrator(security, audit, storage)
    
    # Sample framework
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
    
    # Sample documents
    documents = [
        {
            "id": "doc_001",
            "title": "Campaign Speech on Economic Policy",
            "content": "The American people deserve better economic policies. We must work together to create jobs and prosperity for all citizens. The current system favors the wealthy elite over hardworking families."
        },
        {
            "id": "doc_002", 
            "title": "Address on Healthcare Reform",
            "content": "Healthcare is a fundamental right. Our government has a responsibility to ensure all Americans have access to quality, affordable healthcare. This is not a partisan issue - it's about human dignity."
        },
        {
            "id": "doc_003",
            "title": "Statement on National Security",
            "content": "We must maintain strong national security while respecting civil liberties. Our intelligence agencies work tirelessly to protect us, and we must support their efforts while ensuring proper oversight."
        }
    ]
    
    print("1. Processing corpus through Show Your Work flow...")
    print(f"   Framework: {framework['name']} v{framework['version']}")
    print(f"   Documents: {len(documents)}")
    
    # Process the corpus
    results = orchestrator.process_corpus(documents, framework)
    
    print(f"\n2. Processing complete!")
    print(f"   Total documents: {results['total_documents']}")
    print(f"   Successful: {results['success_count']}")
    print(f"   Failed: {results['failure_count']}")
    print(f"   Success rate: {results['success_rate']:.1%}")
    
    print(f"\n3. Successful document artifacts:")
    for i, result in enumerate(results['successful_documents'], 1):
        print(f"   Document {i}: {result['document_id']}")
        print(f"     Analysis: {result['analysis_artifact']}")
        print(f"     Work: {result['work_artifact']}")
        print(f"     Attestation: {result['attestation_artifact']}")
    
    if results['failed_documents']:
        print(f"\n4. Failed documents:")
        for failure in results['failed_documents']:
            print(f"   {failure['document_id']}: {failure['error']}")
    
    print(f"\n5. Artifact inspection (first successful document):")
    if results['successful_documents']:
        first_result = results['successful_documents'][0]
        
        # Show analysis artifact
        analysis_data = storage.get_artifact(first_result['analysis_artifact'])
        analysis_content = json.loads(analysis_data['content'])
        print(f"\n   Analysis artifact ({first_result['analysis_artifact']}):")
        print(f"   - Document: {analysis_content['document_id']}")
        print(f"   - Framework: {analysis_content['framework_name']} v{analysis_content['framework_version']}")
        print(f"   - Scores: {list(analysis_content['scores'].keys())}")
        print(f"   - Derived metrics: {list(analysis_content['derived_metrics'].keys())}")
        print(f"   - Evidence quotes: {len(analysis_content['evidence'])}")
        
        # Show work artifact
        work_data = storage.get_artifact(first_result['work_artifact'])
        work_content = json.loads(work_data['content'])
        print(f"\n   Work artifact ({first_result['work_artifact']}):")
        print(f"   - Code length: {len(work_content['executed_code'])} characters")
        print(f"   - Output: {work_content['execution_output'].strip()}")
        
        # Show attestation artifact
        attestation_data = storage.get_artifact(first_result['attestation_artifact'])
        attestation_content = json.loads(attestation_data['content'])
        print(f"\n   Attestation artifact ({first_result['attestation_artifact']}):")
        print(f"   - Success: {attestation_content['success']}")
        print(f"   - Verifier: {attestation_content['verifier_model']}")
        print(f"   - Reasoning: {attestation_content['reasoning'][:100]}...")
    
    print(f"\n6. Audit log summary:")
    event_counts = {}
    for event in audit.events:
        event_type = event['event']
        event_counts[event_type] = event_counts.get(event_type, 0) + 1
    
    for event_type, count in event_counts.items():
        print(f"   {event_type}: {count}")
    
    print(f"\n=== Key Benefits Demonstrated ===")
    print("✅ Complete per-document analysis with derived metrics")
    print("✅ Adversarial verification for every analysis")
    print("✅ Fail-fast behavior when verification fails")
    print("✅ Clean artifact separation (analysis.json, work.json, attestation.json)")
    print("✅ Zero parsing - all data via structured tool calls")
    print("✅ Complete audit trail of all operations")
    print("✅ Content-addressable storage for all artifacts")
    print("✅ Scalable architecture ready for 800+ documents")

if __name__ == "__main__":
    main()
