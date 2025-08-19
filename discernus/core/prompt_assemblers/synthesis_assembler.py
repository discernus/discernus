#!/usr/bin/env python3
"""
Synthesis Prompt Assembler for Discernus v8.1
==============================================

Assembles comprehensive synthesis prompts by combining:
- Complete research data (raw scores, derived metrics, statistical results)
- Framework specifications and methodology
- Evidence database for RAG-based citation
- Experiment context and objectives

Uses proven THIN approach with natural language instructions for reliable synthesis.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class SynthesisPromptAssembler:
    """Assembles synthesis prompts for final report generation."""
    
    def assemble_prompt(self, 
                       framework_path: Path,
                       experiment_path: Path, 
                       research_data_artifact_hash: str,
                       artifact_storage,
                       evidence_artifacts: list) -> str:
        """
        Assemble comprehensive synthesis prompt for final report generation.
        
        Args:
            framework_path: Path to framework file
            experiment_path: Path to experiment file
            research_data_artifact_hash: Hash of complete research data artifact
            artifact_storage: Storage instance to retrieve artifacts
            evidence_artifacts: List of evidence artifact hashes
            
        Returns:
            Complete synthesis prompt
        """
        # 1. Load framework content and methodology
        framework_content = framework_path.read_text(encoding='utf-8')
        framework_yaml = self._parse_framework_yaml(framework_content)
        
        # 2. Load experiment objectives and hypotheses
        experiment_content = experiment_path.read_text(encoding='utf-8')
        experiment_yaml = self._parse_experiment_yaml(experiment_content)
        
        # 3. Load complete research data
        research_data_content = artifact_storage.get_artifact(research_data_artifact_hash)
        research_data = json.loads(research_data_content.decode('utf-8'))
        
        # 4. Prepare statistical summary for context
        statistical_summary = self._create_statistical_summary(research_data['statistical_results'])
        
        # 5. Prepare evidence count for RAG context
        total_evidence_pieces = sum(len(self._get_evidence_from_artifact(artifact_storage.get_artifact(hash))) 
                                  for hash in evidence_artifacts)
        
        # 6. Assemble the comprehensive prompt
        prompt = f"""You are an expert research analyst specializing in computational social science. Your task is to generate a comprehensive, publication-ready research report based on the complete analysis results provided.

FRAMEWORK METHODOLOGY:
{self._extract_framework_description(framework_content)}

EXPERIMENT OBJECTIVES:
{self._extract_experiment_objectives(experiment_content)}

RESEARCH HYPOTHESES:
{self._format_hypotheses(experiment_yaml.get('hypotheses', []))}

STATISTICAL ANALYSIS RESULTS:
{statistical_summary}

RAG EVIDENCE DATABASE:
You have access to {total_evidence_pieces} pieces of textual evidence extracted during analysis. For each major finding, you should query the evidence database to retrieve supporting quotes that validate your statistical interpretations.

EVIDENCE RETRIEVAL INSTRUCTIONS:
- Use semantic queries to find relevant evidence for each statistical finding
- Ensure every major claim is supported by direct quotes with proper attribution
- Include speaker identification and source document for all citations
- Prioritize evidence with high confidence scores (>0.8)

REQUIRED REPORT STRUCTURE:

# [Experiment Name]: [Framework Name] Analysis

## Executive Summary
[2-3 paragraphs summarizing key findings, methodology, and implications]

## Methodology  
[Brief description of framework, corpus, and analytical approach]

## Results

### Dimensional Analysis
[Analysis of raw dimensional scores with evidence support]

### Derived Metrics Analysis  
[Analysis of calculated tension indices and composite metrics with evidence support]

### Statistical Findings
[Comprehensive interpretation of statistical results with evidence support]

### Framework-Corpus Fit Assessment
[Evaluation of how well the framework captured meaningful variance in the corpus]

## Discussion
[Interpretation of findings in broader context with theoretical implications]

## Conclusion
[Key takeaways, limitations, and future research directions]

## Evidence Citations
[Complete bibliography of all quoted evidence with source attribution]

CRITICAL REQUIREMENTS:
1. Every major statistical claim MUST be supported by direct textual evidence
2. Use proper academic citation format: "As [Speaker] stated: '[exact quote]' (Source: [document_name])"
3. Integrate statistical findings with qualitative evidence to create coherent narratives
4. Maintain academic rigor throughout - no unsupported claims or speculation
5. Ensure all calculations and interpretations are grounded in the provided data

Generate a complete research report that meets publication standards for computational social science research."""

        return prompt
    
    def _parse_framework_yaml(self, content: str) -> Dict[str, Any]:
        """Parse YAML from framework's machine-readable appendix."""
        try:
            if '## Part 2: The Machine-Readable Appendix' in content:
                _, appendix_content = content.split('## Part 2: The Machine-Readable Appendix', 1)
                if '```yaml' in appendix_content:
                    yaml_start = appendix_content.find('```yaml') + 7
                    yaml_end = appendix_content.rfind('```')
                    yaml_content = appendix_content[yaml_start:yaml_end].strip() if yaml_end > yaml_start else appendix_content[yaml_start:].strip()
                    return yaml.safe_load(yaml_content)
            return {}
        except Exception:
            return {}
    
    def _parse_experiment_yaml(self, content: str) -> Dict[str, Any]:
        """Parse YAML from experiment's configuration appendix."""
        try:
            if '## Configuration Appendix' in content:
                _, appendix_content = content.split('## Configuration Appendix', 1)
                if '```yaml' in appendix_content:
                    yaml_start = appendix_content.find('```yaml') + 7
                    yaml_end = appendix_content.rfind('```')
                    yaml_content = appendix_content[yaml_start:yaml_end].strip() if yaml_end > yaml_start else appendix_content[yaml_start:].strip()
                    return yaml.safe_load(yaml_content)
            return {}
        except Exception:
            return {}
    
    def _extract_framework_description(self, framework_content: str) -> str:
        """Extract the descriptive content from framework for context."""
        if '## Part 1: The Scholarly Document' in framework_content:
            parts = framework_content.split('## Part 2: The Machine-Readable Appendix', 1)
            scholarly_content = parts[0]
            # Return first 1000 characters for context
            return scholarly_content[:1000] + "..." if len(scholarly_content) > 1000 else scholarly_content
        return "Framework description not available."
    
    def _extract_experiment_objectives(self, experiment_content: str) -> str:
        """Extract experiment objectives from the descriptive content."""
        if '## Research Objectives' in experiment_content:
            parts = experiment_content.split('## Research Objectives', 1)[1]
            if '##' in parts:
                objectives = parts.split('##', 1)[0]
            else:
                objectives = parts.split('## Configuration Appendix', 1)[0] if '## Configuration Appendix' in parts else parts
            return objectives.strip()
        return "Research objectives not specified."
    
    def _format_hypotheses(self, hypotheses: list) -> str:
        """Format experiment hypotheses for the prompt."""
        if not hypotheses:
            return "No specific hypotheses defined."
        
        formatted = []
        for i, hypothesis in enumerate(hypotheses, 1):
            if isinstance(hypothesis, dict):
                name = hypothesis.get('name', f'Hypothesis {i}')
                description = hypothesis.get('description', 'No description')
                formatted.append(f"{i}. **{name}**: {description}")
            else:
                formatted.append(f"{i}. {hypothesis}")
        
        return "\n".join(formatted)
    
    def _create_statistical_summary(self, statistical_results: Dict[str, Any]) -> str:
        """Create a concise summary of statistical results for context."""
        summary_parts = []
        
        for category, results in statistical_results.items():
            if isinstance(results, dict) and results:
                summary_parts.append(f"**{category.replace('_', ' ').title()}**: {len(results)} metrics calculated")
            elif isinstance(results, list) and results:
                summary_parts.append(f"**{category.replace('_', ' ').title()}**: {len(results)} results")
        
        return "\n".join(summary_parts) if summary_parts else "Statistical analysis completed."
    
    def _get_evidence_from_artifact(self, evidence_content: bytes) -> list:
        """Extract evidence list from evidence artifact."""
        try:
            evidence_data = json.loads(evidence_content.decode('utf-8'))
            return evidence_data.get('evidence_data', [])
        except Exception:
            return []
