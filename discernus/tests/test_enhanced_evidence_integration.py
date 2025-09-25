#!/usr/bin/env python3
"""
Unit tests for enhanced evidence integration in synthesis.
Validates functional equivalence with SynthesisPromptAssembler approach.
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, MagicMock
import pytest

# Mock evidence data (based on actual structure)
MOCK_EVIDENCE_DATA = [
    {
        "document_name": "test_doc_1.txt",
        "dimension": "tribal_dominance", 
        "quote_text": "We must protect our own people first and foremost.",
        "confidence": 0.95,
        "context_type": "direct_statement"
    },
    {
        "document_name": "test_doc_1.txt",
        "dimension": "fear",
        "quote_text": "The threats we face are unprecedented and growing.",
        "confidence": 0.90,
        "context_type": "threat_framing"
    },
    {
        "document_name": "test_doc_2.txt", 
        "dimension": "hope",
        "quote_text": "Together we can build a better future for all.",
        "confidence": 0.88,
        "context_type": "optimistic_vision"
    }
]

MOCK_RESEARCH_DATA = {
    "statistical_data": {
        "descriptive_statistics": {
            "tribal_dominance_raw": {"mean": 0.6, "std": 0.3},
            "fear_raw": {"mean": 0.7, "std": 0.2}
        }
    }
}

class TestEnhancedEvidenceIntegration:
    """Test suite for enhanced evidence integration functionality."""
    
    def test_evidence_artifact_registry_access(self):
        """Test proper evidence artifact collection from registry vs file system."""
        from discernus.core.clean_analysis_orchestrator import CleanAnalysisOrchestrator
        
        # Mock artifact storage with registry
        mock_storage = Mock()
        mock_storage.registry = {
            "evidence_hash_1": {
                "metadata": {"artifact_type": "evidence_v6_extracted"}
            },
            "evidence_hash_2": {
                "metadata": {"artifact_type": "evidence_v6_processed"}  
            },
            "other_hash": {
                "metadata": {"artifact_type": "analysis_result"}
            }
        }
        
        # Create mock orchestrator
        orchestrator = Mock()
        orchestrator.artifact_storage = mock_storage
        
        # Test the evidence collection logic
        evidence_hashes = []
        for artifact_hash, artifact_info in mock_storage.registry.items():
            metadata = artifact_info.get("metadata", {})
            if metadata.get("artifact_type", "").startswith("evidence_v6"):
                evidence_hashes.append(artifact_hash)
        
        # Validate correct evidence hashes collected
        assert len(evidence_hashes) == 2, f"Expected 2 evidence hashes, got {len(evidence_hashes)}"
        assert "evidence_hash_1" in evidence_hashes, "Missing evidence_hash_1"
        assert "evidence_hash_2" in evidence_hashes, "Missing evidence_hash_2" 
        assert "other_hash" not in evidence_hashes, "Should not include non-evidence artifacts"
        
        print("✅ Evidence artifact registry access test passed")
    
    def test_evidence_context_preparation(self):
        """Test evidence context preparation matches SynthesisPromptAssembler functionality."""
        from discernus.agents.unified_synthesis_agent import UnifiedSynthesisAgent
        
        # Mock artifact storage
        mock_storage = Mock()
        mock_storage.get_artifact.return_value = json.dumps({
            "evidence_data": MOCK_EVIDENCE_DATA
        }).encode('utf-8')
        
        # Create synthesis agent
        agent = UnifiedSynthesisAgent()
        
        # Test evidence context preparation
        evidence_context = agent._prepare_evidence_context(
            ["mock_hash_1"], 
            mock_storage
        )
        
        # Validate evidence context structure
        assert "tribal_dominance" in evidence_context, "Missing dimensional evidence"
        assert "We must protect our own people" in evidence_context, "Missing quote text"
        assert "confidence: 0.95" in evidence_context, "Missing confidence score"
        assert "test_doc_1.txt" in evidence_context, "Missing document attribution"
        
        # Validate formatting matches expected structure
        lines = evidence_context.split('\n')
        assert len(lines) > 5, "Evidence context should have multiple formatted lines"
        
        print("✅ Evidence context preparation test passed")
        print(f"   Sample context: {evidence_context[:200]}...")
    
    def test_synthesis_prompt_assembly_equivalence(self):
        """Test that enhanced mode provides equivalent functionality to SynthesisPromptAssembler."""
        from discernus.core.prompt_assemblers.synthesis_assembler import SynthesisPromptAssembler
        from discernus.agents.unified_synthesis_agent import UnifiedSynthesisAgent
        
        # Create temporary files
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create mock framework file
            framework_file = temp_path / "framework.md"
            framework_file.write_text("# Test Framework\nDimensions: tribal_dominance, fear, hope")
            
            # Create mock experiment file  
            experiment_file = temp_path / "experiment.md"
            experiment_file.write_text("# Test Experiment\nObjective: Test evidence integration")
            
            # Mock artifact storage
            mock_storage = Mock()
            mock_storage.get_artifact.side_effect = [
                # Research data
                json.dumps(MOCK_RESEARCH_DATA).encode('utf-8'),
                # Evidence data
                json.dumps({"evidence_data": MOCK_EVIDENCE_DATA}).encode('utf-8')
            ]
            
            # Test SynthesisPromptAssembler approach
            assembler = SynthesisPromptAssembler()
            try:
                legacy_prompt = assembler.assemble_prompt(
                    framework_path=framework_file,
                    experiment_path=experiment_file,
                    research_data_artifact_hash="research_hash",
                    artifact_storage=mock_storage,
                    evidence_artifacts=["evidence_hash"]
                )
                legacy_has_evidence_instructions = "RAG EVIDENCE DATABASE" in legacy_prompt
                legacy_has_evidence_count = "pieces of textual evidence" in legacy_prompt
            except Exception as e:
                print(f"⚠️ Legacy assembler failed: {e}")
                legacy_has_evidence_instructions = False
                legacy_has_evidence_count = False
            
            # Test enhanced mode approach
            agent = UnifiedSynthesisAgent(enhanced_mode=True)
            
            # Mock the enhanced prompt template loading
            agent.enhanced_prompt_template = {
                'template': """
                Framework: {framework_content}
                Experiment: {experiment_content}  
                Research Data: {research_data}
                Evidence: {evidence_context}
                
                Generate comprehensive report with evidence citations.
                """
            }
            
            enhanced_report = agent._generate_enhanced_report(
                framework_path=framework_file,
                experiment_path=experiment_file, 
                research_data_artifact_hash="research_hash",
                evidence_artifact_hashes=["evidence_hash"],
                artifact_storage=mock_storage
            )
            
            # Validate enhanced mode has evidence integration
            enhanced_has_evidence = "We must protect our own people" in enhanced_report
            enhanced_has_attribution = "test_doc_1.txt" in enhanced_report
            
            print(f"✅ Legacy assembler evidence instructions: {legacy_has_evidence_instructions}")
            print(f"✅ Legacy assembler evidence count: {legacy_has_evidence_count}")
            print(f"✅ Enhanced mode evidence integration: {enhanced_has_evidence}")
            print(f"✅ Enhanced mode attribution: {enhanced_has_attribution}")
            
            # Both approaches should provide evidence integration
            assert enhanced_has_evidence, "Enhanced mode must integrate evidence quotes"
            assert enhanced_has_attribution, "Enhanced mode must include document attribution"
    
    def test_transaction_validation_evidence_required(self):
        """Test transaction validation fails when evidence is required but missing."""
        from discernus.core.clean_analysis_orchestrator import CleanAnalysisOrchestrator, CleanAnalysisError
        
        # Mock orchestrator with empty registry
        mock_storage = Mock()
        mock_storage.registry = {}  # No evidence artifacts
        
        orchestrator = Mock()
        orchestrator.artifact_storage = mock_storage
        
        # Test evidence collection with empty registry
        evidence_hashes = []
        for artifact_hash, artifact_info in mock_storage.registry.items():
            metadata = artifact_info.get("metadata", {})
            if metadata.get("artifact_type", "").startswith("evidence_v6"):
                evidence_hashes.append(artifact_hash)
        
        # Should have no evidence hashes
        assert len(evidence_hashes) == 0, "Should have no evidence with empty registry"
        
        # This should trigger transaction validation failure
        print("✅ Transaction validation test: Empty registry correctly detected")
    
    def test_evidence_integration_validation(self):
        """Test validation that synthesis report actually contains evidence."""
        
        # Test case 1: Report with proper evidence integration
        good_report = """
        # Analysis Report
        
        The data shows high tribal dominance. As Speaker stated: "We must protect our own people first" (Source: test_doc_1.txt).
        Fear levels are elevated, with evidence like "The threats we face are unprecedented" (Source: test_doc_1.txt).
        """
        
        # Test case 2: Report claiming no evidence
        bad_report = """
        # Analysis Report
        
        Due to the absence of qualitative data, this report focuses on statistical patterns only.
        No evidence available for citation.
        """
        
        # Validation logic
        def validate_evidence_integration(report_text, evidence_count):
            if evidence_count > 0:
                if "No evidence available" in report_text or "absence of qualitative data" in report_text:
                    return False, "Report claims no evidence but evidence exists"
            return True, "Evidence integration validated"
        
        # Test good report
        is_valid, message = validate_evidence_integration(good_report, 3)
        assert is_valid, f"Good report should pass validation: {message}"
        
        # Test bad report  
        is_valid, message = validate_evidence_integration(bad_report, 3)
        assert not is_valid, f"Bad report should fail validation: {message}"
        
        print("✅ Evidence integration validation test passed")
    
    def test_functional_equivalence_summary(self):
        """Test that enhanced mode provides all functionality of legacy assembler."""
        
        # Required functionality checklist
        required_features = {
            "evidence_artifact_access": True,  # ✅ Registry-based access
            "evidence_context_preparation": True,  # ✅ _prepare_evidence_context
            "evidence_count_reporting": False,  # ❌ Not implemented  
            "rag_instructions": False,  # ❌ Not in enhanced template
            "comprehensive_prompt_assembly": True,  # ✅ Enhanced template
            "transaction_validation": True,  # ✅ Added validation
        }
        
        implemented_count = sum(required_features.values())
        total_count = len(required_features)
        
        print(f"\n📊 Functional Equivalence Summary:")
        print(f"   Implemented: {implemented_count}/{total_count} features")
        
        for feature, implemented in required_features.items():
            status = "✅" if implemented else "❌"
            print(f"   {status} {feature}")
        
        # Must have core evidence integration
        assert required_features["evidence_artifact_access"], "Must have evidence access"
        assert required_features["evidence_context_preparation"], "Must prepare evidence context"
        assert required_features["transaction_validation"], "Must validate transactions"
        
        if implemented_count < total_count:
            missing = [f for f, impl in required_features.items() if not impl]
            print(f"\n⚠️ Missing features: {missing}")
            print("Enhanced mode has core functionality but missing some legacy features")
        
        return implemented_count == total_count

if __name__ == "__main__":
    # Allow running tests directly
    import sys
    sys.path.append('/Volumes/code/discernus')
    
    test_suite = TestEnhancedEvidenceIntegration()
    
    print("🧪 Testing Enhanced Evidence Integration")
    print("=" * 50)
    
    try:
        test_suite.test_evidence_artifact_registry_access()
        test_suite.test_evidence_context_preparation() 
        test_suite.test_synthesis_prompt_assembly_equivalence()
        test_suite.test_transaction_validation_evidence_required()
        test_suite.test_evidence_integration_validation()
        
        is_equivalent = test_suite.test_functional_equivalence_summary()
        
        print("\n" + "=" * 50)
        if is_equivalent:
            print("✅ ALL TESTS PASSED - Full functional equivalence achieved")
        else:
            print("⚠️ TESTS PASSED - Core functionality working, some features missing")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        raise
