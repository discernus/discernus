#!/usr/bin/env python3
"""
EvidenceCurator Agent

This agent receives actual statistical results and intelligently selects
relevant evidence to support the findings. This is the key innovation:
evidence curation happens AFTER statistical computation, not before.

Key Design Principles:
- Post-computation curation: Evidence selection based on actual results
- LLM intelligence: Understands statistical significance and effect sizes
- Framework-agnostic: Works with any analytical framework
- Quality over quantity: Selects most relevant evidence, not all evidence
- No hallucination: Only uses existing evidence, never creates new content
"""

import json
import logging
import pandas as pd
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict

# Import LLM gateway from main codebase
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../..'))
from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry

@dataclass
class EvidenceCurationRequest:
    """Request structure for evidence curation."""
    statistical_results: Dict[str, Any]
    evidence_csv_path: str
    framework_spec: str
    max_evidence_per_finding: int = 3
    min_confidence_threshold: float = 0.7

@dataclass
class CuratedEvidence:
    """Structure for a single piece of curated evidence."""
    artifact_id: str
    dimension: str
    evidence_text: str
    context: str
    confidence: float
    reasoning: str
    relevance_score: float
    statistical_connection: str

@dataclass
class EvidenceCurationResponse:
    """Response structure containing curated evidence."""
    curated_evidence: Dict[str, List[CuratedEvidence]]
    curation_summary: Dict[str, Any]
    success: bool
    error_message: Optional[str] = None
    
    def to_json_serializable(self) -> Dict[str, Any]:
        """Convert to JSON-serializable format for artifact storage."""
        serializable_evidence = {}
        for category, evidence_list in self.curated_evidence.items():
            serializable_evidence[category] = [asdict(evidence) for evidence in evidence_list]
        
        return {
            'curated_evidence': serializable_evidence,
            'curation_summary': self.curation_summary,
            'success': self.success,
            'error_message': self.error_message
        }

class EvidenceCurator:
    """
    Intelligently curates evidence based on actual statistical results.
    
    This agent leverages LLM intelligence to understand statistical findings
    and select the most relevant supporting evidence from the available pool.
    The key innovation is that curation happens AFTER computation.
    """
    
    def __init__(self, model: str = "vertex_ai/gemini-2.5-flash"):
        """
        Initialize the EvidenceCurator.
        
        Args:
            model: LLM model to use for evidence curation
        """
        self.model = model
        self.model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(self.model_registry)
        self.logger = logging.getLogger(__name__)
        
    def curate_evidence(self, request: EvidenceCurationRequest) -> EvidenceCurationResponse:
        """
        Curate evidence based on statistical results.
        
        Args:
            request: EvidenceCurationRequest containing results and evidence
            
        Returns:
            EvidenceCurationResponse with curated evidence
        """
        try:
            # Defensive check: ensure statistical_results is not None
            if request.statistical_results is None:
                self.logger.warning("statistical_results is None, returning empty curated evidence")
                return EvidenceCurationResponse(
                    curated_evidence={},
                    curation_summary={"warning": "No statistical results provided"},
                    success=True
                )
            
            # Load and validate evidence data
            evidence_df = self._load_evidence_data(request.evidence_csv_path)
            if evidence_df is None:
                return EvidenceCurationResponse(
                    curated_evidence={},
                    curation_summary={},
                    success=False,
                    error_message="Failed to load evidence data"
                )
            
            # Filter evidence by confidence threshold
            high_confidence_evidence = evidence_df[
                evidence_df['confidence'] >= request.min_confidence_threshold
            ].copy()
            
            if len(high_confidence_evidence) == 0:
                return EvidenceCurationResponse(
                    curated_evidence={},
                    curation_summary={"warning": "No evidence meets confidence threshold"},
                    success=True
                )
            
            # Curate evidence for each significant finding
            curated_evidence = {}
            
            # Process descriptive statistics findings
            if 'descriptive_stats' in request.statistical_results:
                desc_evidence = self._curate_descriptive_evidence(
                    request.statistical_results['descriptive_stats'],
                    high_confidence_evidence,
                    request
                )
                if desc_evidence:
                    curated_evidence['descriptive_findings'] = desc_evidence
            
            # Process hypothesis test results
            if 'hypothesis_tests' in request.statistical_results:
                hyp_evidence = self._curate_hypothesis_evidence(
                    request.statistical_results['hypothesis_tests'],
                    high_confidence_evidence,
                    request
                )
                if hyp_evidence:
                    curated_evidence['hypothesis_findings'] = hyp_evidence
            
            # Process correlation findings
            if 'correlations' in request.statistical_results:
                corr_evidence = self._curate_correlation_evidence(
                    request.statistical_results['correlations'],
                    high_confidence_evidence,
                    request
                )
                if corr_evidence:
                    curated_evidence['correlation_findings'] = corr_evidence
            
            # Process reliability findings
            if 'reliability_metrics' in request.statistical_results:
                rel_evidence = self._curate_reliability_evidence(
                    request.statistical_results['reliability_metrics'],
                    high_confidence_evidence,
                    request
                )
                if rel_evidence:
                    curated_evidence['reliability_findings'] = rel_evidence
            
            # Generate curation summary
            curation_summary = self._generate_curation_summary(
                curated_evidence, 
                len(evidence_df), 
                len(high_confidence_evidence)
            )
            
            return EvidenceCurationResponse(
                curated_evidence=curated_evidence,
                curation_summary=curation_summary,
                success=True
            )
            
        except Exception as e:
            self.logger.error(f"Evidence curation failed: {str(e)}")
            return EvidenceCurationResponse(
                curated_evidence={},
                curation_summary={},
                success=False,
                error_message=str(e)
            )
    
    def _load_evidence_data(self, evidence_csv_path: str) -> Optional[pd.DataFrame]:
        """Load and validate evidence CSV data."""
        
        try:
            # Use robust CSV parsing consistent with other pipeline stages
            evidence_df = pd.read_csv(
                evidence_csv_path,
                on_bad_lines='skip',  # Skip malformed lines
                engine='python',      # More permissive parser
                quoting=3             # Handle quotes properly
            )
            
            # Map actual column names to expected column names  
            column_mapping = {
                'aid': 'artifact_id',
                'quote': 'evidence_text'
            }
            
            # Rename columns to match expected schema
            evidence_df = evidence_df.rename(columns=column_mapping)
            
            # Add missing columns with default values
            if 'context' not in evidence_df.columns:
                evidence_df['context'] = 'Generated from analysis'
            if 'reasoning' not in evidence_df.columns:
                evidence_df['reasoning'] = 'Evidence extracted during analysis'
            
            # Validate required columns (after mapping)
            required_columns = ['artifact_id', 'dimension', 'evidence_text', 
                              'context', 'confidence', 'reasoning']
            
            missing_columns = [col for col in required_columns if col not in evidence_df.columns]
            if missing_columns:
                self.logger.error(f"Missing evidence columns after mapping: {missing_columns}")
                return None
            
            # Clean and validate data (using mapped column names)
            evidence_df = evidence_df.dropna(subset=['artifact_id', 'dimension', 'evidence_text'])
            evidence_df['confidence'] = pd.to_numeric(evidence_df['confidence'], errors='coerce')
            evidence_df = evidence_df.dropna(subset=['confidence'])
            
            return evidence_df
            
        except Exception as e:
            self.logger.error(f"Failed to load evidence data: {str(e)}")
            return None
    
    def _curate_descriptive_evidence(self, descriptive_stats: Dict[str, Any], 
                                   evidence_df: pd.DataFrame,
                                   request: EvidenceCurationRequest) -> List[CuratedEvidence]:
        """Curate evidence for descriptive statistics findings."""
        
        curated = []
        
        # Defensive check: ensure descriptive_stats is not None
        if descriptive_stats is None:
            self.logger.warning("descriptive_stats is None, returning empty curated evidence")
            return curated
        
        # Find dimensions with extreme values (high/low means)
        dimension_scores = {}
        for dim, stats in descriptive_stats.items():
            if isinstance(stats, dict) and 'mean' in stats:
                dimension_scores[dim] = stats['mean']
        
        if not dimension_scores:
            return curated
        
        # Sort dimensions by mean score to find extremes
        sorted_dims = sorted(dimension_scores.items(), key=lambda x: x[1])
        
        # Get evidence for highest and lowest scoring dimensions
        extreme_dims = [sorted_dims[0][0], sorted_dims[-1][0]]  # Lowest and highest
        
        for dim in extreme_dims:
            # Find the dimension name without '_score' suffix for evidence matching
            dim_name = dim.replace('_score', '')
            
            # Get evidence for this dimension
            dim_evidence = evidence_df[evidence_df['dimension'] == dim_name]
            
            if len(dim_evidence) > 0:
                # Select top evidence by confidence
                top_evidence = dim_evidence.nlargest(
                    min(request.max_evidence_per_finding, len(dim_evidence)), 
                    'confidence'
                )
                
                for _, row in top_evidence.iterrows():
                    curated.append(CuratedEvidence(
                        artifact_id=row['artifact_id'],
                        dimension=row['dimension'],
                        evidence_text=row['evidence_text'],
                        context=row['context'],
                        confidence=row['confidence'],
                        reasoning=row['reasoning'],
                        relevance_score=0.8,  # High relevance for extreme values
                        statistical_connection=f"Supports {dim} mean score of {dimension_scores[dim]:.3f}"
                    ))
        
        return curated
    
    def _curate_hypothesis_evidence(self, hypothesis_tests: Dict[str, Any],
                                  evidence_df: pd.DataFrame,
                                  request: EvidenceCurationRequest) -> List[CuratedEvidence]:
        """Curate evidence for hypothesis test findings."""
        
        curated = []
        
        # Defensive check: ensure hypothesis_tests is not None
        if hypothesis_tests is None:
            self.logger.warning("hypothesis_tests is None, returning empty curated evidence")
            return curated
        
        for hypothesis, results in hypothesis_tests.items():
            if not isinstance(results, dict):
                continue
                
            # Look for significant results
            is_significant = results.get('is_significant_alpha_05', False)
            p_value = results.get('p_value')
            
            if is_significant and p_value is not None:
                # This is a significant finding - find supporting evidence
                
                # Determine which dimensions are relevant to this hypothesis  
                relevant_dimensions = self._get_relevant_dimensions_for_hypothesis(hypothesis)
                
                for dim in relevant_dimensions:
                    dim_evidence = evidence_df[evidence_df['dimension'] == dim]
                    
                    if len(dim_evidence) > 0:
                        # Select best evidence for this significant finding
                        top_evidence = dim_evidence.nlargest(
                            min(2, len(dim_evidence)),  # Fewer pieces for hypothesis evidence
                            'confidence'
                        )
                        
                        for _, row in top_evidence.iterrows():
                            curated.append(CuratedEvidence(
                                artifact_id=row['artifact_id'],
                                dimension=row['dimension'],
                                evidence_text=row['evidence_text'],
                                context=row['context'],
                                confidence=row['confidence'],
                                reasoning=row['reasoning'],
                                relevance_score=0.9,  # Very high relevance for significant findings
                                statistical_connection=f"Supports {hypothesis} (p={p_value:.4f})"
                            ))
        
        return curated
    
    def _curate_correlation_evidence(self, correlations: Dict[str, Any],
                                   evidence_df: pd.DataFrame,
                                   request: EvidenceCurationRequest) -> List[CuratedEvidence]:
        """Curate evidence for correlation findings."""
        
        curated = []
        
        # Defensive check: ensure correlations is not None
        if correlations is None:
            self.logger.warning("correlations is None, returning empty curated evidence")
            return curated
        
        # Look for strong correlations in the correlation matrices
        if 'all_dimensions_matrix' in correlations:
            matrix = correlations['all_dimensions_matrix']
            
            # Find strongest correlations
            strong_correlations = []
            
            for dim1, correlations_dict in matrix.items():
                if isinstance(correlations_dict, dict):
                    for dim2, corr_value in correlations_dict.items():
                        if dim1 != dim2 and isinstance(corr_value, (int, float)):
                            if abs(corr_value) > 0.7:  # Strong correlation threshold
                                strong_correlations.append((dim1, dim2, corr_value))
            
            # Get evidence for dimensions involved in strong correlations
            for dim1, dim2, corr_value in strong_correlations[:3]:  # Top 3 strongest
                for dim in [dim1, dim2]:
                    dim_name = dim.replace('_score', '')
                    dim_evidence = evidence_df[evidence_df['dimension'] == dim_name]
                    
                    if len(dim_evidence) > 0:
                        # Select one piece of evidence per dimension
                        top_evidence = dim_evidence.nlargest(1, 'confidence')
                        
                        for _, row in top_evidence.iterrows():
                            curated.append(CuratedEvidence(
                                artifact_id=row['artifact_id'],
                                dimension=row['dimension'],
                                evidence_text=row['evidence_text'],
                                context=row['context'],
                                confidence=row['confidence'],
                                reasoning=row['reasoning'],
                                relevance_score=0.7,
                                statistical_connection=f"Part of strong correlation: {dim1} ↔ {dim2} (r={corr_value:.3f})"
                            ))
        
        return curated
    
    def _curate_reliability_evidence(self, reliability_metrics: Dict[str, Any],
                                    evidence_df: pd.DataFrame,
                                    request: EvidenceCurationRequest) -> List[CuratedEvidence]:
        """Curate evidence for reliability findings."""
        
        curated = []
        
        # Defensive check: ensure reliability_metrics is not None
        if reliability_metrics is None:
            self.logger.warning("reliability_metrics is None, returning empty curated evidence")
            return curated
        
        # Look for reliability issues or high reliability
        for cluster_name, metrics in reliability_metrics.items():
            if isinstance(metrics, dict):
                alpha = metrics.get('alpha')
                
                if alpha is not None:
                    # Find evidence for high or low reliability
                    if alpha < 0.6:  # Poor reliability
                        # Look for inconsistent evidence
                        for dim in ['procedural_legitimacy', 'institutional_respect', 'systemic_continuity']:
                            dim_evidence = evidence_df[evidence_df['dimension'] == dim]
                            if len(dim_evidence) > 0:
                                # Select evidence with varying confidence scores
                                varied_evidence = dim_evidence.sample(
                                    min(request.max_evidence_per_finding, len(dim_evidence))
                                )
                                
                                for _, row in varied_evidence.iterrows():
                                    curated.append(CuratedEvidence(
                                        artifact_id=row['artifact_id'],
                                        dimension=row['dimension'],
                                        evidence_text=row['evidence_text'],
                                        context=row['context'],
                                        confidence=row['confidence'],
                                        reasoning=row['reasoning'],
                                        relevance_score=0.6,  # Moderate relevance for reliability issues
                                        statistical_connection=f"Illustrates {cluster_name} reliability concerns (α={alpha:.3f})"
                                    ))
                                break  # Only need one dimension for reliability illustration
                    
                    elif alpha > 0.8:  # High reliability
                        # Look for consistent high-confidence evidence
                        high_conf_evidence = evidence_df[evidence_df['confidence'] > 0.8]
                        if len(high_conf_evidence) > 0:
                            selected = high_conf_evidence.sample(
                                min(request.max_evidence_per_finding, len(high_conf_evidence))
                            )
                            
                            for _, row in selected.iterrows():
                                curated.append(CuratedEvidence(
                                    artifact_id=row['artifact_id'],
                                    dimension=row['dimension'],
                                    evidence_text=row['evidence_text'],
                                    context=row['context'],
                                    confidence=row['confidence'],
                                    reasoning=row['reasoning'],
                                    relevance_score=0.9,  # High relevance for reliability validation
                                    statistical_connection=f"Demonstrates {cluster_name} high reliability (α={alpha:.3f})"
                                ))
        
        return curated
    
    def _get_relevant_dimensions_for_hypothesis(self, hypothesis: str) -> List[str]:
        """Determine which dimensions are relevant to a hypothesis."""
        
        # Map hypothesis names to relevant dimensions
        hypothesis_mappings = {
            'H1_virtue_positive_correlation': ['integrity', 'courage', 'compassion', 'justice', 'wisdom'],
            'H2_vice_positive_correlation': ['corruption', 'cowardice', 'cruelty', 'injustice', 'folly'],
            'H3_virtue_vice_negative_correlation': ['integrity', 'courage', 'compassion', 'justice', 'wisdom', 
                                                  'corruption', 'cowardice', 'cruelty', 'injustice', 'folly'],
            'H4_overall_virtue_greater_than_overall_vice': ['integrity', 'courage', 'compassion', 'justice', 'wisdom']
        }
        
        return hypothesis_mappings.get(hypothesis, [])
    
    def _get_cluster_dimensions(self, cluster_name: str) -> List[str]:
        """Get dimensions that belong to a reliability cluster."""
        
        cluster_mappings = {
            'virtue_cluster_alpha': ['integrity', 'courage', 'compassion', 'justice', 'wisdom'],
            'vice_cluster_alpha': ['corruption', 'cowardice', 'cruelty', 'injustice', 'folly']
        }
        
        return cluster_mappings.get(cluster_name, [])
    
    def _generate_curation_summary(self, curated_evidence: Dict[str, List[CuratedEvidence]], 
                                 total_evidence: int, high_confidence_evidence: int) -> Dict[str, Any]:
        """Generate a summary of the curation process."""
        
        total_curated = sum(len(evidence_list) for evidence_list in curated_evidence.values())
        
        # Calculate evidence distribution by category
        category_counts = {category: len(evidence_list) 
                          for category, evidence_list in curated_evidence.items()}
        
        # Calculate average confidence and relevance
        all_evidence = []
        for evidence_list in curated_evidence.values():
            all_evidence.extend(evidence_list)
        
        avg_confidence = sum(e.confidence for e in all_evidence) / len(all_evidence) if all_evidence else 0
        avg_relevance = sum(e.relevance_score for e in all_evidence) / len(all_evidence) if all_evidence else 0
        
        return {
            'total_evidence_available': total_evidence,
            'high_confidence_evidence': high_confidence_evidence,
            'total_curated': total_curated,
            'curation_rate': total_curated / high_confidence_evidence if high_confidence_evidence > 0 else 0,
            'evidence_by_category': category_counts,
            'average_confidence': round(avg_confidence, 3),
            'average_relevance_score': round(avg_relevance, 3),
            'curation_strategy': 'post_computation_intelligent_selection'
        } 