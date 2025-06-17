#!/usr/bin/env python3
"""
Quality Transaction Manager

Implements analysis quality validation for experiments:
- Analysis quality threshold enforcement
- Framework fit score validation
- Statistical significance requirement verification
- LLM response quality assessment

Requirements:
- Any quality uncertainty triggers graceful experiment termination
- Framework fit scores below thresholds indicate invalid analysis
- Statistical significance requirements must be met for meaningful results
- LLM response quality must meet academic standards
"""

import json
import logging
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import statistics

logger = logging.getLogger(__name__)

class QualityValidationResult(Enum):
    """Quality validation result codes"""
    VALID = "valid"
    FRAMEWORK_FIT_LOW = "framework_fit_low"
    STATISTICAL_INSUFFICIENT = "statistical_insufficient"
    LLM_RESPONSE_POOR = "llm_response_poor"
    CONFIDENCE_LOW = "confidence_low"
    SAMPLE_SIZE_INSUFFICIENT = "sample_size_insufficient"
    VARIANCE_TOO_HIGH = "variance_too_high"
    VALIDATION_ERROR = "validation_error"

@dataclass
class QualityThresholds:
    """Quality threshold configuration"""
    min_framework_fit_score: float = 0.70
    min_statistical_power: float = 0.80
    min_confidence_level: float = 0.95
    min_sample_size: int = 10
    max_coefficient_variation: float = 0.30
    min_llm_response_length: int = 100
    min_llm_response_coherence: float = 0.75
    required_statistical_tests: List[str] = None
    
    def __post_init__(self):
        if self.required_statistical_tests is None:
            self.required_statistical_tests = ["correlation", "significance"]

@dataclass
class QualityTransactionState:
    """Quality transaction state for rollback capability"""
    analysis_component: str
    metric_name: str
    measured_value: float
    threshold_value: float
    validation_result: QualityValidationResult
    error_details: List[str] = None
    transaction_id: str = ""
    timestamp: str = ""
    additional_context: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.error_details is None:
            self.error_details = []
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
        if self.additional_context is None:
            self.additional_context = {}

class QualityTransactionManager:
    """
    Quality Transaction Integrity Manager
    
    Ensures analysis quality meets academic standards.
    Any quality uncertainty results in graceful experiment failure.
    """
    
    def __init__(self, transaction_id: str = None, thresholds: QualityThresholds = None):
        self.transaction_id = transaction_id or f"qtx_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.thresholds = thresholds or QualityThresholds()
        self.transaction_states: List[QualityTransactionState] = []
        
        logger.info(f"🔒 Quality Transaction Manager initialized: {self.transaction_id}")
        logger.info(f"   Framework fit threshold: {self.thresholds.min_framework_fit_score}")
        logger.info(f"   Statistical power threshold: {self.thresholds.min_statistical_power}")
        logger.info(f"   Confidence level threshold: {self.thresholds.min_confidence_level}")
    
    def validate_framework_fit_scores(self, analysis_results: Dict[str, Any]) -> List[QualityTransactionState]:
        """
        🔒 TRANSACTION INTEGRITY: Validate framework fit scores
        
        Args:
            analysis_results: Dictionary containing analysis results with fit scores
            
        Returns:
            List of QualityTransactionState with validation results
        """
        logger.info(f"🔍 Validating framework fit scores")
        
        # Extract fit scores from analysis results
        fit_scores = self._extract_fit_scores(analysis_results)
        
        for component, score in fit_scores.items():
            state = QualityTransactionState(
                analysis_component="framework_fit",
                metric_name=component,
                measured_value=score,
                threshold_value=self.thresholds.min_framework_fit_score,
                validation_result=QualityValidationResult.VALIDATION_ERROR,
                transaction_id=self.transaction_id
            )
            
            # Validate framework fit score
            if score < self.thresholds.min_framework_fit_score:
                state.validation_result = QualityValidationResult.FRAMEWORK_FIT_LOW
                state.error_details.append(
                    f"Framework fit score {score:.3f} below threshold {self.thresholds.min_framework_fit_score}"
                )
                state.additional_context = {
                    'component': component,
                    'score': score,
                    'threshold': self.thresholds.min_framework_fit_score,
                    'analysis_type': 'framework_fit'
                }
            else:
                state.validation_result = QualityValidationResult.VALID
                logger.info(f"✅ Framework fit validation PASSED: {component} ({score:.3f})")
            
            self.transaction_states.append(state)
            self._log_validation_result(state)
        
        return self.transaction_states
    
    def validate_statistical_significance(self, analysis_results: Dict[str, Any]) -> List[QualityTransactionState]:
        """
        🔒 TRANSACTION INTEGRITY: Validate statistical significance requirements
        
        Args:
            analysis_results: Dictionary containing statistical analysis results
            
        Returns:
            List of QualityTransactionState with validation results
        """
        logger.info(f"🔍 Validating statistical significance")
        
        # Extract statistical measures
        statistical_measures = self._extract_statistical_measures(analysis_results)
        
        for measure_name, measure_data in statistical_measures.items():
            state = QualityTransactionState(
                analysis_component="statistical_significance",
                metric_name=measure_name,
                measured_value=measure_data.get('value', 0.0),
                threshold_value=measure_data.get('threshold', 0.05),
                validation_result=QualityValidationResult.VALIDATION_ERROR,
                transaction_id=self.transaction_id
            )
            
            # Validate statistical significance
            if measure_name == 'p_value':
                if state.measured_value > state.threshold_value:
                    state.validation_result = QualityValidationResult.STATISTICAL_INSUFFICIENT
                    state.error_details.append(
                        f"P-value {state.measured_value:.4f} above significance threshold {state.threshold_value}"
                    )
                else:
                    state.validation_result = QualityValidationResult.VALID
                    
            elif measure_name == 'confidence_interval':
                ci_width = measure_data.get('width', float('inf'))
                max_width = measure_data.get('max_width', 0.2)
                
                if ci_width > max_width:
                    state.validation_result = QualityValidationResult.CONFIDENCE_LOW
                    state.measured_value = ci_width
                    state.threshold_value = max_width
                    state.error_details.append(
                        f"Confidence interval too wide: {ci_width:.4f} > {max_width}"
                    )
                else:
                    state.validation_result = QualityValidationResult.VALID
                    
            elif measure_name == 'sample_size':
                if state.measured_value < self.thresholds.min_sample_size:
                    state.validation_result = QualityValidationResult.SAMPLE_SIZE_INSUFFICIENT
                    state.threshold_value = self.thresholds.min_sample_size
                    state.error_details.append(
                        f"Sample size {state.measured_value} below minimum {self.thresholds.min_sample_size}"
                    )
                else:
                    state.validation_result = QualityValidationResult.VALID
            
            state.additional_context = {
                'measure_type': measure_name,
                'analysis_details': measure_data
            }
            
            self.transaction_states.append(state)
            self._log_validation_result(state)
        
        return self.transaction_states
    
    def validate_llm_response_quality(self, llm_responses: List[Dict[str, Any]]) -> List[QualityTransactionState]:
        """
        🔒 TRANSACTION INTEGRITY: Validate LLM response quality
        
        Args:
            llm_responses: List of LLM response dictionaries
            
        Returns:
            List of QualityTransactionState with validation results
        """
        logger.info(f"🔍 Validating LLM response quality for {len(llm_responses)} responses")
        
        for i, response in enumerate(llm_responses):
            response_id = f"response_{i+1}"
            
            # Validate response length
            length_state = self._validate_response_length(response, response_id)
            self.transaction_states.append(length_state)
            
            # Validate response coherence
            coherence_state = self._validate_response_coherence(response, response_id)
            self.transaction_states.append(coherence_state)
            
            # Validate response completeness
            completeness_state = self._validate_response_completeness(response, response_id)
            self.transaction_states.append(completeness_state)
        
        return self.transaction_states
    
    def validate_analysis_variance(self, analysis_results: Dict[str, Any]) -> List[QualityTransactionState]:
        """
        🔒 TRANSACTION INTEGRITY: Validate analysis result variance
        
        Args:
            analysis_results: Dictionary containing analysis results with variance measures
            
        Returns:
            List of QualityTransactionState with validation results
        """
        logger.info(f"🔍 Validating analysis variance")
        
        # Extract variance measures
        variance_measures = self._extract_variance_measures(analysis_results)
        
        for measure_name, variance_data in variance_measures.items():
            state = QualityTransactionState(
                analysis_component="variance_analysis",
                metric_name=measure_name,
                measured_value=variance_data.get('coefficient_of_variation', 0.0),
                threshold_value=self.thresholds.max_coefficient_variation,
                validation_result=QualityValidationResult.VALIDATION_ERROR,
                transaction_id=self.transaction_id
            )
            
            # Validate coefficient of variation
            if state.measured_value > self.thresholds.max_coefficient_variation:
                state.validation_result = QualityValidationResult.VARIANCE_TOO_HIGH
                state.error_details.append(
                    f"Coefficient of variation {state.measured_value:.3f} exceeds threshold {self.thresholds.max_coefficient_variation}"
                )
                state.additional_context = {
                    'measure_name': measure_name,
                    'variance_data': variance_data,
                    'mean': variance_data.get('mean', 0.0),
                    'std_dev': variance_data.get('std_dev', 0.0)
                }
            else:
                state.validation_result = QualityValidationResult.VALID
                logger.info(f"✅ Variance validation PASSED: {measure_name} (CV: {state.measured_value:.3f})")
            
            self.transaction_states.append(state)
            self._log_validation_result(state)
        
        return self.transaction_states
    
    def is_transaction_valid(self) -> Tuple[bool, List[str]]:
        """
        🔒 TRANSACTION INTEGRITY: Check if all quality validations are valid
        
        Returns:
            Tuple of (is_valid, error_messages)
            is_valid=False means experiment should terminate
        """
        invalid_states = []
        error_messages = []
        
        for state in self.transaction_states:
            if state.validation_result != QualityValidationResult.VALID:
                invalid_states.append(state)
                error_messages.extend([
                    f"Quality check {state.analysis_component}.{state.metric_name}: {state.validation_result.value}",
                    *state.error_details
                ])
        
        is_valid = len(invalid_states) == 0
        
        if not is_valid:
            logger.error(f"🚨 QUALITY TRANSACTION FAILURE: {len(invalid_states)} quality check(s) failed")
            for msg in error_messages:
                logger.error(f"   {msg}")
        else:
            logger.info(f"✅ Quality transaction validation passed: {len(self.transaction_states)} check(s)")
        
        return is_valid, error_messages
    
    def generate_rollback_guidance(self) -> Dict[str, Any]:
        """
        Generate user guidance for fixing quality transaction failures
        
        Returns:
            Dictionary with specific guidance for each failed quality check
        """
        guidance = {
            'transaction_id': self.transaction_id,
            'total_checks': len(self.transaction_states),
            'failed_checks': [],
            'recommendations': [],
            'commands_to_run': []
        }
        
        quality_issues = {}
        
        for state in self.transaction_states:
            if state.validation_result != QualityValidationResult.VALID:
                failure_info = {
                    'analysis_component': state.analysis_component,
                    'metric_name': state.metric_name,
                    'measured_value': state.measured_value,
                    'threshold_value': state.threshold_value,
                    'validation_result': state.validation_result.value,
                    'error_details': state.error_details,
                    'additional_context': state.additional_context
                }
                
                guidance['failed_checks'].append(failure_info)
                
                # Group by quality issue type for targeted guidance
                issue_type = state.validation_result
                if issue_type not in quality_issues:
                    quality_issues[issue_type] = []
                quality_issues[issue_type].append(state)
        
        # Generate specific recommendations by issue type
        for issue_type, states in quality_issues.items():
            
            if issue_type == QualityValidationResult.FRAMEWORK_FIT_LOW:
                guidance['recommendations'].append(
                    f"Framework fit scores below threshold detected in {len(states)} component(s). "
                    f"Consider framework selection or text preprocessing improvements."
                )
                guidance['commands_to_run'].extend([
                    "# Review framework-text compatibility",
                    "# Check preprocessing quality: python3 scripts/analyze_preprocessing.py",
                    "# Try alternative framework: python3 scripts/suggest_framework.py",
                    "# Validate text quality: python3 scripts/validate_text_quality.py"
                ])
            
            elif issue_type == QualityValidationResult.STATISTICAL_INSUFFICIENT:
                guidance['recommendations'].append(
                    f"Statistical significance requirements not met in {len(states)} test(s). "
                    f"Increase sample size or adjust analysis parameters."
                )
                guidance['commands_to_run'].extend([
                    "# Increase sample size if possible",
                    "# Check power analysis: python3 scripts/power_analysis.py",
                    "# Review statistical test selection",
                    "# Validate data preprocessing for noise reduction"
                ])
            
            elif issue_type == QualityValidationResult.LLM_RESPONSE_POOR:
                guidance['recommendations'].append(
                    f"LLM response quality issues detected in {len(states)} response(s). "
                    f"Consider prompt optimization or model selection changes."
                )
                guidance['commands_to_run'].extend([
                    "# Review LLM prompt templates",
                    "# Try different LLM model: --model gpt-4",
                    "# Validate response parsing: python3 scripts/validate_llm_parsing.py",
                    "# Check API response quality indicators"
                ])
            
            elif issue_type == QualityValidationResult.SAMPLE_SIZE_INSUFFICIENT:
                guidance['recommendations'].append(
                    f"Sample size insufficient for reliable analysis in {len(states)} component(s). "
                    f"Minimum required: {self.thresholds.min_sample_size}"
                )
                guidance['commands_to_run'].extend([
                    "# Add more data to corpus",
                    "# Review corpus selection criteria",
                    "# Consider lowering significance requirements (with caution)",
                    "# Use bootstrap sampling if appropriate"
                ])
            
            elif issue_type == QualityValidationResult.VARIANCE_TOO_HIGH:
                guidance['recommendations'].append(
                    f"Analysis variance too high in {len(states)} measure(s). "
                    f"Results may not be reliable due to high variability."
                )
                guidance['commands_to_run'].extend([
                    "# Check for outliers in data",
                    "# Improve text preprocessing consistency",
                    "# Validate framework application consistency",
                    "# Consider variance reduction techniques"
                ])
        
        return guidance
    
    def rollback_transaction(self) -> bool:
        """
        🔒 ROLLBACK: Undo any analysis changes made during this transaction
        
        Returns:
            True if rollback successful, False if issues remain
        """
        logger.warning(f"🔄 Rolling back quality transaction: {self.transaction_id}")
        
        # Quality validation rollback is primarily about stopping analysis
        # and providing guidance - no file system changes to undo
        rollback_success = True
        
        # Clear transaction states
        cleared_states = len(self.transaction_states)
        self.transaction_states = []
        
        logger.info(f"✅ Quality transaction rollback completed: cleared {cleared_states} states")
        
        return rollback_success
    
    def _extract_fit_scores(self, analysis_results: Dict[str, Any]) -> Dict[str, float]:
        """Extract framework fit scores from analysis results"""
        fit_scores = {}
        
        # Look for fit scores in various locations
        if 'framework_fit_score' in analysis_results:
            fit_scores['overall'] = analysis_results['framework_fit_score']
        
        if 'well_fit_scores' in analysis_results:
            well_scores = analysis_results['well_fit_scores']
            if isinstance(well_scores, dict):
                for well_name, score in well_scores.items():
                    fit_scores[f'well_{well_name}'] = score
        
        if 'quality_metrics' in analysis_results:
            quality_metrics = analysis_results['quality_metrics']
            if isinstance(quality_metrics, dict):
                for metric_name, value in quality_metrics.items():
                    if 'fit' in metric_name.lower() and isinstance(value, (int, float)):
                        fit_scores[metric_name] = value
        
        # If no fit scores found, estimate from other metrics
        if not fit_scores:
            # Use correlation or other indicators as proxy
            if 'correlations' in analysis_results:
                correlations = analysis_results['correlations']
                if isinstance(correlations, dict):
                    avg_correlation = statistics.mean([abs(v) for v in correlations.values() if isinstance(v, (int, float))])
                    fit_scores['estimated_from_correlation'] = avg_correlation
        
        return fit_scores
    
    def _extract_statistical_measures(self, analysis_results: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Extract statistical significance measures from analysis results"""
        measures = {}
        
        # Extract p-values
        if 'p_values' in analysis_results:
            p_values = analysis_results['p_values']
            if isinstance(p_values, dict):
                for test_name, p_value in p_values.items():
                    measures[f'p_value_{test_name}'] = {
                        'value': p_value,
                        'threshold': 0.05,
                        'type': 'p_value'
                    }
            elif isinstance(p_values, (int, float)):
                measures['p_value'] = {
                    'value': p_values,
                    'threshold': 0.05,
                    'type': 'p_value'
                }
        
        # Extract confidence intervals
        if 'confidence_intervals' in analysis_results:
            ci_data = analysis_results['confidence_intervals']
            if isinstance(ci_data, dict):
                for ci_name, ci_info in ci_data.items():
                    if isinstance(ci_info, dict) and 'width' in ci_info:
                        measures[f'confidence_interval_{ci_name}'] = {
                            'width': ci_info['width'],
                            'max_width': 0.2,
                            'type': 'confidence_interval'
                        }
        
        # Extract sample size
        if 'sample_size' in analysis_results:
            measures['sample_size'] = {
                'value': analysis_results['sample_size'],
                'threshold': self.thresholds.min_sample_size,
                'type': 'sample_size'
            }
        
        return measures
    
    def _extract_variance_measures(self, analysis_results: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Extract variance measures from analysis results"""
        measures = {}
        
        # Look for coefficient of variation
        if 'variance_analysis' in analysis_results:
            variance_data = analysis_results['variance_analysis']
            if isinstance(variance_data, dict):
                for measure_name, measure_info in variance_data.items():
                    if isinstance(measure_info, dict):
                        measures[measure_name] = measure_info
        
        # Calculate CV from mean and std if available
        if 'statistics' in analysis_results:
            stats = analysis_results['statistics']
            if isinstance(stats, dict):
                mean = stats.get('mean')
                std_dev = stats.get('std_dev') or stats.get('standard_deviation')
                
                if mean and std_dev and mean != 0:
                    cv = std_dev / abs(mean)
                    measures['overall_cv'] = {
                        'coefficient_of_variation': cv,
                        'mean': mean,
                        'std_dev': std_dev
                    }
        
        return measures
    
    def _validate_response_length(self, response: Dict[str, Any], response_id: str) -> QualityTransactionState:
        """Validate LLM response length"""
        content = response.get('content', response.get('text', ''))
        length = len(content.strip())
        
        state = QualityTransactionState(
            analysis_component="llm_response_quality",
            metric_name=f"{response_id}_length",
            measured_value=length,
            threshold_value=self.thresholds.min_llm_response_length,
            validation_result=QualityValidationResult.VALIDATION_ERROR,
            transaction_id=self.transaction_id
        )
        
        if length < self.thresholds.min_llm_response_length:
            state.validation_result = QualityValidationResult.LLM_RESPONSE_POOR
            state.error_details.append(
                f"Response length {length} below minimum {self.thresholds.min_llm_response_length}"
            )
        else:
            state.validation_result = QualityValidationResult.VALID
        
        state.additional_context = {
            'response_id': response_id,
            'content_preview': content[:100] + "..." if len(content) > 100 else content
        }
        
        return state
    
    def _validate_response_coherence(self, response: Dict[str, Any], response_id: str) -> QualityTransactionState:
        """Validate LLM response coherence"""
        content = response.get('content', response.get('text', ''))
        
        # Simple coherence scoring based on structural indicators
        coherence_score = self._calculate_coherence_score(content)
        
        state = QualityTransactionState(
            analysis_component="llm_response_quality",
            metric_name=f"{response_id}_coherence",
            measured_value=coherence_score,
            threshold_value=self.thresholds.min_llm_response_coherence,
            validation_result=QualityValidationResult.VALIDATION_ERROR,
            transaction_id=self.transaction_id
        )
        
        if coherence_score < self.thresholds.min_llm_response_coherence:
            state.validation_result = QualityValidationResult.LLM_RESPONSE_POOR
            state.error_details.append(
                f"Response coherence {coherence_score:.3f} below threshold {self.thresholds.min_llm_response_coherence}"
            )
        else:
            state.validation_result = QualityValidationResult.VALID
        
        state.additional_context = {
            'response_id': response_id,
            'coherence_indicators': self._get_coherence_indicators(content)
        }
        
        return state
    
    def _validate_response_completeness(self, response: Dict[str, Any], response_id: str) -> QualityTransactionState:
        """Validate LLM response completeness"""
        content = response.get('content', response.get('text', ''))
        
        # Check for completeness indicators
        completeness_score = self._calculate_completeness_score(content)
        
        state = QualityTransactionState(
            analysis_component="llm_response_quality",
            metric_name=f"{response_id}_completeness",
            measured_value=completeness_score,
            threshold_value=0.80,  # 80% completeness threshold
            validation_result=QualityValidationResult.VALIDATION_ERROR,
            transaction_id=self.transaction_id
        )
        
        if completeness_score < 0.80:
            state.validation_result = QualityValidationResult.LLM_RESPONSE_POOR
            state.error_details.append(
                f"Response completeness {completeness_score:.3f} below threshold 0.80"
            )
        else:
            state.validation_result = QualityValidationResult.VALID
        
        state.additional_context = {
            'response_id': response_id,
            'completeness_indicators': self._get_completeness_indicators(content)
        }
        
        return state
    
    def _calculate_coherence_score(self, content: str) -> float:
        """Calculate coherence score based on structural indicators"""
        if not content:
            return 0.0
        
        score = 0.0
        indicators = 0
        
        # Check for proper sentence structure
        sentences = re.split(r'[.!?]+', content)
        valid_sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
        if len(valid_sentences) > 0:
            score += 0.3
            indicators += 1
        
        # Check for logical connectors
        connectors = ['therefore', 'however', 'furthermore', 'additionally', 'consequently', 'moreover']
        connector_count = sum(1 for conn in connectors if conn in content.lower())
        if connector_count > 0:
            score += min(0.3, connector_count * 0.1)
            indicators += 1
        
        # Check for structured analysis
        if re.search(r'\b(analysis|conclusion|result|finding)\b', content.lower()):
            score += 0.2
            indicators += 1
        
        # Check for appropriate length distribution
        if len(content) > 50:
            score += 0.2
            indicators += 1
        
        return min(1.0, score) if indicators > 0 else 0.0
    
    def _calculate_completeness_score(self, content: str) -> float:
        """Calculate completeness score based on expected elements"""
        if not content:
            return 0.0
        
        score = 0.0
        
        # Check for expected analysis elements
        expected_elements = [
            r'\b(score|rating|value)\b',  # Scoring/rating present
            r'\b(well|dimension|aspect)\b',  # Framework elements mentioned
            r'\b(because|since|due to)\b',  # Reasoning provided
            r'\b(high|low|medium|moderate)\b'  # Qualitative assessments
        ]
        
        for element_pattern in expected_elements:
            if re.search(element_pattern, content.lower()):
                score += 0.25
        
        return min(1.0, score)
    
    def _get_coherence_indicators(self, content: str) -> Dict[str, Any]:
        """Get detailed coherence indicators for debugging"""
        sentences = re.split(r'[.!?]+', content)
        valid_sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
        
        return {
            'sentence_count': len(valid_sentences),
            'avg_sentence_length': statistics.mean([len(s) for s in valid_sentences]) if valid_sentences else 0,
            'has_connectors': bool(re.search(r'\b(therefore|however|furthermore)\b', content.lower())),
            'has_analysis_terms': bool(re.search(r'\b(analysis|conclusion|result)\b', content.lower()))
        }
    
    def _get_completeness_indicators(self, content: str) -> Dict[str, Any]:
        """Get detailed completeness indicators for debugging"""
        return {
            'has_scoring': bool(re.search(r'\b(score|rating|value)\b', content.lower())),
            'has_framework_terms': bool(re.search(r'\b(well|dimension|aspect)\b', content.lower())),
            'has_reasoning': bool(re.search(r'\b(because|since|due to)\b', content.lower())),
            'has_qualitative_assessment': bool(re.search(r'\b(high|low|medium|moderate)\b', content.lower())),
            'content_length': len(content)
        }
    
    def _log_validation_result(self, state: QualityTransactionState):
        """Log detailed validation result"""
        if state.validation_result == QualityValidationResult.VALID:
            logger.info(f"✅ Quality validation PASSED: {state.analysis_component}.{state.metric_name} ({state.measured_value:.3f})")
        else:
            logger.error(f"❌ Quality validation FAILED: {state.analysis_component}.{state.metric_name} - {state.validation_result.value}")
            for error in state.error_details:
                logger.error(f"   {error}") 