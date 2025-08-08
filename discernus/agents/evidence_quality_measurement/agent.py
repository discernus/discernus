#!/usr/bin/env python3
"""
Evidence Quality Measurement Agent

Implements Epic #354 requirements for systematic evidence quality measurement:
- REQ-EU-001: Measure evidence utilization rate (pieces used / pieces available)
- REQ-EU-002: Track interpretive claim coverage (claims backed / total claims)
- REQ-EU-003: Implement evidence-claim alignment scoring
- REQ-EU-004: Create evidence relevance ranking system
- REQ-EU-005: Build evidence quality scoring framework

This agent provides comprehensive quality metrics for evidence integration
to ensure academic rigor and peer-review ready standards.
"""

import json
import logging
import re
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

from ...gateway.llm_gateway import LLMGateway
from ...gateway.model_registry import ModelRegistry


@dataclass
class EvidenceQualityMetrics:
    """Comprehensive evidence quality metrics."""
    # Utilization metrics
    evidence_utilization_rate: float  # pieces used / pieces available
    total_evidence_available: int
    total_evidence_used: int
    unique_evidence_used: int
    
    # Coverage metrics
    interpretive_claim_coverage: float  # claims backed / total claims
    total_interpretive_claims: int
    claims_with_evidence: int
    
    # Alignment metrics
    evidence_claim_alignment_score: float  # 0.0-1.0
    average_evidence_relevance: float  # 0.0-1.0
    evidence_diversity_score: float  # 0.0-1.0
    
    # Quality metrics
    overall_quality_score: float  # 0.0-1.0
    evidence_strength_validation: float  # 0.0-1.0
    evidence_context_preservation: float  # 0.0-1.0
    
    # Detailed breakdowns
    evidence_by_dimension: Dict[str, int]
    evidence_by_document: Dict[str, int]
    claim_evidence_mapping: Dict[str, List[str]]
    relevance_scores: Dict[str, float]


@dataclass
class QualityMeasurementRequest:
    """Request for evidence quality measurement."""
    txtai_curator: Any  # RAG curator for evidence access
    statistical_results: Dict[str, Any]  # Statistical findings
    synthesis_report: str  # Final synthesis report
    framework_spec: str  # Framework specification
    experiment_context: Optional[str] = None


@dataclass
class QualityMeasurementResponse:
    """Response with comprehensive quality metrics."""
    success: bool
    metrics: Optional[EvidenceQualityMetrics] = None
    error_message: Optional[str] = None
    recommendations: List[str] = None


class EvidenceQualityMeasurementAgent:
    """
    Comprehensive evidence quality measurement agent.
    
    Implements Epic #354 requirements for systematic quality measurement
    to ensure peer-review ready academic standards.
    """
    
    def __init__(self, model: str, audit_logger=None):
        """
        Initialize the Evidence Quality Measurement Agent.
        
        Args:
            model: LLM model for quality assessment
            audit_logger: Optional audit logger for cost tracking
        """
        self.model = model
        self.model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(self.model_registry)
        self.logger = logging.getLogger(__name__)
        self.audit_logger = audit_logger
        
    def measure_evidence_quality(self, request: QualityMeasurementRequest) -> QualityMeasurementResponse:
        """
        Main entry point for RAG-compliant evidence quality measurement.
        
        Implements Epic #354 requirements using query-based evidence access:
        - REQ-EU-001: Evidence utilization rate measurement
        - REQ-EU-002: Interpretive claim coverage tracking
        - REQ-EU-003: Evidence-claim alignment scoring
        - REQ-EU-004: Evidence relevance ranking
        - REQ-EU-005: Evidence quality scoring framework
        """
        try:
            # Use RAG curator for evidence access (not bulk loading)
            txtai_curator = request.txtai_curator
            
            # Generate quality assessment queries from synthesis report
            quality_queries = self._generate_quality_queries(request.synthesis_report, request.statistical_results)
            
            # Calculate utilization metrics using RAG queries (REQ-EU-001)
            utilization_metrics = self._calculate_utilization_metrics_rag(txtai_curator, request.synthesis_report)
            
            # Calculate coverage metrics using RAG queries (REQ-EU-002)
            coverage_metrics = self._calculate_coverage_metrics_rag(txtai_curator, request.statistical_results)
            
            # Calculate alignment metrics using RAG queries (REQ-EU-003)
            alignment_metrics = self._calculate_alignment_metrics_rag(txtai_curator, request.synthesis_report)
            
            # Calculate relevance metrics using RAG queries (REQ-EU-004)
            relevance_metrics = self._calculate_relevance_metrics_rag(txtai_curator, request.framework_spec)
            
            # Calculate quality metrics using RAG queries (REQ-EU-005)
            quality_metrics = self._calculate_quality_metrics_rag(txtai_curator, request.synthesis_report)
            
            # Combine all metrics
            combined_metrics = EvidenceQualityMetrics(
                # Utilization
                evidence_utilization_rate=utilization_metrics['utilization_rate'],
                total_evidence_available=utilization_metrics['total_available'],
                total_evidence_used=utilization_metrics['total_used'],
                unique_evidence_used=utilization_metrics['unique_used'],
                
                # Coverage
                interpretive_claim_coverage=coverage_metrics['claim_coverage'],
                total_interpretive_claims=coverage_metrics['total_claims'],
                claims_with_evidence=coverage_metrics['claims_with_evidence'],
                
                # Alignment
                evidence_claim_alignment_score=alignment_metrics['alignment_score'],
                average_evidence_relevance=alignment_metrics['avg_relevance'],
                evidence_diversity_score=alignment_metrics['diversity_score'],
                
                # Quality
                overall_quality_score=quality_metrics['overall_score'],
                evidence_strength_validation=quality_metrics['strength_validation'],
                evidence_context_preservation=quality_metrics['context_preservation'],
                
                # Detailed breakdowns
                evidence_by_dimension=utilization_metrics['by_dimension'],
                evidence_by_document=utilization_metrics['by_document'],
                claim_evidence_mapping=coverage_metrics['claim_mapping'],
                relevance_scores=relevance_metrics['relevance_scores']
            )
            
            # Generate recommendations
            recommendations = self._generate_quality_recommendations(combined_metrics)
            
            return QualityMeasurementResponse(
                success=True,
                metrics=combined_metrics,
                recommendations=recommendations
            )
            
        except Exception as e:
            self.logger.error(f"Evidence quality measurement failed: {str(e)}")
            return QualityMeasurementResponse(
                success=False,
                error_message=str(e)
            )
    
    def _generate_quality_queries(self, synthesis_report: str, statistical_results: Dict[str, Any]) -> List[str]:
        """Generate quality assessment queries from synthesis report and statistical results."""
        queries = []
        
        # Extract queries from synthesis report
        synthesis_queries = self._extract_queries_from_synthesis(synthesis_report)
        queries.extend(synthesis_queries)
        
        # Extract queries from statistical results
        statistical_queries = self._extract_queries_from_statistical_results(statistical_results)
        queries.extend(statistical_queries)
        
        return queries
    
    def _extract_queries_from_synthesis(self, synthesis_report: str) -> List[str]:
        """Extract evidence queries from synthesis report."""
        queries = []
        
        # Extract dimension names mentioned in synthesis
        dimension_patterns = [
            'dignity', 'truth', 'justice', 'hope', 'pragmatism',
            'tribalism', 'manipulation', 'resentment', 'fear', 'fantasy'
        ]
        
        for dimension in dimension_patterns:
            if dimension.lower() in synthesis_report.lower():
                queries.append(f"{dimension} evidence")
        
        # Extract document names mentioned in synthesis
        document_pattern = r'\[(\d+)\].*?document_id:\s*([^,\s]+)'
        matches = re.findall(document_pattern, synthesis_report)
        for _, doc_name in matches:
            queries.append(f"document {doc_name}")
        
        return queries
    
    def _extract_queries_from_statistical_results(self, statistical_results: Dict[str, Any]) -> List[str]:
        """Extract evidence queries from statistical results."""
        queries = []
        
        # Look for dimension scores in statistical results
        for result_key, result_data in statistical_results.items():
            if isinstance(result_data, dict):
                # Extract dimension names from result keys
                for key in result_data.keys():
                    if '_score' in key:
                        dimension = key.replace('_score', '')
                        queries.append(f"{dimension} evidence")
        
        return queries
    
    def _calculate_utilization_metrics_rag(self, txtai_curator, synthesis_report: str) -> Dict[str, Any]:
        """
        REQ-EU-001: Calculate evidence utilization rate using RAG queries.
        
        Returns:
            Dict with utilization_rate, total_available, total_used, unique_used,
            by_dimension, by_document
        """
        # Extract evidence references from synthesis report
        evidence_refs = self._extract_evidence_references(synthesis_report)
        
        # Query for evidence that appears in synthesis
        synthesis_queries = self._extract_queries_from_synthesis(synthesis_report)
        
        total_evidence_found = 0
        by_dimension = {}
        by_document = {}
        
        for query in synthesis_queries[:10]:  # Limit queries for efficiency
            try:
                evidence = txtai_curator._query_evidence(query)
                if evidence:
                    total_evidence_found += len(evidence)
                    
                    # Track by dimension and document
                    for ev in evidence:
                        dimension = ev.get('dimension', 'unknown')
                        by_dimension[dimension] = by_dimension.get(dimension, 0) + 1
                        
                        document = ev.get('document_name', 'unknown')
                        by_document[document] = by_document.get(document, 0) + 1
            except Exception as e:
                self.logger.debug(f"Query failed for '{query}': {e}")
        
        # Estimate utilization rate based on evidence references vs. found evidence
        unique_used = len(evidence_refs)
        total_available = len(txtai_curator.documents) if hasattr(txtai_curator, 'documents') and txtai_curator.documents else 100  # Estimate
        utilization_rate = unique_used / total_available if total_available > 0 else 0.0
        
        return {
            'utilization_rate': utilization_rate,
            'total_available': total_available,
            'total_used': total_evidence_found,
            'unique_used': unique_used,
            'by_dimension': by_dimension,
            'by_document': by_document
        }
    
    def _extract_evidence_references(self, synthesis_report: str) -> List[str]:
        """Extract evidence references from synthesis report."""
        # Look for evidence reference patterns like [1], [2], etc.
        ref_pattern = r'\[(\d+)\]'
        matches = re.findall(ref_pattern, synthesis_report)
        return list(set(matches))  # Remove duplicates
    
    def _calculate_coverage_metrics_rag(self, txtai_curator, statistical_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        REQ-EU-002: Calculate interpretive claim coverage using RAG queries.
        
        Returns:
            Dict with claim_coverage, total_claims, claims_with_evidence, claim_mapping
        """
        # Extract interpretive claims from statistical results
        interpretive_claims = []
        claim_mapping = {}
        
        # Look for claims in statistical results
        for result_key, result_data in statistical_results.items():
            if isinstance(result_data, dict):
                # Check if this is an interpretive claim (has narrative content)
                if 'narrative' in result_data or 'interpretation' in result_data:
                    interpretive_claims.append(result_key)
                    
                    # Generate query for this claim
                    claim_query = self._generate_claim_query(result_key, result_data)
                    
                    # Query for evidence relevant to this claim
                    try:
                        evidence = txtai_curator._query_evidence(claim_query)
                        claim_evidence = [ev.get('quote_text', '') for ev in evidence] if evidence else []
                        claim_mapping[result_key] = claim_evidence
                    except Exception as e:
                        self.logger.debug(f"Claim query failed for '{result_key}': {e}")
                        claim_mapping[result_key] = []
        
        total_claims = len(interpretive_claims)
        claims_with_evidence = len([c for c in claim_mapping.values() if c])
        claim_coverage = claims_with_evidence / total_claims if total_claims > 0 else 0.0
        
        return {
            'claim_coverage': claim_coverage,
            'total_claims': total_claims,
            'claims_with_evidence': claims_with_evidence,
            'claim_mapping': claim_mapping
        }
    
    def _generate_claim_query(self, result_key: str, result_data: Dict[str, Any]) -> str:
        """Generate evidence query for a specific claim."""
        # Extract key terms from result key and data
        query_terms = []
        
        # Add result key terms
        query_terms.extend(result_key.split('_'))
        
        # Add terms from result data
        if isinstance(result_data, dict):
            for key, value in result_data.items():
                if isinstance(value, str):
                    query_terms.extend(value.split()[:5])  # First 5 words
        
        # Create query from terms
        query = ' '.join(query_terms[:10])  # Limit to 10 terms
        return query
    
    def _calculate_alignment_metrics_rag(self, txtai_curator, synthesis_report: str) -> Dict[str, Any]:
        """
        REQ-EU-003: Calculate evidence-claim alignment scoring using RAG queries.
        
        Returns:
            Dict with alignment_score, avg_relevance, diversity_score
        """
        # Extract evidence references from synthesis report
        evidence_refs = self._extract_evidence_references(synthesis_report)
        
        # Query for evidence that appears in synthesis
        synthesis_queries = self._extract_queries_from_synthesis(synthesis_report)
        
        evidence_in_synthesis = 0
        relevance_scores = []
        unique_documents = set()
        total_evidence_checked = 0
        
        for query in synthesis_queries[:10]:  # Limit queries for efficiency
            try:
                evidence = txtai_curator._query_evidence(query)
                if evidence:
                    total_evidence_checked += len(evidence)
                    
                    for ev in evidence:
                        quote = ev.get('quote_text', '')
                        if quote and quote in synthesis_report:
                            evidence_in_synthesis += 1
                            relevance_scores.append(1.0)  # Perfect alignment
                        elif quote:
                            relevance_scores.append(0.5)  # Partial alignment
                        else:
                            relevance_scores.append(0.0)
                        
                        # Track document diversity
                        doc = ev.get('document_name', '')
                        if doc:
                            unique_documents.add(doc)
            except Exception as e:
                self.logger.debug(f"Alignment query failed for '{query}': {e}")
        
        alignment_score = evidence_in_synthesis / total_evidence_checked if total_evidence_checked > 0 else 0.0
        avg_relevance = sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0.0
        diversity_score = len(unique_documents) / total_evidence_checked if total_evidence_checked > 0 else 0.0
        
        return {
            'alignment_score': alignment_score,
            'avg_relevance': avg_relevance,
            'diversity_score': diversity_score
        }
    
    def _calculate_relevance_metrics_rag(self, txtai_curator, framework_spec: str) -> Dict[str, Any]:
        """
        REQ-EU-004: Calculate evidence relevance ranking using RAG queries.
        
        Returns:
            Dict with relevance_scores
        """
        relevance_scores = {}
        
        # Query for evidence from framework dimensions
        dimension_queries = self._extract_dimension_queries(framework_spec)
        
        for query in dimension_queries[:5]:  # Limit queries for efficiency
            try:
                evidence = txtai_curator._query_evidence(query)
                if evidence:
                    for ev in evidence:
                        quote = ev.get('quote_text', '')
                        dimension = ev.get('dimension', '')
                        confidence = ev.get('confidence', 0.0)
                        
                        # Calculate relevance based on multiple factors
                        relevance_score = 0.0
                        
                        # Factor 1: Confidence score (0.0-1.0)
                        relevance_score += confidence * 0.4
                        
                        # Factor 2: Dimension relevance to framework
                        if dimension and dimension.lower() in framework_spec.lower():
                            relevance_score += 0.3
                        
                        # Factor 3: Quote length (prefer substantial quotes)
                        quote_length = len(quote) if quote else 0
                        if 50 <= quote_length <= 200:
                            relevance_score += 0.2
                        elif quote_length > 200:
                            relevance_score += 0.1
                        
                        # Factor 4: Document quality (prefer named documents)
                        doc_name = ev.get('document_name', '')
                        if doc_name and not doc_name.startswith('unknown'):
                            relevance_score += 0.1
                        
                        relevance_scores[quote[:50] + "..."] = min(relevance_score, 1.0)
            except Exception as e:
                self.logger.debug(f"Relevance query failed for '{query}': {e}")
        
        return {
            'relevance_scores': relevance_scores
        }
    
    def _extract_dimension_queries(self, framework_spec: str) -> List[str]:
        """Extract dimension queries from framework specification."""
        queries = []
        
        # Look for dimension names in framework spec
        dimension_patterns = [
            'dignity', 'truth', 'justice', 'hope', 'pragmatism',
            'tribalism', 'manipulation', 'resentment', 'fear', 'fantasy'
        ]
        
        for dimension in dimension_patterns:
            if dimension.lower() in framework_spec.lower():
                queries.append(f"{dimension} evidence")
        
        return queries
    
    def _calculate_quality_metrics_rag(self, txtai_curator, synthesis_report: str) -> Dict[str, Any]:
        """
        REQ-EU-005: Calculate evidence quality scoring framework using RAG queries.
        
        Returns:
            Dict with overall_score, strength_validation, context_preservation
        """
        # Query for evidence that appears in synthesis
        synthesis_queries = self._extract_queries_from_synthesis(synthesis_report)
        
        confidence_scores = []
        context_preserved = 0
        total_evidence_checked = 0
        
        for query in synthesis_queries[:10]:  # Limit queries for efficiency
            try:
                evidence = txtai_curator._query_evidence(query)
                if evidence:
                    total_evidence_checked += len(evidence)
                    
                    for ev in evidence:
                        # Track confidence scores
                        confidence = ev.get('confidence', 0.0)
                        confidence_scores.append(confidence)
                        
                        # Track context preservation
                        doc_name = ev.get('document_name', '')
                        if doc_name and not doc_name.startswith('unknown'):
                            context_preserved += 1
            except Exception as e:
                self.logger.debug(f"Quality query failed for '{query}': {e}")
        
        if total_evidence_checked == 0:
            return {
                'overall_score': 0.0,
                'strength_validation': 0.0,
                'context_preservation': 0.0
            }
        
        # Calculate strength validation (average confidence scores)
        strength_validation = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
        
        # Calculate context preservation
        context_preservation = context_preserved / total_evidence_checked if total_evidence_checked > 0 else 0.0
        
        # Calculate overall quality score (weighted average)
        evidence_count_factor = min(total_evidence_checked / 10.0, 1.0)  # Normalize by expected evidence count
        overall_score = (strength_validation * 0.4 + context_preservation * 0.3 + evidence_count_factor * 0.3)
        
        return {
            'overall_score': min(overall_score, 1.0),
            'strength_validation': strength_validation,
            'context_preservation': context_preservation
        }
    
    def _evidence_relevant_to_claim(self, evidence: Dict[str, Any], claim_data: Dict[str, Any]) -> bool:
        """Check if evidence is relevant to a specific claim."""
        # Simple relevance check (can be enhanced with LLM analysis)
        evidence_dimension = evidence.get('dimension', '').lower()
        claim_text = str(claim_data).lower()
        
        # Check if evidence dimension appears in claim
        if evidence_dimension in claim_text:
            return True
        
        # Check if evidence quote appears in claim
        evidence_quote = evidence.get('quote_text', '').lower()
        if evidence_quote and any(word in claim_text for word in evidence_quote.split()[:5]):
            return True
        
        return False
    
    def _generate_quality_recommendations(self, metrics: EvidenceQualityMetrics) -> List[str]:
        """Generate quality improvement recommendations based on metrics."""
        recommendations = []
        
        # Utilization recommendations
        if metrics.evidence_utilization_rate < 0.7:
            recommendations.append("Increase evidence utilization rate (currently {:.1%}) to >70%".format(metrics.evidence_utilization_rate))
        
        # Coverage recommendations
        if metrics.interpretive_claim_coverage < 0.8:
            recommendations.append("Improve interpretive claim coverage (currently {:.1%}) to >80%".format(metrics.interpretive_claim_coverage))
        
        # Alignment recommendations
        if metrics.evidence_claim_alignment_score < 0.8:
            recommendations.append("Enhance evidence-claim alignment (currently {:.1%}) to >80%".format(metrics.evidence_claim_alignment_score))
        
        # Quality recommendations
        if metrics.overall_quality_score < 0.8:
            recommendations.append("Improve overall evidence quality score (currently {:.1%}) to >80%".format(metrics.overall_quality_score))
        
        # Diversity recommendations
        if metrics.evidence_diversity_score < 0.6:
            recommendations.append("Increase evidence diversity (currently {:.1%}) to >60%".format(metrics.evidence_diversity_score))
        
        return recommendations
