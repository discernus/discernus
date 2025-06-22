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

Enhanced with experiment-specific QA that validates against research goals and hypotheses.

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

from ..framework_utils import get_framework_yaml_path

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
    experiment_specific_issues: List[str] = None  # NEW: Experiment-specific problems

@dataclass
class ExperimentContext:
    """Experiment context for hypothesis-aware validation."""
    name: str
    description: str
    version: str
    hypotheses: List[str]
    success_criteria: List[str]
    research_context: str
    expected_outcomes: Dict[str, Any] = None
    framework_requirements: Dict[str, Any] = None
    corpus_requirements: Dict[str, Any] = None
    statistical_requirements: Dict[str, Any] = None
    tags: List[str] = None

class ExperimentSpecificQualityAssurance:
    """
    Layer 2: Experiment-Specific Quality Assurance
    
    Validates analysis results against researcher-defined goals, hypotheses,
    and success criteria. Generates dynamic QA checks based on experiment definition.
    """
    
    def __init__(self):
        self.hypothesis_patterns = {
            'discriminative_validity': [
                'distinguish', 'discriminate', 'differentiate', 'separate',
                'conservative vs progressive', 'dignity vs tribalism'
            ],
            'ideological_detection': [
                'conservative', 'progressive', 'liberal', 'political',
                'ideology', 'ideological', 'partisan'
            ],
            'moral_foundations': [
                'moral', 'foundation', 'care', 'harm', 'fairness', 'loyalty',
                'authority', 'sanctity', 'liberty', 'moral foundations theory'
            ],
            'narrative_positioning': [
                'position', 'coordinate', 'locate', 'map', 'space',
                'narrative gravity', 'circular', 'elliptical'
            ]
        }
    
    def validate_experiment_alignment(
        self, 
        analysis_results: List[Dict[str, Any]],
        experiment_context: ExperimentContext,
        framework_id: str
    ) -> List[QualityCheck]:
        """
        Validate analysis results against experiment-specific requirements.
        
        Args:
            analysis_results: List of individual analysis results
            experiment_context: Experiment definition and goals
            framework_id: Framework being used for analysis
            
        Returns:
            List of experiment-specific quality checks
        """
        
        experiment_checks = []
        
        # Hypothesis-driven validation
        hypothesis_checks = self._validate_hypotheses_alignment(
            analysis_results, experiment_context.hypotheses, framework_id
        )
        experiment_checks.extend(hypothesis_checks)
        
        # Success criteria validation
        success_checks = self._validate_success_criteria(
            analysis_results, experiment_context.success_criteria
        )
        experiment_checks.extend(success_checks)
        
        # Research question alignment
        research_checks = self._validate_research_alignment(
            analysis_results, experiment_context.research_context, framework_id
        )
        experiment_checks.extend(research_checks)
        
        # Framework-corpus fit validation
        framework_checks = self._validate_framework_corpus_fit(
            analysis_results, experiment_context, framework_id
        )
        experiment_checks.extend(framework_checks)
        
        # Statistical power validation
        power_checks = self._validate_statistical_requirements(
            analysis_results, experiment_context
        )
        experiment_checks.extend(power_checks)
        
        return experiment_checks
    
    def _validate_hypotheses_alignment(
        self, 
        results: List[Dict[str, Any]], 
        hypotheses: List[str], 
        framework_id: str
    ) -> List[QualityCheck]:
        """Validate that results can meaningfully test stated hypotheses."""
        checks = []
        
        if not hypotheses:
            return checks
        
        # Extract analysis data for validation
        all_scores = []
        positions = []
        for result in results:
            if result.get('raw_scores'):
                all_scores.append(result['raw_scores'])
            if 'narrative_position' in result:
                pos = result['narrative_position']
                if isinstance(pos, dict) and 'x' in pos and 'y' in pos:
                    positions.append((pos['x'], pos['y']))
        
        for i, hypothesis in enumerate(hypotheses, 1):
            hypothesis_lower = hypothesis.lower()
            
            # Check for discriminative validity hypotheses
            if any(pattern in hypothesis_lower for pattern in self.hypothesis_patterns['discriminative_validity']):
                # Validate that we have sufficient variance to discriminate
                if all_scores:
                    all_values = []
                    for scores in all_scores:
                        all_values.extend(scores.values())
                    
                    variance = np.var(all_values) if all_values else 0.0
                    discriminative_power = variance > 0.05  # Minimum variance for discrimination
                    
                    checks.append(QualityCheck(
                        layer="EXPERIMENT_SPECIFIC",
                        check_name=f"hypothesis_{i}_discriminative_validity",
                        passed=discriminative_power,
                        score=min(1.0, variance * 10),
                        message=f"H{i} discriminative validity: variance={variance:.4f} {'(sufficient)' if discriminative_power else '(insufficient)'}",
                        severity="CRITICAL" if not discriminative_power else "INFO",
                        details={
                            'hypothesis': hypothesis,
                            'variance': variance,
                            'threshold': 0.05,
                            'can_discriminate': discriminative_power
                        }
                    ))
            
            # Check for ideological detection hypotheses
            if any(pattern in hypothesis_lower for pattern in self.hypothesis_patterns['ideological_detection']):
                # Validate framework supports ideological analysis
                ideological_framework = framework_id in ['civic_virtue', 'political_spectrum', 'moral_foundations_theory']
                
                checks.append(QualityCheck(
                    layer="EXPERIMENT_SPECIFIC",
                    check_name=f"hypothesis_{i}_ideological_framework",
                    passed=ideological_framework,
                    score=1.0 if ideological_framework else 0.0,
                    message=f"H{i} ideological framework: {framework_id} {'supports' if ideological_framework else 'may not support'} ideological analysis",
                    severity="WARNING" if not ideological_framework else "INFO",
                    details={
                        'hypothesis': hypothesis,
                        'framework': framework_id,
                        'supports_ideology': ideological_framework
                    }
                ))
            
            # Check for positioning hypotheses
            if any(pattern in hypothesis_lower for pattern in self.hypothesis_patterns['narrative_positioning']):
                # Validate we have meaningful positioning data
                meaningful_positions = len([pos for pos in positions if pos != (0.0, 0.0)]) if positions else 0
                position_quality = meaningful_positions / len(results) if results else 0.0
                
                checks.append(QualityCheck(
                    layer="EXPERIMENT_SPECIFIC",
                    check_name=f"hypothesis_{i}_positioning_quality",
                    passed=position_quality > 0.5,
                    score=position_quality,
                    message=f"H{i} positioning quality: {meaningful_positions}/{len(results)} non-zero positions ({position_quality:.1%})",
                    severity="CRITICAL" if position_quality <= 0.5 else "INFO",
                    details={
                        'hypothesis': hypothesis,
                        'meaningful_positions': meaningful_positions,
                        'total_analyses': len(results),
                        'position_quality': position_quality
                    }
                ))
        
        return checks
    
    def _validate_success_criteria(
        self, 
        results: List[Dict[str, Any]], 
        success_criteria: List[str]
    ) -> List[QualityCheck]:
        """Validate that results meet stated success criteria."""
        checks = []
        
        if not success_criteria:
            return checks
        
        for i, criterion in enumerate(success_criteria, 1):
            criterion_lower = criterion.lower()
            
            # Sample size requirements
            if 'n>' in criterion_lower or 'n >' in criterion_lower or 'sample' in criterion_lower:
                # Extract required sample size
                import re
                size_match = re.search(r'n\s*>\s*(\d+)', criterion_lower)
                if size_match:
                    required_n = int(size_match.group(1))
                    actual_n = len(results)
                    
                    checks.append(QualityCheck(
                        layer="EXPERIMENT_SPECIFIC",
                        check_name=f"success_criterion_{i}_sample_size",
                        passed=actual_n > required_n,
                        score=min(1.0, actual_n / required_n) if required_n > 0 else 1.0,
                        message=f"Sample size: {actual_n} {'>' if actual_n > required_n else '<='} {required_n} (required)",
                        severity="CRITICAL" if actual_n <= required_n else "INFO",
                        details={
                            'criterion': criterion,
                            'required_n': required_n,
                            'actual_n': actual_n
                        }
                    ))
            
            # Quality threshold requirements
            if 'quality' in criterion_lower or 'confidence' in criterion_lower:
                # Check if we have quality assessments
                quality_scores = []
                for result in results:
                    if 'qa_assessment' in result:
                        qa = result['qa_assessment']
                        if 'confidence_score' in qa:
                            quality_scores.append(qa['confidence_score'])
                
                if quality_scores:
                    avg_quality = np.mean(quality_scores)
                    min_quality = np.min(quality_scores)
                    
                    # Assume criterion requires high quality (>0.7 average)
                    quality_threshold = 0.7
                    meets_quality = avg_quality >= quality_threshold
                    
                    checks.append(QualityCheck(
                        layer="EXPERIMENT_SPECIFIC",
                        check_name=f"success_criterion_{i}_quality",
                        passed=meets_quality,
                        score=avg_quality,
                        message=f"Quality requirement: avg={avg_quality:.2f}, min={min_quality:.2f} ({'meets' if meets_quality else 'below'} threshold)",
                        severity="WARNING" if not meets_quality else "INFO",
                        details={
                            'criterion': criterion,
                            'average_quality': avg_quality,
                            'minimum_quality': min_quality,
                            'threshold': quality_threshold
                        }
                    ))
        
        return checks
    
    def _validate_research_alignment(
        self, 
        results: List[Dict[str, Any]], 
        research_context: str, 
        framework_id: str
    ) -> List[QualityCheck]:
        """Validate analysis aligns with research context and questions."""
        checks = []
        
        if not research_context:
            return checks
        
        context_lower = research_context.lower()
        
        # Framework-research alignment
        framework_alignment = self._assess_framework_research_fit(context_lower, framework_id)
        
        checks.append(QualityCheck(
            layer="EXPERIMENT_SPECIFIC",
            check_name="research_framework_alignment",
            passed=framework_alignment['aligned'],
            score=framework_alignment['score'],
            message=f"Framework-research alignment: {framework_id} {framework_alignment['assessment']}",
            severity="WARNING" if not framework_alignment['aligned'] else "INFO",
            details={
                'research_context': research_context,
                'framework': framework_id,
                'alignment_reasons': framework_alignment['reasons']
            }
        ))
        
        return checks
    
    def _assess_framework_research_fit(self, research_context: str, framework_id: str) -> Dict[str, Any]:
        """Assess how well the framework fits the research context."""
        
        framework_strengths = {
            'civic_virtue': ['dignity', 'tribalism', 'virtue', 'civic', 'political discourse', 'public sphere'],
            'moral_foundations_theory': ['moral', 'foundation', 'ethics', 'care', 'harm', 'fairness', 'loyalty', 'authority', 'sanctity'],
            'political_spectrum': ['conservative', 'liberal', 'progressive', 'political', 'ideology', 'partisan'],
            'fukuyama_identity': ['identity', 'recognition', 'dignity', 'social status', 'respect']
        }
        
        if framework_id not in framework_strengths:
            return {
                'aligned': False,
                'score': 0.0,
                'assessment': 'framework not recognized',
                'reasons': ['Unknown framework']
            }
        
        strengths = framework_strengths[framework_id]
        matches = [strength for strength in strengths if strength in research_context]
        
        alignment_score = len(matches) / len(strengths) if strengths else 0.0
        aligned = alignment_score > 0.2  # At least 20% keyword overlap
        
        return {
            'aligned': aligned,
            'score': alignment_score,
            'assessment': f"{'well aligned' if aligned else 'poorly aligned'} ({len(matches)}/{len(strengths)} keywords match)",
            'reasons': matches if matches else ['No keyword matches found']
        }
    
    def _validate_framework_corpus_fit(
        self, 
        results: List[Dict[str, Any]], 
        experiment_context: ExperimentContext, 
        framework_id: str
    ) -> List[QualityCheck]:
        """Validate framework is appropriate for the corpus being analyzed."""
        checks = []
        
        # Check if corpus types match framework capabilities
        if experiment_context.tags:
            political_tags = [tag for tag in experiment_context.tags if any(
                pol in tag.lower() for pol in ['conservative', 'progressive', 'liberal', 'political']
            )]
            
            if political_tags and framework_id not in ['civic_virtue', 'political_spectrum', 'moral_foundations_theory']:
                checks.append(QualityCheck(
                    layer="EXPERIMENT_SPECIFIC",
                    check_name="framework_corpus_political_fit",
                    passed=False,
                    score=0.0,
                    message=f"Political corpus tags ({political_tags}) may not align with framework {framework_id}",
                    severity="WARNING",
                    details={
                        'political_tags': political_tags,
                        'framework': framework_id,
                        'recommended_frameworks': ['civic_virtue', 'political_spectrum', 'moral_foundations_theory']
                    }
                ))
        
        return checks
    
    def _validate_statistical_requirements(
        self, 
        results: List[Dict[str, Any]], 
        experiment_context: ExperimentContext
    ) -> List[QualityCheck]:
        """Validate statistical power and requirements."""
        checks = []
        
        # Minimum sample size for statistical validity
        min_sample_for_stats = 10  # Conservative minimum
        actual_n = len(results)
        
        sufficient_n = actual_n >= min_sample_for_stats
        
        checks.append(QualityCheck(
            layer="EXPERIMENT_SPECIFIC",
            check_name="statistical_sample_size",
            passed=sufficient_n,
            score=min(1.0, actual_n / min_sample_for_stats),
            message=f"Statistical sample size: {actual_n} {'≥' if sufficient_n else '<'} {min_sample_for_stats} (minimum for statistics)",
            severity="WARNING" if not sufficient_n else "INFO",
            details={
                'actual_n': actual_n,
                'minimum_n': min_sample_for_stats,
                'sufficient_for_statistics': sufficient_n
            }
        ))
        
        # Check for sufficient successful analyses for research validity
        successful_analyses = len([r for r in results if r.get('success', False) and not r.get('qa_failed', False)])
        success_rate = successful_analyses / actual_n if actual_n > 0 else 0.0
        
        adequate_success_rate = success_rate >= 0.7  # At least 70% should pass QA
        
        checks.append(QualityCheck(
            layer="EXPERIMENT_SPECIFIC",
            check_name="research_validity_success_rate",
            passed=adequate_success_rate,
            score=success_rate,
            message=f"Research validity: {successful_analyses}/{actual_n} analyses passed QA ({success_rate:.1%})",
            severity="CRITICAL" if success_rate < 0.5 else ("WARNING" if not adequate_success_rate else "INFO"),
            details={
                'successful_analyses': successful_analyses,
                'total_analyses': actual_n,
                'success_rate': success_rate,
                'adequate_threshold': 0.7
            }
        ))
        
        return checks

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
    
    Enhanced with experiment-specific validation layer.
    """
    
    def __init__(self):
        self.default_value_threshold = 0.3  # Standard default value
        self.default_ratio_critical = 0.5   # >50% defaults = critical
        self.variance_threshold_low = 0.05  # Low variance threshold
        self.zero_position_tolerance = 0.001  # Tolerance for "exactly zero"
        
        # Quality confidence thresholds
        self.high_confidence_threshold = 0.8
        self.medium_confidence_threshold = 0.5
        
        # Initialize experiment-specific QA
        self.experiment_qa = ExperimentSpecificQualityAssurance()
        
    def validate_llm_analysis(
        self, 
        text_input: str,
        framework: str,
        llm_response: Dict[str, Any],
        parsed_scores: Dict[str, float],
        experiment_context: ExperimentContext = None
    ) -> QualityAssessment:
        """
        Run complete quality assurance validation on LLM analysis.
        
        Args:
            text_input: Original text that was analyzed
            framework: Framework used for analysis
            llm_response: Raw LLM response
            parsed_scores: Parsed well scores
            experiment_context: Experiment definition for specific validation
            
        Returns:
            QualityAssessment with confidence scoring and validation results
        """
        
        quality_checks = []
        anomalies = []
        experiment_issues = []
        
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
        
        # NEW: Layer 6: Experiment-Specific Validation
        if experiment_context:
            # Create mock analysis result for experiment validation
            analysis_result = {
                'raw_scores': parsed_scores,
                'success': True,  # Will be updated based on QA
                'qa_failed': False,
                'llm_response': llm_response
            }
            
            # Add positioning if available
            if 'narrative_position' in llm_response:
                analysis_result['narrative_position'] = llm_response['narrative_position']
            
            experiment_checks = self.experiment_qa.validate_experiment_alignment(
                [analysis_result], experiment_context, framework
            )
            quality_checks.extend(experiment_checks)
            
            # Extract experiment-specific issues
            experiment_issues = [
                check.message for check in experiment_checks 
                if not check.passed and check.severity in ['WARNING', 'CRITICAL']
            ]
        
        # Calculate overall confidence score
        confidence_score = self._calculate_confidence_score(quality_checks)
        confidence_level = self._determine_confidence_level(confidence_score)
        
        # Determine if second opinion is needed
        requires_second_opinion = self._needs_second_opinion(quality_checks, anomalies)
        
        # Generate summary
        summary = self._generate_quality_summary(confidence_level, quality_checks, anomalies, experiment_issues)
        
        # Create quality metadata
        quality_metadata = {
            'validation_timestamp': datetime.now().isoformat(),
            'total_checks': len(quality_checks),
            'checks_passed': sum(1 for check in quality_checks if check.passed),
            'critical_failures': sum(1 for check in quality_checks if not check.passed and check.severity == 'CRITICAL'),
            'warnings': sum(1 for check in quality_checks if not check.passed and check.severity == 'WARNING'),
            'anomalies_count': len(anomalies),
            'experiment_issues_count': len(experiment_issues),
            'has_experiment_context': experiment_context is not None
        }
        
        return QualityAssessment(
            confidence_level=confidence_level,
            confidence_score=confidence_score,
            individual_checks=quality_checks,
            anomalies_detected=anomalies,
            requires_second_opinion=requires_second_opinion,
            summary=summary,
            processed_data=parsed_scores,
            quality_metadata=quality_metadata,
            experiment_specific_issues=experiment_issues
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
            from ..coordinate_engine import DiscernusCoordinateEngine
            
            # Try to find framework YAML path for framework-aware calculation
            framework_path = self._get_framework_yaml_path(framework)
            if framework_path:
                engine = DiscernusCoordinateEngine(framework_path=framework_path)
            else:
                engine = DiscernusCoordinateEngine()  # Fallback to default
            
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
    
    def _generate_quality_summary(self, confidence_level: str, quality_checks: List[QualityCheck], anomalies: List[str], experiment_issues: List[str]) -> str:
        """Generate human-readable quality summary."""
        passed_checks = sum(1 for check in quality_checks if check.passed)
        total_checks = len(quality_checks)
        
        summary = f"Quality Assessment: {confidence_level} confidence ({passed_checks}/{total_checks} checks passed)"
        
        if anomalies:
            summary += f". {len(anomalies)} anomalies detected"
        
        critical_issues = [check for check in quality_checks if not check.passed and check.severity == 'CRITICAL']
        if critical_issues:
            summary += f". {len(critical_issues)} critical issues require attention"
        
        if experiment_issues:
            summary += f". {len(experiment_issues)} experiment-specific issues require attention"
        
        return summary
    
    # Helper methods
    
    def _get_framework_yaml_path(self, framework_name: str) -> Optional[str]:
        """Map framework name to its YAML file path for framework-aware QA."""
        return get_framework_yaml_path(framework_name)

    def _get_expected_wells(self, framework: str) -> List[str]:
        """Get expected wells for a framework."""
        framework_wells = {
            'civic_virtue': ['Dignity', 'Truth', 'Justice', 'Hope', 'Pragmatism', 
                           'Tribalism', 'Manipulation', 'Resentment', 'Fantasy', 'Fear'],
            'political_spectrum': ['Progressive', 'Liberal', 'Moderate', 'Conservative', 'Libertarian'],
            'moral_foundations_theory': ['Care', 'Harm', 'Fairness', 'Cheating', 'Loyalty', 'Betrayal', 
                                       'Authority', 'Subversion', 'Sanctity', 'Degradation', 'Liberty', 'Oppression'],
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
def validate_llm_analysis(
    text_input: str, 
    framework: str, 
    llm_response: Dict[str, Any], 
    parsed_scores: Dict[str, float],
    experiment_context: ExperimentContext = None
) -> QualityAssessment:
    """
    Convenience function to run LLM quality assurance validation.
    
    Args:
        text_input: Original text that was analyzed
        framework: Framework used for analysis  
        llm_response: Raw LLM response
        parsed_scores: Parsed well scores
        experiment_context: Optional experiment definition for specific validation
        
    Returns:
        QualityAssessment with confidence scoring and validation results
    """
    qa_system = LLMQualityAssuranceSystem()
    return qa_system.validate_llm_analysis(text_input, framework, llm_response, parsed_scores, experiment_context) 

# Module exports
__all__ = [
    'LLMQualityAssuranceSystem',
    'QualityAssessment', 
    'QualityCheck',
    'ExperimentContext',
    'ExperimentSpecificQualityAssurance',
    'validate_llm_analysis'
]

if __name__ == "__main__":
    # Example usage with experiment-specific QA
    example_scores = {
        'care_harm': 0.7,
        'fairness_cheating': 0.6,
        'loyalty_betrayal': 0.4,
        'authority_subversion': 0.5,
        'sanctity_degradation': 0.3,
        'liberty_oppression': 0.8
    }
    
    example_llm_response = {
        'well_scores': example_scores,
        'justification': 'Example analysis of moral foundations...',
        'confidence': 'medium',
        'narrative_position': {'x': 0.15, 'y': -0.23}
    }
    
    # Example with experiment context for enhanced QA
    experiment_context = ExperimentContext(
        name="MFT Architecture Validation Test",
        description="Validate moral foundations theory framework",
        version="1.0.0",
        hypotheses=[
            "The framework can distinguish between conservative and progressive narratives",
            "Moral foundations positioning will show meaningful variance across different political texts"
        ],
        success_criteria=[
            "N > 4 successful analyses",
            "Quality confidence > 70%",
            "Statistical significance in ideological distinctions"
        ],
        research_context="Testing moral foundations theory framework for political narrative analysis with focus on discriminative validity",
        tags=["conservative", "progressive", "moral_foundations", "political_analysis"]
    )
    
    qa_result = validate_llm_analysis(
        text_input="Example political speech text discussing healthcare reform and government responsibility...",
        framework="moral_foundations_theory",
        llm_response=example_llm_response,
        parsed_scores=example_scores,
        experiment_context=experiment_context
    )
    
    print(f"🎯 Quality Assessment: {qa_result.confidence_level}")
    print(f"📊 Confidence Score: {qa_result.confidence_score:.3f}")
    print(f"📋 Summary: {qa_result.summary}")
    print(f"🔍 Total Checks: {qa_result.quality_metadata['total_checks']}")
    print(f"✅ Checks Passed: {qa_result.quality_metadata['checks_passed']}")
    
    if qa_result.anomalies_detected:
        print(f"⚠️  Anomalies: {qa_result.anomalies_detected}")
        
    if qa_result.experiment_specific_issues:
        print(f"🔬 Experiment Issues: {qa_result.experiment_specific_issues}")
        
    if qa_result.requires_second_opinion:
        print("❌ Second opinion recommended")
    
    # Show layer-by-layer breakdown
    print("\n📑 Quality Check Details:")
    for check in qa_result.individual_checks:
        status = "✅" if check.passed else "❌"
        print(f"  {status} [{check.layer}] {check.check_name}: {check.message}")
        if check.severity == "CRITICAL" and not check.passed:
            print(f"      🚨 CRITICAL: This check must pass for research validity")
        elif check.layer == "EXPERIMENT_SPECIFIC":
            print(f"      🔬 Experiment-specific validation based on research goals") 