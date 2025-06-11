"""
Component Quality Assurance Framework

Provides automated validation and quality assessment for:
- Prompt templates (clarity, consistency, format compliance)
- Framework architectures (coherence, completeness, theoretical grounding)
- Weighting methodologies (mathematical validity, edge case handling)

Implements systematic quality checks supporting academic standards.
"""

import json
import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from .seed_prompts import ComponentType


class QualityLevel(Enum):
    """Quality assessment levels."""
    EXCELLENT = "excellent"
    GOOD = "good"
    ACCEPTABLE = "acceptable"
    NEEDS_IMPROVEMENT = "needs_improvement"
    UNACCEPTABLE = "unacceptable"


@dataclass
class QualityCheck:
    """Individual quality check result."""
    check_name: str
    passed: bool
    score: float  # 0.0-1.0
    message: str
    recommendation: str = ""
    severity: str = "info"  # info, warning, error


@dataclass
class QualityReport:
    """Comprehensive quality assessment report."""
    component_type: ComponentType
    component_name: str
    version: str
    overall_score: float
    overall_level: QualityLevel
    checks: List[QualityCheck]
    recommendations: List[str]
    academic_readiness: bool
    validation_requirements: List[str]


class ComponentQualityValidator:
    """
    Automated quality assurance for component development.
    
    Provides systematic validation across multiple dimensions:
    - Technical compliance and format validation
    - Content quality and completeness assessment
    - Academic standards and methodological rigor
    - Integration compatibility and performance prediction
    """
    
    def __init__(self):
        self.quality_thresholds = {
            QualityLevel.EXCELLENT: 0.9,
            QualityLevel.GOOD: 0.8,
            QualityLevel.ACCEPTABLE: 0.7,
            QualityLevel.NEEDS_IMPROVEMENT: 0.5,
            QualityLevel.UNACCEPTABLE: 0.0
        }
    
    def validate_prompt_template(self, 
                                template_content: str,
                                template_type: str = "hierarchical",
                                framework_context: Optional[Dict] = None) -> QualityReport:
        """
        Comprehensive quality validation for prompt templates.
        
        Args:
            template_content: The prompt template text
            template_type: Type of template (standard, hierarchical)
            framework_context: Optional framework information for context validation
            
        Returns:
            Detailed quality assessment report
        """
        checks = []
        
        # Technical compliance checks
        checks.extend(self._check_prompt_format_compliance(template_content, template_type))
        
        # Content quality checks
        checks.extend(self._check_prompt_clarity(template_content))
        checks.extend(self._check_instruction_completeness(template_content, template_type))
        checks.extend(self._check_output_specification(template_content))
        
        # Academic standards checks
        checks.extend(self._check_reasoning_requirements(template_content))
        checks.extend(self._check_evidence_requirements(template_content))
        checks.extend(self._check_scoring_methodology_alignment(template_content, framework_context))
        
        # Performance prediction checks
        checks.extend(self._check_consistency_enablers(template_content))
        checks.extend(self._check_edge_case_handling(template_content))
        
        return self._compile_quality_report(
            ComponentType.PROMPT_TEMPLATE,
            "prompt_template",
            "current",
            checks
        )
    
    def validate_framework(self,
                          framework_data: Dict,
                          framework_name: str,
                          theoretical_foundation: Optional[str] = None) -> QualityReport:
        """
        Comprehensive quality validation for framework architectures.
        
        Args:
            framework_data: Complete framework configuration
            framework_name: Name of the framework
            theoretical_foundation: Optional theoretical grounding description
            
        Returns:
            Detailed quality assessment report
        """
        checks = []
        
        # Technical compliance checks
        checks.extend(self._check_framework_structure(framework_data))
        checks.extend(self._check_dipole_completeness(framework_data))
        
        # Content quality checks
        checks.extend(self._check_conceptual_distinctness(framework_data))
        checks.extend(self._check_operational_clarity(framework_data))
        checks.extend(self._check_domain_coverage(framework_data))
        
        # Academic standards checks
        checks.extend(self._check_theoretical_grounding(framework_data, theoretical_foundation))
        checks.extend(self._check_framework_coherence(framework_data))
        checks.extend(self._check_analytical_precision(framework_data))
        
        # Application readiness checks
        checks.extend(self._check_measurability(framework_data))
        checks.extend(self._check_cross_narrative_applicability(framework_data))
        
        return self._compile_quality_report(
            ComponentType.FRAMEWORK,
            framework_name,
            "current",
            checks
        )
    
    def validate_weighting_methodology(self,
                                     methodology_data: Dict,
                                     methodology_name: str,
                                     test_scenarios: Optional[List[Dict]] = None) -> QualityReport:
        """
        Comprehensive quality validation for weighting methodologies.
        
        Args:
            methodology_data: Complete methodology specification
            methodology_name: Name of the methodology
            test_scenarios: Optional test cases for validation
            
        Returns:
            Detailed quality assessment report
        """
        checks = []
        
        # Technical compliance checks
        checks.extend(self._check_mathematical_specification(methodology_data))
        checks.extend(self._check_parameter_validity(methodology_data))
        checks.extend(self._check_implementation_completeness(methodology_data))
        
        # Mathematical validity checks
        checks.extend(self._check_mathematical_soundness(methodology_data))
        checks.extend(self._check_edge_case_behavior(methodology_data, test_scenarios))
        checks.extend(self._check_normalization_properties(methodology_data))
        
        # Performance characteristics checks
        checks.extend(self._check_hierarchy_enhancement(methodology_data))
        checks.extend(self._check_statistical_properties(methodology_data))
        checks.extend(self._check_computational_efficiency(methodology_data))
        
        # Integration compatibility checks
        checks.extend(self._check_pipeline_compatibility(methodology_data))
        checks.extend(self._check_interpretability(methodology_data))
        
        return self._compile_quality_report(
            ComponentType.WEIGHTING_METHODOLOGY,
            methodology_name,
            "current",
            checks
        )
    
    def validate_component_compatibility(self,
                                       prompt_template: str,
                                       framework_data: Dict,
                                       weighting_data: Dict) -> QualityReport:
        """
        Validate compatibility between component combination.
        
        Args:
            prompt_template: Prompt template content
            framework_data: Framework specification
            weighting_data: Weighting methodology specification
            
        Returns:
            Component compatibility assessment
        """
        checks = []
        
        # Cross-component alignment checks
        checks.extend(self._check_prompt_framework_alignment(prompt_template, framework_data))
        checks.extend(self._check_framework_weighting_alignment(framework_data, weighting_data))
        checks.extend(self._check_output_input_compatibility(prompt_template, weighting_data))
        
        # Integration quality checks
        checks.extend(self._check_workflow_coherence(prompt_template, framework_data, weighting_data))
        checks.extend(self._check_performance_synergy(prompt_template, framework_data, weighting_data))
        
        return self._compile_quality_report(
            ComponentType.PROMPT_TEMPLATE,  # Using as representative type
            "component_combination",
            "compatibility_check",
            checks
        )
    
    # Prompt Template Quality Checks
    
    def _check_prompt_format_compliance(self, content: str, template_type: str) -> List[QualityCheck]:
        """Check prompt format compliance."""
        checks = []
        
        # Check for required hierarchical elements
        if template_type == "hierarchical":
            has_ranking = any(keyword in content.lower() for keyword in ["rank", "ranking", "hierarchy", "dominant"])
            checks.append(QualityCheck(
                "hierarchical_ranking_requirement",
                has_ranking,
                1.0 if has_ranking else 0.0,
                "Hierarchical prompts must require ranking/dominance assessment",
                "Add explicit instructions for ranking or identifying dominant themes"
            ))
            
            has_weighting = any(keyword in content.lower() for keyword in ["weight", "percentage", "sum to 100", "relative"])
            checks.append(QualityCheck(
                "relative_weighting_requirement",
                has_weighting,
                1.0 if has_weighting else 0.0,
                "Hierarchical prompts must require relative weighting",
                "Add instructions for providing relative weights that sum to 100%"
            ))
        
        # Check for JSON output format requirement
        has_json_format = "json" in content.lower() or "{" in content
        checks.append(QualityCheck(
            "structured_output_format",
            has_json_format,
            1.0 if has_json_format else 0.0,
            "Prompts should specify structured output format",
            "Add clear JSON format specification with required fields"
        ))
        
        return checks
    
    def _check_prompt_clarity(self, content: str) -> List[QualityCheck]:
        """Check prompt instruction clarity."""
        checks = []
        
        # Check for ambiguous language
        ambiguous_terms = ["might", "could", "perhaps", "maybe", "probably"]
        ambiguous_count = sum(1 for term in ambiguous_terms if term in content.lower())
        clarity_score = max(0.0, 1.0 - (ambiguous_count * 0.2))
        
        checks.append(QualityCheck(
            "instruction_clarity",
            clarity_score >= 0.8,
            clarity_score,
            f"Instruction clarity score: {clarity_score:.2f}",
            "Reduce ambiguous language and use direct, actionable instructions"
        ))
        
        # Check for step-by-step structure
        has_steps = bool(re.search(r'\d+\.|\d+\)|step \d+', content.lower()))
        checks.append(QualityCheck(
            "step_by_step_structure",
            has_steps,
            1.0 if has_steps else 0.5,
            "Clear step-by-step instructions improve LLM performance",
            "Add numbered steps or clear sequential instructions"
        ))
        
        return checks
    
    def _check_instruction_completeness(self, content: str, template_type: str) -> List[QualityCheck]:
        """Check instruction completeness."""
        checks = []
        
        required_elements = ["analysis", "evidence", "score"]
        if template_type == "hierarchical":
            required_elements.extend(["ranking", "dominant"])
        
        present_elements = sum(1 for element in required_elements if element in content.lower())
        completeness_score = present_elements / len(required_elements)
        
        checks.append(QualityCheck(
            "instruction_completeness",
            completeness_score >= 0.8,
            completeness_score,
            f"Instruction completeness: {present_elements}/{len(required_elements)} elements",
            f"Add missing elements: {[e for e in required_elements if e not in content.lower()]}"
        ))
        
        return checks
    
    def _check_output_specification(self, content: str) -> List[QualityCheck]:
        """Check output format specification."""
        checks = []
        
        # Check for required output fields
        required_fields = ["score", "evidence", "confidence"]
        field_mentions = sum(1 for field in required_fields if field in content.lower())
        field_score = field_mentions / len(required_fields)
        
        checks.append(QualityCheck(
            "output_field_specification",
            field_score >= 0.8,
            field_score,
            f"Output field specification: {field_mentions}/{len(required_fields)} fields mentioned",
            "Specify all required output fields: score, evidence, confidence"
        ))
        
        return checks
    
    def _check_reasoning_requirements(self, content: str) -> List[QualityCheck]:
        """Check reasoning chain requirements."""
        checks = []
        
        reasoning_keywords = ["explain", "reasoning", "because", "justify", "why"]
        has_reasoning = any(keyword in content.lower() for keyword in reasoning_keywords)
        
        checks.append(QualityCheck(
            "reasoning_chain_requirement",
            has_reasoning,
            1.0 if has_reasoning else 0.3,
            "Reasoning requirements guide LLM analytical process",
            "Add explicit requirements for explanation and justification"
        ))
        
        return checks
    
    def _check_evidence_requirements(self, content: str) -> List[QualityCheck]:
        """Check evidence extraction requirements."""
        checks = []
        
        evidence_keywords = ["quote", "evidence", "examples", "citation", "text"]
        has_evidence_req = any(keyword in content.lower() for keyword in evidence_keywords)
        
        checks.append(QualityCheck(
            "evidence_extraction_requirement",
            has_evidence_req,
            1.0 if has_evidence_req else 0.2,
            "Evidence requirements improve analytical grounding",
            "Add requirements for textual evidence and specific quotes"
        ))
        
        return checks
    
    def _check_scoring_methodology_alignment(self, content: str, framework_context: Optional[Dict]) -> List[QualityCheck]:
        """Check alignment with scoring methodology."""
        checks = []
        
        if framework_context:
            framework_wells = framework_context.get('wells', [])
            well_mentions = sum(1 for well in framework_wells if well.lower() in content.lower())
            alignment_score = well_mentions / len(framework_wells) if framework_wells else 0.5
            
            checks.append(QualityCheck(
                "framework_alignment",
                alignment_score >= 0.5,
                alignment_score,
                f"Framework alignment: {well_mentions}/{len(framework_wells)} wells mentioned",
                "Ensure prompt references framework-specific wells and concepts"
            ))
        
        return checks
    
    def _check_consistency_enablers(self, content: str) -> List[QualityCheck]:
        """Check elements that enable consistency."""
        checks = []
        
        consistency_enablers = ["consistent", "systematic", "standard", "objective"]
        enabler_count = sum(1 for enabler in consistency_enablers if enabler in content.lower())
        consistency_score = min(1.0, enabler_count * 0.3)
        
        checks.append(QualityCheck(
            "consistency_enablers",
            consistency_score >= 0.6,
            consistency_score,
            f"Consistency enablers: {enabler_count} elements present",
            "Add language emphasizing consistent, systematic analysis"
        ))
        
        return checks
    
    def _check_edge_case_handling(self, content: str) -> List[QualityCheck]:
        """Check edge case handling instructions."""
        checks = []
        
        edge_case_terms = ["ambiguous", "unclear", "conflicting", "missing", "edge case"]
        has_edge_handling = any(term in content.lower() for term in edge_case_terms)
        
        checks.append(QualityCheck(
            "edge_case_handling",
            has_edge_handling,
            1.0 if has_edge_handling else 0.4,
            "Edge case handling improves robustness",
            "Add instructions for handling ambiguous or unclear scenarios"
        ))
        
        return checks
    
    # Framework Quality Checks
    
    def _check_framework_structure(self, framework_data: Dict) -> List[QualityCheck]:
        """Check framework structural requirements."""
        checks = []
        
        required_fields = ["dipoles", "wells", "theoretical_foundation"]
        present_fields = sum(1 for field in required_fields if field in framework_data)
        structure_score = present_fields / len(required_fields)
        
        checks.append(QualityCheck(
            "framework_structure",
            structure_score >= 0.8,
            structure_score,
            f"Framework structure: {present_fields}/{len(required_fields)} required fields",
            f"Add missing fields: {[f for f in required_fields if f not in framework_data]}"
        ))
        
        return checks
    
    def _check_dipole_completeness(self, framework_data: Dict) -> List[QualityCheck]:
        """Check dipole completeness."""
        checks = []
        
        dipoles = framework_data.get("dipoles", {})
        complete_dipoles = 0
        
        for dipole_name, dipole_data in dipoles.items():
            if isinstance(dipole_data, dict):
                has_positive = "positive_well" in dipole_data
                has_negative = "negative_well" in dipole_data
                if has_positive and has_negative:
                    complete_dipoles += 1
        
        completeness_score = complete_dipoles / len(dipoles) if dipoles else 0.0
        
        checks.append(QualityCheck(
            "dipole_completeness",
            completeness_score >= 0.9,
            completeness_score,
            f"Dipole completeness: {complete_dipoles}/{len(dipoles)} complete dipoles",
            "Ensure all dipoles have both positive and negative wells defined"
        ))
        
        return checks
    
    def _check_conceptual_distinctness(self, framework_data: Dict) -> List[QualityCheck]:
        """Check conceptual distinctness between dipoles."""
        checks = []
        
        dipoles = framework_data.get("dipoles", {})
        if len(dipoles) < 2:
            return checks
        
        # Simple distinctness check based on well names
        all_wells = []
        for dipole_data in dipoles.values():
            if isinstance(dipole_data, dict):
                pos_well = dipole_data.get("positive_well", {}).get("name", "")
                neg_well = dipole_data.get("negative_well", {}).get("name", "")
                all_wells.extend([pos_well.lower(), neg_well.lower()])
        
        unique_wells = len(set(all_wells))
        total_wells = len(all_wells)
        distinctness_score = unique_wells / total_wells if total_wells > 0 else 0.0
        
        checks.append(QualityCheck(
            "conceptual_distinctness",
            distinctness_score >= 0.9,
            distinctness_score,
            f"Conceptual distinctness: {unique_wells}/{total_wells} unique wells",
            "Ensure well names and concepts are distinct across dipoles"
        ))
        
        return checks
    
    def _check_operational_clarity(self, framework_data: Dict) -> List[QualityCheck]:
        """Check operational clarity of framework definitions."""
        checks = []
        
        dipoles = framework_data.get("dipoles", {})
        clear_definitions = 0
        
        for dipole_data in dipoles.values():
            if isinstance(dipole_data, dict):
                pos_well = dipole_data.get("positive_well", {})
                neg_well = dipole_data.get("negative_well", {})
                
                pos_desc = pos_well.get("description", "")
                neg_desc = neg_well.get("description", "")
                
                if len(pos_desc) > 10 and len(neg_desc) > 10:
                    clear_definitions += 1
        
        clarity_score = clear_definitions / len(dipoles) if dipoles else 0.0
        
        checks.append(QualityCheck(
            "operational_clarity",
            clarity_score >= 0.8,
            clarity_score,
            f"Operational clarity: {clear_definitions}/{len(dipoles)} well-defined dipoles",
            "Add detailed descriptions for all wells to enable consistent application"
        ))
        
        return checks
    
    def _check_domain_coverage(self, framework_data: Dict) -> List[QualityCheck]:
        """Check domain coverage comprehensiveness."""
        checks = []
        
        dipoles = framework_data.get("dipoles", {})
        ideal_dipole_count = 5  # Target number of dipoles for comprehensive coverage
        
        coverage_score = min(1.0, len(dipoles) / ideal_dipole_count)
        
        checks.append(QualityCheck(
            "domain_coverage",
            coverage_score >= 0.8,
            coverage_score,
            f"Domain coverage: {len(dipoles)}/{ideal_dipole_count} dipoles (target for comprehensive coverage)",
            f"Consider adding {ideal_dipole_count - len(dipoles)} more dipoles for comprehensive domain coverage"
        ))
        
        return checks
    
    def _check_theoretical_grounding(self, framework_data: Dict, theoretical_foundation: Optional[str]) -> List[QualityCheck]:
        """Check theoretical grounding."""
        checks = []
        
        has_foundation = bool(theoretical_foundation and len(theoretical_foundation) > 50)
        
        checks.append(QualityCheck(
            "theoretical_grounding",
            has_foundation,
            1.0 if has_foundation else 0.3,
            "Theoretical grounding supports academic credibility",
            "Add substantial theoretical foundation linking to established scholarship"
        ))
        
        return checks
    
    def _check_framework_coherence(self, framework_data: Dict) -> List[QualityCheck]:
        """Check internal framework coherence."""
        checks = []
        
        # Check for consistent dipole structure
        dipoles = framework_data.get("dipoles", {})
        consistent_structure = True
        
        required_well_fields = ["name", "description"]
        for dipole_data in dipoles.values():
            if isinstance(dipole_data, dict):
                pos_well = dipole_data.get("positive_well", {})
                neg_well = dipole_data.get("negative_well", {})
                
                for field in required_well_fields:
                    if field not in pos_well or field not in neg_well:
                        consistent_structure = False
        
        checks.append(QualityCheck(
            "framework_coherence",
            consistent_structure,
            1.0 if consistent_structure else 0.5,
            "Framework coherence through consistent dipole structure",
            "Ensure all wells have consistent field structure (name, description)"
        ))
        
        return checks
    
    def _check_analytical_precision(self, framework_data: Dict) -> List[QualityCheck]:
        """Check analytical precision enablers."""
        checks = []
        
        dipoles = framework_data.get("dipoles", {})
        precise_definitions = 0
        
        precision_indicators = ["specific", "measurable", "clear", "distinct", "operational"]
        
        for dipole_data in dipoles.values():
            if isinstance(dipole_data, dict):
                pos_desc = dipole_data.get("positive_well", {}).get("description", "").lower()
                neg_desc = dipole_data.get("negative_well", {}).get("description", "").lower()
                
                pos_precision = sum(1 for indicator in precision_indicators if indicator in pos_desc)
                neg_precision = sum(1 for indicator in precision_indicators if indicator in neg_desc)
                
                if pos_precision > 0 and neg_precision > 0:
                    precise_definitions += 1
        
        precision_score = precise_definitions / len(dipoles) if dipoles else 0.0
        
        checks.append(QualityCheck(
            "analytical_precision",
            precision_score >= 0.6,
            precision_score,
            f"Analytical precision: {precise_definitions}/{len(dipoles)} precisely defined dipoles",
            "Add specific, measurable language to well descriptions"
        ))
        
        return checks
    
    def _check_measurability(self, framework_data: Dict) -> List[QualityCheck]:
        """Check framework measurability through textual analysis."""
        checks = []
        
        # This is a simplified check - in practice, would involve more sophisticated analysis
        dipoles = framework_data.get("dipoles", {})
        measurable_count = 0
        
        measurability_terms = ["language", "words", "phrases", "expressions", "mentions", "references"]
        
        for dipole_data in dipoles.values():
            if isinstance(dipole_data, dict):
                pos_desc = dipole_data.get("positive_well", {}).get("description", "").lower()
                neg_desc = dipole_data.get("negative_well", {}).get("description", "").lower()
                
                combined_desc = pos_desc + " " + neg_desc
                if any(term in combined_desc for term in measurability_terms):
                    measurable_count += 1
        
        measurability_score = measurable_count / len(dipoles) if dipoles else 0.0
        
        checks.append(QualityCheck(
            "textual_measurability",
            measurability_score >= 0.5,
            measurability_score,
            f"Textual measurability: {measurable_count}/{len(dipoles)} dipoles reference language/textual indicators",
            "Add references to specific language patterns or textual indicators for each well"
        ))
        
        return checks
    
    def _check_cross_narrative_applicability(self, framework_data: Dict) -> List[QualityCheck]:
        """Check cross-narrative applicability."""
        checks = []
        
        # Check for domain-agnostic language in descriptions
        dipoles = framework_data.get("dipoles", {})
        general_language_count = 0
        
        specific_domain_terms = ["political", "economic", "social", "environmental"]  # Example domain-specific terms
        
        for dipole_data in dipoles.values():
            if isinstance(dipole_data, dict):
                pos_desc = dipole_data.get("positive_well", {}).get("description", "").lower()
                neg_desc = dipole_data.get("negative_well", {}).get("description", "").lower()
                
                combined_desc = pos_desc + " " + neg_desc
                if not any(term in combined_desc for term in specific_domain_terms):
                    general_language_count += 1
        
        applicability_score = general_language_count / len(dipoles) if dipoles else 0.0
        
        checks.append(QualityCheck(
            "cross_narrative_applicability",
            applicability_score >= 0.7,
            applicability_score,
            f"Cross-narrative applicability: {general_language_count}/{len(dipoles)} dipoles use general language",
            "Consider using more domain-agnostic language for broader applicability"
        ))
        
        return checks
    
    # Weighting Methodology Quality Checks
    
    def _check_mathematical_specification(self, methodology_data: Dict) -> List[QualityCheck]:
        """Check mathematical specification completeness."""
        checks = []
        
        required_fields = ["algorithm_type", "mathematical_formula", "parameters"]
        present_fields = sum(1 for field in required_fields if field in methodology_data)
        specification_score = present_fields / len(required_fields)
        
        checks.append(QualityCheck(
            "mathematical_specification",
            specification_score >= 0.8,
            specification_score,
            f"Mathematical specification: {present_fields}/{len(required_fields)} required fields",
            f"Add missing fields: {[f for f in required_fields if f not in methodology_data]}"
        ))
        
        return checks
    
    def _check_parameter_validity(self, methodology_data: Dict) -> List[QualityCheck]:
        """Check parameter validity and ranges."""
        checks = []
        
        parameters = methodology_data.get("parameters", {})
        valid_params = 0
        total_params = len(parameters)
        
        for param_name, param_value in parameters.items():
            if isinstance(param_value, (int, float)):
                # Check for reasonable parameter ranges
                if 0.0 <= param_value <= 10.0:  # Most algorithm parameters should be in this range
                    valid_params += 1
        
        validity_score = valid_params / total_params if total_params > 0 else 0.5
        
        checks.append(QualityCheck(
            "parameter_validity",
            validity_score >= 0.8,
            validity_score,
            f"Parameter validity: {valid_params}/{total_params} parameters in valid ranges",
            "Ensure all parameters have reasonable values for the algorithm type"
        ))
        
        return checks
    
    def _check_implementation_completeness(self, methodology_data: Dict) -> List[QualityCheck]:
        """Check implementation completeness."""
        checks = []
        
        has_algorithm = "algorithm_type" in methodology_data
        has_formula = "mathematical_formula" in methodology_data
        has_description = "description" in methodology_data and len(methodology_data.get("description", "")) > 20
        
        completeness_elements = [has_algorithm, has_formula, has_description]
        completeness_score = sum(completeness_elements) / len(completeness_elements)
        
        checks.append(QualityCheck(
            "implementation_completeness",
            completeness_score >= 0.8,
            completeness_score,
            f"Implementation completeness: {sum(completeness_elements)}/{len(completeness_elements)} elements present",
            "Add missing elements: algorithm type, mathematical formula, detailed description"
        ))
        
        return checks
    
    def _check_mathematical_soundness(self, methodology_data: Dict) -> List[QualityCheck]:
        """Check mathematical soundness."""
        checks = []
        
        # Basic soundness checks - would be enhanced with actual mathematical validation
        algorithm_type = methodology_data.get("algorithm_type", "")
        formula = methodology_data.get("mathematical_formula", "")
        
        known_algorithms = ["linear", "exponential", "winner_take_most", "threshold_based"]
        is_known_algorithm = algorithm_type in known_algorithms
        
        has_mathematical_operators = any(op in formula for op in ["+", "-", "*", "/", "^", "exp", "log"])
        
        soundness_score = (0.5 if is_known_algorithm else 0.0) + (0.5 if has_mathematical_operators else 0.0)
        
        checks.append(QualityCheck(
            "mathematical_soundness",
            soundness_score >= 0.7,
            soundness_score,
            f"Mathematical soundness: algorithm type recognized, formula contains mathematical operators",
            "Ensure algorithm type is well-defined and formula contains proper mathematical operations"
        ))
        
        return checks
    
    def _check_edge_case_behavior(self, methodology_data: Dict, test_scenarios: Optional[List[Dict]]) -> List[QualityCheck]:
        """Check edge case behavior."""
        checks = []
        
        # If test scenarios provided, analyze their coverage
        if test_scenarios:
            edge_case_types = ["all_zeros", "single_dominant", "equal_values", "extreme_values"]
            covered_cases = []
            
            for scenario in test_scenarios:
                scenario_name = scenario.get("name", "").lower()
                for case_type in edge_case_types:
                    if case_type.replace("_", " ") in scenario_name:
                        covered_cases.append(case_type)
            
            coverage_score = len(set(covered_cases)) / len(edge_case_types)
            
            checks.append(QualityCheck(
                "edge_case_coverage",
                coverage_score >= 0.75,
                coverage_score,
                f"Edge case coverage: {len(set(covered_cases))}/{len(edge_case_types)} case types covered",
                f"Add test scenarios for: {[c for c in edge_case_types if c not in covered_cases]}"
            ))
        else:
            checks.append(QualityCheck(
                "edge_case_testing",
                False,
                0.0,
                "No edge case test scenarios provided",
                "Create test scenarios for edge cases: all zeros, single dominant, equal values, extreme values"
            ))
        
        return checks
    
    def _check_normalization_properties(self, methodology_data: Dict) -> List[QualityCheck]:
        """Check normalization properties."""
        checks = []
        
        formula = methodology_data.get("mathematical_formula", "").lower()
        description = methodology_data.get("description", "").lower()
        
        # Check for normalization considerations
        normalization_terms = ["normalize", "sum", "total", "proportion", "relative"]
        has_normalization = any(term in formula or term in description for term in normalization_terms)
        
        checks.append(QualityCheck(
            "normalization_properties",
            has_normalization,
            1.0 if has_normalization else 0.4,
            "Normalization properties ensure comparable results",
            "Consider normalization requirements to ensure results are comparable across analyses"
        ))
        
        return checks
    
    def _check_hierarchy_enhancement(self, methodology_data: Dict) -> List[QualityCheck]:
        """Check hierarchy enhancement capabilities."""
        checks = []
        
        algorithm_type = methodology_data.get("algorithm_type", "").lower()
        description = methodology_data.get("description", "").lower()
        
        hierarchy_terms = ["dominance", "hierarchy", "amplify", "enhance", "prominent"]
        enhances_hierarchy = any(term in algorithm_type or term in description for term in hierarchy_terms)
        
        checks.append(QualityCheck(
            "hierarchy_enhancement",
            enhances_hierarchy,
            1.0 if enhances_hierarchy else 0.3,
            "Hierarchy enhancement improves thematic distinction",
            "Design algorithm to amplify dominant themes and enhance hierarchical patterns"
        ))
        
        return checks
    
    def _check_statistical_properties(self, methodology_data: Dict) -> List[QualityCheck]:
        """Check statistical properties."""
        checks = []
        
        # Check for statistical considerations
        description = methodology_data.get("description", "").lower()
        statistical_terms = ["variance", "distribution", "stability", "consistency", "statistical"]
        has_statistical_awareness = any(term in description for term in statistical_terms)
        
        checks.append(QualityCheck(
            "statistical_properties",
            has_statistical_awareness,
            1.0 if has_statistical_awareness else 0.5,
            "Statistical properties support academic analysis",
            "Consider statistical properties: variance, distribution characteristics, stability"
        ))
        
        return checks
    
    def _check_computational_efficiency(self, methodology_data: Dict) -> List[QualityCheck]:
        """Check computational efficiency considerations."""
        checks = []
        
        # Simple efficiency check based on algorithm complexity
        algorithm_type = methodology_data.get("algorithm_type", "").lower()
        formula = methodology_data.get("mathematical_formula", "").lower()
        
        # Check for potentially expensive operations
        expensive_operations = ["nested", "iteration", "recursive", "exponential"]
        has_expensive_ops = any(op in algorithm_type or op in formula for op in expensive_operations)
        
        efficiency_score = 0.7 if not has_expensive_ops else 0.9  # Assume efficient unless proven otherwise
        
        checks.append(QualityCheck(
            "computational_efficiency",
            efficiency_score >= 0.7,
            efficiency_score,
            f"Computational efficiency: {'efficient' if not has_expensive_ops else 'potentially expensive'} operations detected",
            "Consider computational complexity for large-scale analysis applications"
        ))
        
        return checks
    
    def _check_pipeline_compatibility(self, methodology_data: Dict) -> List[QualityCheck]:
        """Check pipeline integration compatibility."""
        checks = []
        
        # Check for input/output compatibility
        has_input_spec = "input_format" in methodology_data or "input" in methodology_data.get("description", "").lower()
        has_output_spec = "output_format" in methodology_data or "output" in methodology_data.get("description", "").lower()
        
        compatibility_score = (0.5 if has_input_spec else 0.0) + (0.5 if has_output_spec else 0.0)
        
        checks.append(QualityCheck(
            "pipeline_compatibility",
            compatibility_score >= 0.5,
            compatibility_score,
            f"Pipeline compatibility: input/output specifications {'present' if compatibility_score >= 0.5 else 'missing'}",
            "Specify input and output formats for pipeline integration"
        ))
        
        return checks
    
    def _check_interpretability(self, methodology_data: Dict) -> List[QualityCheck]:
        """Check result interpretability."""
        checks = []
        
        description = methodology_data.get("description", "").lower()
        formula = methodology_data.get("mathematical_formula", "").lower()
        
        interpretability_terms = ["interpret", "meaning", "significant", "threshold", "scale"]
        has_interpretability = any(term in description or term in formula for term in interpretability_terms)
        
        checks.append(QualityCheck(
            "result_interpretability",
            has_interpretability,
            1.0 if has_interpretability else 0.4,
            "Result interpretability supports academic analysis",
            "Add guidance for interpreting results and understanding output scales/thresholds"
        ))
        
        return checks
    
    # Component Compatibility Checks
    
    def _check_prompt_framework_alignment(self, prompt_template: str, framework_data: Dict) -> List[QualityCheck]:
        """Check alignment between prompt and framework."""
        checks = []
        
        # Check if prompt mentions framework wells
        dipoles = framework_data.get("dipoles", {})
        all_wells = []
        for dipole_data in dipoles.values():
            if isinstance(dipole_data, dict):
                pos_well = dipole_data.get("positive_well", {}).get("name", "")
                neg_well = dipole_data.get("negative_well", {}).get("name", "")
                all_wells.extend([pos_well, neg_well])
        
        mentioned_wells = sum(1 for well in all_wells if well.lower() in prompt_template.lower())
        alignment_score = mentioned_wells / len(all_wells) if all_wells else 0.5
        
        checks.append(QualityCheck(
            "prompt_framework_alignment",
            alignment_score >= 0.3,
            alignment_score,
            f"Prompt-framework alignment: {mentioned_wells}/{len(all_wells)} framework wells mentioned in prompt",
            "Ensure prompt template references relevant framework wells and concepts"
        ))
        
        return checks
    
    def _check_framework_weighting_alignment(self, framework_data: Dict, weighting_data: Dict) -> List[QualityCheck]:
        """Check alignment between framework and weighting methodology."""
        checks = []
        
        # Check if weighting methodology is appropriate for framework size
        dipole_count = len(framework_data.get("dipoles", {}))
        well_count = dipole_count * 2
        
        algorithm_type = weighting_data.get("algorithm_type", "").lower()
        
        # Different algorithms work better with different numbers of wells
        algorithm_suitability = {
            "linear": well_count <= 10,
            "winner_take_most": well_count >= 6,
            "exponential": well_count >= 4,
            "threshold_based": well_count >= 8
        }
        
        is_suitable = algorithm_suitability.get(algorithm_type, True)
        
        checks.append(QualityCheck(
            "framework_weighting_alignment",
            is_suitable,
            1.0 if is_suitable else 0.6,
            f"Framework-weighting alignment: {algorithm_type} algorithm with {well_count} wells",
            f"Consider algorithm suitability for {well_count} wells in framework"
        ))
        
        return checks
    
    def _check_output_input_compatibility(self, prompt_template: str, weighting_data: Dict) -> List[QualityCheck]:
        """Check compatibility between prompt output and weighting input."""
        checks = []
        
        # Check if prompt requires structured output that weighting can process
        requires_scores = "score" in prompt_template.lower()
        requires_json = "json" in prompt_template.lower()
        
        algorithm_type = weighting_data.get("algorithm_type", "")
        
        # Most algorithms require numerical scores
        compatibility = requires_scores and (requires_json or "structured" in prompt_template.lower())
        
        checks.append(QualityCheck(
            "output_input_compatibility",
            compatibility,
            1.0 if compatibility else 0.3,
            f"Output-input compatibility: prompt requires {'structured scores' if compatibility else 'unstructured output'}",
            "Ensure prompt template requires structured numerical scores compatible with weighting algorithm"
        ))
        
        return checks
    
    def _check_workflow_coherence(self, prompt_template: str, framework_data: Dict, weighting_data: Dict) -> List[QualityCheck]:
        """Check overall workflow coherence."""
        checks = []
        
        # Check for coherent analytical approach across components
        prompt_type = "hierarchical" if "rank" in prompt_template.lower() else "standard"
        algorithm_type = weighting_data.get("algorithm_type", "").lower()
        
        # Hierarchical prompts work better with hierarchy-enhancing algorithms
        coherent_combination = (
            (prompt_type == "hierarchical" and "hierarchy" in algorithm_type) or
            (prompt_type == "hierarchical" and "winner" in algorithm_type) or
            (prompt_type == "hierarchical" and "dominance" in algorithm_type) or
            prompt_type == "standard"
        )
        
        checks.append(QualityCheck(
            "workflow_coherence",
            coherent_combination,
            1.0 if coherent_combination else 0.7,
            f"Workflow coherence: {prompt_type} prompt with {algorithm_type} algorithm",
            "Ensure prompt type and weighting algorithm work together coherently"
        ))
        
        return checks
    
    def _check_performance_synergy(self, prompt_template: str, framework_data: Dict, weighting_data: Dict) -> List[QualityCheck]:
        """Check potential performance synergy."""
        checks = []
        
        # Look for synergistic elements
        synergy_score = 0.0
        
        # Evidence requirements + hierarchy algorithms = good synergy
        has_evidence = "evidence" in prompt_template.lower()
        enhances_hierarchy = "dominance" in weighting_data.get("algorithm_type", "").lower()
        if has_evidence and enhances_hierarchy:
            synergy_score += 0.3
        
        # Structured output + mathematical rigor = good synergy
        has_structure = "json" in prompt_template.lower()
        has_math_rigor = "formula" in weighting_data
        if has_structure and has_math_rigor:
            synergy_score += 0.3
        
        # Framework complexity + prompt sophistication = good synergy
        framework_complexity = len(framework_data.get("dipoles", {}))
        prompt_sophistication = len(prompt_template.split()) > 100
        if framework_complexity >= 4 and prompt_sophistication:
            synergy_score += 0.4
        
        checks.append(QualityCheck(
            "performance_synergy",
            synergy_score >= 0.5,
            synergy_score,
            f"Performance synergy: {synergy_score:.1f} synergy score",
            "Optimize component combination for enhanced performance synergy"
        ))
        
        return checks
    
    def _compile_quality_report(self,
                              component_type: ComponentType,
                              component_name: str,
                              version: str,
                              checks: List[QualityCheck]) -> QualityReport:
        """Compile comprehensive quality report."""
        # Calculate overall score
        if not checks:
            overall_score = 0.0
        else:
            total_score = sum(check.score for check in checks)
            overall_score = total_score / len(checks)
        
        # Determine quality level
        overall_level = QualityLevel.UNACCEPTABLE
        for level, threshold in sorted(self.quality_thresholds.items(), 
                                     key=lambda x: x[1], reverse=True):
            if overall_score >= threshold:
                overall_level = level
                break
        
        # Generate recommendations
        recommendations = []
        failed_checks = [check for check in checks if not check.passed]
        for check in failed_checks[:5]:  # Top 5 most important issues
            if check.recommendation:
                recommendations.append(check.recommendation)
        
        # Determine academic readiness
        critical_checks = [check for check in checks if check.severity == "error"]
        academic_readiness = len(critical_checks) == 0 and overall_score >= 0.7
        
        # Generate validation requirements
        validation_requirements = []
        if overall_score < 0.8:
            validation_requirements.append("Comprehensive testing with representative corpus")
        if overall_score < 0.7:
            validation_requirements.append("Human expert validation study")
        if overall_score < 0.6:
            validation_requirements.append("Fundamental redesign before academic use")
        
        return QualityReport(
            component_type=component_type,
            component_name=component_name,
            version=version,
            overall_score=overall_score,
            overall_level=overall_level,
            checks=checks,
            recommendations=recommendations,
            academic_readiness=academic_readiness,
            validation_requirements=validation_requirements
        ) 