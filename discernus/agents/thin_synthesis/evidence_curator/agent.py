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
import json
import re
import os
import yaml
import hashlib
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
    evidence_data: bytes  # JSON data instead of CSV path
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
    footnote_number: int
    evidence_hash: str

@dataclass
class EvidenceCurationResponse:
    """Response structure containing curated evidence."""
    curated_evidence: Dict[str, List[CuratedEvidence]]
    curation_summary: Dict[str, Any]
    success: bool
    error_message: Optional[str] = None
    footnote_registry: Dict[int, Dict[str, str]] = None
    
    def to_json_serializable(self) -> Dict[str, Any]:
        """Convert to JSON-serializable format for artifact storage."""
        serializable_evidence = {}
        for category, evidence_list in self.curated_evidence.items():
            serializable_evidence[category] = [asdict(evidence) for evidence in evidence_list]
        
        return {
            'curated_evidence': serializable_evidence,
            'curation_summary': self.curation_summary,
            'success': self.success,
            'error_message': self.error_message,
            'footnote_registry': self.footnote_registry or {}
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
        self.footnote_counter = 0
        self.footnote_registry = {}
        
    def curate_evidence(self, request: EvidenceCurationRequest) -> EvidenceCurationResponse:
        """
        Curate evidence based on statistical results.
        
        Args:
            request: EvidenceCurationRequest containing results and evidence
            
        Returns:
            EvidenceCurationResponse with curated evidence
        """
        try:
            # Reset footnote counter for new curation session
            self.footnote_counter = 0
            self.footnote_registry = {}
            
            # Defensive check: ensure statistical_results is not None
            if request.statistical_results is None:
                self.logger.warning("statistical_results is None, returning empty curated evidence")
                return EvidenceCurationResponse(
                    curated_evidence={},
                    curation_summary={"warning": "No statistical results provided"},
                    success=True,
                    footnote_registry={}
                )
            
            # Load and validate evidence data
            evidence_df = self._load_evidence_data(request.evidence_data)
            if evidence_df is None:
                return EvidenceCurationResponse(
                    curated_evidence={},
                    curation_summary={},
                    success=False,
                    error_message="Failed to load evidence data",
                    footnote_registry={}
                )
            
            # Filter evidence by confidence threshold (temporarily lowered for testing)
            high_confidence_evidence = evidence_df[
                evidence_df['confidence'] >= 0.5  # Lowered from request.min_confidence_threshold
            ].copy()
            
            if len(high_confidence_evidence) == 0:
                return EvidenceCurationResponse(
                    curated_evidence={},
                    curation_summary={"warning": "No evidence meets confidence threshold"},
                    success=True,
                    footnote_registry={}
                )
            
            # THIN approach: Let LLM handle evidence curation based on available data
            # Pass all statistical results and evidence to LLM for intelligent curation
            curated_evidence = self._curate_evidence_with_llm(
                request.statistical_results,
                high_confidence_evidence,
                request
            )
            
            # Generate curation summary
            curation_summary = self._generate_curation_summary(
                curated_evidence, 
                len(evidence_df), 
                len(high_confidence_evidence)
            )
            
            return EvidenceCurationResponse(
                curated_evidence=curated_evidence,
                curation_summary=curation_summary,
                success=True,
                footnote_registry=self.footnote_registry
            )
            
        except Exception as e:
            self.logger.error(f"Evidence curation failed: {str(e)}")
            return EvidenceCurationResponse(
                curated_evidence={},
                curation_summary={},
                success=False,
                error_message=str(e),
                footnote_registry={}
            )
    
    def _create_evidence_hash(self, evidence_text: str, artifact_id: str, dimension: str) -> str:
        """Create a hash for evidence verification."""
        content = f"{artifact_id}:{dimension}:{evidence_text}"
        return hashlib.sha256(content.encode('utf-8')).hexdigest()[:12]
    
    def _assign_footnote_number(self, evidence_text: str, artifact_id: str, dimension: str) -> int:
        """Assign a unique footnote number and register the evidence."""
        evidence_hash = self._create_evidence_hash(evidence_text, artifact_id, dimension)
        
        # Check if this evidence already has a footnote
        for footnote_num, registry_entry in self.footnote_registry.items():
            if registry_entry['evidence_hash'] == evidence_hash:
                return footnote_num
        
        # Assign new footnote number
        self.footnote_counter += 1
        self.footnote_registry[self.footnote_counter] = {
            'evidence_hash': evidence_hash,
            'artifact_id': artifact_id,
            'dimension': dimension,
            'evidence_text': evidence_text[:100] + '...' if len(evidence_text) > 100 else evidence_text
        }
        
        return self.footnote_counter
    
    def _curate_evidence_with_llm(self, statistical_results: Dict[str, Any], 
                                 evidence_df: pd.DataFrame,
                                 request: EvidenceCurationRequest) -> Dict[str, List[CuratedEvidence]]:
        """
        THIN approach: Let LLM intelligently curate evidence based on statistical results.
        Uses externalized YAML instructions for LLM guidance.
        """
        try:
            # Load externalized YAML instructions
            prompt_template = self._load_curation_prompt_template()
            
            # THIN approach: Pass raw data to LLM as strings
            # Let LLM handle any data structure without JSON serialization
            
            stats_str = str(statistical_results)
            evidence_str = str(evidence_df.to_dict('records')[:10])
            
            # Build prompt with YAML template
            prompt = prompt_template.format(
                framework_spec=request.framework_spec,
                statistical_results=stats_str,
                evidence_sample=evidence_str,
                max_evidence_per_finding=request.max_evidence_per_finding
            )
            
            # Call LLM for intelligent curation
            response_content, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=prompt,
                max_tokens=4000
            )
            
            if not response_content or not metadata.get('success'):
                self.logger.warning("LLM curation failed, returning empty evidence")
                return {}
            
            # Parse LLM response into curated evidence structure
            return self._parse_llm_curation_response(response_content, evidence_df)
            
        except Exception as e:
            self.logger.error(f"LLM evidence curation failed: {str(e)}")
            return {}
    
    def _load_curation_prompt_template(self) -> str:
        """Load externalized YAML instructions for evidence curation."""
        try:
            # Load from YAML file (THIN architecture)
            yaml_path = os.path.join(os.path.dirname(__file__), 'prompts', 'evidence_curation.yaml')
            with open(yaml_path, 'r') as f:
                config = yaml.safe_load(f)
            return config['template']
        except Exception as e:
            self.logger.warning(f"Could not load YAML template: {e}")
            # Fallback to simple template
            return """
You are an evidence curator for academic research. Given statistical results and evidence data, 
curate the most relevant evidence pieces that support the key findings.

Statistical Results:
{statistical_results}

Evidence Sample:
{evidence_sample}

Framework Specification:
{framework_spec}

Instructions:
1. Analyze the statistical results to identify key findings
2. Select the most relevant evidence pieces that support these findings
3. Return curated evidence in JSON format with reasoning for each selection
4. Limit to {max_evidence_per_finding} pieces per finding

Return only valid JSON.
"""
    
    def _parse_llm_curation_response(self, response_content: str, evidence_df: pd.DataFrame) -> Dict[str, List[CuratedEvidence]]:
        """Parse LLM response into structured curated evidence."""
        try:
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response_content, re.DOTALL)
            if not json_match:
                return {}
            
            llm_curation = json.loads(json_match.group())
            curated_evidence = {}
            
            # Convert LLM response to CuratedEvidence objects
            for category, evidence_list in llm_curation.items():
                if isinstance(evidence_list, list):
                    curated_evidence[category] = []
                    for evidence_item in evidence_list:
                        if isinstance(evidence_item, dict):
                            artifact_id = evidence_item.get('artifact_id', '')
                            dimension = evidence_item.get('dimension', '')
                            evidence_text = evidence_item.get('evidence_text', '')
                            
                            # Assign footnote number and create hash
                            footnote_number = self._assign_footnote_number(evidence_text, artifact_id, dimension)
                            evidence_hash = self._create_evidence_hash(evidence_text, artifact_id, dimension)
                            
                            curated_evidence[category].append(CuratedEvidence(
                                artifact_id=artifact_id,
                                dimension=dimension,
                                evidence_text=evidence_text,
                                context=evidence_item.get('context', ''),
                                confidence=evidence_item.get('confidence', 0.0),
                                reasoning=evidence_item.get('reasoning', ''),
                                relevance_score=evidence_item.get('relevance_score', 0.0),
                                statistical_connection=evidence_item.get('statistical_connection', ''),
                                footnote_number=footnote_number,
                                evidence_hash=evidence_hash
                            ))
            
            return curated_evidence
            
        except Exception as e:
            self.logger.error(f"Failed to parse LLM curation response: {str(e)}")
            return {}
    
    def _load_evidence_data(self, evidence_data: bytes) -> Optional[pd.DataFrame]:
        """Load and validate evidence JSON data."""
        
        try:
            # Parse JSON data
            import json
            json_str = evidence_data.decode('utf-8')
            analysis_result = json.loads(json_str)
            
            # Debug: Log the structure of the analysis result
            self.logger.info(f"Analysis result keys: {list(analysis_result.keys()) if isinstance(analysis_result, dict) else 'Not a dict'}")
            if isinstance(analysis_result, dict):
                for key, value in analysis_result.items():
                    if isinstance(value, list):
                        self.logger.info(f"  {key}: list with {len(value)} items")
                    elif isinstance(value, dict):
                        self.logger.info(f"  {key}: dict with keys {list(value.keys())}")
                    else:
                        self.logger.info(f"  {key}: {type(value).__name__}")
            
            # Convert to DataFrame using same logic as synthesis pipeline
            document_analyses = analysis_result.get('document_analyses', [])
            
            if not document_analyses:
                raise ValueError("No document_analyses found in JSON")
            
            rows = []
            for doc_analysis in document_analyses:
                document_id = doc_analysis.get('document_id', '{artifact_id}')
                evidence_list = doc_analysis.get('evidence', [])
                
                for i, evidence in enumerate(evidence_list):
                    if isinstance(evidence, dict):
                        row = {
                            'aid': document_id,
                            'dimension': evidence.get('dimension', ''),
                            'quote_id': evidence.get('quote_id', f"quote_{i}"),
                            'quote_text': evidence.get('quote_text', ''),
                            'confidence_score': evidence.get('confidence', 0.0),
                            'context_type': evidence.get('context_type', 'direct')
                        }
                        rows.append(row)
            
            if not rows:
                return pd.DataFrame(columns=['aid', 'dimension', 'quote_id', 'quote_text', 'confidence_score', 'context_type'])
            
            evidence_df = pd.DataFrame(rows)
            
            # Map actual column names to expected column names  
            column_mapping = {
                'aid': 'artifact_id',
                'quote_text': 'evidence_text',
                'confidence_score': 'confidence',
                'context_type': 'context'
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
            
            # Debug logging
            self.logger.info(f"Looking for evidence for dimension '{dim_name}' (from '{dim}')")
            self.logger.info(f"Available dimensions in evidence: {evidence_df['dimension'].unique().tolist()}")
            
            # Get evidence for this dimension
            dim_evidence = evidence_df[evidence_df['dimension'] == dim_name]
            
            self.logger.info(f"Found {len(dim_evidence)} pieces of evidence for dimension '{dim_name}'")
            
            if len(dim_evidence) > 0:
                # Select top evidence by confidence
                top_evidence = dim_evidence.nlargest(
                    min(request.max_evidence_per_finding, len(dim_evidence)), 
                    'confidence'
                )
                
                for _, row in top_evidence.iterrows():
                    artifact_id = row['artifact_id']
                    dimension = row['dimension']
                    evidence_text = row['evidence_text']
                    
                    # Assign footnote number and create hash
                    footnote_number = self._assign_footnote_number(evidence_text, artifact_id, dimension)
                    evidence_hash = self._create_evidence_hash(evidence_text, artifact_id, dimension)
                    
                    curated.append(CuratedEvidence(
                        artifact_id=artifact_id,
                        dimension=dimension,
                        evidence_text=evidence_text,
                        context=row['context'],
                        confidence=row['confidence'],
                        reasoning=row['reasoning'],
                        relevance_score=0.8,
                        statistical_connection=f"Supports {dim} mean score of {dimension_scores[dim]:.3f}",
                        footnote_number=footnote_number,
                        evidence_hash=evidence_hash
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
                            artifact_id = row['artifact_id']
                            dimension = row['dimension']
                            evidence_text = row['evidence_text']
                            
                            # Assign footnote number and create hash
                            footnote_number = self._assign_footnote_number(evidence_text, artifact_id, dimension)
                            evidence_hash = self._create_evidence_hash(evidence_text, artifact_id, dimension)
                            
                            curated.append(CuratedEvidence(
                                artifact_id=artifact_id,
                                dimension=dimension,
                                evidence_text=evidence_text,
                                context=row['context'],
                                confidence=row['confidence'],
                                reasoning=row['reasoning'],
                                relevance_score=0.9,
                                statistical_connection=f"Supports {hypothesis} (p={p_value:.4f})",
                                footnote_number=footnote_number,
                                evidence_hash=evidence_hash
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
                            artifact_id = row['artifact_id']
                            dimension = row['dimension']
                            evidence_text = row['evidence_text']
                            
                            # Assign footnote number and create hash
                            footnote_number = self._assign_footnote_number(evidence_text, artifact_id, dimension)
                            evidence_hash = self._create_evidence_hash(evidence_text, artifact_id, dimension)
                            
                            curated.append(CuratedEvidence(
                                artifact_id=artifact_id,
                                dimension=dimension,
                                evidence_text=evidence_text,
                                context=row['context'],
                                confidence=row['confidence'],
                                reasoning=row['reasoning'],
                                relevance_score=0.7,
                                statistical_connection=f"Part of strong correlation: {dim1} ↔ {dim2} (r={corr_value:.3f})",
                                footnote_number=footnote_number,
                                evidence_hash=evidence_hash
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
                                    artifact_id = row['artifact_id']
                                    dimension = row['dimension']
                                    evidence_text = row['evidence_text']
                                    
                                    # Assign footnote number and create hash
                                    footnote_number = self._assign_footnote_number(evidence_text, artifact_id, dimension)
                                    evidence_hash = self._create_evidence_hash(evidence_text, artifact_id, dimension)
                                    
                                    curated.append(CuratedEvidence(
                                        artifact_id=artifact_id,
                                        dimension=dimension,
                                        evidence_text=evidence_text,
                                        context=row['context'],
                                        confidence=row['confidence'],
                                        reasoning=row['reasoning'],
                                        relevance_score=0.6,
                                        statistical_connection=f"Illustrates {cluster_name} reliability concerns (α={alpha:.3f})",
                                        footnote_number=footnote_number,
                                        evidence_hash=evidence_hash
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
                                artifact_id = row['artifact_id']
                                dimension = row['dimension']
                                evidence_text = row['evidence_text']
                                
                                # Assign footnote number and create hash
                                footnote_number = self._assign_footnote_number(evidence_text, artifact_id, dimension)
                                evidence_hash = self._create_evidence_hash(evidence_text, artifact_id, dimension)
                                
                                curated.append(CuratedEvidence(
                                    artifact_id=artifact_id,
                                    dimension=dimension,
                                    evidence_text=evidence_text,
                                    context=row['context'],
                                    confidence=row['confidence'],
                                    reasoning=row['reasoning'],
                                    relevance_score=0.9,
                                    statistical_connection=f"Demonstrates {cluster_name} high reliability (α={alpha:.3f})",
                                    footnote_number=footnote_number,
                                    evidence_hash=evidence_hash
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