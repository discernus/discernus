#!/usr/bin/env python3
"""
Model Quality Assessment Framework for Discernus
===============================================

Provides tools for comparing analysis quality between different LLM models,
particularly useful for assessing fallback model performance and ensuring
research integrity across model switches.
"""

# Copyright (C) 2025  Discernus Team

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import json
import re
import statistics
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
import numpy as np
from scipy import stats


class ModelQualityAssessment:
    """
    Framework for assessing and comparing analysis quality between different LLM models.
    
    This is particularly important for fallback scenarios where different models
    may be used for the same analysis tasks, ensuring research integrity is maintained.
    """
    
    def __init__(self, experiment_path: Path):
        """
        Initialize quality assessment framework.
        
        Args:
            experiment_path: Path to experiment directory
        """
        self.experiment_path = experiment_path
        self.artifacts_dir = experiment_path / "shared_cache" / "artifacts"
        self.registry_file = self.artifacts_dir / "artifact_registry.json"
        
    def load_analysis_artifacts(self) -> List[Dict[str, Any]]:
        """
        Load all analysis artifacts from the experiment.
        
        Returns:
            List of analysis artifact dictionaries
        """
        artifacts = []
        
        if not self.artifacts_dir.exists():
            return artifacts
        
        # Load registry to get artifact metadata
        if self.registry_file.exists():
            with open(self.registry_file) as f:
                registry = json.load(f)
            
            for artifact_id, info in registry.items():
                artifact_type = info.get("metadata", {}).get("artifact_type")
                if artifact_type == "analysis_json_v6":
                    artifact_file = self.artifacts_dir / artifact_id
                    if artifact_file.exists():
                        try:
                            with open(artifact_file) as f:
                                artifact_data = json.load(f)
                                artifacts.append(artifact_data)
                        except Exception as e:
                            print(f"Warning: Could not load artifact {artifact_id}: {e}")
        
        return artifacts
    
    def group_artifacts_by_model(self, artifacts: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Group analysis artifacts by the model that generated them.
        
        Args:
            artifacts: List of analysis artifacts
            
        Returns:
            Dictionary mapping model names to lists of artifacts
        """
        model_groups = {}
        
        for artifact in artifacts:
            model_used = artifact.get("model_used", "unknown")
            if model_used not in model_groups:
                model_groups[model_used] = []
            model_groups[model_used].append(artifact)
        
        return model_groups
    
    def extract_dimensional_scores(self, artifact: Dict[str, Any]) -> Dict[str, float]:
        """
        Extract dimensional scores from an analysis artifact.
        
        Args:
            artifact: Analysis artifact dictionary
            
        Returns:
            Dictionary mapping dimension names to raw scores
        """
        scores = {}
        
        try:
            raw_response = artifact.get("raw_analysis_response", "")
            
            # Extract JSON from delimited format
            import re
            json_pattern = r'<<<DISCERNUS_ANALYSIS_JSON_v6>>>\s*({.*?})\s*<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>'
            json_match = re.search(json_pattern, raw_response, re.DOTALL)
            
            if json_match:
                analysis_data = json.loads(json_match.group(1).strip())
                document_analyses = analysis_data.get('document_analyses', [])
                
                for doc_analysis in document_analyses:
                    dimensional_scores = doc_analysis.get('dimensional_scores', {})
                    for dimension, score_data in dimensional_scores.items():
                        if isinstance(score_data, dict) and 'raw_score' in score_data:
                            scores[dimension] = score_data['raw_score']
        except Exception as e:
            print(f"Warning: Could not extract scores from artifact: {e}")
        
        return scores
    
    def calculate_model_statistics(self, model_artifacts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate quality statistics for a group of artifacts from the same model.
        
        Args:
            model_artifacts: List of artifacts from the same model
            
        Returns:
            Dictionary with quality statistics
        """
        all_scores = {}
        confidence_scores = []
        evidence_counts = []
        
        for artifact in model_artifacts:
            # Extract dimensional scores
            scores = self.extract_dimensional_scores(artifact)
            for dimension, score in scores.items():
                if dimension not in all_scores:
                    all_scores[dimension] = []
                all_scores[dimension].append(score)
            
            # Extract confidence scores
            try:
                raw_response = artifact.get("raw_analysis_response", "")
                json_pattern = r'<<<DISCERNUS_ANALYSIS_JSON_v6>>>\s*({.*?})\s*<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>'
                json_match = re.search(json_pattern, raw_response, re.DOTALL)
                
                if json_match:
                    analysis_data = json.loads(json_match.group(1).strip())
                    metadata = analysis_data.get('analysis_metadata', {})
                    confidence = metadata.get('analyst_confidence', 0.0)
                    confidence_scores.append(confidence)
                    
                    # Count evidence items
                    document_analyses = analysis_data.get('document_analyses', [])
                    for doc_analysis in document_analyses:
                        evidence = doc_analysis.get('evidence', [])
                        evidence_counts.append(len(evidence))
            except Exception:
                pass
        
        # Calculate statistics
        stats_dict = {
            "artifact_count": len(model_artifacts),
            "confidence_stats": {
                "mean": statistics.mean(confidence_scores) if confidence_scores else 0.0,
                "std": statistics.stdev(confidence_scores) if len(confidence_scores) > 1 else 0.0,
                "min": min(confidence_scores) if confidence_scores else 0.0,
                "max": max(confidence_scores) if confidence_scores else 0.0
            },
            "evidence_stats": {
                "mean": statistics.mean(evidence_counts) if evidence_counts else 0.0,
                "std": statistics.stdev(evidence_counts) if len(evidence_counts) > 1 else 0.0,
                "min": min(evidence_counts) if evidence_counts else 0.0,
                "max": max(evidence_counts) if evidence_counts else 0.0
            },
            "dimensional_stats": {}
        }
        
        # Calculate dimensional statistics
        for dimension, scores in all_scores.items():
            if scores:
                stats_dict["dimensional_stats"][dimension] = {
                    "mean": statistics.mean(scores),
                    "std": statistics.stdev(scores) if len(scores) > 1 else 0.0,
                    "min": min(scores),
                    "max": max(scores),
                    "count": len(scores)
                }
        
        return stats_dict
    
    def compare_models(self, model_groups: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """
        Compare quality metrics between different models.
        
        Args:
            model_groups: Dictionary mapping model names to artifact lists
            
        Returns:
            Dictionary with comparison results
        """
        comparison = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "models_compared": list(model_groups.keys()),
            "model_statistics": {},
            "statistical_tests": {},
            "quality_assessment": {}
        }
        
        # Calculate statistics for each model
        for model_name, artifacts in model_groups.items():
            comparison["model_statistics"][model_name] = self.calculate_model_statistics(artifacts)
        
        # Perform statistical comparisons if we have multiple models
        if len(model_groups) >= 2:
            model_names = list(model_groups.keys())
            
            # Compare confidence scores
            confidence_comparison = self._compare_confidence_scores(model_groups)
            comparison["statistical_tests"]["confidence_comparison"] = confidence_comparison
            
            # Compare evidence counts
            evidence_comparison = self._compare_evidence_counts(model_groups)
            comparison["statistical_tests"]["evidence_comparison"] = evidence_comparison
            
            # Compare dimensional scores
            dimensional_comparison = self._compare_dimensional_scores(model_groups)
            comparison["statistical_tests"]["dimensional_comparison"] = dimensional_comparison
        
        # Generate quality assessment
        comparison["quality_assessment"] = self._generate_quality_assessment(comparison)
        
        return comparison
    
    def _compare_confidence_scores(self, model_groups: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Compare confidence scores between models."""
        model_confidence = {}
        
        for model_name, artifacts in model_groups.items():
            confidences = []
            for artifact in artifacts:
                try:
                    raw_response = artifact.get("raw_analysis_response", "")
                    json_pattern = r'<<<DISCERNUS_ANALYSIS_JSON_v6>>>\s*({.*?})\s*<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>'
                    json_match = re.search(json_pattern, raw_response, re.DOTALL)
                    
                    if json_match:
                        analysis_data = json.loads(json_match.group(1).strip())
                        metadata = analysis_data.get('analysis_metadata', {})
                        confidence = metadata.get('analyst_confidence', 0.0)
                        confidences.append(confidence)
                except Exception:
                    pass
            
            if confidences:
                model_confidence[model_name] = confidences
        
        # Perform statistical tests
        if len(model_confidence) >= 2:
            model_names = list(model_confidence.keys())
            model1_conf = model_confidence[model_names[0]]
            model2_conf = model_confidence[model_names[1]]
            
            try:
                # T-test for confidence scores
                t_stat, p_value = stats.ttest_ind(model1_conf, model2_conf)
                
                return {
                    "test_type": "independent_t_test",
                    "models": model_names,
                    "t_statistic": float(t_stat),
                    "p_value": float(p_value),
                    "significant": p_value < 0.05,
                    "model1_mean": statistics.mean(model1_conf),
                    "model2_mean": statistics.mean(model2_conf),
                    "interpretation": self._interpret_confidence_difference(
                        statistics.mean(model1_conf), 
                        statistics.mean(model2_conf), 
                        p_value
                    )
                }
            except Exception as e:
                return {"error": f"Statistical test failed: {e}"}
        
        return {"error": "Insufficient data for comparison"}
    
    def _compare_evidence_counts(self, model_groups: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Compare evidence counts between models."""
        model_evidence = {}
        
        for model_name, artifacts in model_groups.items():
            evidence_counts = []
            for artifact in artifacts:
                try:
                    raw_response = artifact.get("raw_analysis_response", "")
                    json_pattern = r'<<<DISCERNUS_ANALYSIS_JSON_v6>>>\s*({.*?})\s*<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>'
                    json_match = re.search(json_pattern, raw_response, re.DOTALL)
                    
                    if json_match:
                        analysis_data = json.loads(json_match.group(1).strip())
                        document_analyses = analysis_data.get('document_analyses', [])
                        for doc_analysis in document_analyses:
                            evidence = doc_analysis.get('evidence', [])
                            evidence_counts.append(len(evidence))
                except Exception:
                    pass
            
            if evidence_counts:
                model_evidence[model_name] = evidence_counts
        
        # Perform statistical tests
        if len(model_evidence) >= 2:
            model_names = list(model_evidence.keys())
            model1_evidence = model_evidence[model_names[0]]
            model2_evidence = model_evidence[model_names[1]]
            
            try:
                # Mann-Whitney U test for evidence counts (non-parametric)
                u_stat, p_value = stats.mannwhitneyu(model1_evidence, model2_evidence, alternative='two-sided')
                
                return {
                    "test_type": "mann_whitney_u_test",
                    "models": model_names,
                    "u_statistic": float(u_stat),
                    "p_value": float(p_value),
                    "significant": p_value < 0.05,
                    "model1_median": statistics.median(model1_evidence),
                    "model2_median": statistics.median(model2_evidence),
                    "interpretation": self._interpret_evidence_difference(
                        statistics.median(model1_evidence), 
                        statistics.median(model2_evidence), 
                        p_value
                    )
                }
            except Exception as e:
                return {"error": f"Statistical test failed: {e}"}
        
        return {"error": "Insufficient data for comparison"}
    
    def _compare_dimensional_scores(self, model_groups: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Compare dimensional scores between models."""
        model_scores = {}
        
        for model_name, artifacts in model_groups.items():
            dimensional_scores = {}
            for artifact in artifacts:
                scores = self.extract_dimensional_scores(artifact)
                for dimension, score in scores.items():
                    if dimension not in dimensional_scores:
                        dimensional_scores[dimension] = []
                    dimensional_scores[dimension].append(score)
            
            if dimensional_scores:
                model_scores[model_name] = dimensional_scores
        
        # Compare each dimension
        dimensional_comparisons = {}
        
        if len(model_scores) >= 2:
            model_names = list(model_scores.keys())
            model1_scores = model_scores[model_names[0]]
            model2_scores = model_scores[model_names[1]]
            
            # Find common dimensions
            common_dimensions = set(model1_scores.keys()) & set(model2_scores.keys())
            
            for dimension in common_dimensions:
                scores1 = model1_scores[dimension]
                scores2 = model2_scores[dimension]
                
                try:
                    # T-test for dimensional scores
                    t_stat, p_value = stats.ttest_ind(scores1, scores2)
                    
                    dimensional_comparisons[dimension] = {
                        "test_type": "independent_t_test",
                        "t_statistic": float(t_stat),
                        "p_value": float(p_value),
                        "significant": p_value < 0.05,
                        "model1_mean": statistics.mean(scores1),
                        "model2_mean": statistics.mean(scores2),
                        "model1_std": statistics.stdev(scores1) if len(scores1) > 1 else 0.0,
                        "model2_std": statistics.stdev(scores2) if len(scores2) > 1 else 0.0,
                        "effect_size": self._calculate_cohens_d(scores1, scores2)
                    }
                except Exception as e:
                    dimensional_comparisons[dimension] = {"error": f"Statistical test failed: {e}"}
        
        return {
            "dimensions_compared": len(dimensional_comparisons),
            "significant_differences": sum(1 for comp in dimensional_comparisons.values() 
                                        if isinstance(comp, dict) and comp.get("significant", False)),
            "detailed_comparisons": dimensional_comparisons
        }
    
    def _calculate_cohens_d(self, group1: List[float], group2: List[float]) -> float:
        """Calculate Cohen's d effect size."""
        try:
            n1, n2 = len(group1), len(group2)
            s1, s2 = statistics.stdev(group1) if n1 > 1 else 0.0, statistics.stdev(group2) if n2 > 1 else 0.0
            
            # Pooled standard deviation
            pooled_std = np.sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / (n1 + n2 - 2))
            
            if pooled_std == 0:
                return 0.0
            
            # Cohen's d
            d = (statistics.mean(group1) - statistics.mean(group2)) / pooled_std
            return float(d)
        except Exception:
            return 0.0
    
    def _interpret_confidence_difference(self, mean1: float, mean2: float, p_value: float) -> str:
        """Interpret confidence score differences."""
        if p_value >= 0.05:
            return "No significant difference in confidence scores between models"
        
        if mean1 > mean2:
            return f"Model 1 shows significantly higher confidence (p={p_value:.3f})"
        else:
            return f"Model 2 shows significantly higher confidence (p={p_value:.3f})"
    
    def _interpret_evidence_difference(self, median1: float, median2: float, p_value: float) -> str:
        """Interpret evidence count differences."""
        if p_value >= 0.05:
            return "No significant difference in evidence counts between models"
        
        if median1 > median2:
            return f"Model 1 provides significantly more evidence (p={p_value:.3f})"
        else:
            return f"Model 2 provides significantly more evidence (p={p_value:.3f})"
    
    def _generate_quality_assessment(self, comparison: Dict[str, Any]) -> Dict[str, Any]:
        """Generate overall quality assessment."""
        assessment = {
            "overall_quality": "unknown",
            "research_integrity": "unknown",
            "recommendations": [],
            "concerns": []
        }
        
        # Check for significant differences
        statistical_tests = comparison.get("statistical_tests", {})
        
        # Assess confidence differences
        confidence_test = statistical_tests.get("confidence_comparison", {})
        if confidence_test.get("significant", False):
            if confidence_test.get("model1_mean", 0) > confidence_test.get("model2_mean", 0):
                assessment["concerns"].append("Model 1 shows significantly higher confidence than Model 2")
            else:
                assessment["concerns"].append("Model 2 shows significantly higher confidence than Model 1")
        
        # Assess evidence differences
        evidence_test = statistical_tests.get("evidence_comparison", {})
        if evidence_test.get("significant", False):
            assessment["concerns"].append("Models differ significantly in evidence provision")
        
        # Assess dimensional differences
        dimensional_test = statistical_tests.get("dimensional_comparison", {})
        significant_dims = dimensional_test.get("significant_differences", 0)
        total_dims = dimensional_test.get("dimensions_compared", 0)
        
        if total_dims > 0:
            significant_ratio = significant_dims / total_dims
            if significant_ratio > 0.3:  # More than 30% of dimensions show significant differences
                assessment["concerns"].append(f"Models differ significantly in {significant_ratio:.1%} of dimensions")
                assessment["research_integrity"] = "compromised"
            elif significant_ratio > 0.1:  # 10-30% show differences
                assessment["research_integrity"] = "questionable"
                assessment["recommendations"].append("Consider model consistency for research validity")
            else:
                assessment["research_integrity"] = "maintained"
        
        # Overall assessment
        if not assessment["concerns"]:
            assessment["overall_quality"] = "good"
        elif len(assessment["concerns"]) <= 2:
            assessment["overall_quality"] = "acceptable"
        else:
            assessment["overall_quality"] = "poor"
        
        return assessment
    
    def generate_quality_report(self, output_file: Optional[Path] = None) -> str:
        """
        Generate a comprehensive model quality assessment report.
        
        Args:
            output_file: Optional output file path
            
        Returns:
            Report content as string
        """
        # Load and analyze artifacts
        artifacts = self.load_analysis_artifacts()
        if not artifacts:
            return "No analysis artifacts found for quality assessment"
        
        model_groups = self.group_artifacts_by_model(artifacts)
        comparison = self.compare_models(model_groups)
        
        # Generate report
        report = f"""# Model Quality Assessment Report
Generated: {comparison['timestamp']}
Experiment: {self.experiment_path.name}

## Summary
- **Models Analyzed**: {', '.join(comparison['models_compared'])}
- **Total Artifacts**: {sum(len(artifacts) for artifacts in model_groups.values())}
- **Research Integrity**: {comparison['quality_assessment']['research_integrity'].title()}
- **Overall Quality**: {comparison['quality_assessment']['overall_quality'].title()}

## Model Statistics
"""
        
        for model_name, stats in comparison['model_statistics'].items():
            report += f"\n### {model_name}\n"
            report += f"- **Artifacts**: {stats['artifact_count']}\n"
            report += f"- **Mean Confidence**: {stats['confidence_stats']['mean']:.3f} ± {stats['confidence_stats']['std']:.3f}\n"
            report += f"- **Mean Evidence Count**: {stats['evidence_stats']['mean']:.1f} ± {stats['evidence_stats']['std']:.1f}\n"
            
            # Show dimensional statistics
            if stats['dimensional_stats']:
                report += "- **Dimensional Scores**:\n"
                for dimension, dim_stats in stats['dimensional_stats'].items():
                    report += f"  - {dimension}: {dim_stats['mean']:.3f} ± {dim_stats['std']:.3f} (n={dim_stats['count']})\n"
        
        # Statistical comparisons
        if comparison['statistical_tests']:
            report += "\n## Statistical Comparisons\n"
            
            # Confidence comparison
            conf_test = comparison['statistical_tests'].get('confidence_comparison', {})
            if 'error' not in conf_test:
                report += f"\n### Confidence Scores\n"
                report += f"- **Test**: {conf_test.get('test_type', 'N/A')}\n"
                report += f"- **P-value**: {conf_test.get('p_value', 'N/A'):.3f}\n"
                report += f"- **Significant**: {'Yes' if conf_test.get('significant', False) else 'No'}\n"
                report += f"- **Interpretation**: {conf_test.get('interpretation', 'N/A')}\n"
            
            # Evidence comparison
            evid_test = comparison['statistical_tests'].get('evidence_comparison', {})
            if 'error' not in evid_test:
                report += f"\n### Evidence Counts\n"
                report += f"- **Test**: {evid_test.get('test_type', 'N/A')}\n"
                report += f"- **P-value**: {evid_test.get('p_value', 'N/A'):.3f}\n"
                report += f"- **Significant**: {'Yes' if evid_test.get('significant', False) else 'No'}\n"
                report += f"- **Interpretation**: {evid_test.get('interpretation', 'N/A')}\n"
            
            # Dimensional comparison
            dim_test = comparison['statistical_tests'].get('dimensional_comparison', {})
            if dim_test.get('dimensions_compared', 0) > 0:
                report += f"\n### Dimensional Scores\n"
                report += f"- **Dimensions Compared**: {dim_test['dimensions_compared']}\n"
                report += f"- **Significant Differences**: {dim_test['significant_differences']}\n"
                
                # Show significant differences
                detailed = dim_test.get('detailed_comparisons', {})
                significant_dims = [dim for dim, comp in detailed.items() 
                                  if isinstance(comp, dict) and comp.get('significant', False)]
                
                if significant_dims:
                    report += f"- **Significantly Different Dimensions**: {', '.join(significant_dims)}\n"
        
        # Quality assessment
        assessment = comparison['quality_assessment']
        report += f"\n## Quality Assessment\n"
        report += f"- **Research Integrity**: {assessment['research_integrity'].title()}\n"
        report += f"- **Overall Quality**: {assessment['overall_quality'].title()}\n"
        
        if assessment['concerns']:
            report += f"\n### Concerns\n"
            for concern in assessment['concerns']:
                report += f"- {concern}\n"
        
        if assessment['recommendations']:
            report += f"\n### Recommendations\n"
            for rec in assessment['recommendations']:
                report += f"- {rec}\n"
        
        # Save report if requested
        if output_file:
            output_file.write_text(report)
            report += f"\n\nReport saved to: {output_file}"
        
        return report


def assess_model_quality(experiment_path: Path, output_file: Optional[Path] = None) -> str:
    """
    Convenience function to assess model quality for an experiment.
    
    Args:
        experiment_path: Path to experiment directory
        output_file: Optional output file path
        
    Returns:
        Quality assessment report
    """
    assessor = ModelQualityAssessment(experiment_path)
    return assessor.generate_quality_report(output_file)
