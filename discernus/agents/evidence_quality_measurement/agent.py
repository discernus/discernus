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
    available_evidence_data: bytes  # Full evidence pool
    used_evidence_data: bytes  # Evidence actually used in synthesis
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
        Main entry point for comprehensive evidence quality measurement.
        
        Implements Epic #354 requirements:
        - REQ-EU-001: Evidence utilization rate measurement
        - REQ-EU-002: Interpretive claim coverage tracking
        - REQ-EU-003: Evidence-claim alignment scoring
        - REQ-EU-004: Evidence relevance ranking
        - REQ-EU-005: Evidence quality scoring framework
        """
        try:
            # Parse evidence data
            available_evidence = self._parse_evidence_data(request.available_evidence_data)
            used_evidence = self._parse_evidence_data(request.used_evidence_data)
            
            # Calculate utilization metrics (REQ-EU-001)
            utilization_metrics = self._calculate_utilization_metrics(available_evidence, used_evidence)
            
            # Calculate coverage metrics (REQ-EU-002)
            coverage_metrics = self._calculate_coverage_metrics(request.statistical_results, used_evidence)
            
            # Calculate alignment metrics (REQ-EU-003)
            alignment_metrics = self._calculate_alignment_metrics(request.synthesis_report, used_evidence)
            
            # Calculate relevance metrics (REQ-EU-004)
            relevance_metrics = self._calculate_relevance_metrics(used_evidence, request.framework_spec)
            
            # Calculate quality metrics (REQ-EU-005)
            quality_metrics = self._calculate_quality_metrics(used_evidence, request.synthesis_report)
            
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
    
    def _parse_evidence_data(self, evidence_data: bytes) -> List[Dict[str, Any]]:
        """Parse evidence data from bytes to structured format."""
        try:
            evidence_json = json.loads(evidence_data.decode('utf-8'))
            return evidence_json.get('evidence_data', [])
        except Exception as e:
            self.logger.error(f"Failed to parse evidence data: {e}")
            return []
    
    def _calculate_utilization_metrics(self, available_evidence: List[Dict], used_evidence: List[Dict]) -> Dict[str, Any]:
        """
        REQ-EU-001: Calculate evidence utilization rate and breakdowns.
        
        Returns:
            Dict with utilization_rate, total_available, total_used, unique_used,
            by_dimension, by_document
        """
        total_available = len(available_evidence)
        total_used = len(used_evidence)
        
        # Calculate unique evidence used (deduplicate by quote text)
        unique_quotes = set()
        for evidence in used_evidence:
            quote = evidence.get('quote_text', '')
            if quote:
                unique_quotes.add(quote)
        unique_used = len(unique_quotes)
        
        # Calculate utilization rate
        utilization_rate = unique_used / total_available if total_available > 0 else 0.0
        
        # Calculate breakdowns by dimension
        by_dimension = {}
        for evidence in used_evidence:
            dimension = evidence.get('dimension', 'unknown')
            by_dimension[dimension] = by_dimension.get(dimension, 0) + 1
        
        # Calculate breakdowns by document
        by_document = {}
        for evidence in used_evidence:
            document = evidence.get('document_name', 'unknown')
            by_document[document] = by_document.get(document, 0) + 1
        
        return {
            'utilization_rate': utilization_rate,
            'total_available': total_available,
            'total_used': total_used,
            'unique_used': unique_used,
            'by_dimension': by_dimension,
            'by_document': by_document
        }
    
    def _calculate_coverage_metrics(self, statistical_results: Dict[str, Any], used_evidence: List[Dict]) -> Dict[str, Any]:
        """
        REQ-EU-002: Calculate interpretive claim coverage.
        
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
                    
                    # Map evidence to this claim
                    claim_evidence = []
                    for evidence in used_evidence:
                        # Simple relevance check (can be enhanced with LLM)
                        if self._evidence_relevant_to_claim(evidence, result_data):
                            claim_evidence.append(evidence.get('quote_text', ''))
                    
                    claim_mapping[result_key] = claim_evidence
        
        total_claims = len(interpretive_claims)
        claims_with_evidence = len([c for c in claim_mapping.values() if c])
        claim_coverage = claims_with_evidence / total_claims if total_claims > 0 else 0.0
        
        return {
            'claim_coverage': claim_coverage,
            'total_claims': total_claims,
            'claims_with_evidence': claims_with_evidence,
            'claim_mapping': claim_mapping
        }
    
    def _calculate_alignment_metrics(self, synthesis_report: str, used_evidence: List[Dict]) -> Dict[str, Any]:
        """
        REQ-EU-003: Calculate evidence-claim alignment scoring.
        
        Returns:
            Dict with alignment_score, avg_relevance, diversity_score
        """
        # Calculate alignment by checking if evidence appears in synthesis
        evidence_in_synthesis = 0
        relevance_scores = []
        
        for evidence in used_evidence:
            quote = evidence.get('quote_text', '')
            if quote and quote in synthesis_report:
                evidence_in_synthesis += 1
                relevance_scores.append(1.0)  # Perfect alignment
            elif quote:
                # Partial alignment (quote might be paraphrased)
                relevance_scores.append(0.5)
            else:
                relevance_scores.append(0.0)
        
        alignment_score = evidence_in_synthesis / len(used_evidence) if used_evidence else 0.0
        avg_relevance = sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0.0
        
        # Calculate diversity (unique documents / total evidence)
        unique_documents = set()
        for evidence in used_evidence:
            doc = evidence.get('document_name', '')
            if doc:
                unique_documents.add(doc)
        
        diversity_score = len(unique_documents) / len(used_evidence) if used_evidence else 0.0
        
        return {
            'alignment_score': alignment_score,
            'avg_relevance': avg_relevance,
            'diversity_score': diversity_score
        }
    
    def _calculate_relevance_metrics(self, used_evidence: List[Dict], framework_spec: str) -> Dict[str, Any]:
        """
        REQ-EU-004: Calculate evidence relevance ranking.
        
        Returns:
            Dict with relevance_scores
        """
        relevance_scores = {}
        
        for evidence in used_evidence:
            quote = evidence.get('quote_text', '')
            dimension = evidence.get('dimension', '')
            confidence = evidence.get('confidence', 0.0)
            
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
            doc_name = evidence.get('document_name', '')
            if doc_name and not doc_name.startswith('unknown'):
                relevance_score += 0.1
            
            relevance_scores[quote[:50] + "..."] = min(relevance_score, 1.0)
        
        return {
            'relevance_scores': relevance_scores
        }
    
    def _calculate_quality_metrics(self, used_evidence: List[Dict], synthesis_report: str) -> Dict[str, Any]:
        """
        REQ-EU-005: Calculate evidence quality scoring framework.
        
        Returns:
            Dict with overall_score, strength_validation, context_preservation
        """
        if not used_evidence:
            return {
                'overall_score': 0.0,
                'strength_validation': 0.0,
                'context_preservation': 0.0
            }
        
        # Calculate strength validation (average confidence scores)
        confidence_scores = [e.get('confidence', 0.0) for e in used_evidence]
        strength_validation = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
        
        # Calculate context preservation (evidence with document names)
        context_preserved = 0
        for evidence in used_evidence:
            doc_name = evidence.get('document_name', '')
            if doc_name and not doc_name.startswith('unknown'):
                context_preserved += 1
        
        context_preservation = context_preserved / len(used_evidence) if used_evidence else 0.0
        
        # Calculate overall quality score (weighted average)
        overall_score = (strength_validation * 0.4 + context_preservation * 0.3 + 
                        (len(used_evidence) / 10.0) * 0.3)  # Normalize by expected evidence count
        
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
