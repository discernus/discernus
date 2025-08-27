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
import logging


class SynthesisPromptAssembler:
    """Assembles synthesis prompts for final report generation."""
    
    def __init__(self):
        """Initialize with external YAML prompt template."""
        self.prompt_template = self._load_prompt_template()
        self.logger = logging.getLogger(__name__)
    
    def _load_prompt_template(self) -> Dict[str, Any]:
        """Load external YAML prompt template following THIN architecture."""
        import yaml
        
        # Load the enhanced synthesis prompt template
        prompt_file = Path(__file__).parent.parent.parent / "agents" / "unified_synthesis_agent" / "prompt.yaml"
        
        if not prompt_file.exists():
            raise FileNotFoundError(f"Enhanced synthesis prompt template not found: {prompt_file}")
        
        with open(prompt_file, 'r') as f:
            return yaml.safe_load(f)
    
    def assemble_prompt(self, 
                       framework_path: Path,
                       experiment_path: Path, 
                       research_data_artifact_hash: str,
                       artifact_storage,
                       curated_evidence_hash: Optional[str]) -> str:
        """
        Assemble comprehensive synthesis prompt for final report generation.
        
        Args:
            framework_path: Path to framework file
            experiment_path: Path to experiment file
            research_data_artifact_hash: Hash of complete research data artifact
            artifact_storage: Storage instance to retrieve artifacts
            curated_evidence_hash: Hash of the curated evidence artifact from EvidenceRetrieverAgent.
            
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
        
        # 5. Prepare evidence context from CURATED evidence if available
        if curated_evidence_hash:
            self.logger.info(f"Curated evidence artifact found ({curated_evidence_hash}). Formatting for prompt.")
            evidence_context = self._format_curated_evidence(curated_evidence_hash, artifact_storage)
        else:
            # Fallback if curated evidence is not available
            self.logger.warning("No curated evidence artifact provided. Synthesis will proceed without curated evidence.")
            evidence_context = "No curated evidence was available for this synthesis run. The report will be based on statistical findings only."

        # 6. Load and include corpus manifest data
        corpus_manifest = self._load_corpus_manifest(experiment_path)
        
        # 7. Assemble the comprehensive prompt
        # Use external YAML prompt template (THIN architecture)
        prompt = self.prompt_template['template'].format(
            experiment_metadata=self._create_experiment_metadata(experiment_yaml),
            framework_content=self._extract_framework_description(framework_content),
            experiment_content=self._extract_experiment_objectives(experiment_content),
            research_data=statistical_summary,
            corpus_manifest=corpus_manifest,
            evidence_context=evidence_context
        )

        return prompt
    
    def _create_experiment_metadata(self, experiment_yaml: Dict[str, Any]) -> str:
        """Create experiment metadata section for provenance."""
        metadata_parts = []
        
        if 'name' in experiment_yaml:
            metadata_parts.append(f"**Experiment**: {experiment_yaml['name']}")
        if 'framework' in experiment_yaml:
            metadata_parts.append(f"**Framework**: {experiment_yaml['framework']}")
        if 'corpus' in experiment_yaml:
            metadata_parts.append(f"**Corpus**: {experiment_yaml['corpus']}")
        
        return "\n".join(metadata_parts) if metadata_parts else "**Experiment Metadata**: Available in experiment configuration"
    
    def _load_corpus_manifest(self, experiment_path: Path) -> str:
        """Load and format corpus manifest data for synthesis context."""
        try:
            # Corpus manifest should be at corpus.md in the experiment directory
            experiment_dir = experiment_path.parent
            corpus_path = experiment_dir / "corpus.md"
            
            if not corpus_path.exists():
                return "**Corpus Manifest**: Not available - corpus.md not found"
            
            corpus_content = corpus_path.read_text(encoding='utf-8')
            
            # Extract the YAML manifest section
            if '```yaml' in corpus_content:
                yaml_start = corpus_content.find('```yaml') + 7
                yaml_end = corpus_content.find('```', yaml_start)
                if yaml_end > yaml_start:
                    yaml_content = corpus_content[yaml_start:yaml_end].strip()
                    try:
                        corpus_data = yaml.safe_load(yaml_content)
                        return self._format_corpus_manifest(corpus_data)
                    except yaml.YAMLError:
                        pass
            
            # Fallback: return the descriptive content before the YAML
            description_end = corpus_content.find('```yaml')
            if description_end > 0:
                description = corpus_content[:description_end].strip()
                return f"**Corpus Description**:\n{description}"
            
            return "**Corpus Manifest**: Available but could not be parsed"
            
        except Exception as e:
            return f"**Corpus Manifest**: Error loading corpus data: {str(e)}"
    
    def _format_corpus_manifest(self, corpus_data: Dict[str, Any]) -> str:
        """Format corpus manifest data for synthesis prompt."""
        lines = []
        lines.append("**Corpus Manifest**:")
        
        # Basic corpus info
        if 'name' in corpus_data:
            lines.append(f"- **Name**: {corpus_data['name']}")
        if 'total_documents' in corpus_data:
            lines.append(f"- **Documents**: {corpus_data['total_documents']}")
        if 'date_range' in corpus_data:
            lines.append(f"- **Date Range**: {corpus_data['date_range']}")
        
        # Document details
        documents = corpus_data.get('documents', [])
        if documents:
            lines.append("\n**Document Details**:")
            for doc in documents:
                filename = doc.get('filename', 'Unknown')
                metadata = doc.get('metadata', {})
                
                speaker = metadata.get('speaker', 'Unknown Speaker')
                year = metadata.get('year', 'Unknown Year')
                party = metadata.get('party', 'Unknown Party')
                style = metadata.get('style', 'Unknown Style')
                
                lines.append(f"- **{filename}**: {speaker} ({party}, {year}) - {style}")
        
        return "\n".join(lines)
    
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
        """Provide complete statistical results as JSON for LLM to format into tables."""
        # THIN approach: Provide the raw data and let the LLM create the tables
        return f"Complete Statistical Results (format into Markdown tables as instructed):\n{json.dumps(statistical_results, indent=2)}"
    
    def _get_evidence_from_artifact(self, evidence_content: bytes) -> list:
        """Extract evidence list from evidence artifact."""
        try:
            evidence_data = json.loads(evidence_content.decode('utf-8'))
            return evidence_data.get('evidence_data', [])
        except Exception:
            return []

    def _format_curated_evidence(self, curated_evidence_hash: str, artifact_storage) -> str:
        """Load and format the curated evidence artifact into a string for the prompt."""
        try:
            content = artifact_storage.get_artifact(curated_evidence_hash)
            curated_data = json.loads(content.decode('utf-8'))
            
            evidence_results = curated_data.get("evidence_results", [])
            if not evidence_results:
                self.logger.warning(f"Curated evidence artifact ({curated_evidence_hash}) was empty.")
                return "No curated evidence was found."

            self.logger.info(f"Formatting {len(evidence_results)} findings from curated evidence artifact.")
            formatted_text = ["**Curated Evidence for Key Statistical Findings:**\n"]
            
            total_quotes = 0
            for item in evidence_results:
                finding_desc = item.get("finding", {}).get("description", "Unnamed Finding")
                quotes = item.get("quotes", [])
                
                formatted_text.append(f"**Finding:** {finding_desc}\n")
                if not quotes:
                    formatted_text.append("- *No direct evidence quotes found for this finding.*\n")
                else:
                    total_quotes += len(quotes)
                    for quote in quotes:
                        quote_text = quote.get('quote_text', 'N/A').strip()
                        doc_name = quote.get('document_name', 'Unknown')
                        relevance = quote.get('relevance_score', 0.0)
                        formatted_text.append(f'- "{quote_text}" (Source: {doc_name}, Relevance: {relevance:.2f})')
                formatted_text.append("\n")

            self.logger.info(f"Successfully formatted curated evidence, total quotes included: {total_quotes}.")
            return "\n".join(formatted_text)

        except Exception as e:
            self.logger.error(f"Failed to load or format curated evidence artifact ({curated_evidence_hash}): {e}")
            return f"**Error:** Could not load or format curated evidence. Synthesis will proceed without it. Details: {str(e)}"
