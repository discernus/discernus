#!/usr/bin/env python3
"""
Test Phase 2 Statistical Agents Architecture Validation
======================================================

This test validates the Phase 2 statistical agents architecture using mock LLM responses
to ensure the batch statistical processing flow works correctly.
"""

import json
import tempfile
import os
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

# Import the production agents
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.evidence_csv_export import EvidenceCSVExportModule

# Mock the enhanced LLM gateway for testing
class MockStatisticalLLMGateway:
    """Mock enhanced LLM gateway for statistical analysis"""
    
    def __init__(self, model_registry):
        self.model_registry = model_registry
        self.call_count = 0
    
    def execute_call_with_tools(self, model: str, prompt: str, system_prompt: str, 
                               tools: List[Dict[str, Any]] = None, max_retries: int = 3, 
                               context: Optional[str] = None, **kwargs) -> tuple[str, Dict[str, Any]]:
        """Simulate statistical analysis LLM call with tool calling"""
        self.call_count += 1
        
        if "statistical" in system_prompt.lower() and "verification" not in system_prompt.lower():
            # Statistical analysis call
            tool_call_response = {
                "id": f"statistical_call_{self.call_count}",
                "type": "function",
                "function": {
                    "name": "record_statistical_results",
                    "arguments": json.dumps({
                        "statistics_payload": {
                            "tests": [
                                {
                                    "name": "descriptive_statistics",
                                    "parameters": {"method": "comprehensive"},
                                    "metrics": {
                                        "mean_sentiment": 0.65,
                                        "std_sentiment": 0.15,
                                        "mean_populism": 0.72,
                                        "std_populism": 0.18,
                                        "mean_authority": 0.45,
                                        "std_authority": 0.22
                                    }
                                },
                                {
                                    "name": "correlation_analysis",
                                    "parameters": {"method": "pearson"},
                                    "metrics": {
                                        "sentiment_populism_correlation": 0.34,
                                        "sentiment_authority_correlation": -0.28,
                                        "populism_authority_correlation": -0.45
                                    }
                                },
                                {
                                    "name": "anova_test",
                                    "parameters": {"method": "one_way"},
                                    "metrics": {
                                        "f_statistic": 12.45,
                                        "p_value": 0.001,
                                        "effect_size": 0.23
                                    }
                                }
                            ],
                            "aggregated_rows": [
                                {
                                    "document_id": "doc_001",
                                    "sentiment_score": 0.7,
                                    "populism_score": 0.8,
                                    "authority_score": 0.3,
                                    "overall_intensity": 0.6,
                                    "rhetorical_complexity": 0.25
                                },
                                {
                                    "document_id": "doc_002", 
                                    "sentiment_score": 0.6,
                                    "populism_score": 0.7,
                                    "authority_score": 0.5,
                                    "overall_intensity": 0.6,
                                    "rhetorical_complexity": 0.15
                                },
                                {
                                    "document_id": "doc_003",
                                    "sentiment_score": 0.7,
                                    "populism_score": 0.6,
                                    "authority_score": 0.6,
                                    "overall_intensity": 0.63,
                                    "rhetorical_complexity": 0.1
                                }
                            ]
                        },
                        "executed_code": """
# Statistical Analysis
import numpy as np
import pandas as pd
from scipy import stats
import pingouin as pg

# Load data
data = [
    {'document_id': 'doc_001', 'sentiment_score': 0.7, 'populism_score': 0.8, 'authority_score': 0.3, 'overall_intensity': 0.6, 'rhetorical_complexity': 0.25},
    {'document_id': 'doc_002', 'sentiment_score': 0.6, 'populism_score': 0.7, 'authority_score': 0.5, 'overall_intensity': 0.6, 'rhetorical_complexity': 0.15},
    {'document_id': 'doc_003', 'sentiment_score': 0.7, 'populism_score': 0.6, 'authority_score': 0.6, 'overall_intensity': 0.63, 'rhetorical_complexity': 0.1}
]

df = pd.DataFrame(data)

# Descriptive statistics
sentiment_stats = df['sentiment_score'].describe()
populism_stats = df['populism_score'].describe()
authority_stats = df['authority_score'].describe()

print(f"Sentiment - Mean: {sentiment_stats['mean']:.2f}, Std: {sentiment_stats['std']:.2f}")
print(f"Populism - Mean: {populism_stats['mean']:.2f}, Std: {populism_stats['std']:.2f}")
print(f"Authority - Mean: {authority_stats['mean']:.2f}, Std: {authority_stats['std']:.2f}")

# Correlation analysis
correlation_matrix = df[['sentiment_score', 'populism_score', 'authority_score']].corr()
print(f"Sentiment-Populism correlation: {correlation_matrix.loc['sentiment_score', 'populism_score']:.3f}")
print(f"Sentiment-Authority correlation: {correlation_matrix.loc['sentiment_score', 'authority_score']:.3f}")
print(f"Populism-Authority correlation: {correlation_matrix.loc['populism_score', 'authority_score']:.3f}")

# ANOVA test
f_stat, p_value = stats.f_oneway(df['sentiment_score'], df['populism_score'], df['authority_score'])
print(f"ANOVA F-statistic: {f_stat:.2f}, p-value: {p_value:.3f}")
""",
                        "execution_output": """Sentiment - Mean: 0.67, Std: 0.06
Populism - Mean: 0.70, Std: 0.10
Authority - Mean: 0.47, Std: 0.15
Sentiment-Populism correlation: 0.340
Sentiment-Authority correlation: -0.280
Populism-Authority correlation: -0.450
ANOVA F-statistic: 12.45, p-value: 0.001
"""
                    })
                }
            }
        else:
            # Statistical verification call
            tool_call_response = {
                "id": f"verification_call_{self.call_count}",
                "type": "function",
                "function": {
                    "name": "record_statistical_attestation",
                    "arguments": json.dumps({
                        "success": True,
                        "verifier_model": "vertex_ai/gemini-2.5-pro",
                        "verifier_model_version": "2.5.0",
                        "reasoning": "Re-executed the statistical analysis code and verified all calculations. The descriptive statistics are correct, correlation coefficients are properly calculated, and the ANOVA test results are mathematically sound. All statistical procedures are appropriate for the data type and research questions.",
                        "executed_code_digest_sha256": "statistical_abc123def456789",
                        "statistics_digest_sha256": "statistical_def456abc123789",
                        "re_execution_output": "Sentiment - Mean: 0.67, Std: 0.06\nPopulism - Mean: 0.70, Std: 0.10\nAuthority - Mean: 0.47, Std: 0.15\nSentiment-Populism correlation: 0.340\nSentiment-Authority correlation: -0.280\nPopulism-Authority correlation: -0.450\nANOVA F-statistic: 12.45, p-value: 0.001\n"
                    })
                }
            }
        
        # Simulate metadata
        metadata = {
            "success": True,
            "usage": {
                "total_tokens": 2000 if "statistical" in system_prompt.lower() else 1000,
                "prompt_tokens": 1500 if "statistical" in system_prompt.lower() else 750,
                "completion_tokens": 500 if "statistical" in system_prompt.lower() else 250,
                "response_cost_usd": 0.002 if "statistical" in system_prompt.lower() else 0.001
            },
            "model": model,
            "tool_calls": [tool_call_response]
        }
        
        return "Statistical analysis completed", metadata

def create_test_environment():
    """Create a test environment with proper directory structure"""
    test_dir = Path(tempfile.mkdtemp(prefix="syw_phase2_test_"))
    
    # Create experiment directory structure
    experiment_dir = test_dir / "test_experiment"
    experiment_dir.mkdir()
    
    # Create experiment.md file
    (experiment_dir / "experiment.md").write_text("# Test Experiment\n\nThis is a test experiment for Phase 2 Show Your Work architecture.")
    
    # Create logs directory
    (experiment_dir / "logs").mkdir()
    
    return test_dir, experiment_dir

def create_sample_analysis_artifacts(storage):
    """Create sample analysis artifacts for testing"""
    sample_analyses = [
        {
            "document_id": "doc_001",
            "framework_name": "political_discourse_v1",
            "framework_version": "1.0.0",
            "scores": {
                "sentiment": {"raw_score": 0.7, "salience": 0.8, "confidence": 0.9},
                "populism": {"raw_score": 0.8, "salience": 0.9, "confidence": 0.85},
                "authority": {"raw_score": 0.3, "salience": 0.6, "confidence": 0.8}
            },
            "derived_metrics": {
                "overall_intensity": 0.6,
                "rhetorical_complexity": 0.25
            },
            "evidence": [
                {
                    "dimension": "sentiment",
                    "quote": "The American people deserve better leadership",
                    "source": "paragraph_1",
                    "offset": 0,
                    "confidence": 0.9
                },
                {
                    "dimension": "populism",
                    "quote": "We must work together for all citizens",
                    "source": "paragraph_1",
                    "offset": 50,
                    "confidence": 0.85
                }
            ]
        },
        {
            "document_id": "doc_002",
            "framework_name": "political_discourse_v1",
            "framework_version": "1.0.0",
            "scores": {
                "sentiment": {"raw_score": 0.6, "salience": 0.7, "confidence": 0.8},
                "populism": {"raw_score": 0.7, "salience": 0.8, "confidence": 0.9},
                "authority": {"raw_score": 0.5, "salience": 0.7, "confidence": 0.75}
            },
            "derived_metrics": {
                "overall_intensity": 0.6,
                "rhetorical_complexity": 0.15
            },
            "evidence": [
                {
                    "dimension": "sentiment",
                    "quote": "Healthcare is a fundamental right",
                    "source": "paragraph_2",
                    "offset": 0,
                    "confidence": 0.8
                },
                {
                    "dimension": "authority",
                    "quote": "Our government has a responsibility",
                    "source": "paragraph_2",
                    "offset": 30,
                    "confidence": 0.75
                }
            ]
        },
        {
            "document_id": "doc_003",
            "framework_name": "political_discourse_v1",
            "framework_version": "1.0.0",
            "scores": {
                "sentiment": {"raw_score": 0.7, "salience": 0.8, "confidence": 0.85},
                "populism": {"raw_score": 0.6, "salience": 0.7, "confidence": 0.8},
                "authority": {"raw_score": 0.6, "salience": 0.8, "confidence": 0.9}
            },
            "derived_metrics": {
                "overall_intensity": 0.63,
                "rhetorical_complexity": 0.1
            },
            "evidence": [
                {
                    "dimension": "authority",
                    "quote": "We must maintain strong national security",
                    "source": "paragraph_1",
                    "offset": 0,
                    "confidence": 0.9
                }
            ]
        }
    ]
    
    artifact_ids = []
    for analysis in sample_analyses:
        content = json.dumps(analysis, indent=2).encode('utf-8')
        artifact_id = storage.put_artifact(content, {
            "artifact_type": "analysis",
            "document_id": analysis["document_id"]
        })
        artifact_ids.append(artifact_id)
    
    return artifact_ids

def main():
    """Test the Phase 2 statistical agents architecture with validation"""
    print("=== Phase 2 Statistical Agents Architecture Validation ===\n")
    
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
        
        # Create sample analysis artifacts
        analysis_artifact_ids = create_sample_analysis_artifacts(storage)
        print(f"\n2. Created {len(analysis_artifact_ids)} sample analysis artifacts")
        
        # Mock the LLM gateways
        with patch('discernus.agents.statistical_planning_execution.agent.EnhancedLLMGateway', MockStatisticalLLMGateway):
            with patch('discernus.agents.statistical_verification.agent.EnhancedLLMGateway', MockStatisticalLLMGateway):
                # Import the agents after patching
                from discernus.agents.statistical_planning_execution.agent import StatisticalPlanningExecutionAgent
                from discernus.agents.statistical_verification.agent import StatisticalVerificationAgent
                
                # Create the statistical planning + execution agent
                statistical_agent = StatisticalPlanningExecutionAgent(security, audit, storage)
                print("\n3. Created Statistical Planning + Execution Agent")
                
                # Create the statistical verification agent
                verification_agent = StatisticalVerificationAgent(security, audit, storage)
                print("4. Created Statistical Verification Agent")
                
                # Create the evidence CSV export module
                evidence_module = EvidenceCSVExportModule(storage, audit)
                print("5. Created Evidence CSV Export Module")
                
                # Sample hypotheses
                hypotheses = {
                    "h1": "Populism scores will be higher than authority scores",
                    "h2": "Sentiment and populism will be positively correlated",
                    "h3": "There will be significant differences between documents"
                }
                
                print(f"\n6. Sample hypotheses prepared: {len(hypotheses)} hypotheses")
                
                # Test statistical analysis
                print("\n7. Running batch statistical analysis...")
                try:
                    statistical_result = statistical_agent.analyze_batch(
                        analysis_artifact_ids, 
                        hypotheses
                    )
                    
                    print(f"   ✅ Statistical analysis completed successfully!")
                    print(f"   Statistics Artifact: {statistical_result['statistics_artifact']}")
                    print(f"   Work Artifact: {statistical_result['work_artifact']}")
                    print(f"   CSV Artifact: {statistical_result['csv_artifact']}")
                    
                    # Test statistical verification
                    print("\n8. Running statistical verification...")
                    try:
                        verification_result = verification_agent.verify_statistical_analysis(
                            statistical_result['statistics_artifact'],
                            statistical_result['work_artifact'],
                            statistical_result['csv_artifact']
                        )
                        
                        print(f"   ✅ Statistical verification completed!")
                        print(f"   Success: {verification_result['success']}")
                        print(f"   Attestation Artifact: {verification_result['attestation_artifact']}")
                        print(f"   Reasoning: {verification_result['reasoning'][:100]}...")
                        
                        # Test evidence CSV generation
                        print("\n9. Generating evidence CSV...")
                        try:
                            csv_artifact_id = evidence_module.generate_evidence_csv(analysis_artifact_ids)
                            
                            print(f"   ✅ Evidence CSV generated successfully!")
                            print(f"   CSV Artifact: {csv_artifact_id}")
                            
                            # Get evidence summary
                            summary = evidence_module.get_evidence_summary(analysis_artifact_ids)
                            print(f"   Total evidence items: {summary['total_evidence_items']}")
                            print(f"   Dimensions: {list(summary['dimension_counts'].keys())}")
                            
                            # Inspect artifacts
                            print("\n10. Artifact inspection:")
                            
                            # Statistics artifact
                            stats_data = storage.get_artifact(statistical_result['statistics_artifact'])
                            stats_content = json.loads(stats_data.decode('utf-8'))
                            print(f"\n   Statistics artifact ({statistical_result['statistics_artifact']}):")
                            print(f"   - Tests: {len(stats_content['tests'])}")
                            print(f"   - Aggregated rows: {len(stats_content['aggregated_rows'])}")
                            print(f"   - Test names: {[t['name'] for t in stats_content['tests']]}")
                            
                            # Work artifact
                            work_data = storage.get_artifact(statistical_result['work_artifact'])
                            work_content = json.loads(work_data.decode('utf-8'))
                            print(f"\n   Work artifact ({statistical_result['work_artifact']}):")
                            print(f"   - Code length: {len(work_content['executed_code'])} characters")
                            print(f"   - Output: {work_content['execution_output'].strip()}")
                            
                            # CSV artifact
                            csv_data = storage.get_artifact(statistical_result['csv_artifact'])
                            csv_content = csv_data.decode('utf-8')
                            print(f"\n   CSV artifact ({statistical_result['csv_artifact']}):")
                            print(f"   - Rows: {len(csv_content.split(chr(10)))-1}")  # -1 for header
                            print(f"   - Preview: {csv_content.split(chr(10))[0]}")
                            
                            # Attestation artifact
                            attestation_data = storage.get_artifact(verification_result['attestation_artifact'])
                            attestation_content = json.loads(attestation_data.decode('utf-8'))
                            print(f"\n   Attestation artifact ({verification_result['attestation_artifact']}):")
                            print(f"   - Success: {attestation_content['success']}")
                            print(f"   - Verifier: {attestation_content['verifier_model']}")
                            print(f"   - Reasoning: {attestation_content['reasoning'][:100]}...")
                            
                            print(f"\n=== Phase 2 Test Results ===")
                            print("✅ Statistical Planning + Execution Agent: WORKING")
                            print("✅ Statistical Verification Agent: WORKING")
                            print("✅ Evidence CSV Export Module: WORKING")
                            print("✅ Batch statistical analysis: WORKING")
                            print("✅ Statistical verification: WORKING")
                            print("✅ Evidence CSV generation: WORKING")
                            print("✅ Phase 2 architecture validated with mock responses")
                            
                        except Exception as e:
                            print(f"   ❌ Evidence CSV generation failed: {e}")
                            raise
                            
                    except Exception as e:
                        print(f"   ❌ Statistical verification failed: {e}")
                        raise
                        
                except Exception as e:
                    print(f"   ❌ Statistical analysis failed: {e}")
                    raise
                    
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        raise
        
    finally:
        # Cleanup
        import shutil
        shutil.rmtree(test_dir)
        print(f"\n11. Cleaned up test directory: {test_dir}")

if __name__ == "__main__":
    # Import patch after the main function definition
    from unittest.mock import patch
    main()
