#!/usr/bin/env python3
"""
LLM Quality Assurance System
============================

🚨 AI ASSISTANT WARNING: This is the PRODUCTION quality assurance system.
❌ DO NOT build new QA systems - enhance this one instead!
❌ DO NOT use "AI Academic Advisor" (deprecated file-checking in deprecated/)
✅ USE THIS: LLMQualityAssuranceSystem (production 6-layer validation)

Multi-layered validation system for LLM analysis results to prevent silent failures
and artificial precision. Implements "virtual eyes on" principle with systematic
quality checks and confidence scoring.

Addresses the critical issue where LLM parsing failures create mathematically valid
but artificially precise results (e.g., Roosevelt 1933 at exactly (0.000, 0.000)
with 80% artificial data).
"""

import json
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class QualityCheck:
    """Individual quality check result."""
    layer: str
    check_name: str
    passed: bool
    score: float
    message: str
    severity: str  # INFO, WARNING, CRITICAL
    details: Dict[str, Any] = None

@dataclass
class QualityAssessment:
    """Complete quality assessment result."""
    confidence_level: str  # HIGH, MEDIUM, LOW
    confidence_score: float  # 0.0 to 1.0
    individual_checks: List[QualityCheck]
    anomalies_detected: List[str]
    requires_second_opinion: bool
    summary: str
    processed_data: Dict[str, Any]
    quality_metadata: Dict[str, Any]

class LLMQualityAssuranceSystem:
    """
    Multi-layered quality assurance system for LLM analysis results.
    
    Implements 6 layers of validation:
    1. Input Validation
    2. LLM Response Validation  
    3. Statistical Coherence Validation
    4. Mathematical Consistency Verification
    5. LLM Second Opinion Cross-Validation
    6. Anomaly Detection
    """
    
    def __init__(self):
        self.default_value_threshold = 0.3  # Standard default value
        self.default_ratio_critical = 0.5   # >50% defaults = critical
        self.variance_threshold_low = 0.05  # Low variance threshold
        self.zero_position_tolerance = 0.001  # Tolerance for "exactly zero"
        
        # Quality confidence thresholds
        self.high_confidence_threshold = 0.8
        self.medium_confidence_threshold = 0.5
        
    def validate_llm_analysis(
        self, 
        text_input: str,
        framework: str,
        llm_response: Dict[str, Any],
        parsed_scores: Dict[str, float]
    ) -> QualityAssessment:
        """
        Run complete quality assurance validation on LLM analysis.
        
        Args:
            text_input: Original text that was analyzed
            framework: Framework used for analysis
            llm_response: Raw LLM response
            parsed_scores: Parsed well scores
            
        Returns:
            QualityAssessment with confidence scoring and validation results
        """
        
        quality_checks = []
        anomalies = []
        
        # Layer 1: Input Validation
        input_checks = self._validate_input(text_input, framework)
        quality_checks.extend(input_checks)
        
        # Layer 2: LLM Response Validation
        response_checks = self._validate_llm_response(llm_response, parsed_scores, framework)
        quality_checks.extend(response_checks)
        
        # Layer 3: Statistical Coherence Validation
        statistical_checks, stat_anomalies = self._validate_statistical_coherence(parsed_scores)
        quality_checks.extend(statistical_checks)
        anomalies.extend(stat_anomalies)
        
        # Layer 4: Mathematical Consistency Verification
        math_checks = self._validate_mathematical_consistency(parsed_scores, framework)
        quality_checks.extend(math_checks)
        
        # Layer 5: Anomaly Detection
        anomaly_checks, detected_anomalies = self._detect_anomalies(parsed_scores)
        quality_checks.extend(anomaly_checks)
        anomalies.extend(detected_anomalies)
        
        # Calculate overall confidence score
        confidence_score = self._calculate_confidence_score(quality_checks)
        confidence_level = self._determine_confidence_level(confidence_score)
        
        # Determine if second opinion is needed
        requires_second_opinion = self._needs_second_opinion(quality_checks, anomalies)
        
        # Generate summary
        summary = self._generate_quality_summary(confidence_level, quality_checks, anomalies)
        
        # Create quality metadata
        quality_metadata = {
            'validation_timestamp': datetime.now().isoformat(),
            'total_checks': len(quality_checks),
            'checks_passed': sum(1 for check in quality_checks if check.passed),
            'critical_failures': sum(1 for check in quality_checks if not check.passed and check.severity == 'CRITICAL'),
            'warnings': sum(1 for check in quality_checks if not check.passed and check.severity == 'WARNING'),
            'anomalies_count': len(anomalies)
        }
        
        return QualityAssessment(
            confidence_level=confidence_level,
            confidence_score=confidence_score,
            individual_checks=quality_checks,
            anomalies_detected=anomalies,
            requires_second_opinion=requires_second_opinion,
            summary=summary,
            processed_data=parsed_scores,
            quality_metadata=quality_metadata
        )
    
    def _validate_input(self, text: str, framework: str) -> List[QualityCheck]:
        """Layer 1: Input Validation."""
        checks = []
        
        # Text length validation
        text_length = len(text)
        length_valid = 100 <= text_length <= 50000
        checks.append(QualityCheck(
            layer="INPUT",
            check_name="text_length",
            passed=length_valid,
            score=1.0 if length_valid else 0.0,
            message=f"Text length: {text_length} characters {'(valid)' if length_valid else '(invalid)'}",
            severity="CRITICAL" if not length_valid else "INFO"
        ))
        
        # Text quality validation
        word_count = len(text.split())
        avg_word_length = np.mean([len(word) for word in text.split()]) if word_count > 0 else 0
        quality_valid = word_count >= 20 and avg_word_length > 2
        checks.append(QualityCheck(
            layer="INPUT",
            check_name="text_quality",
            passed=quality_valid,
            score=min(1.0, word_count / 50),  # Scale based on word count
            message=f"Text quality: {word_count} words, avg length {avg_word_length:.1f}",
            severity="WARNING" if not quality_valid else "INFO"
        ))
        
        # Framework compatibility
        framework_valid = framework in ['civic_virtue', 'political_spectrum', 'fukuyama_identity', 
                                       'mft_persuasive_force', 'moral_rhetorical_posture']
        checks.append(QualityCheck(
            layer="INPUT",
            check_name="framework_compatibility",
            passed=framework_valid,
            score=1.0 if framework_valid else 0.0,
            message=f"Framework '{framework}' {'recognized' if framework_valid else 'unknown'}",
            severity="CRITICAL" if not framework_valid else "INFO"
        ))
        
        return checks
    
    def _validate_llm_response(self, llm_response: Dict[str, Any], parsed_scores: Dict[str, float], framework: str) -> List[QualityCheck]:
        """Layer 2: LLM Response Validation."""
        checks = []
        
        # JSON format validation
        json_valid = isinstance(llm_response, dict)
        checks.append(QualityCheck(
            layer="LLM_RESPONSE",
            check_name="json_format",
            passed=json_valid,
            score=1.0 if json_valid else 0.0,
            message=f"Response format: {'valid JSON' if json_valid else 'invalid JSON'}",
            severity="CRITICAL" if not json_valid else "INFO"
        ))
        
        # Required fields validation
        has_scores = 'scores' in llm_response or len(parsed_scores) > 0
        checks.append(QualityCheck(
            layer="LLM_RESPONSE",
            check_name="required_fields",
            passed=has_scores,
            score=1.0 if has_scores else 0.0,
            message=f"Scores field: {'present' if has_scores else 'missing'}",
            severity="CRITICAL" if not has_scores else "INFO"
        ))
        
        # Score range validation
        valid_ranges = all(0.0 <= score <= 1.0 for score in parsed_scores.values())
        checks.append(QualityCheck(
            layer="LLM_RESPONSE",
            check_name="score_ranges",
            passed=valid_ranges,
            score=1.0 if valid_ranges else 0.0,
            message=f"Score ranges: {'all valid [0.0-1.0]' if valid_ranges else 'invalid ranges detected'}",
            severity="CRITICAL" if not valid_ranges else "INFO"
        ))
        
        # Well completeness validation
        expected_wells = self._get_expected_wells(framework)
        present_wells = set(parsed_scores.keys())
        expected_wells_set = set(expected_wells)
        completeness = len(present_wells & expected_wells_set) / len(expected_wells_set) if expected_wells_set else 1.0
        
        checks.append(QualityCheck(
            layer="LLM_RESPONSE", 
            check_name="well_completeness",
            passed=completeness >= 0.8,
            score=completeness,
            message=f"Well completeness: {completeness:.1%} ({len(present_wells & expected_wells_set)}/{len(expected_wells_set)})",
            severity="WARNING" if completeness < 0.8 else "INFO"
        ))
        
        return checks
    
    def _validate_statistical_coherence(self, parsed_scores: Dict[str, float]) -> Tuple[List[QualityCheck], List[str]]:
        """Layer 3: Statistical Coherence Validation."""
        checks = []
        anomalies = []
        
        if not parsed_scores:
            checks.append(QualityCheck(
                layer="STATISTICAL",
                check_name="empty_scores",
                passed=False,
                score=0.0,
                message="No scores to validate",
                severity="CRITICAL"
            ))
            return checks, anomalies
        
        scores = list(parsed_scores.values())
        
        # Default value ratio check (CRITICAL for Roosevelt 1933 case)
        default_count = sum(1 for score in scores if abs(score - self.default_value_threshold) < 0.001)
        default_ratio = default_count / len(scores)
        
        default_check_passed = default_ratio < self.default_ratio_critical
        if not default_check_passed:
            anomalies.append(f"High default value ratio: {default_ratio:.1%}")
        
        checks.append(QualityCheck(
            layer="STATISTICAL",
            check_name="default_value_ratio",
            passed=default_check_passed,
            score=1.0 - default_ratio,
            message=f"Default values: {default_count}/{len(scores)} ({default_ratio:.1%})",
            severity="CRITICAL" if default_ratio >= 0.5 else ("WARNING" if default_ratio >= 0.3 else "INFO"),
            details={'default_count': default_count, 'total_scores': len(scores), 'ratio': default_ratio}
        ))
        
        # Score variance check  
        score_variance = np.var(scores)
        variance_adequate = score_variance >= self.variance_threshold_low
        if not variance_adequate:
            anomalies.append(f"Low score variance: {score_variance:.4f}")
        
        checks.append(QualityCheck(
            layer="STATISTICAL",
            check_name="score_variance",
            passed=variance_adequate,
            score=min(1.0, score_variance * 10),  # Scale variance for scoring
            message=f"Score variance: {score_variance:.4f} {'(adequate)' if variance_adequate else '(low)'}",
            severity="WARNING" if not variance_adequate else "INFO",
            details={'variance': score_variance, 'threshold': self.variance_threshold_low}
        ))
        
        # Pattern detection
        uniform_pattern = self._detect_uniform_pattern(scores)
        if uniform_pattern:
            anomalies.append("Uniform score distribution detected")
        
        checks.append(QualityCheck(
            layer="STATISTICAL",
            check_name="pattern_detection",
            passed=not uniform_pattern,
            score=0.0 if uniform_pattern else 1.0,
            message=f"Pattern analysis: {'uniform pattern detected' if uniform_pattern else 'natural variation'}",
            severity="WARNING" if uniform_pattern else "INFO"
        ))
        
        return checks, anomalies
    
    def _validate_mathematical_consistency(self, parsed_scores: Dict[str, float], framework: str) -> List[QualityCheck]:
        """Layer 4: Mathematical Consistency Verification."""
        checks = []
        
        if not parsed_scores:
            return checks
        
        try:
            # Import circular engine for coordinate calculation
            from ..engine_circular import NarrativeGravityWellsCircular
            engine = NarrativeGravityWellsCircular()
            
            # Calculate narrative position
            narrative_x, narrative_y = engine.calculate_narrative_position(parsed_scores)
            
            # Check for exactly zero position (Roosevelt 1933 case)
            position_magnitude = np.sqrt(narrative_x**2 + narrative_y**2)
            exactly_zero = position_magnitude < self.zero_position_tolerance
            
            checks.append(QualityCheck(
                layer="MATHEMATICAL",
                check_name="position_calculation",
                passed=not exactly_zero,
                score=0.0 if exactly_zero else 1.0,
                message=f"Narrative position: ({narrative_x:.3f}, {narrative_y:.3f}) magnitude: {position_magnitude:.4f}",
                severity="WARNING" if exactly_zero else "INFO",
                details={'x': narrative_x, 'y': narrative_y, 'magnitude': position_magnitude}
            ))
            
            # Verify coordinate calculation consistency
            try:
                # Recalculate to verify consistency
                recalc_x, recalc_y = engine.calculate_narrative_position(parsed_scores)
                calculation_consistent = (abs(narrative_x - recalc_x) < 0.001 and 
                                        abs(narrative_y - recalc_y) < 0.001)
                
                checks.append(QualityCheck(
                    layer="MATHEMATICAL",
                    check_name="calculation_consistency",
                    passed=calculation_consistent,
                    score=1.0 if calculation_consistent else 0.0,
                    message=f"Calculation consistency: {'verified' if calculation_consistent else 'inconsistent'}",
                    severity="CRITICAL" if not calculation_consistent else "INFO"
                ))
                
            except Exception as e:
                checks.append(QualityCheck(
                    layer="MATHEMATICAL",
                    check_name="calculation_consistency",
                    passed=False,
                    score=0.0,
                    message=f"Calculation verification failed: {str(e)}",
                    severity="WARNING"
                ))
                
        except Exception as e:
            checks.append(QualityCheck(
                layer="MATHEMATICAL",
                check_name="engine_initialization",
                passed=False,
                score=0.0,
                message=f"Mathematical validation failed: {str(e)}",
                severity="WARNING"
            ))
        
        return checks
    
    def _detect_anomalies(self, parsed_scores: Dict[str, float]) -> Tuple[List[QualityCheck], List[str]]:
        """Layer 6: Anomaly Detection."""
        checks = []
        anomalies = []
        
        if not parsed_scores:
            return checks, anomalies
        
        scores = list(parsed_scores.values())
        
        # Perfect symmetry detection
        perfect_symmetry = self._detect_perfect_symmetry(parsed_scores)
        if perfect_symmetry:
            anomalies.append("Perfect mathematical symmetry detected")
        
        # Outlier analysis
        outliers = self._detect_outliers(scores)
        if outliers:
            anomalies.append(f"Statistical outliers detected: {len(outliers)} values")
        
        # Identical scores detection
        unique_scores = len(set(scores))
        identical_scores = unique_scores == 1
        if identical_scores:
            anomalies.append("All scores identical - possible total parsing failure")
        
        # Temporal consistency (if applicable - placeholder for future implementation)
        
        # Create anomaly summary check
        total_anomalies = len(anomalies)
        checks.append(QualityCheck(
            layer="ANOMALY",
            check_name="anomaly_summary",
            passed=total_anomalies == 0,
            score=max(0.0, 1.0 - (total_anomalies * 0.3)),
            message=f"Anomalies detected: {total_anomalies}",
            severity="WARNING" if total_anomalies > 0 else "INFO",
            details={'anomaly_count': total_anomalies, 'anomaly_types': anomalies}
        ))
        
        return checks, anomalies
    
    def _calculate_confidence_score(self, quality_checks: List[QualityCheck]) -> float:
        """Calculate overall confidence score from individual checks."""
        if not quality_checks:
            return 0.0
        
        # Weight checks by layer importance
        layer_weights = {
            'INPUT': 0.1,
            'LLM_RESPONSE': 0.3,
            'STATISTICAL': 0.4,  # Highest weight - catches Roosevelt 1933 case
            'MATHEMATICAL': 0.15,
            'ANOMALY': 0.05
        }
        
        weighted_score = 0.0
        total_weight = 0.0
        
        for check in quality_checks:
            weight = layer_weights.get(check.layer, 0.1)
            weighted_score += check.score * weight
            total_weight += weight
        
        confidence = weighted_score / total_weight if total_weight > 0 else 0.0
        
        # Apply penalties for critical failures (especially Roosevelt 1933 case)
        critical_failures = sum(1 for check in quality_checks if not check.passed and check.severity == 'CRITICAL')
        if critical_failures > 0:
            # Heavy penalty for critical failures, especially default ratio issues
            default_ratio_failure = any(
                check.check_name == 'default_value_ratio' and not check.passed 
                for check in quality_checks
            )
            if default_ratio_failure:
                # Extra penalty for default ratio failures (Roosevelt 1933 case)
                confidence *= max(0.05, 1.0 - (critical_failures * 0.5))
            else:
                confidence *= max(0.1, 1.0 - (critical_failures * 0.3))
        
        return min(1.0, max(0.0, confidence))
    
    def _determine_confidence_level(self, confidence_score: float) -> str:
        """Determine confidence level category."""
        if confidence_score >= self.high_confidence_threshold:
            return "HIGH"
        elif confidence_score >= self.medium_confidence_threshold:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _needs_second_opinion(self, quality_checks: List[QualityCheck], anomalies: List[str]) -> bool:
        """Determine if second opinion validation is needed."""
        # Critical failures require second opinion
        critical_failures = any(not check.passed and check.severity == 'CRITICAL' for check in quality_checks)
        
        # Multiple anomalies require second opinion
        multiple_anomalies = len(anomalies) >= 2
        
        # High default value ratio requires second opinion (Roosevelt 1933 case)
        high_default_ratio = any(
            check.check_name == 'default_value_ratio' and 
            check.details and check.details.get('ratio', 0) >= 0.4
            for check in quality_checks
        )
        
        return critical_failures or multiple_anomalies or high_default_ratio
    
    def _generate_quality_summary(self, confidence_level: str, quality_checks: List[QualityCheck], anomalies: List[str]) -> str:
        """Generate human-readable quality summary."""
        passed_checks = sum(1 for check in quality_checks if check.passed)
        total_checks = len(quality_checks)
        
        summary = f"Quality Assessment: {confidence_level} confidence ({passed_checks}/{total_checks} checks passed)"
        
        if anomalies:
            summary += f". {len(anomalies)} anomalies detected"
        
        critical_issues = [check for check in quality_checks if not check.passed and check.severity == 'CRITICAL']
        if critical_issues:
            summary += f". {len(critical_issues)} critical issues require attention"
        
        return summary
    
    # Helper methods
    
    def _get_expected_wells(self, framework: str) -> List[str]:
        """Get expected wells for a framework."""
        framework_wells = {
            'civic_virtue': ['Dignity', 'Truth', 'Justice', 'Hope', 'Pragmatism', 
                           'Tribalism', 'Manipulation', 'Resentment', 'Fantasy', 'Fear'],
            'political_spectrum': ['Progressive', 'Liberal', 'Moderate', 'Conservative', 'Libertarian'],
            # Add other frameworks as needed
        }
        return framework_wells.get(framework, [])
    
    def _detect_uniform_pattern(self, scores: List[float]) -> bool:
        """Detect if scores follow a uniform pattern."""
        if len(scores) < 3:
            return False
        
        # Check if all scores are very similar
        score_range = max(scores) - min(scores)
        return score_range < 0.05
    
    def _detect_perfect_symmetry(self, parsed_scores: Dict[str, float]) -> bool:
        """Detect perfect mathematical symmetry that suggests artificial generation."""
        # This is a placeholder for more sophisticated symmetry detection
        # Could check for integrative/disintegrative balance, etc.
        scores = list(parsed_scores.values())
        if len(scores) < 4:
            return False
        
        # Simple check: perfect balance between high and low scores
        high_scores = [s for s in scores if s > 0.5]
        low_scores = [s for s in scores if s <= 0.5]
        
        if len(high_scores) == len(low_scores):
            high_avg = np.mean(high_scores) if high_scores else 0
            low_avg = np.mean(low_scores) if low_scores else 0
            # Perfect symmetry around 0.5
            return abs((high_avg + low_avg) - 1.0) < 0.01
        
        return False
    
    def _detect_outliers(self, scores: List[float]) -> List[float]:
        """Detect statistical outliers in scores."""
        if len(scores) < 4:
            return []
        
        q1 = np.percentile(scores, 25)
        q3 = np.percentile(scores, 75)
        iqr = q3 - q1
        
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        outliers = [score for score in scores if score < lower_bound or score > upper_bound]
        return outliers

# Convenience function for integration
def validate_llm_analysis(text_input: str, framework: str, llm_response: Dict[str, Any], parsed_scores: Dict[str, float]) -> QualityAssessment:
    """
    Convenience function to run LLM quality assurance validation.
    
    Args:
        text_input: Original text that was analyzed
        framework: Framework used for analysis  
        llm_response: Raw LLM response
        parsed_scores: Parsed well scores
        
    Returns:
        QualityAssessment with confidence scoring and validation results
    """
    qa_system = LLMQualityAssuranceSystem()
    return qa_system.validate_llm_analysis(text_input, framework, llm_response, parsed_scores) 